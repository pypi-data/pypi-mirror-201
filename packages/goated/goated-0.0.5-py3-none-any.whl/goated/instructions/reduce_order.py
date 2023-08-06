from .enums import *
from decimal import Decimal
import json
from datetime import datetime
from typing import List
from ..utils.encoder import OrderEncoder


class ReduceOrderArgs():

    def __init__(
        self,
        order_id: int,
        new_quantity: Decimal,
        quantity_format: QuantityFormat,
    ):
        self.order = order_id
        self.new_quantity = new_quantity
        self.quantity_format = quantity_format

    @classmethod
    def load_from_json(
        self,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        self.id = data.get('id')
        self.new_quantity = Decimal(data.get('new_quantity'))
        self.quantity_format = QuantityFormat(data.get('quantity_format'))
    
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
