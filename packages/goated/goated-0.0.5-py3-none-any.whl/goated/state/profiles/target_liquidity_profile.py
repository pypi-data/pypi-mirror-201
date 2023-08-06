from .pool_profile import PoolProfile


class TargetLiquidityProfile(PoolProfile):

    # Inherits all necessary functionality 
    # from the parent PoolProfile class

    def print(
        self
    ):
        print('='*40)
        print('TARGET LIQUIDITY PROFILE')
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