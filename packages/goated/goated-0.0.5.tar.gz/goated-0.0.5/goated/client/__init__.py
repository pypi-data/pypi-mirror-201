"""
Client Module
-------------
This module contains BaseClient and TradingClient classes.
The BaseClient handles authentication and basic request wrappers.
The TradingClient extends the base client to include functionality
required to source listing information and to interact with 
the platform (managing orders) for an authenticated user account.


"""

from .base_client import BaseClient
from .trading_client import TradingClient
