class Player:
    def __init__(self, id_, score=0):
        self._id = id_
        self.hand = []
        self.score = score

    def assign_hand(self, hand):
        """Assign a list of Dominos as this player's hand."""
        self.hand = hand

    def add_domino_to_hand(self, domino):
        self.hand.append(domino)

    def add_points(self, points):
        self.score += points

    def get_hand_value(self):
        """Return the sum of the pips in this player's hand, rounded to the nearest 5."""
        pass
