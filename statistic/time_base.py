from typing import List
import matplotlib.pyplot as plt
import matplotlib

from ABM import Ant, Feader, Status


matplotlib.use('Agg')


class TimeBase:
    def __init__(self, feaders: List[Feader]) -> None:
        self.feaders: List[Feader] = feaders
        self.records = []
        self.status = []

    def add_records(self, ants: List[Ant]):
        self.records.extend(ants)

        cur_status = {feader.name: 0 for feader in self.feaders}
        cur_status['uncommitted'] = 0
        for ant in ants:
            if ant.state == Status.UNCOMMITTED:
                cur_status['uncommitted'] += 1
            else:
                cur_status[ant.committed_to.name] += 1

        self.status.append(cur_status)

    def draw_status(self):
        states = [feader.name for feader in self.feaders]
        states.append('uncommitted')

        plt.xlabel('time step')
        plt.ylabel('number of ants')

        for state in states:
            state_track = [status[state] for status in self.status]
            plt.plot(state_track, label=state)

        plt.legend()
        plt.savefig('./part1_result/ants_status.png')
