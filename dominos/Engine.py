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

        for i in range(len(hand)):
            domino = hand[i]
            valid_dirs = board.get_valid_placements(hand[i])    
            if len(valid_dirs) == 0:
                print(f"Couldn't add {str(domino)} to the board")
            else:
                print(valid_dirs, f"Adding {str(domino)} on step {i}")
                board.add_domino(domino, random.choice(valid_dirs))

        print(board)



if __name__ == "__main__":
    e = Engine()
    e.play()
