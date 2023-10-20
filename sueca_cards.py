from typing import List
from sueca_suits_ranks import *

class CardInvalid(Exception):
    pass

class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit.upper()
        self.rank = rank.upper()
        # print('Card created: ' + self.rank + self.suit)

    def points(self):
        # points: int = rank_points(self.rank)
        # if(points <= 0): return (self.show())
        return rank_points(self.rank)

    def higher_than(self: 'Card', other: 'Card', s: str, t: str) -> bool:

        # First, check if both cards are of the same suit. If they are, then compare simply by rank
        if(self.suit == other.suit):
            return rank_higher_than(self.rank, other.rank)

        ## From here, the cards are of different suits ##

        # Check if either of the cards are trump cards. If they are, then the trump card is higher
        if(self.suit == t): return True
        if(other.suit == t): return False

        ## From here, neither card is a trump card ##

        # Check if either of the cards are lead cards. If they are, then the lead card is higher
        if(self.suit == s): return True
        if(other.suit == s): return False

        ## From here, neither card is a lead card or a trump card ##

        # Returns True if this card's rank is higher than the other card's rank, False otherwise (as none of the cards are of the lead suit or the trump suit)
        return (rank_higher_than(self.rank, other.rank))

    def show(self) -> str:
        return (self.rank + self.suit)


# Examples: 'AH' or '2C' or '7D' or 'QS'
def parseCard(cs: str) -> Card:
    # cs = cs.upper()
    defaultError: str = "Card '" + cs + "' is invalid!"

    if(len(cs) != 2):
        raise CardInvalid(defaultError + "\nA card string representation must contain 2 characters only")
    
    suit: str = cs[-1]
    rank: str = cs[:-1]
    if(not valid_rank(rank)): raise CardInvalid(defaultError + "\nInvalid rank symbol: " + rank)
    if(not valid_suit(suit)): raise CardInvalid(defaultError + "\nInvalid suit symbol: " + suit)

    return Card(suit, rank)