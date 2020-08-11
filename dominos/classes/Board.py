"""A class representing the dominos currently in play."""


class Board:
    def __init__(self):
        self.board = {}
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.spinner_x = None

    """
    def get_north(self):
        return self.north

    def get_east(self):
        return self.east

    def get_south(self):
        return self.south

    def get_west(self):
        return self.west
    """

    def add_domino(self, domino, direction=""):
        valid, reverse = self.verify_placement(domino, direction)
        if not valid:
            raise ValueError(f"Domino {str(domino)} cannot be added in the {direction} direction")

        if direction == "":
            # When placing the first domino
            if (0, 0) in self.board:
                raise Exception("Must specify a valid direction if the board contains dominos")
            self.board[(0, 0)] = domino
            self.north = 0
            self.east = 0
            self.south = 0
            self.west = 0
            if domino.is_double():
                self.set_spinner_x(0)
                domino.mark_as_spinner()
        elif direction == "N":
            if self.spinner_x is None:
                raise Exception("Cannot add domino to north side when spinner isn't set")
            self.north += 1
            self.board[(self.spinner_x, self.north)] = domino
        elif direction == "E":
            self.east += 1
            self.board[(self.east, 0)] = domino
            if self.spinner_x is None and domino.is_double():
                self.set_spinner_x(self.east)
                domino.mark_as_spinner()
        elif direction == "S":
            if self.spinner_x is None:
                raise Exception("Cannot add domino to south side when spinner isn't set")
            self.south -= 1
            self.board[(self.spinner_x, self.south)] = domino
        elif direction == "W":
            self.west -= 1
            self.board[(self.west, 0)] = domino
            if self.spinner_x is None and domino.is_double():
                self.set_spinner_x(self.west)
                domino.mark_as_spinner()
        else:
            raise ValueError("Unknown direction:", direction)

        if reverse:
            domino.reverse()

    def verify_placement(self, domino, direction):
        """Return whether a domino can be placed in the given direction and whether it needs to be reversed
           in order to be valid."""
        if direction == "":
            if (0, 0) in self.board:
                return False, False
            return True, False  # No need to check in this case as it's the first placement
        elif direction == "N":
            if self.spinner_x is None or self.east == self.spinner_x or self.west == self.spinner_x:
                return False, False
            coordinate = (self.spinner_x, self.north)
        elif direction == "E":
            coordinate = (self.east, 0)
        elif direction == "S":
            if self.spinner_x is None or self.east == self.spinner_x or self.west == self.spinner_x:
                return False, False
            coordinate = (self.spinner_x, self.south)
        elif direction == "W":
            coordinate = (self.west, 0)
        else:
            raise ValueError("Invalid direction:", direction)

        if direction in ["N", "W"]:
            hook = self.board[coordinate].head()
        else:
            hook = self.board[coordinate].tail()
            
        if self.get_link_end(domino, direction) == hook:
            return True, False
        elif self.get_free_end(domino, direction) == hook:
            return True, True
        return False, False 

    def get_link_end(self, domino, direction):
        return domino.tail() if direction in ["N", "W"] else domino.head()

    def get_free_end(self, domino, direction):
        return domino.head() if direction in ["N", "W"] else domino.tail()

    def get_valid_placements(self, domino):
        """Return which directions a domino can be placed in."""
        if self.is_empty():
            return [""]
        valid_dirs = []
        for direction in ["N", "E", "S", "W"]:
            valid, _ = self.verify_placement(domino, direction)
            if valid:
                valid_dirs.append(direction)
        return valid_dirs

    def get_valid_placements_for_hand(self, hand):
        placements = [] 
        for i, domino in enumerate(hand):
            placements.append((i, domino, self.get_valid_placements(domino)))
        return placements

    def set_spinner_x(self, x):
        if self.spinner_x is not None:
            raise Exception("Spinner already set, cannot update")
        self.spinner_x = x

    def is_empty(self):
        return len(self.board) == 0

    def score_board(self):
        if self.is_empty():
            raise Exception("Cannot score an empty board")

        total = 0
        if self.east == 0 and self.west == 0:
            total += self.board[(0, 0)].total()
        else:
            # We have at least two dominos, so each domino on the end will only count once
            
            # Handle east-west
            east = self.board[(self.east, 0)] 
            west = self.board[(self.west, 0)] 
            
            if east.is_double():
                total += east.total()
            else:
                total += self.get_free_end(east, "E")

            if west.is_double():
                total += west.total()
            else:
                total += self.get_free_end(west, "W")

            # Handle north-south
            if self.north > 0:
                north = self.board[(self.spinner_x, self.north)]
                if north.is_double():
                    total += north.total()
                else:
                    total += self.get_free_end(north, "N")

            if self.south < 0:
                south = self.board[(self.spinner_x, self.south)]
                if south.is_double():
                    total += south.total()
                else:
                    total += self.get_free_end(south, "S")

        return total if total % 5 == 0 else 0

    def __str__(self):
        """Prints the current board state."""
        if self.north is None:
            return "."
        rep = ""
        for r in range(self.north, self.south - 1, -1):
            for c in range(self.west, self.east + 1):
#                 print(r, c)
                if (c, r) in self.board:
                    rep += str(self.board[(c, r)])
                else:
                    rep += "  .  " 
            rep += "\n"
        return rep   

    def render_board(self):
        pass
