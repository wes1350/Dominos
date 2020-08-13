"""A game engine for running a game of Dominos."""
import sys, random
sys.path.insert(0, '..')  # For importing app config, required for using db
from dominos.Config import Config
from dominos.classes.Board import Board
from dominos.classes.Pack import Pack
from dominos.classes.Player import Player

class Engine:
    def __init__(self):
        self.config = Config()
        self.n_players = self.config.n_players
        self.hand_size = self.config.hand_size
        self.win_threshold = self.config.win_threshold
        self.check_5_doubles = self.config.check_5_doubles
        self.players = []
        self.board = None
        self.pack = None
        for i in range(self.n_players):
            self.players.append(Player(i))
        self.current_player = None
        self.n_passes = 0

    def run_game(self):
        """Start and run a game until completion, handling game logic as necessary."""
        print("Scores:", self.get_scores())
        next_round_fresh = self.play_round(fresh_round=True)
        while not self.game_is_over():
            next_round_fresh = self.play_round(next_round_fresh)

        scores = self.get_scores(indexed=False)

        winner = scores.index(max(scores))
        self.shout("Game is over!\n\nPlayer {} wins!".format(winner))
        self.shout("", "game_over")
        return winner

    def play_round(self, fresh_round=False):
        self.board = Board()
        self.draw_hands(fresh_round)
        if fresh_round:
            self.current_player = self.determine_first_player()
        blocked = False
        play_fresh = fresh_round
        while self.players_have_dominos() and not blocked and not self.game_is_over():
            blocked = self.play_turn(play_fresh)
            self.next_turn()
            print("Scores:", self.get_scores())
            play_fresh = False
        if not self.players_have_dominos():
            # Reverse current player switch
            self.current_player = (self.current_player + self.n_players - 1) % self.n_players
            self.players[self.current_player].add_points(self.get_value_on_domino(self.current_player))
            print(f"Player {self.current_player} dominoed!")
            print("Scores:", self.get_scores())
            return False
        elif blocked:
            print("Game blocked!")
            blocked_scorer, points = self.get_blocked_result()
            if blocked_scorer is not None:
                print(f"Player {blocked_scorer} scores {points}")
                self.players[blocked_scorer].add_points(points)
            print("Scores:", self.get_scores())
            return True
        else:  # Game is over
            return False

    def play_turn(self, play_fresh=False):
        domino, direction = self.query_move(self.current_player, play_fresh)
        if domino is not None:
            self.board.add_domino(domino, direction)
            self.players[self.current_player].remove_domino(domino)
            score = self.board.score_board()
            self.players[self.current_player].add_points(score)
            self.n_passes = 0
        else:  # Player passes
            self.n_passes += 1

        if self.n_passes == self.n_players:
            return True

        print(self.board)
        return False

    def next_turn(self) -> None:
        """Update the player to move."""
        self.current_player = (self.current_player + 1) % self.n_players

    def draw_hands(self, fresh_round=False):
        while True:
            self.pack = Pack()
            hands = []
            for i in range(self.n_players):
                hands.append(self.pack.pull(self.hand_size))
            if self.verify_hands(hands, check_any_double=fresh_round,
                                 check_5_doubles=self.check_5_doubles):
                for i in range(self.n_players):
                    self.players[i].assign_hand(hands[i])
                return

    def verify_hands(self, hands, check_5_doubles=True, check_any_double=False):
        if not check_5_doubles and not check_any_double:
            return True

        # Check that no hand has 5 doubles
        no_doubles = True
        for hand in hands:
            n_doubles = len([d for d in hand if d.is_double()])
            if check_5_doubles:
                if n_doubles >= 5:
                    return False
            if n_doubles > 0:
                no_doubles = False

        # Check that some hand has a double
        if check_any_double:
            if no_doubles:
                return False

        return True

    def determine_first_player(self):
        """Determine who has the largest double, and thus who will play first.
           Assumes each player's hand is assigned and a double exists among them."""
        for i in range(6, -1, -1):
            for p in range(self.n_players):
                for d in self.players[p].get_hand():
                    if d.equals(i, i):
                        return p
        raise Exception("Could not find double in player's hands")

    def players_have_dominos(self):
        return min([len(p.get_hand()) for p in self.players]) > 0

    def game_is_over(self):
        return max(self.get_scores(indexed=False)) >= self.win_threshold

    def get_scores(self, indexed=True):
        if indexed:
            return {i: self.get_player_score(i) for i in range(len(self.players))}
        else:
            return [self.get_player_score(i) for i in range(len(self.players))]

    def get_player_score(self, player):
        return self.players[player].get_score()

    def query_move(self, player, play_fresh=False):
        while True:
            possible_placements = self.board.get_valid_placements_for_hand(self.players[player].get_hand(), play_fresh)
            pretty_placements = [(x[0], str(x[1]), x[2]) for x in possible_placements]
            print("Possible placements:")
            for el in pretty_placements:
                print(" --- " + str(el))
            move_possible = any([len(t[-1]) > 0 for t in possible_placements])
            if move_possible:
                try:
                    domino_index = int(input(f"Player {player}, what domino do you select?\n").strip())
                    if not (0 <= domino_index < len(possible_placements)) or len(possible_placements[domino_index][-1]) == 0:
                        self.whisper("Invalid domino choice: " + str(domino_index), player)
                    else:
                        domino = possible_placements[domino_index][1]
                        if len(possible_placements[domino_index][-1]) == 1:
                            direction = possible_placements[domino_index][-1][0]
                            return domino, direction
                        else:
                            while True:
                                direction = input(f"Player {player}, what direction do you select?\n").strip()
                                if direction not in possible_placements[domino_index][-1]:
                                    self.whisper("Invalid direction: " + direction, player)
                                else:
                                    return domino, direction
                except Exception as e:
                    print("CAUGHT ERROR:", e)
                    self.whisper("Invalid input, try again", player)
            else:
                pulled = self.pack.pull()
                _ = input(f"Player {player}, you have no valid moves. Press Enter to pull\n")
                if pulled is not None:
                    self.players[player].add_domino(pulled)
                else:
                    self.shout("Pack is empty, cannot pull. Skipping turn")
                    return None, None

    def get_value_on_domino(self, player):
        """Get the value of a 'Domino' by a player, i.e. the sum, rounded to the
           nearest 5, of the other players' hand totals."""
        total = sum([p.hand_total() for i, p in enumerate(self.players) if i != player])
        if total % 5 > 2:
            total += (5 - (total % 5))
        else:
            total -= total % 5
        return total

    def get_blocked_result(self):
        """Find the player (if any) that wins points when the game is blocked and return
           that player and the points they receive."""
        totals = [p.hand_total() for p in self.players]
        print("Totals:", {i: totals[i] for i in range(len(totals))})
        if len([t for t in totals if t == min(totals)]) > 1:
            # Multiple players have lowest count, so nobody gets points
            return None, 0
        else:
            # Find the player with minimum score and the sum of the other players' hands, rounded to the nearest 5
            scorer = totals.index(min(totals))
            total = sum(totals) - min(totals)
            if total % 5 > 2:
                total += (5 - (total % 5))
            else:
                total -= total % 5
            return scorer, total


    def whisper(self, msg, player):
        print(player, ":", msg)

    def shout(self, msg, msg_type=None):
        print(msg)


if __name__ == "__main__":
    e = Engine()
    winner = e.run_game()
