from typing import Union, List
import json
from ..utils.payoff_signature import PayoffSignature
from decimal import Decimal
import time

class Selection():

    def __init__(
        self,
        state,
        id: int,
        market_id: int,
        name: str,
        competitor: Union[dict, None],
        resolution_status: Union[str, None],
        payoff_signature: str,
        display_order: int,
        status: str,
        price_probability: str
    ):
        self.state = state
        self.id = id
        self.market_id = market_id
        self.name = name
        self.competitor = competitor
        self.resolution_status = resolution_status
        self.payoff_signature = PayoffSignature.from_string(payoff_signature)
        self.display_order = display_order
        self.status = status
        self.price_probability = Decimal(price_probability) if price_probability else Decimal(1)
        self._update_timestamp = time.time()

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
            market_id = data.get('market'),
            name = data.get('name'),
            competitor = data.get('competitor'),
            resolution_status = data.get('resolution_status'),
            payoff_signature = data.get('payoff_signature'),
            display_order = data.get('display_order'),
            status =data.get('status'),
            price_probability = data.get('price_probability'),
        )
        
    @classmethod
    def load_from_client(
        cls,
        state,
        id: int
    ):
        selection_data = state.client.get_selections(
            selection_ids = [id]
        )[0]
        return cls.load_from_json(
            state = state,
            data = selection_data
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
    def positions(self):
        return self.state.positions.get(
            self.id
        )

    @property
    def orders(self):
        
        return list(
            filter(
                lambda o: o.selection_id == self.id,
                self.state.orders.values()
            )
        )

    @property
    def fair_price(self):
        
        return self.price_probability/self.market.book_total if self.market.book_total else self.price_probability

    def __repr__(self):
        return f"<Selection: {self.id}>"

    def __str__(self):
        return f"<Selection: {self.id}>"
