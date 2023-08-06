from .enums import *
from decimal import Decimal
import json
from datetime import datetime
from typing import List
from ..utils.encoder import OrderEncoder


class NewOrderArgs():

    def __init__(
        self,
        market_id: int,
        selection_id: int,
        side: OrderSide,
        type: OrderType,
        price: Decimal,
        price_format: PriceFormat,
        quantity: Decimal,
        quantity_format: QuantityFormat,
        persistence_type: PersistenceType,
        custom_order_id: str = None,
        custom_strategy_id: str = None,
    ):
        self.market = market_id
        self.selection = selection_id
        self.side = side
        self.type = type
        self.price = price
        self.price_format = price_format
        self.quantity = quantity
        self.quantity_format = quantity_format
        self.persistence_type = persistence_type
        self.custom_order_id = custom_order_id
        self.custom_strategy_id = custom_strategy_id


    @classmethod
    def load_from_json(
        self,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        self.market_id = data.get('market')
        self.selection_id = data.get('selection')
        self.side = OrderSide(data.get('side'))
        self.type = OrderType(data.get('type'))
        self.price = Decimal(data.get('price'))
        self.price_format = PriceFormat(data.get('price_format'))
        self.quantity = Decimal(data.get('quantity'))
        self.quantity_format = QuantityFormat(data.get('quantity_format'))
        self.persistence_type = PersistenceType(data.get('persistence_type'))

    def serialize_to_json(
        self,
    ):
        return json.dumps(
            self.__dict__,
            cls=OrderEncoder
        )
    
    def serialize_to_dict(
        self,
    ):
        d = json.loads(
            self.serialize_to_json()
        )
        keys = [k for k in d.keys()]
        for k in keys:
            if d.get(k) == None:
                d.pop(k)
        return d
