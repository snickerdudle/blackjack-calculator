"""The configuration of the game"""

from enum import Enum


class NumDecks(Enum):
    """The NumDecks enum represents the different number of decks in a shoe"""

    ONE_DECK = 1
    TWO_DECKS = 2
    FOUR_DECKS = 4
    SIX_DECKS = 6
    EIGHT_DECKS = 8


class ShufflePoint(Enum):
    """The ShufflePoint enum represents the different shuffle points in a shoe.

    The number is the threshold beyond the use of which the shoe is reshuffled,
    so 0.25 means that the shoe is reshuffled when 25% of the cards have been
    dealt (75% of the cards remain)."""

    EVERY_PLAY = 0
    QUARTER = 0.25
    HALF = 0.5
    THREE_QUARTERS = 0.75
    FULL = 1.0


class BlackjackPayout(Enum):
    """The BlackjackPayout enum represents the different payouts for a blackjack"""

    THREE_TO_TWO = 1.5
    SIX_TO_FIVE = 1.2
    EVEN_MONEY = 1.0


class DealerHitSoft17(Enum):
    """The DealerHitSoft17 enum represents the different rules for a soft 17"""

    HIT = 1
    STAND = 0


class DoubleAfterSplit(Enum):
    """The DoubleAfterSplit enum represents the different rules for doubling after a split"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class DoubleRange(Enum):
    """The DoubleRange enum represents the different rules for doubling after a split"""

    ANY = 1
    NINE_TO_ELEVEN = 0


class SplittingAces(Enum):
    """The SplittingAces enum represents the different rules for splitting aces"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class SplittingTens(Enum):
    """The SplittingTens enum represents the different rules for splitting tens"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class ResplittingAces(Enum):
    """The ResplittingAces enum represents the different rules for resplitting aces"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class ResplittingTens(Enum):
    """The ResplittingTens enum represents the different rules for resplitting tens"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class Surrender(Enum):
    """The Surrender enum represents the different rules for surrendering"""

    ALLOWED = 1
    NOT_ALLOWED = 0


class DealerPeek(Enum):
    """The DealerPeek enum represents the different rules for the dealer peeking"""

    PEEK = 1
    NO_PEEK = 0


class BasicGameConfig:
    def __init__(self):
        self.num_decks = NumDecks.SIX_DECKS
        self.shuffle_point = ShufflePoint.QUARTER
        self.blackjack_payout = BlackjackPayout.SIX_TO_FIVE
        self.dealer_hit_soft_17 = DealerHitSoft17.HIT
        self.double_after_split = DoubleAfterSplit.ALLOWED
        self.double_range = DoubleRange.ANY
        self.splitting_aces = SplittingAces.ALLOWED
        self.splitting_tens = SplittingTens.ALLOWED
        self.resplitting_aces = ResplittingAces.ALLOWED
        self.resplitting_tens = ResplittingTens.ALLOWED
        self.surrender = Surrender.NOT_ALLOWED
        self.dealer_peek = DealerPeek.PEEK


class EllisIslandConfig(BasicGameConfig):
    def __init__(self):
        super().__init__()
        self.shuffle_point = ShufflePoint.EVERY_PLAY
        self.blackjack_payout = BlackjackPayout.THREE_TO_TWO
