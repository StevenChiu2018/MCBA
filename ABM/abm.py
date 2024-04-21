import random
from typing import List, Dict, Tuple

from statistic import TimeBase
from .ant import Ant, Status
from .feader import Feader
from .nature import Nature
from .nest import Nest


class ABM:
    def __init__(self, ants: List[Ant], feaders: List[Feader], nest: Nest, need_report: bool = False) -> None:
        self.ants: List[Ant] = ants
        self.feaders: List[Feader] = feaders
        self.nest: Nest = nest
        self.nature: Nature = Nature(self.feaders, self.nest)
        self.statistic: TimeBase = TimeBase(
            feaders=feaders, ant_amount=len(ants), need_report=need_report)

    def execute(self) -> int:
        time_step = 0

        while True:
            if any([feader.unit <= 0 for feader in self.feaders]):
                break

            commited_ants: List[Ant] = []
            position_ants_dict: Dict[Tuple[int, int], List[Ant]] = {}
            for ant in self.ants:
                ant.go()
                if ant.state == Status.COMMITTED:
                    commited_ants.append(ant)
                else:
                    if ant.position.tuplize() in position_ants_dict:
                        position_ants_dict[ant.position.tuplize()].append(ant)
                    else:
                        position_ants_dict[ant.position.tuplize()] = [ant]

            for ant in commited_ants:
                surrounding_positions = [position for position in Nature.surrounding_feasible_positions(
                    ant.position) if position.tuplize() in position_ants_dict]
                if ant.position.tuplize() in position_ants_dict:
                    surrounding_positions.append(ant.position)

                for surrounding_position in surrounding_positions:
                    for surrounding_ant in position_ants_dict[surrounding_position.tuplize()]:
                        if random.random() < ant.committed_to.recuitment_possibility:
                            surrounding_ant.recruit(ant.committed_to)

            self.statistic.add_records(self.ants, time_step=time_step)
            time_step += 1

        self.statistic.close_file()
        return time_step
