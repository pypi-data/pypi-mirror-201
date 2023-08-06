import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):

    recognized_types = [
        str, int, float, list, dict, bool,
    ]

    def default(self, obj):

        if isinstance(obj, Decimal):
            return f"{obj:.18f}"
            
        elif not type(obj) in self.recognized_types:
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class OrderEncoder(json.JSONEncoder):

    recognized_types = [
        str, int, float, list, dict, bool,
    ]

    def default(self, obj):

        if isinstance(obj, Decimal):
            return f"{obj:.6f}"
            
        elif not type(obj) in self.recognized_types:
            return obj.value

        return json.JSONEncoder.default(self, obj)
