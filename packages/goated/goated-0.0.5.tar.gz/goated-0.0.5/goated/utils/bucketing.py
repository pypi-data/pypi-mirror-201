from typing import List
from decimal import Decimal
from ..instructions import PriceFormat

PRICE_ROUNDING_TOLERANCE = Decimal(10**-5)

class PriceSchema():

    def __init__(
        self,
        price_format: PriceFormat,
        absolute_min: Decimal,
        absolute_max: Decimal,
        mins: List[Decimal],
        maxs: List[Decimal],
        increments: List[Decimal]
    ):
        self._price_format = price_format
        self._format_absolute_min = absolute_min
        self._format_absolute_max = absolute_max
        self._format_mins = mins
        self._format_maxs = maxs
        self._format_increments = increments
        self.get_min_max()
        self.generate_range()


    def get_min_max(
        self
    ):
        if self._price_format == PriceFormat.PROBABILITY:
            self.max = Decimal(self._format_maxs[-1])
            self.min = Decimal(self._format_mins[0])
        elif self._price_format == PriceFormat.DECIMAL:
            self.max = Decimal(1/self._format_mins[0])
            self.min = Decimal(1/self._format_maxs[-1])
        elif self._price_format == PriceFormat.AMERICAN:
            self.max = Decimal(self._format_mins[0]/(100+self._format_mins[0]) if self._format_mins[0] < 0 else 100/(100+self._format_mins[0]))
            self.min = Decimal(self._format_maxs[-1]/(100+self._format_maxs[-1]) if self._format_maxs[-1] < 0 else 100/(100+self._format_maxs[-1]))

    @classmethod
    def load(
        cls,
        config: dict
    ):
        return cls(
            price_format = PriceFormat(config['price_format']),
            absolute_min = config['absolute_min'],
            absolute_max = config['absolute_max'],
            mins = config['mins'],
            maxs = config['maxs'],
            increments= config['increments'], 
        )

    def convert_from_probability(
        self,
        probability_price: Decimal
    ):
        if self._price_format == PriceFormat.DECIMAL:
            format_price = Decimal(1 / probability_price)
        elif self._price_format == PriceFormat.AMERICAN:
            if probability_price < 0.5:
                format_price = Decimal(Decimal(1/probability_price)*100 - 100)
            else:
                format_price = Decimal((probability_price*100)/(1-probability_price))
        else:
            format_price = probability_price
        return format_price


    def convert_to_probability(
        self,
        format_price: Decimal
    ):
        if self._price_format == PriceFormat.DECIMAL:
            probability_price = Decimal(1/format_price)
            
        elif self._price_format == PriceFormat.AMERICAN:
            if format_price < 0:
                if format_price == Decimal(-100):
                    probability_price = Decimal(0.5)
                else:
                    probability_price = Decimal(format_price/(100+format_price))
            else:
                probability_price = Decimal(100/(100+format_price))

        else:
            probability_price = format_price

        return probability_price 
    
    @property
    def prudent_is_lower(
        self,
    ):
        # Peudent here means a higher probability price
        # i.e. we're rounding the price at which a match is 'sold' up 
        # to the next acceptable tick.
        if self._price_format == PriceFormat.DECIMAL:
            prudent_is_lower = True
        elif self._price_format == PriceFormat.AMERICAN:
            prudent_is_lower = True
        else:
            prudent_is_lower = False
        return prudent_is_lower


    def bucket(
        self,
        raw_price: Decimal,
        bucket_inverted: bool = False,
        prudent: bool = False
    ) -> Decimal:

        # If we're bucketing inverted then operate on price = (1-price)
        # and convert back at the end
        # Prudent direction is the opposite if inverted
        if bucket_inverted:
            raw_price = (1-raw_price)
            prudent_is_lower = not self.prudent_is_lower
        else:
            prudent_is_lower = self.prudent_is_lower

        # If price out of bounds, then we have a problem
        if raw_price <= 0 or raw_price >= 1:
            raise Exception(f'Price is out of bounds: {raw_price}')


        # If the price is within bounds but 
        # outside the acceptable min/max then we can simply
        # return this absolute min/max bound
        if bucket_inverted:
            if raw_price >= Decimal(1) - self.min:
                return self.min
            elif raw_price <= Decimal(1) - self.max:
                return self.max
        else:
            if raw_price >= self.max:
                return self.max
            elif raw_price <= self.min:
                return self.min

        # Convert the probabity price to te format price
        format_raw_price = self.convert_from_probability(
            probability_price = raw_price
        )

        # Find the containing band
        lower_bound_index = next(
            (
                idx for idx, x in enumerate(self._format_mins)
                if x >= format_raw_price
            ),
            None
        )
        lower_bound_index = (
            len(self._format_mins) - 1
            if lower_bound_index == None
            else lower_bound_index - 1
        )
        increment = Decimal(
            self._format_increments[lower_bound_index]
        )

        # Naively round to the nearest tick
        bucketed_format_price = Decimal(
            Decimal(round(format_raw_price / increment)) * increment
        )

        # If prudent, then find the nearest prudent tick
        if prudent:
            if abs(bucketed_format_price - format_raw_price) < Decimal(PRICE_ROUNDING_TOLERANCE):
                pass # Close enough, don't do anything
            elif prudent_is_lower and format_raw_price > bucketed_format_price:
                pass # Already prudent
            elif not prudent_is_lower and format_raw_price < bucketed_format_price:
                pass # Already prudent
            elif prudent_is_lower:
                bucketed_format_price -= increment
            elif not prudent_is_lower:
                bucketed_format_price += increment
                
        # Convert back to probability
        bucketed_probability_price = self.convert_to_probability(
            format_price = bucketed_format_price
        )

        # Flip it back if inverted
        if bucket_inverted:
            bucketed_probability_price = Decimal(1) - bucketed_probability_price

        return bucketed_probability_price

    
    def index_of_nearest_tick_greater_than(
        self,
        probability_price
    ):
        return next(
            (
                index for index, item in enumerate(self.probability_range)
                if item > probability_price
            ),
            None
        )
    
    def index_of_nearest_tick_less_than_equal(
        self,
        probability_price
    ):
        return self.index_of_nearest_tick_greater_than(probability_price) - 1


    def nearest_tick_greater_than(
        self,
        probability_price
    ):
        return self.probability_range(self.index_of_nearest_tick_greater_than(probability_price))
    

    def nearest_tick_less_than_equal(
        self,
        probability_price
    ):
        return self.probability_range(
            self.index_of_nearest_tick_less_than_equal(probability_price)
        )
        
        
    def nearest_tick_with_number_ticks_offset(
        self,
        probability_price,
        ticks_to_offset: int # +/- number of ticks to step away from nearest
    ):
        index_nearest_over = self.index_of_nearest_tick_greater_than(probability_price)
        index_nearest_under= index_nearest_over - 1
        above = Decimal(self.probability_range[index_nearest_over])
        below = Decimal(self.probability_range[index_nearest_under])
        if abs(above - probability_price) < abs(below - probability_price):
            nearest_index = index_nearest_over
        else:
            nearest_index = index_nearest_under
        return self.probability_range[nearest_index + ticks_to_offset]

    def nearest_tick(
        self,
        probability_price
    ):
        return self.nearest_tick_with_number_ticks_offset(
            probability_price = probability_price,
            ticks_to_offset = 0
        )

    def generate_range(
        self,
    ):
        values_in_format = [self._format_absolute_min]
        for idx in range(len(self._format_mins)):
            if self._format_mins[idx] in values_in_format:
                v = self._format_mins[idx] + self._format_increments[idx]
            else:
                v = self._format_mins[idx]
            while v <= self._format_maxs[idx]:
                values_in_format.append(v)
                v += self._format_increments[idx]
            if self._format_maxs[idx] not in values_in_format:
                values_in_format.append(self._format_maxs[idx])
        if self._format_absolute_max not in values_in_format:
            values_in_format.append(self._format_absolute_max)
        
        if self._price_format == PriceFormat.PROBABILITY: # Prices ascending for probability already
            self.format_range = sorted(set(values_in_format))
            self.probability_range = self.format_range
        else:
            self.format_range = sorted(set(values_in_format))[::-1] # Flip prices from descending to ascending for decimal or american format
            self.probability_range = [self.convert_to_probability(format_price=fp) for fp in self.format_range]
        

