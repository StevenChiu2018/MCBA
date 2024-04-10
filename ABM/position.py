class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def tuplize(self):
        return (self.x, self.y)

    def __add__(self, add_position: 'Position'):
        return Position(self.x + add_position.x, self.y + add_position.y)

    def __sub__(self, subtract_position: 'Position'):
        return sum([abs(self.x - subtract_position.x), abs(self.y - subtract_position.y)])

    def __eq__(self, compare_position: 'Position') -> bool:
        return self.x == compare_position.x and self.y == compare_position.y
