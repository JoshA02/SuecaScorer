from sueca_suits_ranks import suit_full_name
from os.path import exists
from sys import argv
import sueca_tricks
from sueca_games import Game

class GameFileCouldNotBeFound(Exception):
    pass

class SuecaGameIncomplete(Exception):
    pass


### Intro Logic
def __main__():
    if len(argv) <= 1:
        userFriendlyRunGame()
        return
    
    # Convert all arguments to lowercase
    for i, v in enumerate(argv):
        argv[i] = v.lower()

    showCards = False if '-c' not in argv else True
    showGame = False if '-g' not in argv else True
    fname = 'game_data/' + formatFileName(argv[len(argv) - 1])

    runGame(fname, showCards, showGame)

def formatFileName(fname: str):
    if(not fname.endswith('.sueca')): fname += '.sueca'
    return fname

def userFriendlyRunGame():
    print('Welcome to Sueca Scorer!')
    fname = input("Enter the name of the file with the game data (must be within the 'game_data' folder): ")
    fpath = 'game_data/' + formatFileName(fname)

    # Check if file exists; if not, display user-friendly error message and exit:
    if(not exists(fpath)):
        print("Could not find the game file '" + fname + "'\nMake sure the file is within the 'game_data' folder.\nExiting...")
        return
    
    runGame(fpath, showCards=True, showGame=True)


### Game Logic
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

if __name__ == "__main__":
    __main__()