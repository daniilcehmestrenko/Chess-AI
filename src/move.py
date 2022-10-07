
class Move:

    def __init__(self, initial, final):
        #исоздный квадрат и куда хотим пойти
        self.initial = initial
        self.final = final

    def __eq__(self, other) -> bool:
        return self.initial == other.initial and self.final == other.final