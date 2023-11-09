"""The deck module contains the Deck class, which represents a deck of cards"""
import random
from collections import UserList
from typing import Optional


suits = ["♥️", "♣️", "♦️", "♠️"]
card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Card:
    def __init__(self, value: Optional[str] = None, suit: Optional[str] = None):
        # Value, like King or 9
        self.value = value or random.choice(card_values)
        # Suit, like Hearts or Clubs
        self.suit = suit or random.choice(suits)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.value}{self.suit}".rjust(4)

    @property
    def num(self) -> int:
        """Returns the numerical value of the card in Blackjack.

        Returns 11 for an Ace, 10 for a face card, and the number for a number card."""
        if self.value in card_values[-3:]:
            return 10
        elif self.value == "A":
            return 11
        elif self.value.isdigit():
            return int(self.value)
        else:
            raise ValueError(f"Invalid card value: {self.value}")

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit


class Deck(UserList):
    def __init__(self):
        self.data = []
        self.reset()

    def reset(self):
        """Reset the Deck to the original state, unsuffled."""
        self.data = []
        for suit in suits:
            for value in card_values:
                self.append(Card(value, suit))
        return self

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.data)


class Hand(UserList):
    def __init__(self, cards: Optional[list[Card]] = None):
        self.data = cards or []

    def value(self) -> tuple[int, bool]:
        """Returns the value of the hand, and whether or not it is soft.

        Returns:
            value: int, the value of the hand
            soft: bool, whether or not the hand is soft
        """
        non_aces = [card for card in self if card.value != "A"]
        aces = [card for card in self if card.value == "A"]
        value = sum([card.num for card in non_aces])
        soft = False

        # Now look for the aces. We want to add them in the best way possible.
        # If we can add 11 to the value without going over 21, we do that and
        # set soft to True. Otherwise, we add 1.
        for card in aces:
            if value + 11 <= 21:
                value += 11
                soft = True
            else:
                value += 1

        # If we have a soft hand, and we're over 21, we need to make it hard.
        if soft and value > 21:
            value -= 10
            soft = False

        return value, soft

    def __str__(self):
        if not self:
            s = "empty"
        else:
            s = ", ".join([str(card) for card in self])

        value, soft = self.value()

        return f"<{s}>({'S' if soft else ''}{value})"

    def isBlackjack(self) -> bool:
        """Returns whether or not the hand is a blackjack"""
        return self.value()[0] == 21 and len(self) == 2

    def isBust(self) -> bool:
        """Returns whether or not the hand is a bust"""
        return self.value()[0] > 21

    @classmethod
    def copyHand(cls, new_hand):
        """Copies the cards in the hand to a new hand"""
        return cls([card for card in new_hand])


if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    print(d)

    for _ in range(5):
        h = Hand([d.pop(), d.pop(), d.pop()])
        print(h, end=" => ")
        print(h.value())
