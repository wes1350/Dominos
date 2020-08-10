"""A class representing a single domino."""

class Domino:
    def __init__(self, big_end, small_end):
        self.ends = (big_end, small_end)
        self.coordinates = None
        self.is_spinner = False
    
    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def is_double(self):
        return self.ends[0] == self.ends[1]

    def is_spinner(self):
        return self.is_spinner

    def mark_as_spinner(self):
        if not self.is_double():
            raise Exception("Cannot mark non-double as spinner")
        self.is_spinner = True

    def __eq__(self, other):
        return self.ends == other.ends

    def __hash__(self):
        return hash(self.ends)

    def __str__(self):
        return f"[{self.ends[0]},{self.ends[1]}]" 
