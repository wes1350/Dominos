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

    def add_domino(self, domino, direction=None):
        valid, reverse = self.verify_placement(domino, direction)
        if not valid:
            raise ValueError(f"Domino {str(domino)} cannot be added in the {direction} direction")

        if direction is None:
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
        if direction is None:
            if (0, 0) in self.board:
                return False, False
            return True, False  # No need to check in this case as it's the first placement
        elif direction == "N":
            if self.spinner_x is None:
                return False, False
            coordinate = (self.spinner_x, self.north)
        elif direction == "E":
            coordinate = (self.east, 0)
        elif direction == "S":
            if self.spinner_x is None:
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
            
        link_end = domino.tail() if direction in ["N", "W"] else domino.head()
        free_end = domino.head() if direction in ["N", "W"] else domino.tail()
        if link_end == hook:
            return True, False
        elif free_end == hook:
            return True, True
        return False, False 

    def get_valid_placements(self, domino):
        """Return which directions a domino can be placed in."""
        if self.is_empty():
            return [None]
        valid_dirs = []
        for direction in ["N", "E", "S", "W"]:
            valid, _ = self.verify_placement(domino, direction)
            if valid:
                valid_dirs.append(direction)
        return valid_dirs

    def set_spinner_x(self, x):
        if self.spinner_x is not None:
            raise Exception("Spinner already set, cannot update")
        self.spinner_x = x

    def is_empty(self):
        return len(self.board) == 0

    def __str__(self):
        """Prints the current board state."""
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
