from decimal import Decimal
from typing import List
import json
import time

class Position():
    
    def __init__(
        self,
        probability_price: Decimal,
        decimal_price: Decimal,
        american_price: Decimal,
        payout: Decimal,
        stake: Decimal,
    ):
        self.probability_price = probability_price
        self.decimal_price = decimal_price
        self.american_price = american_price
        self.payout = payout
        self.stake = stake


class SelectionPosition():

    def __init__(
        self,
        state,
        market_id: int,
        selection_id: int,
        net_payout: Decimal,
        net_stake: Decimal,
        buys: List[Position],
        sells: List[Position],
    ):
        self.state = state
        self.market_id = market_id
        self.selection_id = selection_id
        self.net_payout = net_payout
        self.net_stake = net_stake
        self.buys = buys
        self.sells = sells
        self._update_timestamp = time.time()

    @property
    def probability_price(
        self,
    ):
        return self.net_stake / self.net_payout if self.net_payout != Decimal(0) else None

    @classmethod
    def load_from_json(
        cls,
        state,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        return cls(
            state = state,
            market_id = data.get('market'),
            selection_id = data.get('id'),
            net_stake = Decimal(data.get('net_stake')),
            net_payout = Decimal(data.get('net_payout')),
            buys = [
                Position(
                    probability_price = Decimal(p.get('probability_price')),
                    decimal_price = Decimal(p.get('decimal_price')),
                    american_price = Decimal(p.get('american_price')),
                    payout = Decimal(p.get('payout')),
                    stake = Decimal(p.get('stake'))
                )
                for p in data.get('buys')
            ],
            sells = [
                Position(
                    probability_price = Decimal(p.get('probability_price')),
                    decimal_price = Decimal(p.get('decimal_price')),
                    american_price = Decimal(p.get('american_price')),
                    payout = Decimal(p.get('payout')),
                    stake = Decimal(p.get('stake'))
                )
                for p in data.get('sells')
            ]
        )


    @property
    def selection(self):
        return self.state.selections.get(
            self.selection_id
        )
    
    @property
    def market(self):
        if self.selection:
            return self.selection.market
        return None

    @property
    def pool(self):
        if self.market:
            return self.market.pool
        return None

    
    def __repr__(self):
        return f"<Position: {self.market_id} {self.selection_id} | S: {self.net_stake:.2f} / P: {self.net_payout:.3f} >"

    def __str__(self):
        return f"<Position: {self.market_id} {self.selection_id} | S: {self.net_stake:.2f} / P: {self.net_payout:.3f} >"

