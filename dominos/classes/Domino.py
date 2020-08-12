"""A class representing a single domino."""

class Domino:
    def __init__(self, big_end, small_end):
        if big_end < small_end:
            raise ValueError("Must pass in big end of Domino first")
        self.ends = (big_end, small_end)
        self.coordinates = None
        self.is_spinner = False
        self.reversed = False
#         self.reversed_for_print = False
    
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

    def reverse(self):
        if self.reversed:
            raise Exception("Domino should not be reversed twice")
        self.reversed = True

#     def reverse_for_print(self):
#         self.reversed_for_print = True

    def head(self):
        return self.ends[1] if self.reversed else self.ends[0]
    
    def tail(self):
        return self.ends[0] if self.reversed else self.ends[1]

    def total(self):
        return sum(self.ends)

    def equals(self, a, b):
        return self.ends == (a, b) or self.ends == (b, a)

    def __eq__(self, other):
        return self.ends == other.ends

    def __hash__(self):
        return hash(self.ends)

    def __str__(self):
#          a = 0 if (self.reversed == self.reversed_for_print) else 1
         a = 1 if self.reversed else 0
         return f"[{self.ends[a]},{self.ends[1 - a]}]" 
