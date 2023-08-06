import json
from typing import Union, List
from .order import Order
from .position import SelectionPosition
from .pool import Pool
from .market import Market
from .selection import Selection

class Container():

    def __init__(
        self,
    ):
        self.balances = {}
        self.positions = {}
        self.orders = {}
        self.pools = {}
        self.markets = {}
        self.selections = {}

    def update_balances(
        self,
        data: Union[str, dict]
    ):  
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for balance in data:
            self.balances[balance.get('currency')] = balance

    def remove_balance(
        self,
        currency: str
    ):
        if currency in self.balances.keys():
            self.orders.pop(str(currency))
        else:
            print('No balance found for this currency')


    def update_orders(
        self,
        data: Union[dict, str, list]
    ):
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for order_data in data:

            # Create an in-memory representation
            order = Order.load_from_json(
                state = self,
                data = order_data
            )

            # If the order has been removed, pop it from our collection
            if order.is_removed and order.id in self.orders.keys():
                self.orders.pop(order.id)

            # Otherwise, if it's open (not failed/pending) then we should include or update
            #  it within our collection
            elif order_data.get('is_open') and order_data.get('status') not in ['pending', 'failed']:
                self.orders[order_data.get('id')] = order
      
            else:
                pass # Don't store orders which aren't open
            
            
    def remove_order(
        self,
        order_id: int
    ):
        if order_id in self.orders.keys():
            self.orders.pop(int(order_id))
        else:
            print('No order found for this order_id')


    def update_positions(
        self,
        data: Union[dict, str, list]
    ):
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for position_data in data:
            position = SelectionPosition.load_from_json(
                state = self,
                data = position_data
            )
            self.positions[position_data.get('id')] = position
            if position.pool:
                position.pool._positions_updated = True
            


    def remove_position(
        self,
        selection_id: int
    ):
        if selection_id in self.positions.keys():
            self.positions.pop(int(selection_id))
        else:
            print('No positions found for this selection_id')


    def update_pools(
        self,
        data: Union[dict, str, list]
    ):
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for pool_data in data:
            if pool_data.get('id') not in self.pools.keys():
                self.pools[pool_data.get('id')] = Pool.load_from_json(
                    state = self,
                    data = pool_data
                )
            else:
                self.pools[pool_data.get('id')].update_from_json(
                    state = self,
                    data = pool_data
                )

    def remove_pool(
        self,
        pool_id: int,
        remove_markets: bool = True,
        remove_selections: bool = True
    ):
        if pool_id in self.pools.keys():
            pool = self.pools.pop(int(pool_id))
            if remove_markets:
                for market in pool.markets:
                    self.remove_market(
                        market_id = market.id,
                        remove_selections = remove_selections
                    )
        else:
            print('No pool found for this id')
    
    def update_markets(
        self,
        data: Union[dict, str, list]
    ):
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for market_data in data:
            market = Market.load_from_json(
                state = self,
                data = market_data
            )
            self.markets[market.id] = market
            if market.pool:
                market.pool._markets_updated = True
           

    def remove_market(
        self,
        market_id: int,
        remove_selections: bool = True
    ):
        if market_id in self.markets.keys():
            market = self.markets.pop(int(market_id))
            if remove_selections:
                for selection in market.selections:
                    self.remove_selection(
                        selection_id = selection.id
                    )
        else:
            print('No market found for this id')


    def update_selections(
        self,
        data: Union[dict, str, list]
    ):
        if type(data) == str:
            data = json.loads(data)
        if type(data) != list:
            data = [data]
        for selection_data in data:
            selection = Selection.load_from_json(
                state = self,
                data = selection_data
            )
            self.selections[selection_data.get('id')] = selection
            if selection.pool:
                selection.pool._selections_updated = True
            

    def remove_selection(
        self,
        selection_id: int
    ):
        if selection_id in self.selections.keys():
            selection = self.selections.pop(int(selection_id))
        else:
            print('No selection found for this id')

  
    @property
    def market_ids(
        self,
    ): 
        return list(self.markets.keys())
    
    @property
    def selection_ids(
        self,
    ): 
        return list(self.selections.keys())
    
    @property
    def order_ids(
        self,
    ): 
        return list(self.orders.keys())