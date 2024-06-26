from typing import Dict, List
import random

from env import ENV
from .position import Position
from .feader import Feader
from .nest import Nest

DIRECTIONS = [Position(1, 0), Position(0, 1), Position(-1, 0), Position(0, -1),
              Position(1, 1), Position(1, -1), Position(-1, 1), Position(-1, -1)]


class Nature:
    def __init__(self, feaders: List[Feader], nest: Nest) -> None:
        self.feaders: Dict[Feader] = {
            feader.position.tuplize(): feader for feader in feaders}

        self.nest: Nest = nest

    def is_feader(self, position: Position) -> bool:
        return position.tuplize() in self.feaders

    def get_feader(self, position: Position) -> Feader:
        return self.feaders[position.tuplize()]

    def get_nest(self):
        return self.nest

    @staticmethod
    def random_direction(current_position: Position) -> Position:
        feasible_direction = Nature.feasible_directions(
            current_position=current_position)

        return random.choice(feasible_direction)

    @staticmethod
    def surrounding_feasible_positions(position: Position) -> List[Position]:
        feasible_directions = Nature.feasible_directions(
            current_position=position)

        return [direction + position for direction in feasible_directions]

    @staticmethod
    def feasible_directions(current_position: Position) -> List[Position]:
        return [direction for direction in DIRECTIONS if Nature.is_feasible(
            current_position + direction)]

    @staticmethod
    def is_feasible(position: Position) -> bool:
        boundary_x = ENV.get('NATURE_BOUNDARY_X')
        boundary_y = ENV.get('NATURE_BOUNDARY_Y')

        return 0 <= position.x and position.x <= boundary_x and 0 <= position.y and position.y <= boundary_y
