
from ..instructions import NewOrderArgs, OrderSide
from typing import Union, List
import json
from .profiles import CurrentLiquidityProfile
from .profiles import MatchedPositionProfile
from decimal import Decimal
import numpy as np
from ..utils.converter import convert_to_probability
from ..utils.bucketing import DEFAULT_AMERICAN_SCHEMA, DEFAULT_DECIMAL_SCHEMA, DEFAULT_PROBABILITY_SCHEMA
import time

class Pool():

    def __init__(
        self,
        state,
        id: int,
        scenario_space: str,
        currency: str,
        payoff_signature_length: int,
        price_schema: str,
        status: str,
        min_residual_quantity: Decimal,
        min_post_quantity: Decimal,
        supports_in_play: bool,
        in_play_delay_seconds: Decimal,
        event_id: int,
    ):
        self.state = state
        self.id = id
        self.scenario_space = scenario_space
        self.currency = currency
        self.payoff_signature_length = payoff_signature_length
        self._price_schema = price_schema
        self.status = status
        self.min_residual_quantity = min_residual_quantity
        self.min_post_quantity = min_post_quantity
        self.supports_in_play = supports_in_play
        self.in_play_delay_seconds = in_play_delay_seconds
        self.event_id = event_id
        self._update_timestamp = time.time()

        # Profiles
        self.refresh_profiles(perform_regardless=True)

        # Checks on whether profile refreshes are required
        self._orders_updated = False
        self._positions_updated = False
        self._selections_updated = False
        self._markets_updated = False
        


    @property
    def is_frozen(
        self,
    ):
        if self._frozen == False:
            return False
        else:
            if (
                self._new_orders_to_thaw == [] and
                self._cancel_orders_to_thaw == [] and
                self._reduce_orders_to_thaw == []
            ):
                self._frozen = False
            if (
                self._freeze_time and 
                (time.time() - self._freeze_time) > 15
            ):
                print(f"Freeze time elapsed for pool {self.id}")
                self._frozen = False

        return self._frozen


    def refresh_profiles(
        self,
        perform_regardless = False
    ):

        if perform_regardless:
            self.refresh_matched_position_profile()
            self.refresh_current_liquidity_profile()
        else:
            if self._orders_updated:
                self.refresh_current_liquidity_profile()
                self._orders_updated = False
            if self._positions_updated:
                self.refresh_matched_position_profile()
                self._positions_updated = False
            # if self._selections_updated:
            #     self.refresh_arb_free_prices()
            #     self._selections_updated = False
            if self._markets_updated:
                self._markets_updated = False
                pass

    def refresh_current_liquidity_profile(
        self,
    ):
        self.current_liquidity_profile = CurrentLiquidityProfile.generate_from_orders(
            pool = self
        )
        # self.current_liquidity_profile.print()
        return self.current_liquidity_profile


    def refresh_matched_position_profile(
        self,
    ):
        self.matched_position_profile = MatchedPositionProfile.generate_from_positions(
            pool = self
        )
        # self.matched_position_profile.print()
        return self.matched_position_profile


    @classmethod
    def load_from_json(
        cls,
        state,
        data: Union[str, dict]
    ):
        if type(data) == str:
            data = json.loads(data)
        return cls(
            state = state,
            id = data.get('id'),
            scenario_space = data.get('scenario_space'),
            currency = data.get('currency'),
            payoff_signature_length = data.get('payoff_signature_length'),
            price_schema = data.get('price_schema'),
            status = data.get('status'),
            min_residual_quantity = Decimal(data.get('min_residual_quantity')),
            min_post_quantity = Decimal(data.get('min_post_quantity')),
            supports_in_play = data.get('supports_in_play'),
            in_play_delay_seconds = Decimal(data.get('in_play_delay_seconds')),
            event_id = data.get('event')
        )
    

    def update_from_json(
        self,
        data: Union[str, dict]
    ):
        if type(data) == str:
            data = json.loads(data)
        self.scenario_space = data.get('scenario_space')
        self.currency = data.get('currency')
        self.payoff_signature_length = data.get('payoff_signature_length')
        self.price_schema = data.get('price_schema')
        self.status = data.get('status')
        self.min_residual_quantity = Decimal(data.get('min_residual_quantity'))
        self.min_post_quantity = Decimal(data.get('min_post_quantity'))
        self.supports_in_play = data.get('supports_in_play')
        self.in_play_delay_seconds = Decimal(data.get('in_play_delay_seconds'))
        self.event_id = data.get('event')
        

    @classmethod
    def load_from_client(
        cls,
        state,
        id: int
    ):
        pool_data = state.client.get_pools(
            pool_ids = [id]
        )[0]
        return cls.load_from_json(
            state = state,
            data = pool_data
        )

    @property
    def markets(self):
        return list(filter(
            lambda m: m.pool_id == self.id,
            self.state.markets.values()
        ))

    @property
    def selections(self):
        selections = []
        for m in self.markets:
            selections += m.selections
        return selections

    @property
    def orders(self):
        return list(filter(
            lambda o: o.pool_id == self.id,
            self.state.orders.values()
        ))

    @property
    def positions(self):
        positions = []
        for s in self.selections:
            position = self.state.positions.get(s.id)
            if position:
                positions += [position]
        return positions

    @property
    def price_schema(self):
        if self._price_schema.upper() == 'DEFAULT_PROBABILITY_SCHEMA':
            return DEFAULT_PROBABILITY_SCHEMA
        elif self._price_schema.upper() == 'DEFAULT_DECIMAL_SCHEMA':
            return DEFAULT_DECIMAL_SCHEMA
        elif self._price_schema.upper() == 'DEFAULT_AMERICAN_SCHEMA':
            return DEFAULT_AMERICAN_SCHEMA
        else:
            raise Exception
    
    @property
    def matched_exposure_vector(
        self,
    ):
        return self.matched_position_profile.calculate_exposure_vector()

    @property
    def unmatched_exposure_vector(
        self,
    ):
        return self.current_liquidity_profile.calculate_exposure_vector()
        
    @property
    def matched_and_unmatched_exposure_vector(
        self,
    ):
        return np.add(
            self.matched_exposure_vector,
            self.unmatched_exposure_vector
        )
    
    @property
    def max_liability(
        self
    ):
        return  Decimal(-1 * np.min(self.matched_and_unmatched_exposure_vector))


    def marginal_collateral_required_for_new_orders(
        self,
        new_orders: List[NewOrderArgs]
    ):
        new_matched_and_unmatched_exposure_vector = np.copy(self.matched_and_unmatched_exposure_vector)
        for order in new_orders:
            selection = self.state.selections.get(order.selection_id)
            if selection != None:
                probability_price = convert_to_probability(order.price, order.price_format)
                if order.side == OrderSide.BUY:
                    order_exposure_vector = selection.payoff_signature.generate_net_payoff_vector(
                        price = probability_price
                    ) * order.payout_quantity_remaining
                else:
                    order_exposure_vector = selection.payoff_signature.invert().generate_net_payoff_vector(
                        price= (Decimal(1)-probability_price)
                    ) * order.payout_quantity_remaining
            
            order_exposure_vector[
                order_exposure_vector > 0
            ] = Decimal(0)

            new_matched_and_unmatched_exposure_vector = np.add(
                new_matched_and_unmatched_exposure_vector,
                order_exposure_vector
            )

        new_max_liability = -1 * np.min(new_matched_and_unmatched_exposure_vector)

        marginal_capital_required = new_max_liability - self.max_liability 

        return marginal_capital_required




    def __repr__(self):
        return f"<Pool: {self.id}>"

    def __str__(self):
        return f"Pool: {self.id}"