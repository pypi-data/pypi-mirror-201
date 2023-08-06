from decimal import Decimal
from typing import List
from datetime import datetime
from ..instructions import OrderSide, OrderType, PriceFormat, QuantityFormat, PersistenceType
import json
import time

class Order():
    
    def __init__(
        self,
        state,
        id: int,
        market_id: int,
        selection_id: int,
        currency: str,
        side: OrderSide,
        type: OrderType,
        custom_order_id: str,
        custom_strategy_id: str,
        probability_price: Decimal,
        price: Decimal,
        price_format: PriceFormat,
        quantity: Decimal,
        quantity_format: QuantityFormat,
        persistence_type: PersistenceType,
        status: str,
        payout_quantity_requested: Decimal,
        stake_quantity_requested: Decimal,
        payout_quantity_filled: Decimal,
        stake_quantity_filled: Decimal,
        payout_quantity_cancelled: Decimal,
        stake_quantity_cancelled: Decimal,
        payout_quantity_lapsed: Decimal,
        stake_quantity_lapsed: Decimal,
        payout_quantity_voided: Decimal,
        stake_quantity_voided: Decimal,
        payout_quantity_remaining: Decimal,
        stake_quantity_remaining: Decimal,
        average_matched_price: Decimal,
        removal_reason: str,
        matched_timestamp: datetime,
        lapse_timestamp: datetime,
        cancel_timestamp: datetime,
        created: datetime,
        is_removed = bool,
        is_open  = bool,
        is_matched = bool, 
        is_settled = bool,
    ):
        self.state = state
        self.id = id
        self.market_id = market_id
        self.selection_id = selection_id
        self.currency = currency
        self.side = side
        self.type = type
        self.custom_order_id = custom_order_id
        self.custom_strategy_id = custom_strategy_id
        self.probability_price = probability_price
        self.price = price
        self.price_format = price_format
        self.quantity = quantity
        self.quantity_format = quantity_format
        self.persistence_type = persistence_type
        self.status = status
        self.payout_quantity_requested = payout_quantity_requested
        self.stake_quantity_requested = stake_quantity_requested
        self.payout_quantity_filled = payout_quantity_filled
        self.stake_quantity_filled = stake_quantity_filled
        self.payout_quantity_cancelled = payout_quantity_cancelled
        self.stake_quantity_cancelled = stake_quantity_cancelled
        self.payout_quantity_lapsed = payout_quantity_lapsed
        self.stake_quantity_lapsed = stake_quantity_lapsed
        self.payout_quantity_voided = payout_quantity_voided
        self.stake_quantity_voided = stake_quantity_voided
        self.payout_quantity_remaining = payout_quantity_remaining
        self.stake_quantity_remaining = stake_quantity_remaining
        self.average_matched_price = average_matched_price
        self.removal_reason = removal_reason
        self.matched_timestamp = matched_timestamp
        self.lapse_timestamp = lapse_timestamp
        self.cancel_timestamp = cancel_timestamp
        self.created = created
        self.is_removed= is_removed
        self.is_open = is_open 
        self.is_matched = is_matched 
        self.is_settled= is_settled
        self._pool_id = None
        self._update_timestamp = time.time()

    

    def __repr__(self):
        return f"<Order: {self.id} | {self.selection_id} | {str(self.side)}" + (f"{self.payout_quantity_remaining:.2f} @ {self.probability_price:.3f}") if self.status != 'pending' else "" + f" {self.status.upper()}>"

    def __str__(self):
        return f"<Order: {self.id} | {self.selection_id} | {str(self.side)}" + (f"{self.payout_quantity_remaining:.2f} @ {self.probability_price:.3f}") if self.status != 'pending' else "" + f" {self.status.upper()}>"

    @classmethod
    def load_from_json(
        cls,
        state,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        return cls(
            state = state,
            id = data.get('id'),
            market_id = data.get('market'),
            selection_id = data.get('selection'),
            currency = data.get('currency'),
            side = OrderSide(data.get('side')),
            type = OrderType(data.get('type')),
            custom_order_id = data.get('custom_order_id'),
            custom_strategy_id = data.get('custom_strategy_id'),
            probability_price = Decimal(data.get('probability_price')) if data.get('probability_price') != None else None,
            price = Decimal(data.get('price')) if data.get('price') != None else None,
            price_format = PriceFormat(data.get('price_format')),
            quantity = Decimal(data.get('quantity')) if data.get('quantity') != None else None,
            quantity_format = QuantityFormat(data.get('quantity_format')),
            persistence_type = PersistenceType(data.get('persistence_type')),
            status = data.get('status'),
            payout_quantity_requested = Decimal(data.get('payout_quantity_requested')) if data.get('payout_quantity_requested') != None else None,
            stake_quantity_requested = Decimal(data.get('stake_quantity_requested')) if data.get('stake_quantity_requested') != None else None,
            payout_quantity_filled = Decimal(data.get('payout_quantity_filled')) if data.get('payout_quantity_filled') != None else None,
            stake_quantity_filled = Decimal(data.get('stake_quantity_filled')) if data.get('stake_quantity_filled') != None else None,
            payout_quantity_cancelled = Decimal(data.get('payout_quantity_cancelled')) if data.get('payout_quantity_cancelled') != None else None,
            stake_quantity_cancelled = Decimal(data.get('stake_quantity_cancelled')) if data.get('stake_quantity_cancelled') != None else None,
            payout_quantity_lapsed = Decimal(data.get('payout_quantity_lapsed')) if data.get('payout_quantity_lapsed') != None else None,
            stake_quantity_lapsed = Decimal(data.get('stake_quantity_lapsed')) if data.get('stake_quantity_lapsed') != None else None,
            payout_quantity_voided = Decimal(data.get('payout_quantity_voided')) if data.get('payout_quantity_voided') != None else None,
            stake_quantity_voided = Decimal(data.get('stake_quantity_voided')) if data.get('stake_quantity_voided') != None else None,
            payout_quantity_remaining = Decimal(data.get('payout_quantity_remaining')) if data.get('payout_quantity_remaining') != None else None,
            stake_quantity_remaining = Decimal(data.get('stake_quantity_remaining')) if data.get('stake_quantity_remaining') != None else None,
            average_matched_price = Decimal(data.get('average_matched_price')) if data.get('average_matched_price') != None else None,
            removal_reason = data.get('removal_reason'),
            matched_timestamp = datetime.strptime(data.get('matched_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get('matched_timestamp') != None else None,
            lapse_timestamp = datetime.strptime(data.get('lapse_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get('lapse_timestamp') != None else None,
            cancel_timestamp = datetime.strptime(data.get('cancel_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get('cancel_timestamp') != None else None,
            created = datetime.strptime(data.get('created'), "%Y-%m-%dT%H:%M:%S.%fZ"),
            is_removed = data.get('is_removed'),
            is_open = data.get('is_open'),
            is_matched = data.get('is_matched'),
            is_settled = data.get('is_settled'),
        )

    @property
    def selection(self):
        return self.state.selections.get(
            self.selection_id
        )
    
    @property
    def market(self):
        return self.state.markets.get(
            self.market_id
        )

    @property
    def pool(self):
        if self.market:
            return self.market.pool
        return None

    @property
    def pool_id(self):
        if not self._pool_id:
            market = self.state.markets.get(self.market_id)  
            if market:
                self._pool_id = market.pool_id
        return self._pool_id