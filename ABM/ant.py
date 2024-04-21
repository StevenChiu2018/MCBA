import random
from enum import Enum
from typing import Optional

from env import ENV
from .feader import Feader
from .position import Position
from .nature import Nature


class Status(Enum):
    UNCOMMITTED = 1
    COMMITTED = 2


class HeadTo(Enum):
    NEST = 1
    FEADER = 2
    RANDOM = 3


class Ant:
    def __init__(self, initial_position, nature: Nature):
        self.nature: Nature = nature

        self.state = Status.UNCOMMITTED
        self.position: Position = initial_position
        self.committed_to: Optional[Feader] = None
        self.head_to: HeadTo = HeadTo.RANDOM

    def go(self):
        if self.state == Status.UNCOMMITTED:
            self.__do_uncommitted_go()
        else:
            self.__do_committed_go()

        return self.state

    def __do_uncommitted_go(self):
        self.position = self.position + Nature.random_direction(self.position)

        if self.nature.is_feader(self.position):
            feader = self.nature.get_feader(self.position)
            if random.random() < feader.discover_possibility:
                feader.commit()
                self.state = Status.COMMITTED
                self.committed_to = feader
                self.head_to = HeadTo.NEST

    def __do_committed_go(self):
        feasible_directions = self.nature.feasible_directions(self.position)

        destination = self.committed_to.position
        if self.head_to == HeadTo.NEST:
            destination = self.nature.get_nest().position

        short_distance = max(ENV.get('NATURE_BOUNDARY_X'),
                             ENV.get('NATURE_BOUNDARY_Y'))
        for direction in feasible_directions:
            if ((self.position + direction) - destination) < short_distance:
                self.position = self.position + direction
                short_distance = ((self.position + direction) - destination)

        if self.position == destination:
            self.head_to = HeadTo((self.head_to.value % 2) + 1)

            if self.position == self.committed_to.position:
                self.committed_to.commit()

        if self.head_to == HeadTo.FEADER and random.random() < self.committed_to.attrition_possibility:
            self.head_to = HeadTo.RANDOM
            self.state = Status.UNCOMMITTED
            self.committed_to = None

    def recruit(self, feader: Feader):
        self.state = Status.COMMITTED
        self.committed_to = feader
        self.head_to = HeadTo.FEADER
