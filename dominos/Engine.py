"""A game engine for running a game of Dominos."""
import sys, random
sys.path.insert(0, '..')  # For importing app config, required for using db
from dominos.classes.Board import Board
from dominos.classes.Pack import Pack
from dominos.classes.Player import Player

class Engine:
    def __init__(self):
        self.n_players = 2
        self.players = []
        self.board = Board()
        self.pack = Pack()
        for i in range(self.n_players):
            self.players.append(Player(i))
            self.players[i].assign_hand(self.pack.pull(7))
        self.current_player = 0
        self.win_threshold = 20
    
    def run_game(self):
        """Start and run a game until completion, handling game logic as necessary."""
        while not self.game_is_over():
#             self.broadcast_state()
            self.play_turn()
            self.next_turn()
#         self.broadcast_state()
        winner = self.players.index(max(self.get_scores()))
        self.shout("Game is over!\n\nPlayer {} wins!".format(winner))
        self.shout("", "game_over")
        return winner
 
    def get_scores(self):
        return [self.get_player_score(i) for i in range(len(self.players))]

    def play_turn(self):
        print(self.board)

     def next_turn(self) -> None:
            """Move on to the next turn, updating the game state as necessary."""
            self.current_player = (self.current_player + 1) % self.n_players

    def game_is_over(self):
        return max(self.get_scores()) >= self.win_threshold

    def whisper(self, msg, player):
        print(player, ":", msg)
    
    def shout(self, msg, msg_type):
        print(msg)


if __name__ == "__main__":
    e = Engine()
    e.run_game()
