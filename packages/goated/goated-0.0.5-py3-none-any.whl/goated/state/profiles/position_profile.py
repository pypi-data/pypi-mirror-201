from .pool_profile import PoolProfile
from decimal import Decimal
from ..position import Position
from ..order import OrderSide
from typing import List


class MatchedPositionProfile(PoolProfile):

    # Inherits all necessary functionality 
    # from the parent PoolProfile class

    @classmethod
    def generate_from_positions(
        cls,
        pool,
        positions: List[Position] = None,
    ):
        instance = cls(
            pool = pool
        )

        if positions == None and pool:
            positions = pool.positions

        for position in positions:
            if position.net_payout > 0:
                side = OrderSide.BUY
                quantity = Decimal(position.net_payout)
            else:
                side = OrderSide.SELL
                quantity = Decimal(-position.net_payout)
            instance.add(
                market_id = int(position.market_id), 
                selection_id = int(position.selection_id),
                side = side,
                price = Decimal(position.new_stake / position.net_payout) if position.net_payout != 0 else Decimal(0),
                quantity = quantity
            )
        return instance

    def print(
        self
    ):
        print('='*40)
        print('POSITION PROFILE')
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