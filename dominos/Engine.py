"""A game engine for running a game of Dominos."""
import sys, random
sys.path.insert(0, '..')  # For importing app config, required for using db
from dominos.classes.Board import Board
from dominos.classes.Pack import Pack

class Engine:
    def __init__(self):
        pass
    
    def play(self):
        board = Board()
        pack = Pack()

        hand = pack.pull(28)
        print([str(d) for d in hand])

        board.set_spinner_x(0)
        for i in range(len(hand)):
            if i == 0:
                board.add_domino(hand[i])
            else:
                board.add_domino(hand[i], random.choice(["N", "E", "S", "W"]))

        print(board)



if __name__ == "__main__":
    e = Engine()
    e.play()
