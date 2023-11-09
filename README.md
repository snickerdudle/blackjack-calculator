# blackjack-calculator
A tool for running Monte Carlo simulations on BlackJack games, and generating the appropriate books

## Dimensions
To run a simulation, you need to specify the following dimensions:
* Fundamentals
  * Number of decks (`num_decks`) - this is the number of decks in the shoe
  * Deck shuffle point (`shuffle_point`) - this is the number of cards left in the shoe before it is reshuffled
  * Blackjack payout (`blackjack_payout`) - this is the payout for a blackjack (typically 3:2 or 6:5)
* Gameplay
  * Dealer hits soft 17 (`dealer_hits_soft_17`) - this is whether the dealer hits a soft 17 (typically yes)
* Doubling
  * Double after split (`double_after_split`) - this is whether you can double after splitting (typically yes)
  * Double range (`double_range`) - this is the range of hands you can double on (typically 9-11)
  * Double payout (`double_payout`) - this is the payout for a double (typically 1:1)
* Splitting
    * Split aces (`split_aces`) - this is whether you can split aces (typically yes)
    * Split tens (`split_tens`) - this is whether you can split tens (typically no)
    * Split range (`split_range`) - this is the range of hands you can split on (typically 2-10)
    * Split payout (`split_payout`) - this is the payout for a split (typically 1:1)
* Surrender
  * Surrender (`surrender`) - this is whether you can surrender (typically yes)
  * Surrender range (`surrender_range`) - this is the range of hands you can surrender on (typically 15-17)
  * Surrender payout (`surrender_payout`) - this is the payout for a surrender (typically 1:2)
* Dealer Peek
    * Dealer peek (`dealer_peek`) - this is whether the dealer peeks for blackjack (typically yes)