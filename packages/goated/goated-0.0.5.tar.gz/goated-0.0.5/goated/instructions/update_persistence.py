from .enums import *
from decimal import Decimal
import json
from datetime import datetime
from typing import List
from ..utils.encoder import OrderEncoder


class UpdateOrderPersistenceArgs():

    def __init__(
        self,
        order_id: int,
        persistence_type: PersistenceType
    ):
        self.order = order_id
        self.persistence_type = persistence_type

    @classmethod
    def load_from_json(
        self,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        self.id = data.get('id')
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