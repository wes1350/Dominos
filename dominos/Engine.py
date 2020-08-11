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
        print(self.board)
        print("Scores:", self.get_scores())
        while not self.game_is_over():
            self.play_turn()
            self.next_turn()
            print("Scores:", self.get_scores())
        winner = self.players.index(max(self.get_scores()))
        self.shout("Game is over!\n\nPlayer {} wins!".format(winner))
        self.shout("", "game_over")
        return winner

    def play_turn(self):
        domino, direction = self.query_move(self.current_player)
        if domino is not None:
            self.board.add_domino(domino, direction)
            score = self.board.score_board()
            self.players[self.current_player].add_points(score)

        print(self.board)

    def next_turn(self) -> None:
        """Move on to the next turn, updating the game state as necessary."""
        self.current_player = (self.current_player + 1) % self.n_players

    def game_is_over(self):
        return max(self.get_scores()) >= self.win_threshold

    def get_scores(self):
        return {i: self.get_player_score(i) for i in range(len(self.players))}

    def get_player_score(self, player):
        return self.players[player].get_score()

    def query_move(self, player):
        while True:
            possible_placements = self.board.get_valid_placements_for_hand(self.players[player].get_hand())
            pretty_placements = [(x[0], str(x[1]), x[2]) for x in possible_placements]
            print("Possible placements:", pretty_placements)
            move_possible = any([len(t[-1]) > 0 for t in possible_placements])
            if move_possible:
                domino_index = int(input("Player {player}, what domino do you select?\n").strip())
                try:
                    if 0 <= domino_index < len(possible_placements):
                        # TODO: don't query direction if none is possible for this domino
                        direction = input("Player {player}, what direction do you select?\n").strip()
                        if direction not in possible_placements[domino_index][-1]:
                            self.whisper("invalid direction: " + direction, player)
                        else:
                            return possible_placements[domino_index][1], direction
                except Exception as e:
                    print("CAUGHT ERROR:", e)
                    self.whisper("Invalid input, try again", player)
            else:
                pulled = self.pack.pull()
                _ = input("Player {player}, you have no valid moves. Press Enter to pull\n")
                if pulled is not None:
                    self.players[player].add_domino(pulled)
                else:
                    self.shout("Pack is empty, cannot pull. Skipping turn")
                    return None, None


    def whisper(self, msg, player):
        print(player, ":", msg)

    def shout(self, msg, msg_type):
        print(msg)


if __name__ == "__main__":
    e = Engine()
    e.run_game()
