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
        else:
            raise ValueError("Unknown direction:", direction)

    def set_spinner_x(self, x):
        if self.spinner_x is not None:
            raise Exception("Spinner already set, cannot update")
        self.spinner_x = x

    def __str__(self):
        """Prints the current board state."""
        print("Keys:", self.board.keys())
        rep = ""
        for r in range(self.north, self.south - 1, -1):
            for c in range(self.west, self.east + 1):
#                 print(r, c)
                if (c, r) in self.board:
                    rep += str(self.board[(c, r)])
                else:
                    rep += "  .  " 
            rep += "\n"
        print([str(self.board[k]) for k in self.board])
        return rep   

    def render_board(self):
        pass

