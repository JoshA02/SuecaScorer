from typing import List, Tuple
from sueca_cards import Card, parseCard
from sueca_tricks import Trick, parseGameFile, parseTrick


class CardAlreadyPlayed(Exception):
    pass

class DealerDoesNotHoldTrumpCard(Exception):
    pass

class IllegalCardPlayed(Exception):
    pass


class Game:
    def __init__(self, trumpCard: Card):
        self.tricks: List[Trick] = []
        self.trumpCard: Card = trumpCard
    
    def gameTrump(self) -> Card:
        return self.trumpCard


    def score(self) -> Tuple[int, int]:
        t1Score = 0 # Team 1's score
        t2Score = 0 # Team 2's score
        
        for i, trick in enumerate(self.tricks):
            winningPlayerNum = self.playerNumberFromPosition(trick.trick_winner(self.trumpCard.suit), i)
            points = trick.points()
            if(winningPlayerNum == 1 or winningPlayerNum == 3): t1Score += points
            elif(winningPlayerNum == 2 or winningPlayerNum == 4): t2Score += points
            else:
                raise Exception('Invalid winning player number: ' + str(winningPlayerNum))

        return (t1Score, t2Score)

    def gameTricks(self) -> List[Trick]:
        return self.tricks

    def playTrick(self, t: Trick) -> None:

        # Catch if any cards from this trick have already been played
        previouslyPlayedCardsLists: List[Card] = [trick.cards for trick in self.tricks] # Adds each card from each trick (self.tricks) to the list
        previouslyPlayedCards: List[str] = [
            card.show().upper() for cardList in previouslyPlayedCardsLists for card in cardList
        ]

        for card in t.cards:
            if(card.show().upper() in previouslyPlayedCards): raise CardAlreadyPlayed('The card ' + card.show() + ' has already been played!')
        

        # Ensure that the dealer held the trump card
            # Because we can't check future tricks, we can only check the current trick
            # We do this by checking if a non-dealer player has dealt the trump card
        for i, card in enumerate(t.cards):
            if(card.show().upper() == self.trumpCard.show().upper()):
                # print('Someone has the trump card in this trick (trick ' + str(len(self.tricks)+1) + '). Who are they?')
                trumpCardPosition = i + 1
                trumpCardPlayerNumber = self.playerNumberFromPosition(trumpCardPosition, len(self.tricks))
                # print('Player ' + str(trumpCardPlayerNumber) + ' has the trump card in this trick')
                if(trumpCardPlayerNumber != 2):
                    raise DealerDoesNotHoldTrumpCard('The dealer does not hold the trump card in this trick, therefore this trick is invalid')
        


        # Check if card played is invalid, in respect to the lead suit
        # With each trick that's added, go through each of the previous tricks and see if a player played a card they shouldn't have.
            # E.g)
            #   1: New trick (trick 3) is about to be added here.
            #   2: Go through each of the previous tricks (trick 1 and trick 2) and see if a player played a non-lead card.
            #   3: If they did, then make sure that they didn't have a lead card in their hand. This can be done by checking what card they played this trick.

            #   In short, if a player plays Trick 2's lead card in Trick 4 but didn't in Trick 2... We now know they had Trick 2's lead card during Trick 2 but didn't play it. Therefore, this trick is invalid.
        for trickIndex, trick in enumerate(self.tricks):
            leadSuit = trick.cards[0].suit

            for cardIndex, card in enumerate(trick.cards):
                if(card.suit.upper() != leadSuit.upper()): 
                    # A player has played a card that isn't the lead suit in this trick. Check if they played the lead suit in a later trick.
                    accusedPlayerNum = self.playerNumberFromPosition(cardIndex+1, trickIndex)

                    # Check each trick after the one they were suspected in (including the current trick being added) to see if they played the lead suit
                    allTricks = self.tricks.copy()
                    allTricks.append(t) # Check this trick too
                    for futureTrickIndex, futureTrick in enumerate(allTricks):
                        if(futureTrickIndex <= trickIndex): continue # Don't check the trick they were suspected in or any previous tricks
                        
                        for futureCardIndex, futureCard in enumerate(futureTrick.cards): # Check each card in the future trick
                            if(futureCard.suit.upper() == leadSuit.upper()): # Is a player playing the lead suit in a later trick?
                                if(self.playerNumberFromPosition(futureCardIndex+1, futureTrickIndex) != accusedPlayerNum): continue # Not the player we're looking for
                                raise IllegalCardPlayed('Player ' + str(accusedPlayerNum) + ' did not play the lead suit (' + leadSuit + ') in trick ' + str(trickIndex+1) + ' but played a card of the same suit in trick ' + str(futureTrickIndex+1))
                            



        self.tricks.append(t)
        # print('Added a trick to the game!\nNow have ' + str(len(self.tricks)) + ' tricks')
        # print('Successfully added trick (' + t.show() + ') to the game')
    

    def getTrickDictionary(self, t) -> dict:
        # Returns a dictionary for the provided trick number (t)
        # The dictionary is of the form {playerPosition: playerNumber}
        # Where playerPosition and playerNumber are integers between 1 and 4
        
        if(t < 0 or t > len(self.tricks)):
            raise ValueError('Invalid trick number ' + str(t) + '\nMust be at least 0 and at most ' + str(len(self.tricks)) + ' (one more than the index of the last trick)\n' + str(t))

        if(t == 0): return {1: 1, 2: 2, 3: 3, 4: 4}

        lastTrick = self.tricks[t-1]
        if(lastTrick == None): raise Exception('Invalid trick number ' + str(t) + ' (last trick is None)')

        lastTrickWinnerPosition = lastTrick.trick_winner(self.trumpCard.suit)
        if(lastTrickWinnerPosition == None): raise Exception('Invalid trick number ' + str(t) + ' (last trick winner is None)')

        lastTrickWinnerNumber = -1

        playerPositionToPlayerNumber = { 1: 1, 2: 2, 3: 3, 4: 4 }
        for(i, trick) in enumerate(self.tricks):
            if(i == t - 1):
                lastTrickWinnerNumber = (playerPositionToPlayerNumber[lastTrickWinnerPosition])
                break

            # Find out who won this trick.
            # Determine the player number of the winner.
            winningPlayerNum = playerPositionToPlayerNumber[trick.trick_winner(self.trumpCard.suit)]

            # Setup for next trick

            playerPositionToPlayerNumber = {
                1: winningPlayerNum,
                2: 4 if (winningPlayerNum + 1) % 4 == 0 else (winningPlayerNum + 1) % 4,
                3: 4 if (winningPlayerNum + 2) % 4 == 0 else (winningPlayerNum + 2) % 4,
                4: 4 if (winningPlayerNum + 3) % 4 == 0 else (winningPlayerNum + 3) % 4
            }

        return ({
            1: lastTrickWinnerNumber,
            2: 4 if (lastTrickWinnerNumber + 1) % 4 == 0 else (lastTrickWinnerNumber + 1) % 4,
            3: 4 if (lastTrickWinnerNumber + 2) % 4 == 0 else (lastTrickWinnerNumber + 2) % 4,
            4: 4 if (lastTrickWinnerNumber + 3) % 4 == 0 else (lastTrickWinnerNumber + 3) % 4
        })



    # Returns the player number of the player in position (p) within trick (t)
    def playerNumberFromPosition(self, p: int, t: int) -> int:
        if(p < 1 or p > 4): raise ValueError('Invalid player number ' + str(p))

        # pos to player num
        playerPositionToNumberDict = self.getTrickDictionary(t)
        return(playerPositionToNumberDict[p])

    
    def playerPositionFromNumber(self, p: int, t: int) -> int:
        playerNum = self.playerNumberFromPosition(p, t)
        playerPosToNum = self.getTrickDictionary(t)

        for k, v in playerPosToNum.items():
            if(v == playerNum): return k

        return None # If it gets through the loop and doesn't return anything, then it's invalid



    # Returns a list of all cards held by player p
    def cardsOf(self, p: int) -> List[Card]:

        if(p < 1 or p > 4): raise ValueError('Invalid player number ' + str(p)) # p must be an integer between 1 and 4

        playerCards: List[Card] = []

        playerCards = []

        playerPosToNum = {
            1: 1,
            2: 2,
            3: 3,
            4: 4
        }

        for i, trick in enumerate(self.tricks):
            winningPlayerNum = playerPosToNum[trick.trick_winner(self.trumpCard.suit)]


            for k, v in playerPosToNum.items():
                if(v == p): playerCards.append(trick.cards[k-1])

            playerPosToNum = {
                1: winningPlayerNum,
                2: 4 if (winningPlayerNum + 1) % 4 == 0 else (winningPlayerNum + 1) % 4,
                3: 4 if (winningPlayerNum + 2) % 4 == 0 else (winningPlayerNum + 2) % 4,
                4: 4 if (winningPlayerNum + 3) % 4 == 0 else (winningPlayerNum + 3) % 4
            }
            
        return playerCards