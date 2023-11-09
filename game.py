"""Code holding the game class."""
from configs import BasicGameConfig
from shoe import Shoe
from cards import Card, Hand
from participants import Dealer, Player
from typing import Union

OUTPUT: bool = False


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
        self.players = []

        for _ in range(num_players):
            player = Player()
            self.players.append(player)

    def simulateRound(self, bet: int = 1):
        """Play a single round of blackjack"""
        # Deal the cards if there are no cards in hands
        if not self.dealer.hand:
            for participant in self.players + [self.dealer]:
                participant.hand.extend(self.shoe.deal(2))
        else:
            # Reset the shoe if we are at the shuffle point
            if self.shoe.fractionUsed <= self.config.shuffle_point.value:
                self.shoe.reset()

        # Print the hands
        printMaybe(f"Dealer hand: {self.dealer.hand}")
        for player in self.players:
            printMaybe(f"Player hand: {player.hand}")

        # Check for dealer blackjack
        if self.dealer.peek and self.dealer.hand.isBlackjack():
            for player in self.players:
                if player.hand.isBlackjack():
                    printMaybe("Player and dealer blackjack!")
                    return player.push(bet)
                else:
                    printMaybe("Dealer blackjack!")
                    return player.lose(bet)
            return

        # Check for player blackjack
        for player in self.players:
            if player.hand.isBlackjack():
                return player.winBlackjack(bet)

        # Play the players' hands
        for player in self.players:
            player.play(self.shoe, self.dealer.hand)

        # Play the dealer's hand
        self.dealer.play(self.shoe)

        # Determine the winners
        for player in self.players:
            result = self.handAgainstDealer(player.hand, self.dealer.hand, bet=bet)
            if result > 0:
                return player.win(bet)
            elif result < 0:
                return player.lose(bet)
            else:
                return player.push(bet)
        return result

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
        dealer_hand: Hand,
        player_hands: Union[list[Hand], Hand],
    ) -> None:
        """Sets the hands of the dealer and player"""
        self.shoe.reset()
        self.shoe.removeHand(dealer_hand)

        self.dealer.hand = Hand.copyHand(dealer_hand)

        if isinstance(player_hands, Hand):
            player_hands = [player_hands]
        for idx, player_hand in enumerate(player_hands):
            self.players[idx].hand = Hand.copyHand(player_hand)
            self.shoe.removeHand(player_hand)

    def simulateNRounds(self, n: int = 10_000, bet: int = 1) -> float:
        """Plays n rounds of blackjack with the current configuration.

        Returns the expected winnings per hand.
        """
        dealer_hand = self.dealer.hand
        player_hands = [player.hand for player in self.players]
        total = 0

        for _ in range(n):
            self.setHands(dealer_hand, player_hands)
            result = self.simulateRound(bet=bet)
            total += result

        return float(total) / n / bet


if __name__ == "__main__":
    game = Game(BasicGameConfig())
    game.simulateRound()

    game.setHands(Hand([Card("A"), Card("A")]), Hand([Card("A"), Card("A")]))
    result = game.simulateNRounds(10_000)
    print(result)
