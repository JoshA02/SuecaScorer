# Contans function definitions for functions dealing with suits and ranks

def valid_suit(s: str) -> bool:
    # s2 = s.upper();
    return s in ['H', 'C', 'S', 'D']

def valid_rank(r: str) -> bool:
    # r2 = r.upper();
    return r in ['A', '2', '3', '4', '5', '6', '7', 'Q', 'J', 'K']

def suit_full_name(s: str) -> str:
    suit_dictionary = {'H': 'Hearts', 'C': 'Clubs', 'S': 'Spades', 'D': 'Diamonds'}
    s2 = s.upper();
    try:
        return suit_dictionary[s2]
    except KeyError:
        return ValueError('Invalid suit symbol ' + s2)
    except:
        return ValueError('Unexpected error')

def rank_points(r: str) -> int:
    if(not valid_rank(r)): raise ValueError('Invalid rank symbol ' + r)

    rank_dictionary = {'A': 11, '7': 10, 'K': 4, 'J': 3, 'Q': 2}
    r2 = r.upper();
    try:
        return rank_dictionary[r2]
    except KeyError:
        return 0 # All other ranks have 0 points
    except:
        return ValueError('Unexpected error')

def rank_higher_than(r1: str, r2: str) -> bool:
    r1 = r1.upper()
    r2 = r2.upper()
    if(r1 == r2): return False # If the ranks are the same, the first card is not higher than the second card
    if(not valid_rank(r1)): raise ValueError('Invalid rank symbol ' + r1)
    if(not valid_rank(r2)): raise ValueError('Invalid rank symbol ' + r2)

    rank_points1 = rank_points(r1)
    rank_points2 = rank_points(r2)

    if(rank_points1 == rank_points2): # Both cards have the same points value; The one with the higher face value is declared higher
        rank_order = ['2', '3', '4', '5', '6']
        return rank_order.index(r1) > rank_order.index(r2)
    else:
        return rank_points1 > rank_points2

