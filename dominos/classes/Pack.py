import random
from dominos.classes.Domino import Domino

class Pack:
    def __init__(self, max_pips=6):
        self.dominos = []
        for i in range(max_pips + 1):
            for j in range(max_pips + 1):
                if i >= j:
                    self.dominos.append(Domino(i, j))

    def pull(self, n=1):
        if n == 1:
            if len(self.dominos) == 0:
                return None
            return self.dominos.pop(random.randint(0, len(self.dominos) - 1))
        else:
            pulled = []
            for i in range(n):
                pulled.append(self.dominos.pop(random.randint(0, len(self.dominos) - 1)))
            return pulled
