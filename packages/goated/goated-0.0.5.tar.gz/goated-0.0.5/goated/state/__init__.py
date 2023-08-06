"""
State Module
------------
This module is intended to support local state management of 
Goated information.

The module include native Python classes for Goated objects - such as Pools,
Markets, Selections, Orders and Positions.

It also included Profiles tools, which can be used to help model
the liquidity shown by traders or market makers on the exchange.

The Container object is a useful implementation for storing and maintaining
relationships between different objects cached in local memory. i.e. it enables
an implementation to retain and refresh cached information from the Goated API and interact
with the related objects naturally.

"""

from .container import Container
from .pool import Pool
from .market import Market
from .selection import Selection
from .order import Order
from .position import Position
from .profiles import CurrentLiquidityProfile, PoolProfile, MatchedPositionProfile, TargetLiquidityProfile