### PRECONFIGURATIONS ###

DEFAULT_PROBABILITY_SCHEMA_CONFIG = {
    'price_format': 'probability', 
    'absolute_min': 0.001,
    'absolute_max': 0.99,
    'mins': [
        0.001,
        0.002,
        0.005,
        0.01,
        0.02,
        0.05,
        0.1
    ],
    'maxs': [
        0.002,
        0.005,
        0.01,
        0.02,
        0.05,
        0.1,
        0.99
    ],
    'increments': [
        0.0001,
        0.00025,
        0.0005,
        0.001,
        0.0025,
        0.005,
        0.01
    ]
}

DEFAULT_PROBABILITY_SCHEMA = PriceSchema.load(
    config = DEFAULT_PROBABILITY_SCHEMA_CONFIG
)

DEFAULT_DECIMAL_SCHEMA_CONFIG = {
    'price_format': 'decimal',
    'absolute_min': 1.01,
    'absolute_max': 1000.0,
    'mins': [
        1.01,
        2.0,
        3.0,
        4.0,
        6.0,
        10.0,
        20.0,
        30.0,
        50.0,
        100.0
    ],
    'maxs': [
        2.0,
        3.0,
        4.0,
        6.0,
        10.0,
        20.0,
        30.0,
        50.0,
        100.0,
        1000.0
    ],
    'increments': [
        0.01,
        0.02,
        0.05,
        0.1,
        0.2,
        0.5,
        1.0,
        2.0,
        5.0,
        10.0
    ]
}

DEFAULT_DECIMAL_SCHEMA = PriceSchema.load(
    config = DEFAULT_DECIMAL_SCHEMA_CONFIG
)

DEFAULT_AMERICAN_SCHEMA_CONFIG = {
    'price_format': 'american',
    'absolute_min': -100000,
    'absolute_max': 100000,
    'mins': [
        -100000,
        -10000,
        -5000,
        -3000,
        -2000,
        -1000,
        -500,
        -300,
        -200,
        -100,
        100,
        200,
        300,
        500,
        1000,
        2000,
        3000,
        5000,
        10000
    ],
    'maxs': [
        -10000,
        -5000,
        -3000,
        -2000,
        -1000,
        -500,
        -300,
        -200,
        -100,
        100,
        200,
        300,
        500,
        1000,
        2000,
        3000,
        5000,
        10000,
        100000
    ],
    'increments': [
        1000,
        500,
        250,
        100,
        50,
        25,
        10,
        5,
        1,
        1,
        1,
        5,
        10,
        25,
        50,
        100,
        250,
        500,
        1000
    ]
}


DEFAULT_AMERICAN_SCHEMA = PriceSchema.load(
    DEFAULT_AMERICAN_SCHEMA_CONFIG
)