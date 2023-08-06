"""
Instructions Module
-------------------
This module deals primarily with assembling and relaying instructions
to the Goated Exchange on behalf of the authenticated user account.

Instructions currently supported include:
- Requests to place new orders on the exchange
- Requests to cancel or remove (in full) existing orders 
- Requests to reduce the remaining (unmatched) quantity of existing orders
- Requests to update the persistency type of an existing order
"""


from .enums import *
from .new_order import NewOrderArgs
from .cancel_order import CancelOrderArgs
from .reduce_order import ReduceOrderArgs
from .update_persistence import UpdateOrderPersistenceArgs
