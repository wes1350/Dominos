"""A class representing the dominos currently in play."""


class Board:
    def __init__(self):
        self.board = {}
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.spinner_x = None

        self.rendered_north = None
        self.rendered_east = None
        self.rendered_south = None
        self.rendered_west = None
        self.rendered_spinner_x = None

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
                self.spinner_x = 0
                self.rendered_spinner_x = 0
                domino.mark_as_spinner()

                self.rendered_east = 1
                self.rendered_west = -1
            else:
                self.rendered_east = 2
                self.rendered_west = -2
            # Since we can only play north/south off doubles, rendered north/south limits are always the same
            self.rendered_north = 2
            self.rendered_south = -2
        elif direction == "N":
            if self.spinner_x is None:
                raise Exception("Cannot add domino to north side when spinner isn't set")
            self.north += 1
            self.rendered_north += 2 if domino.is_double() else 4
            self.board[(self.spinner_x, self.north)] = domino
        elif direction == "E":
            self.east += 1
            self.rendered_east += 2 if domino.is_double() else 4
            self.board[(self.east, 0)] = domino
            if self.spinner_x is None and domino.is_double():
                self.spinner_x = self.east
                self.rendered_spinner_x = self.rendered_east - 1 
                domino.mark_as_spinner()
        elif direction == "S":
            if self.spinner_x is None:
                raise Exception("Cannot add domino to south side when spinner isn't set")
            self.south -= 1
            self.rendered_south -= 2 if domino.is_double() else 4
            self.board[(self.spinner_x, self.south)] = domino
        elif direction == "W":
            self.west -= 1
            self.rendered_west -= 2 if domino.is_double() else 4
            self.board[(self.west, 0)] = domino
            if self.spinner_x is None and domino.is_double():
                self.spinner_x = self.west
                self.rendered_spinner_x = self.rendered_west + 1 
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

    def get_valid_placements_for_hand(self, hand, play_fresh=False):
        placements = [] 
        largest_double = -1
        if play_fresh:
            for domino in hand:
                if domino.is_double():
                    if domino.head() > largest_double:
                        largest_double = domino.head()
        for i, domino in enumerate(hand):
            if play_fresh:
                if domino.head() != largest_double or not domino.is_double():
                    placements.append((i, domino, []))
                else:
                    placements.append((i, domino, self.get_valid_placements(domino)))
            else:
                placements.append((i, domino, self.get_valid_placements(domino)))
        return placements

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

    def get_rendered_position(self, domino, direction):
        if direction == "N":
            if domino.is_double():
                return {"1": [self.rendered_spinner_x - 2, self.rendered_north], 
                        "2": [self.rendered_spinner_x, self.rendered_north]}
            else:
                return {"1": [self.rendered_spinner_x - 1, self.rendered_north], 
                        "2": [self.rendered_spinner_x - 1, self.rendered_north - 2]}
        elif direction == "E" or direction == "":
            if domino.is_double():
                return {"1": [self.rendered_east - 2, 2], 
                        "2": [self.rendered_east - 2, 0]}
            else:
                return {"1": [self.rendered_east - 4, 1], 
                        "2": [self.rendered_east - 2, 1]}
        elif direction == "S":
            if domino.is_double():
                return {"1": [self.rendered_spinner_x - 2, self.rendered_south + 2], 
                        "2": [self.rendered_spinner_x, self.rendered_south + 2]}
            else:
                return {"1": [self.rendered_spinner_x - 1, self.rendered_south + 4], 
                        "2": [self.rendered_spinner_x - 1, self.rendered_south + 2]}
        elif direction == "W":
            if domino.is_double():
                return {"1": [self.rendered_west, 2], 
                        "2": [self.rendered_west, 0]}
            else:
                return {"1": [self.rendered_west, 1], 
                        "2": [self.rendered_west + 2, 1]}

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
