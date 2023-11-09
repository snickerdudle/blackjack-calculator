"""Code holding the dealer class."""
from configs import DealerHitSoft17, DealerPeek
from cards import Hand
from shoe import Shoe


class Player:
    def __init__(self, money: int = 1_000):
        self.hand = Hand()
        self.money = money

    def play(self, shoe: Shoe, dealer_hand: Hand):
        """Play the player's hand"""
        # print(f"Playing player {self.hand}")

    def win(self, bet: int = 1):
        """The player wins the hand"""
        # print("Player wins")
        self.money += bet
        return bet

    def winBlackjack(self, bet: int = 1, blackjack_payout: float = 1.5):
        """The player wins with a blackjack"""
        # print("Player wins with blackjack")
        wins = bet * blackjack_payout
        self.money += wins
        return wins

    def lose(self, bet: int = 1):
        """The player loses the hand"""
        # print("Player loses")
        self.money -= bet
        return -bet

    def push(self, bet: int = 1):
        """The player pushes the hand"""
        # print("Player pushes")
        return 0


class Dealer(Player):
    def __init__(self, hit_soft_17: bool, peek: bool):
        super().__init__()
        self.hit_soft_17 = hit_soft_17
        self.peek = peek

    @classmethod
    def fromEnum(cls, hit_soft_17: DealerHitSoft17, peek: DealerPeek):
        """Creates a dealer from a DealerHitSoft17 enum and a DealerPeek enum"""
        return cls(bool(hit_soft_17.value), bool(peek.value))

    def play(self, shoe: Shoe):
        """Play the dealer's hand"""
        while True:
            value, soft = self.hand.value()
            if value <= 16 or (value == 17 and soft and self.hit_soft_17):
                self.hand.extend(shoe.deal())
            else:
                break
            # print(f"Dealer hand: {self.hand}")
