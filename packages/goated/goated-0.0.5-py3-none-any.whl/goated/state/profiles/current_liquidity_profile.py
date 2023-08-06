from decimal import Decimal
from ..order import Order, OrderSide
from typing import List
from ...instructions import NewOrderArgs, CancelOrderArgs, ReduceOrderArgs, OrderSide, OrderType, QuantityFormat, PersistenceType, PriceFormat
from .pool_profile import PoolProfile

class CurrentLiquidityProfile(PoolProfile):


    @classmethod
    def generate_from_orders(
        cls,
        pool,
        orders: List[Order] = None,
    ):
        instance = cls(
            pool = pool
        )

        if orders == None and pool:
            orders = pool.orders

        for order in orders:
            instance.add(
                market_id = int(order.market_id), 
                selection_id = int(order.selection_id),
                side = order.side,
                price = Decimal(order.probability_price),
                quantity = Decimal(order.payout_quantity_remaining)
            )
        return instance


    def solve_instructions_to_target(
        self,
        target_profile, #TargetLiquidityProfile
    ):
        '''
        Returns a dict of 'new', 'cancel' and 'reduce' lists, containing
        NewOrderArg, CancelOrderArgs and ReduceOrderArgs respectively.
        This is the optimal set of instructions to move from the current liquidity
        profile (self) to the target profile (provided).
        [NB: Optimum where we're optimizing for first removing the newest orders,
        rather than for fewest actions.]
        '''
        instructions = {
            'new': [],
            'cancel': [],
            'reduce': []
        }
        
        delta, actions = self.__class__.generate_delta_from_two_profiles(
            starting_profile = self,
            target_profile = target_profile,
        )

        delta.print()

        for action in actions:
            if action['type'] == 'new':
                instructions['new'] += [
                    NewOrderArgs(
                        market_id = action['market_id'],
                        selection_id = action['selection_id'],
                        side = action['side'],
                        type = OrderType.LIMIT,
                        price = Decimal(action['price']),
                        price_format = PriceFormat.PROBABILITY,
                        quantity = Decimal(action['quantity']),
                        quantity_format = QuantityFormat.PAYOUT,
                        persistence_type = PersistenceType.INCLUDE_IN_AUCTION
                    )
                ]
            elif action['type'] == 'cancel':
                relevant_orders = filter(
                    lambda o: (o.market_id == action['market_id'] and o.selection_id == action['selection_id'] and o.side == OrderSide(action['side']) and abs(o.price - action['price']) < Decimal(0.001)),
                    self.pool.orders
                )
                for o in relevant_orders:
                    instructions['cancel'] += [
                        CancelOrderArgs(
                            id = o.order_id
                        )
                    ]
            elif action['type'] == 'reduce':
                reduce_quantity = -action['quantity']
                relevant_orders = filter(
                    lambda o: (o.market_id == action['market_id'] and o.selection_id == action['selection_id'] and o.side == OrderSide(action['side']) and abs(o.price - action['price']) < Decimal(0.001)),
                    self.pool.orders
                )
                relevant_orders = sorted( # sorted by id in reverse (which is a proxy for sequence) so that we leave older orders (greater priority)
                    relevant_orders,
                    key = lambda o: int(o.id),
                    reverse = True
                )
                for o in relevant_orders:
                    if o.payout_quantity_remaining > reduce_quantity:
                        new_quantity = o.payout_quantity_remaining - reduce_quantity
                        reduce_quantity = 0
                    else:
                        new_quantity = 0
                        reduce_quantity -= o.payout_quantity_remaining
                    if new_quantity > 0:
                        instructions['reduce'] += [
                            ReduceOrderArgs(
                                order_id = o.id,
                                new_quantity = new_quantity,
                                quantity_format = QuantityFormat.PAYOUT
                            )
                        ]
                    else:
                        instructions['cancel'] += [
                            CancelOrderArgs(
                                order_id = o.id
                            )
                        ]
                    if reduce_quantity == 0: # Exit when we've reduced by the quantity required
                        break
            else:
                pass

        return instructions


    def solve_instructions_to_clear(
        self,
    ):
        '''
        Returns a dict of 'cancel' ('new' and 'reduce' there too, but empty)
        lists, containing CancelOrderArgs (NewOrderArg, ReduceOrderArg) required
        to clear the entire liquidity profile
        '''
        instructions = {
            'new': [],
            'cancel': [],
            'reduce': []
        }
        for o in self.orders:
            instructions['cancel'] += [
                CancelOrderArgs(
                    id = o.order_id
                )
            ]
        return instructions
        

    def print(
        self
    ):
        print('='*40)
        print('CURRENT LIQUIDITY PROFILE')
        print(f'Pool: {self.pool.id}')
        print('-'*40)
        for market_id in self.data.keys():
            print(f'MARKET: {market_id}')
            for selection_id in self.data[market_id].keys():
                print(f' - SELECTION: {selection_id}')
                for side in self.data[market_id][selection_id].keys():
                    print(f'   - {side.value.upper()}')
                    for price, quantity in sorted(self.data[market_id][selection_id][side].items()):
                        print(f'      {price:.3f}: {quantity:8.2f}')
            print('-'*40)
        print('='*40)




