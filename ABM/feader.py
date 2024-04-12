from .position import Position


class Feader:
    def __init__(self, name: str, position: Position, discover_possibility: float, attrition_possibility: float, recuitment_possibility: float, unit: int) -> None:
        self.name: str = name
        self.position: Position = position
        self.discover_possibility: float = discover_possibility
        self.attrition_possibility: float = attrition_possibility
        self.recuitment_possibility: float = recuitment_possibility
        self.unit: int = unit

    def commit(self):
        self.unit -= 1
