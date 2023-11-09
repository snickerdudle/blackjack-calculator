"""Code holding the dealer class."""
from configs import DealerHitSoft17, DealerPeek
from cards import Hand, Shoe


class Player:
    def __init__(self, money: int = 1_000):
        self.hand = Hand()
        self.money = money


class Dealer(Player):
    def __init__(self, hit_soft_17: bool, peek: bool):
        super().__init__()
        self.hit_soft_17 = hit_soft_17
        self.peek = peek

    @classmethod
    def fromEnum(cls, hit_soft_17: DealerHitSoft17, peek: DealerPeek):
        """Creates a dealer from a DealerHitSoft17 enum and a DealerPeek enum"""
        return cls(bool(hit_soft_17.value), bool(peek.value))
