from sueca_suits_ranks import suit_full_name
from os.path import exists
import sueca_tricks
from sueca_games import Game

class GameFileCouldNotBeFound(Exception):
    pass

class SuecaGameIncomplete(Exception):
    pass

def runGame(fname: str, showCards: bool = False, showGame: bool = False):
    if(not exists(fname)): raise GameFileCouldNotBeFound("Could not find the game file '" + fname + "'")
    
    trumpCard, tricks = sueca_tricks.parseGameFile(fname)

    if(len(tricks) < 10): raise SuecaGameIncomplete("The given sueca game is incomplete! Has " + len(tricks) + " tricks, but should have 10.")

    game = Game(trumpCard)
    for trick in tricks:
        game.playTrick(trick)

    # Indicate score and winning pair
    score = game.score()
    winningPair = 'A' if score[0] > score[1] else 'B' if score[0] < score[1] else None
    if(winningPair != None): print('Pair ' + winningPair + ' won the given sueca game.')
    else: print('The game resulted in a draw')
    print('Score: ' + str(score[0]) + ' - ' + str(score[1]))

    if(showCards):
        print ("Players' cards in the sueca game")
        for i in range(4):
            playerNum = i + 1
            output = "Player " + str(playerNum) + ": "
            playerCards = game.cardsOf(playerNum)
            for(card) in playerCards:
                output += card.show() + ', '
            print(output[:-2])

    if(showGame):
        print('Trump: ' + trumpCard.show() + " - " + suit_full_name(trumpCard.suit))
        for i, trick in enumerate(game.tricks):
            print(str(i+1) + ': ' + trick.show())




runGame('game_data/game1.sueca', showCards=True, showGame=True)