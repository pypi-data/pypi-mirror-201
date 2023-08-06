
import numpy as np
from typing import List, Union
from decimal import Decimal


class InvalidPayoffSignature(Exception):

    def __init__(self, payoff_signature):
        self.message = f'InvalidPayoffSignature: Invalid payoff signature: {payoff_signature}'
        super().__init__(self.message)


def check_only_valid_values(
    payoff_string: str,
):
    letters = set(payoff_string)
    letters_allowed = ["L" ,"R", "W", "H", "K"]
   
    for letter in letters:
        if letter not in letters_allowed:
            raise InvalidPayoffSignature(payoff_string)
    
    return True

# def check_for_price_dependent_payoffs(
#     payoff_string: str,
# ):
#     letters = set(payoff_string)
#     if "R" in  letters or "H" in letters or "K" in letters:
#         return True
#     return False

class PayoffSignature():

    def __init__(
        self,
        payoff_string: str,
        dimensions: int = 2,
    ):
        '''

        '''
        if dimensions not in [1, 2]:
            raise InvalidPayoffSignature(payoff_string)

        letters = set(payoff_string)
        letters_allowed = ["L" ,"R", "W", "H", "K"]

        for letter in letters:
            if letter not in letters_allowed:
                raise InvalidPayoffSignature(payoff_string)

        self._dimensions = dimensions
        self._string = payoff_string.upper()
        self._length = len(self._string)

        self._has_refund = True if "R" in letters else False
        self._has_half_win = True if "H" in letters else False
        self._has_half_loss = True if "K" in letters else False
        self._has_price_dependent_payoff = self._has_refund or self._has_half_loss or self._has_half_win

        # Where there is a price dependency (i.e. it's possible for get a refund or half-refund)
        #  we may need to do additional checks when optimizing for match payoffs


    def to_string(
        self
    ):
        return self._string

    @classmethod
    def from_string(
        cls,
        payoff_string: str,
        dimensions: int = 2
    ):
        return cls(
           payoff_string = payoff_string,
           dimensions = dimensions 
        )


    @classmethod
    def empty_exposure_vector(
        cls,
        length: int,
        dimensions: int = 2,
    ):
        return np.asarray([Decimal(0) for i in range(length)])


    def to_grid_representation(
        self
    ) -> str:
        '''
        Returns a grid representation where:
          Dark cells =  Win of Half Win
          Shaded cells =  Refund
          Empty cells =  Loss of Half-Loss
        '''
        size = int(np.sqrt(self._length))
        divider = '-'*((size+1)*4+1) + '\n'
        string = divider
        string += '|   '
        for a in range(size):
            string += f"|{a:2d} "
        string += '|\n'
        for h in range(size):
            string += f"|{h:2d} "
            for a in range(size):
                value = self._string[h*(size) + a]
                string += "|▉▉▉" if value in ['W', 'H'] else "|   " if value in ["R"] else "|░░░"
            string += '|\n'
        string += divider
        return string
        
        
    def invert(
        self
    ) -> super:
        '''
        Returns a new instance of PayoffSignture where the payoff is the
        inverse of self.
        '''
        inverted_string = self._string.replace('W', 'l').replace('L', 'w').replace('H', 'k').replace('K','h').upper()
        return PayoffSignature(
            payoff_string = inverted_string,
            dimensions = self._dimensions
        )

    def generate_payoff_vector(
        self,
        price: Decimal # This is the 'post price' - i.e. for a Buyer, the actual price, for a Seller (1-actual price)
    ): 
        price = Decimal(price)
        values = []
        for l in self._string:
            if l == "W":
                value = Decimal(1) 
            elif l == "L":
                value = Decimal(0)
            elif l == "R":
                value = Decimal(price)
            elif l == "H":
                value = Decimal(0.5)*(Decimal(1)+price)
            elif l == "K":
                value = Decimal(0.5)*Decimal(price)
            else:
                raise InvalidPayoffSignature(self._string)
            values += [value]    
        vector = np.asarray(values)
        if len(vector) != self._length:
            raise InvalidPayoffSignature(self._string)

        return vector


    def generate_negative_only_net_payoff_vector(
        self,
        price: Decimal # This is the 'post price' - i.e. for a Buyer, the actual price, for a Seller (1-actual price)
    ): 
        # Net meaning for a win, we have 1-price, for a loss -price, etc.
        price = Decimal(price)
        vector = self.generate_net_payoff_vector(price).copy()
        vector[vector >= 0] = Decimal(0)  # i.e. only return values which are <0 else make them 0.
        return vector


    def generate_net_payoff_vector(
        self,
        price: Decimal # This is the 'post price' - i.e. for a Buyer, the actual price, for a Seller (1-actual price)
    ): 
        # Net meaning for a win, we have 1-price, for a loss -price, etc.
        price = Decimal(price)
        vector = self.generate_payoff_vector(price)
        vector = np.subtract(vector, price) 

        return vector


    def generate_payout_per_unit_risk_vector(
        self,
        price: Decimal # This is the 'post price' - i.e. for a Buyer, the actual price, for a Seller (1-actual price)
    ): 
        price = Decimal(price)
        values = []
        for l in self._string:
            if l == "W":
                value = Decimal(1)/price
            elif l == "L":
                value = Decimal(0)
            elif l == "R":
                value = Decimal(1)
            elif l == "H":
                value = Decimal(0.5)/price
            elif l == "K":
                value = Decimal(0.5)
            else:
                raise InvalidPayoffSignature(self._string)
            values += [value]    
        vector = np.asarray(values)
        if len(vector) != self._length:
            raise InvalidPayoffSignature(self._string)
        return vector

    def generate_net_return_per_unit_risk_vector(
        self,
        price: Decimal # This is the 'post price' - i.e. for a Buyer, the actual price, for a Seller (1-actual price)
    ): 
        # i.e. subtract the $1 risk from each to give the net return
        
        price = Decimal(price)
        vector = self.generate_payout_per_unit_risk_vector(price)
        vector = np.subtract(vector, Decimal(1)) 

        return vector


    def get_minimum_values_from_payoff_vector(
        self,
        payoff_vector: np.ndarray,
        payoff_letter: str
    ):
        '''
        Gets the minimum value for any cells of a particular payoff type
        (as indicated by the payoff letter - i.e. "R", "H", etc)
        for a payoff vector provided.
        Returns None if no value of this type is present.
        '''
        payoff_letter = payoff_letter.upper()
        if len(payoff_vector) != self._length:
            raise InvalidPayoffSignature(self._string)
        result = None
        for idx, letter in enumerate(self._string):
            if letter == payoff_letter:
                if result == None or payoff_vector[idx] < result:
                    result = payoff_vector[idx]
        return result.copy()

