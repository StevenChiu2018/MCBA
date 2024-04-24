from typing import List
import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import Ant, Feader, Status


matplotlib.use('Agg')


class TimeBase:
    def __init__(self, feaders: List[Feader], need_report: bool) -> None:
        self.feaders: List[Feader] = feaders
        self.status = []
        self.need_report = need_report
        self.first_feeder = ""
        self.feeder_amount = {feader.name: 0 for feader in self.feaders}
        if need_report:
            self.report_file = open('./reports/report', 'a')
        self.first_commit = -1

    def is_the_first_feeder_dominate(self):
        max_amount = max(self.feeder_amount.values())
        for key, amount in self.feeder_amount.items():
            if amount == max_amount:
                return self.first_feeder == key

        return False

    def add_records(self, ants: List[Ant], time_step: int):
        cur_status = {feader.name: 0 for feader in self.feaders}
        cur_status['uncommitted'] = 0

        for ant in ants:
            if ant.state == Status.UNCOMMITTED:
                cur_status['uncommitted'] += 1
            else:
                if self.first_commit == -1:
                    self.first_commit = time_step
                if self.first_feeder == "":
                    self.first_feeder = ant.committed_to.name
                cur_status[ant.committed_to.name] += 1
                self.feeder_amount[ant.committed_to.name] += 1

            if self.need_report:
                self.report_file.write(
                    f'{time_step} {ant.commit_method} {ant.state.name} {ant.position.x} {ant.position.y}\n')

        self.status.append(cur_status)

    def draw_status_line_graph(self):
        self.__draw_simulation_result()

    def __draw_simulation_result(self):
        feader_names = [feader.name for feader in self.feaders]
        feader_names.append('uncommitted')

        plt.xlabel('time step')
        plt.ylabel('number of ants')

        for feader_name in feader_names:
            state_track = [status[feader_name] for status in self.status]
            plt.plot(state_track, label=feader_name)

        plt.legend()
        plt.savefig(f'./part1_result/ants_simulation_{time.time()}.png')
        plt.close()

    def close_file(self):
        if self.need_report:
            self.report_file.close()
