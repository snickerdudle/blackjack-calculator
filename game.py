"""Code holding the game class."""
from configs import BasicGameConfig
from shoe import Shoe
from cards import Card, Hand, card_values, suits
from participants import Dealer, Player, ActionType
from typing import Optional
from collections import defaultdict
import pickle

OUTPUT: bool = False
COUNT_BLACKJACK_TOWARDS_ODDS: bool = False
NUM_RUNS = 10_000


# Key: hand_value, first_card_value, action
hard_results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
soft_results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
pair_results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def printMaybe(msg: str):
    if OUTPUT:
        print(msg)


class Game:
    def __init__(self, config: BasicGameConfig, num_players: int = 1):
        self.config = config

        # Get the shoe, dealer, and players from the config
        self.shoe = Shoe.fromEnum(self.config.num_decks)

        self.dealer = Dealer.fromEnum(
            self.config.dealer_hit_soft_17, self.config.dealer_peek
        )
        self.player = Player()

    def simulateRound(self, action: Optional[ActionType] = None, bet: int = 1):
        """Play a single round of blackjack"""
        # Deal the cards if there are no cards in hands
        if not self.dealer.hand:
            self.player.hand.extend(self.shoe.deal(2))
            self.dealer.hand.extend(self.shoe.deal(2))
        else:
            # Reset the shoe if we are at the shuffle point
            if self.shoe.fractionUsed <= self.config.shuffle_point.value:
                self.shoe.reset()

        # Print the hands
        printMaybe(f"Dealer hand: {self.dealer.hand}")
        printMaybe(f"Player hand: {self.player.hand}")

        # Check for dealer blackjack
        if self.dealer.peek and self.dealer.hand.isBlackjack():
            if self.player.hand.isBlackjack():
                printMaybe("Player and dealer blackjack!")
                if COUNT_BLACKJACK_TOWARDS_ODDS:
                    return self.player.push(bet)
                else:
                    return 0
            else:
                printMaybe("Dealer blackjack!")
                if COUNT_BLACKJACK_TOWARDS_ODDS:
                    return self.player.lose(bet)
                else:
                    return 0
            return

        # Check for player blackjack
        if self.player.hand.isBlackjack():
            if COUNT_BLACKJACK_TOWARDS_ODDS:
                return self.player.winBlackjack(bet)
            else:
                return 0

        action = action or ActionType.HIT

        # Play the players' hands
        self.player.play(action=action, shoe=self.shoe, dealer_hand=self.dealer.hand)

        # Play the dealer's hand
        self.dealer.play(shoe=self.shoe)

        # Determine the winners
        result = self.handAgainstDealer(self.player.hand, self.dealer.hand)
        if result > 0:
            return self.player.win(bet)
        elif result < 0:
            return self.player.lose(bet)
        else:
            return self.player.push(bet)

    def handAgainstDealer(self, hand: Hand, dealer_hand: Hand, bet: int = 1) -> int:
        """Returns the winnings for a hand against the dealer"""
        if hand.isBust():
            printMaybe("Player busts")
            return -bet
        elif dealer_hand.isBust():
            printMaybe("Dealer busts")
            return bet
        elif hand.value() > dealer_hand.value():
            return bet
        elif hand.value() < dealer_hand.value():
            return -bet
        else:
            return 0

    def setHands(
        self,
        dealer_hand: Optional[Hand] = None,
        player_hand: Optional[Hand] = None,
    ) -> None:
        """Sets the hands of the dealer and player"""
        self.shoe.reset()
        if dealer_hand is None:
            cur_dealer_hand = Hand([Card(), Card()])
        else:
            if len(dealer_hand) != 2:
                cur_dealer_hand = Hand([dealer_hand[0], Card()])
            else:
                cur_dealer_hand = dealer_hand

        if player_hand is None:
            cur_player_hand = Hand([Card(), Card()])
        else:
            if len(player_hand) != 2:
                cur_player_hand = Hand([player_hand[0], Card()])
            else:
                cur_player_hand = player_hand

        self.shoe.removeHand(cur_dealer_hand)
        self.shoe.removeHand(cur_player_hand)

        self.dealer.hand = Hand.copyHand(cur_dealer_hand)
        self.player.hand = Hand.copyHand(cur_player_hand)

    def simulateNRounds(
        self,
        n: int = 10_000,
        dealer_hand: Optional[Hand] = None,
        player_hand: Optional[Hand] = None,
        action: ActionType = ActionType.HIT,
        bet: int = 1,
    ) -> float:
        """Plays n rounds of blackjack with the current configuration.

        Returns the expected winnings per hand.
        """
        total = 0

        for _ in range(n):
            self.setHands(dealer_hand, player_hand)
            result = self.simulateRound(action=action, bet=bet)
            total += result

        return float(total) / n / bet


if __name__ == "__main__":
    game = Game(BasicGameConfig())
    # game.simulateRound()

    for value1 in card_values:
        card1 = Card(value1)
        for value2 in card_values:
            card2 = Card(value2)
            print(f"Card1: {card1}, Card2: {card2}".rjust(20))
            hand = Hand([card1, card2])
            hand_value, soft = hand.value()

            for first_val in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]:
                dealer_hand = Hand([Card(first_val)])
                print(f"Val: {first_val}".rjust(10), end=" : ")

                for action in ActionType:
                    try:
                        result = game.simulateNRounds(
                            n=NUM_RUNS,
                            player_hand=hand,
                            dealer_hand=dealer_hand,
                            action=action,
                        )
                    except ValueError:
                        result = -1
                    if action == ActionType.DOUBLE:
                        result *= 2
                    print(result, end=" | ")
                    if card1.value == card2.value:
                        pair_results[hand_value][first_val][action].append(result)
                    elif soft:
                        soft_results[hand_value][first_val][action].append(result)
                    else:
                        hard_results[hand_value][first_val][action].append(result)
                print()

    print("Hard hands:")
    for table in [hard_results, soft_results, pair_results]:
        for hand_size, value in table.items():
            print(f"{hand_size}".rjust(5), end=": ")
            for first_card, value2 in value.items():
                m = -1000
                ma = None
                for a, value3 in value2.items():
                    res = sum(value3) / len(value3)
                    if res > m:
                        m = res
                        ma = a
                print(ma.name.rjust(6), end=" ")
            print()

    with open("result.pickle", "wb") as w:
        pickle.dump(
            [
                default_to_regular(hard_results),
                default_to_regular(soft_results),
                default_to_regular(pair_results),
            ],
            w,
        )
