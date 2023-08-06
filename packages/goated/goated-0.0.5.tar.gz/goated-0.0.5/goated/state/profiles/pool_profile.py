from decimal import Decimal
from ..order import Order, OrderSide
from typing import List
import numpy as np


class PoolProfile():

    def __init__(
        self,
        pool
    ):
        self.data = {}
        self.pool = pool

    def __setitem__(
        self,
        index, # (market_id, selection_id, buy/sell, price)
        value
    ):
        market_id, selection_id, side, price = index
        # if side not in [OrderSide.BUY, OrderSide.SELL]:
        #     raise Exception
        if market_id not in self.data.keys():
            self.data[market_id] = {}
        if selection_id not in self.data[market_id].keys():
            self.data[market_id][selection_id] = {
                OrderSide.BUY: {},
                OrderSide.SELL: {}
            }
        self.data[market_id][selection_id][side][price] = value
   
    def __getitem__(
        self,
        index, # (market_id, selection_id, buy/sell, price)
    ):
        # print(index)
        try:
            market_id, selection_id, side, price = index
            # print(market_id, selection_id, side, price)
            return self.data[market_id][selection_id][side][price]
        except:
            return None
   
    def add(
        self,
        market_id: int,
        selection_id: int,
        side: str,
        price: Decimal,
        quantity
    ):
        current_quantity = self[(market_id, selection_id, side, price)]
        if current_quantity is None:
            self[(market_id, selection_id, side, price)] = quantity
        else:
            self[(market_id, selection_id, side, price)] = current_quantity + quantity

    def subtract(
        self,
        market_id: int,
        selection_id: int,
        side: str,
        price: Decimal,
        quantity
    ):
        current_quantity = self[(market_id, selection_id, side, price)]
        if current_quantity is None:
            self[(market_id, selection_id, side, price)] = -quantity
        else:
            self[(market_id, selection_id, side, price)] = current_quantity - quantity

    def remove(
        self,
        market_id: int,
        selection_id: int,
        side: str,
        price: Decimal,
        quantity
    ):
        current_quantity = self[(market_id, selection_id, side, price)]
        if current_quantity is not None:
            self[(market_id, selection_id, side, price)] = current_quantity - quantity


    @property
    def market_ids(
        self,
    ):
        return list(self.data.keys())

    @property
    def selection_ids(
        self,
    ):
        selection_ids = []
        for market_id in self.market_ids:
            selection_ids += list(self.data[market_id].keys())
        return selection_ids


    @classmethod
    def generate_delta_from_two_profiles(
        cls,
        target_profile,
        starting_profile
    ):
        if target_profile.pool != starting_profile.pool:
            raise Exception

        delta_profile = cls(
            pool=target_profile.pool
        )
        actions = []

        for market_id in target_profile.data.keys():
            for selection_id in target_profile.data[market_id].keys():
                for side in target_profile.data[market_id][selection_id].keys():
                    for price in target_profile.data[market_id][selection_id][side].keys():
                        delta_profile.add(
                            market_id = market_id, 
                            selection_id = selection_id,
                            side = side,
                            price = round(price, 5),
                            quantity = target_profile.data[market_id][selection_id][side][price]
                        )

        for market_id in starting_profile.data.keys():
            for selection_id in starting_profile.data[market_id].keys():
                for side in starting_profile.data[market_id][selection_id].keys():
                    for price in starting_profile.data[market_id][selection_id][side].keys():
                        delta_profile.subtract(
                            market_id = market_id, 
                            selection_id = selection_id,
                            side = side,
                            price = round(price, 5),
                            quantity = starting_profile.data[market_id][selection_id][side][price]
                        )

        for market_id in delta_profile.data.keys():
            for selection_id in delta_profile.data[market_id].keys():
                for side in delta_profile.data[market_id][selection_id].keys():
                    for price in delta_profile.data[market_id][selection_id][side].keys():
                        
                        delta_quantity = delta_profile[market_id, selection_id, side, price] 
                        starting_quantity = starting_profile[market_id, selection_id, side, price] 
                        starting_quantity = 0 if starting_quantity == None else starting_quantity
                        action = None

                        if abs(delta_quantity) < Decimal(0.01): #i.e. no material change
                            pass # no action required
                        elif delta_quantity > 0: # Increase only
                            action = {
                                'type': 'new',
                                'market_id': market_id,
                                'selection_id': selection_id,
                                'side': side,
                                'price': price,
                                'quantity': delta_quantity
                            }
                        else: # i.e. delta_quantity < 0:
                            if abs(starting_quantity - delta_quantity) < Decimal(0.01):
                                action = {
                                    'type': 'remove',
                                    'market_id': market_id,
                                    'selection_id': selection_id,
                                    'side': side,
                                    'price': price,
                                    'quantity': delta_quantity
                                }
                            else: # Just a reduction
                                action = {
                                    'type': 'reduce',
                                    'market_id': market_id,
                                    'selection_id': selection_id,
                                    'side': side,
                                    'price': price,
                                    'quantity': delta_quantity
                                }

                        if action:
                            actions += [action]

        return delta_profile, actions

    def calculate_exposure_vector(
        self,
    ):
        unmatched_exposure_vector = np.asarray([Decimal(0) for i in range(self.pool.payoff_signature_length)])
        for market_id in self.data.keys():
            for selection_id in self.data[market_id].keys():
                for side in self.data[market_id][selection_id].keys():
                    for price, quantity in sorted(self.data[market_id][selection_id][side].items()):
                        selection = self.pool.state.selections.get(selection_id)
                        if side == OrderSide.BUY:
                            selection_side_exposure = selection.payoff_signature.generate_negative_only_net_payoff_vector(
                                price = price 
                            ) * quantity
                        else:
                            selection_side_exposure = selection.payoff_signature.invert().generate_negative_only_net_payoff_vector(
                                price = Decimal(1)-price
                            ) * quantity
                        
                        unmatched_exposure_vector = np.add(
                            unmatched_exposure_vector,
                            selection_side_exposure
                        )

        return unmatched_exposure_vector


    def print(
        self
    ):
        print('='*40)
        print('POOL PROFILE')
        print(f'Pool: {self.pool.id}')
        print('-'*40)
        for market_id in self.data.keys():
            print(f'MARKET: {market_id}')
            for selection_id in self.data[market_id].keys():
                print(f' - SELECTION: {selection_id}')
                for side in [OrderSide.SELL, OrderSide.BUY]: #self.data[market_id][selection_id].keys():
                    print(f'   - {side.value.upper()}')
                    ticks = sorted(self.data[market_id][selection_id][side].items())
                    if side == OrderSide.BUY:
                        ticks = ticks[::-1]
                    for price, quantity in ticks:
                        print(f'      {price:.3f}: {quantity:8.2f}')
            print('-'*40)
        print('='*40)





