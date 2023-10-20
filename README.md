# SuecaScorer
Submitted for a first-year university assignment, SuecaScorer is a command-line application that scores and evaluates matches of the Portuguese card game 'Sueca'. Built using Python, with a focus on object-oriented programming and algorithmic design, implementing scoring algorithms based on traditional rules.

## Usage
**Prerequisites**: Python 3

Run as follows:
`python3 sueca_scorer.py [flags] [match file name]`

**Flags**:
- `-g`: Shows the tricks of the given game in the order in which the cards were played.
- `-c`: Shows, in addition to the final result, the cards held by the players in the given game.


## Sueca Match File Format
**Note**: All game files must be contained within the `game_data` subdirectory.

**Layout**:
R = Round, C = Card
```
[Trump Card]
[R1,C1][R1,C2][R1,C3][R1,C4]
[R2,C1][R2,C2][R2,C3][R2,C4]
[R3,C1][R3,C2][R3,C3][R3,C4]
[R4,C1][R4,C2][R4,C3][R4,C4]
...
```

**Example**:
```
7D
AH 2D 5H 2H
AC 3D 4C KC
AS 2S 4S 3S
AD 4H QD 6D
4D 7S 3H JD
7D 5D 7C 3C
KS KD QS 5S
7H QC QH 2C
JH JC KH 6C
5C 6S 6H JS
```
Additional examples can be found in the `game_data` subdirectory.
