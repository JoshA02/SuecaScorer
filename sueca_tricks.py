from typing import List, Tuple
from sueca_cards import Card, parseCard
from sueca_suits_ranks import valid_suit


class Trick:
    # init function which takes in a list of cards
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards

    def points(self) -> int:
        totalPoints: int = 0
        for x in range(len(self.cards)):
            totalPoints += self.cards[x].points()
        return totalPoints

    def trick_winner(self, t: str) -> int:
        try:
            trumpSuit = t.upper()
        except AttributeError:
            raise ValueError('Invalid trump suit type. Must provide a string!')

        if(not valid_suit(trumpSuit)): raise ValueError('Invalid trump suit ' + trumpSuit)

        leadSuit: str = self.cards[0].suit.upper() # The lead suit is the suit of the first card played

        validCards = list(filter( (lambda c: (c.suit == leadSuit) or (c.suit == trumpSuit)), self.cards )) # Filter out all cards that are not of the lead suit or the trump suit

        winningCard = validCards[0]
        for x in range(len(validCards)):
            if(validCards[x].higher_than(winningCard, leadSuit, trumpSuit)):
                winningCard = validCards[x]

        return self.cards.index(winningCard) + 1 # Return the player number of the player who owns the winning card

    def show(self) -> str:
        return (''.join([(c.show() + ' ') for c in self.cards]))[:-1] # Remove the last space


def parseTrick(cs: str) -> Trick:
    # Examples: 'AH 2D 5H 2H' or '2C 7D 3H 7H' or 'QS 3C 4C 5C'
    cards: List[Card] = [parseCard(c) for c in cs.split(' ')]
    if(len(cards) != 4):
        raise ValueError('A trick string must comprise four cards only; the given trick is: ' + cs)
    return Trick(cards)

def parseGameFile(fname: str) -> Tuple[Card, List[Trick]]:
    # Returns a tuple with the trump suit and a list of tricks
    with open(fname, 'r') as f:
        lines = f.readlines()
        trump = lines[0].strip() # Returns the first line of the file with any leading and trailing whitespace removed
        tricks = [parseTrick(l.strip()) for l in lines[1:]] # Returns all lines after the first line of the file with any leading and trailing whitespace removed
        return (parseCard(trump), tricks)