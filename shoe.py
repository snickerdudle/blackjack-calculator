"""The shoe module contains the Shoe class, which represents a shoe of cards"""
from enum import Enum
from cards import Card, Deck, Hand
import random
from configs import NumDecks
from collections import UserList


class Shoe(UserList):
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self.data = []
        self.reset()

    def reset(self):
        """Reset the Shoe to the original state, and shuffle the cards"""
        self.data = []
        for _ in range(self.num_decks):
            self.data.extend(Deck())
        self.shuffle()
        # print(f"Shoe reset with {len(self.data)} cards (num_decks={self.num_decks})")

    def shuffle(self):
        """Shuffle the cards in the shoe"""
        random.shuffle(self.data)
        pass

    @classmethod
    def fromEnum(cls, decks_enum: NumDecks):
        """Creates a shoe from a ShoeType enum"""
        return cls(decks_enum.value)

    @property
    def fractionUsed(self):
        return 1 - len(self.data) / (self.num_decks * 52)

    def deal(self, num_cards: int = 1):
        """Deal a number of cards from the shoe"""
        cards = []
        for _ in range(num_cards):
            cards.append(self.pop())
        return cards

    def removeHand(self, hand: Hand):
        """Remove a hand from the shoe"""
        for card in hand:
            self.removeCard(card)

    def removeCard(self, card: Card):
        """Remove a card from the shoe"""
        for i in range(len(self.data)):
            if self.data[i] == card:
                del self.data[i]
                break
        else:
            raise ValueError(f"Card {card} not in shoe")
        self.data.remove(card)


if __name__ == "__main__":
    shoe = Shoe.fromEnum(NumDecks.SIX_DECKS)
    print(shoe.data)
