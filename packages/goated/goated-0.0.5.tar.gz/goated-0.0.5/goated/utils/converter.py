from ..instructions import PriceFormat
from decimal import Decimal

def convert_probability_to_american(probability_price: Decimal):
    if probability_price == None or Decimal(probability_price) >= Decimal(1) or Decimal(probability_price) <= Decimal(0):
        return 0
    if probability_price > 0.5:
        return -(probability_price / (1 - probability_price)) * 100
    else:
        return ((1 - probability_price) / probability_price) * 100



def convert_to_probability(
    price: Decimal,
    price_format: PriceFormat
):
    if type(price) != Decimal:
        price = Decimal(price)

    if price_format == PriceFormat.PROBABILITY:
        return price
    elif price_format == PriceFormat.DECIMAL:
        return Decimal(1) / price if price != Decimal(0) else Decimal(1)
    elif price_format == PriceFormat.AMERICAN:
        if price > 0:
            return Decimal(100) / (price + Decimal(100))
        else:
            return (Decimal(-1) * price)/ ( (Decimal(-1) * price) + Decimal(100) )
    else:
        return None
