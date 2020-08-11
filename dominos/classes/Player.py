class Player:
    def __init__(self, id_, score=0):
        self._id = id_
        self.hand = []
        self.score = score

    def assign_hand(self, hand):
        """Assign a list of Dominos as this player's hand."""
        self.hand = hand

    def add_domino(self, domino):
        self.hand.append(domino)

    def remove_domino(self, domino):
        for i, d in enumerate(self.hand):
            if d == domino:
                self.hand.pop(i)
                return
        raise Exception(f"Could not find domino {str(domino)} in hand. Hand: {[str(dom) for dom in self.hand]}")

    def add_points(self, points):
        self.score += points

    def get_score(self):
        return self.score

    def get_hand(self):
        return self.hand

    def hand_total(self):
        return sum([d.total() for d in self.hand])

    def hand_is_empty(self):
        return len(self.hand) == 0
