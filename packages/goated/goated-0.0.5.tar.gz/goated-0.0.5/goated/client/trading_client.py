from .exceptions import *
import json
from .base_client import BaseClient
from typing import List
from ..instructions import NewOrderArgs, CancelOrderArgs, ReduceOrderArgs, UpdateOrderPersistenceArgs, PriceFormat, OrderStatus, OrderSide, OrderType, QuantityFormat

class TradingClient(BaseClient):


    # EXCHANGE (GENERAL/PUBLIC) INFORMATION

    def get_categories(
        self,
        category_ids: List[int] = []
    ):
        '''
        Returns a list of categories and category meta data.
        category_ids are an optional list of filter parameters which can be passed to narrow the request.
        '''
        filters = {}
        if category_ids != []:
            filters['category_id'] = ','.join([str(s) for s in category_ids])

        response = self._get_objects(
            endpoint = "exchange/categories",
            filters = filters
        )   

        return response

    def get_subcategories(
        self,
        category_ids: List[int] = [],
        subcategory_ids: List[int] = [],
    ):
        '''
        Returns a list of subcategories and subcategory meta data.
        category_ids and subcategory_ids are an optional list of filter parameters which can be passed to narrow the request.
        '''
        filters = {}
        if category_ids != []:
            filters['category_id'] = ','.join([str(s) for s in category_ids])
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])

        response = self._get_objects(
            endpoint = "exchange/subcategories",
            filters = filters
        )   

        return response
    
    def get_events(
        self,
        category_ids: List[int] = [],
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
    ):
        '''
        Returns a list of events and event meta data.
        category_ids, subcategory_ids and event_ids are an optional list of filter parameters which can be passed to narrow the request.
        '''

        filters = {}
        if category_ids != []:
            filters['category_id'] = ','.join([str(s) for s in category_ids])
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
            
        response = self._get_objects(
            endpoint = "exchange/events",
            filters = filters
        )   

        return response



    def get_markets(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        pool_ids: List[int] = [],
        market_ids: List[int] = [],
        market_type_ids: List[int] = [],
        currencies: List[str] = [],
        lines: List[float] = [],
        going_in_play: bool = None,
        main_market: bool = None,
    ):
        '''
        Returns a list of markets and market data for markets which meet the filter criteria.
        The following optional filter parameters can be used to narrow the search:
        - subcategory_ids
        - event_ids
        - pool_ids
        - market_type_ids
        - currencies
        - lines
        - going_in_play
        - main_market
        '''
        filters = {}
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if pool_ids != []:
            filters['pool_id'] = ','.join([str(p) for p in pool_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if lines != []:
            filters['line'] = ','.join([str(l) for l in lines])
        if currencies != []:
            filters['currency'] = ','.join([str(m) for m in currencies])
        if market_type_ids != []:
            filters['market_type'] = ','.join([str(m) for m in market_type_ids])
        if going_in_play != None:
            filters['going_in_play'] = "true" if going_in_play else "false"
        if main_market != None:
            filters['main_market'] = "true" if main_market else "false"

        response = self._get_objects(
            endpoint = "exchange/markets",
            filters = filters
        )   

        return response

    def get_selections(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        pool_ids: List[int] = [],
        market_ids: List[int] = [],
        selection_ids: List[int] = [],
        market_type_ids: List[int] = [],
        currencies: List[str] = [],
        lines: List[float] = [],
        going_in_play: bool = None,
        main_market: bool = None,
    ):
        '''
        Returns a list of selections and selection data for selections which meet the filter criteria.
        The following optional filter parameters can be used to narrow the search:
        - subcategory_ids
        - event_ids
        - pool_ids
        - market_ids
        - selection_ids
        - market_type_ids
        - currencies
        - lines
        - going_in_play
        - main_market
        '''
        filters = {}
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if pool_ids != []:
            filters['pool_id'] = ','.join([str(p) for p in pool_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if selection_ids != []:
            filters['selection_id'] = ','.join([str(s) for s in selection_ids])
        if lines != []:
            filters['line'] = ','.join([str(l) for l in lines])
        if currencies != []:
            filters['currency'] = ','.join([str(m) for m in currencies])
        if market_type_ids != []:
            filters['market_type'] = ','.join([str(m) for m in market_type_ids])
        if going_in_play != None:
            filters['going_in_play'] = 1 if going_in_play else 0
        if main_market != None:
            filters['main_market'] = 1 if main_market else 0

        response = self._get_objects(
            endpoint = "exchange/selections",
            filters = filters
        )  

        return response

    def get_orderbooks(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        pool_ids: List[int] = [],
        market_ids: List[int] = [],
        selection_ids: List[int] = [],
        main_market: bool = None,
        hybrid: bool = True,
        max_depth: bool = None,
        price_format: PriceFormat = None,
        quantity_format: QuantityFormat = None,
    ):
        '''
        Returns orderbook data for selections which meet the filter criteria.
        The following optional filter parameters can be used to narrow the search:
        - subcategory_ids
        - event_ids
        - pool_ids
        - market_ids
        - selection_ids
        - main_market
        The following parameters can be used to adjust the data which is returned:
        - hybrid: Defaults to True. If True will return the hybrid orderbook view - both 'real' and 'synthetic' or 'cross-matched' orders.
        - max_depth: The maximum number of price ticks to return on any given selection and side. Defaults to provide all.
        - price_format: The format of the price to be returned. Defaults to Probability. Decimal and American odds formats are possible.
        - quantity_format: The format of the quantity to be returned. Defaults to Payout. Stake format also possible.
        '''
        filters = {}
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if pool_ids != []:
            filters['pool_id'] = ','.join([str(p) for p in pool_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if selection_ids != []:
            filters['selection_id'] = ','.join([str(s) for s in selection_ids])
        if main_market != None:
            filters['main_market'] = "true" if main_market else "false"
        if hybrid != None:
            filters['hybrid'] = "true" if hybrid else "false"
        if max_depth != None:
            filters['max_depth'] = str(max_depth)
        if price_format != None:
            filters['price_format'] = str(price_format)
        if quantity_format != None:
            filters['quantity_format'] = str(quantity_format)

        response = self._get_objects(
            endpoint = "exchange/orderbook",
            filters = filters
        )  

        return response

    def get_price_histories(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        pool_ids: List[int] = [],
        market_ids: List[int] = [],
        selection_ids: List[int] = [],
        main_market: bool = None,
        interval: int = None, # 300, 900, 3600, 14400, 28800, 86400
        price_format: PriceFormat = None,
        include_components: bool = None,
    ):
        '''
        Returns price history for selections which meet the filter criteria.
        The following optional filter parameters can be used to narrow the search:
        - subcategory_ids
        - event_ids
        - pool_ids
        - market_ids
        - selection_ids
        - main_market
        The following parameters can be used to adjust the data which is returned:
        - interval: The interval of timesteps at which prices are provided, in seconds. Possible values: 300, 900, 3600, 14400, 28800, 86400. By default, the server will return the interval which approximately 30 time steps.
        - price_format: The format of the price to be returned. Defaults to Probability. Decimal and American odds formats are possible.
        - include_components: Defaults to False. If True, returns a breakdown of the best bid, best ask and last traded price at each time step.
        '''
        filters = {}
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if pool_ids != []:
            filters['pool_id'] = ','.join([str(p) for p in pool_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if selection_ids != []:
            filters['selection_id'] = ','.join([str(s) for s in selection_ids])
        if main_market != None:
            filters['main_market'] = "true" if main_market else "false"
        if include_components != None:
            filters['include_components'] = "true" if include_components else "false"
        if price_format != None:
            filters['price_format'] = str(price_format)
        if interval != None:
            filters['interval'] = str(interval)

        response = self._get_objects(
            endpoint = "exchange/history",
            filters = filters
        )  

        return response


    

    # EXCHANGE USER-SPECIFIC INFORMATION

    def get_balances(
        self,
    ):
        '''
        Returns the balances (for each applicable supported currency) held by the authenticated user account.
        '''
        response = self._send_get(
            endpoint = "balances",
        )   
        return response

    def get_orders(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        market_ids: List[int] = [],
        selection_ids: List[int] = [],
        order_ids: List[int] = [],
        status: List[OrderStatus] = []
    ):
        '''
        Gets orders owned by the authenticaed user account.
        By default this query will return orders which have some non-zero 'open' or unmatched component. i.e. orders which have
        been fully cancelled, fully matched or for which trading has ended will not appear in the response.
        Optional filter parameters:
        - subcategory_ids
        - event_ids 
        - market_ids
        - selection_ids
        - order_ids
        - status
        '''
        filters = {}
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if selection_ids != []:
            filters['selection_id'] = ','.join([str(s) for s in selection_ids])
        if order_ids != []:
            filters['order_id'] = ','.join([str(o) for o in order_ids])
        if status != []:
            filters['status'] = ','.join([str(s) for s in selection_ids])
            
        response = self._get_objects(
            endpoint = "exchange/orders",
            filters = filters
        )

        return response

    def get_positions(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        market_ids: List[int] = [],
        selection_ids: List[int] = [],
    ):
        '''
        Gets matched positions currently held by the authenticaed user account.
        This provides the net/aggregate payout and stake for any selections (within the filtered subset)
        in active markets, for which the user has a non-zero matched exposure.
        Further breakdown is provided by selection, side and price tick.
        Optional parameters:
        - subcategory_ids
        - event_ids 
        - market_ids
        - selection_ids
        '''
        filters = {}
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if market_ids != []:
            filters['market_id'] = ','.join([str(m) for m in market_ids])
        if selection_ids != []:
            filters['selection_id'] = ','.join([str(s) for s in selection_ids])

        response = self._get_objects(
            endpoint = "exchange/positions",
            filters = filters
        )   

        return response

    def get_exposures(
        self,
        subcategory_ids: List[int] = [],
        event_ids: List[int] = [],
        pool_ids: List[int] = [],
    ):
        '''
        Gets the authenticated user's risk exposure profile for a given Pool.
        (Pools are at the level of related markets where some risk offsetting between related markets
        is allowed by the Goated risk engine.)
        Optional parameters:
        - subcategory_ids
        - event_ids 
        - market_ids
        '''
        filters = {}
        if event_ids != []:
            filters['event_id'] = ','.join([str(e) for e in event_ids])
        if subcategory_ids != []:
            filters['subcategory_id'] = ','.join([str(s) for s in subcategory_ids])
        if pool_ids != []:
            filters['pool_id'] = ','.join([str(m) for m in pool_ids])
     

        response = self._get_objects(
            endpoint = "exchange/exposures",
            filters = filters
        )   

        return response


    # EXCHANGE ACTIONS

    def place_orders(
        self,
        orders: List[NewOrderArgs],
        asynchronous: bool = False # TODO: Functionality not yet supported
    ): 
        '''
        Places a list of orders on behalf of the authenticated user.
        Parameters:
        - orders: A list of valid NewOrderArgs
        - asynchronous: (Not currently supported) indicating whether or not the server should hang and await completion of the
        matching engine's round trip before providing an API response, or return a tentative confirmation once the orders have been
        placed.
        '''
        if type(orders) != list:
            orders = [orders]
        data = [
            o.serialize_to_dict()
            for o in orders
        ]
        print(data)
        response = self._send_post(
            endpoint = "exchange/orders/new",
            data = data,
            params = {}
        )
        return response

    def cancel_orders(
        self,
        orders: List[CancelOrderArgs],
        asynchronous: bool = False # TODO: Functionality not yet supported
    ): 
        '''
        Requests to cancel existing orders on behalf of the authenticated user.
        Parameters:
        - orders: A list of valid CancelOrderArgs
        - asynchronous: (Not currently supported) indicating whether or not the server should hang and await completion of the
        matching engine's round trip before providing an API response, or return a tentative confirmation once the cancel 
        order request have been placed.
        '''
        if type(orders) != list:
            orders = [orders]
        data = [
            o.serialize_to_dict()
            for o in orders
        ]
        response = self._send_post(
            endpoint = "exchange/orders/cancel",
            data = data,
            params = {}
        )
        return response

    def reduce_orders(
        self,
        orders: List[ReduceOrderArgs],
        asynchronous: bool = False # TODO: Functionality not yet supported
    ): 
        '''
        Requests to reduce the quantity of existing orders on behalf of the authenticated user.
        Parameters:
        - orders: A list of valid ReduceOrderArgs
        - asynchronous: (Not currently supported) indicating whether or not the server should hang and await completion of the
        matching engine's round trip before providing an API response, or return a tentative confirmation once the reduce 
        order request have been placed.
        '''
        if type(orders) != list:
            orders = [orders]
        data = [
            o.serialize_to_dict()
            for o in orders
        ]
        response = self._send_post(
            endpoint = "exchange/orders/edit",
            data = data,
            params = {}
        )
        return response

    def update_persistence_orders(
        self,
        orders: List[UpdateOrderPersistenceArgs],
        asynchronous: bool = False # TODO: Functionality not yet supported
    ): 
        '''
        Requests to update the persistence type for existing orders on behalf of the authenticated user.
        Parameters:
        - orders: A list of valid CancelOrderArgs
        - asynchronous: (Not currently supported) indicating whether or not the server should hang and await completion of the
        matching engine's round trip before providing an API response, or return a tentative confirmation once the persistence type 
        update requests have been placed.
        '''
        if type(orders) != list:
            orders = [orders]
        data = [
            o.serialize_to_dict()
            for o in orders
        ]
        response = self._send_post(
            endpoint = "exchange/orders/edit",
            data = data,
            params = {}
        )
        return response