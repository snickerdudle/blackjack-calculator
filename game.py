"""Code holding the game class."""
from configs import BasicGameConfig
from shoe import Shoe
from participants import Dealer, Player


class Game:
    def __init__(self, config: BasicGameConfig, num_players: int = 1):
        self.config = config

        # Get the shoe, dealer, and players from the config
        self.shoe = Shoe.fromEnum(self.config.num_decks)

        self.dealer = Dealer.fromEnum(
            self.config.dealer_hit_soft_17, self.config.dealer_peek
        )

        for _ in range(num_players):
            player = Player()
            self.players.append(player)

    def round(self):
        """Play a single round of blackjack"""
        # Reset the shoe if we are at the shuffle point
        if self.shoe.fractionUsed <= self.config.shuffle_point.value:
            self.shoe.reset()

        # Deal the cards
        for participant in self.players + [self.dealer]:
            participant.hand.extend(self.shoe.deal(2))

        # Check for dealer blackjack
        if self.dealer.peek and self.dealer.hand.isBlackjack():
            for player in self.players:
                if player.hand.isBlackjack():
                    player.push()
                else:
                    player.lose()
            return

        # Check for player blackjack
        for player in self.players:
            if player.hand.isBlackjack():
                player.blackjack()
                return

        # Play the players' hands
        for player in self.players:
            player.play(self.shoe, self.dealer.hand)

        # Play the dealer's hand
        self.dealer.play(self.shoe)

        # Determine the winners
        for player in self.players:
            if player.hand.is_bust():
                player.lose()
            elif self.dealer.hand.isBust():
                player.win()
            elif player.hand.value() > self.dealer.hand.value():
                player.win()
            elif player.hand.value() < self.dealer.hand.value():
                player.lose()
            else:
                player.push()


if __name__ == "__main__":
    game = Game(BasicGameConfig())
    game.round()
