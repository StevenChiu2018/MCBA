from typing import List
import math
import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import Ant, Feader, Status


matplotlib.use('Agg')


class TimeBase:
    def __init__(self, feaders: List[Feader], ant_amount: int, need_report: bool) -> None:
        self.feaders: List[Feader] = feaders
        self.status = []
        self.predictions = [{feader.name: 0 for feader in self.feaders}]
        self.ant_amount = ant_amount
        self.need_report = need_report
        if need_report:
            self.report_file = open('./reports/report', 'a')

    def add_records(self, ants: List[Ant], time_step: int):
        cur_status = {feader.name: 0 for feader in self.feaders}
        cur_status['uncommitted'] = 0

        for ant in ants:
            if ant.state == Status.UNCOMMITTED:
                cur_status['uncommitted'] += 1
            else:
                cur_status[ant.committed_to.name] += 1

            if self.need_report:
                self.report_file.write(
                    f'{time_step} {ant.state.name} {ant.position.x} {ant.position.y}\n')

        self.status.append(cur_status)

    def __calculate_prediction(self):
        last_prediction = self.predictions[-1]
        uncommitted_ants = max(0, self.ant_amount -
                               sum(last_prediction.values()))
        next_prediction = {feader.name: 0 for feader in self.feaders}

        for feader in self.feaders:
            diff = feader.discover_possibility * uncommitted_ants + \
                feader.recuitment_possibility * \
                last_prediction[feader.name] * uncommitted_ants - \
                feader.attrition_possibility * last_prediction[feader.name]

            next_prediction[feader.name] = max(
                0, last_prediction[feader.name] + math.ceil(diff))

        self.predictions.append(next_prediction)

    def draw_status_line_graph(self, prediction_round: int = 0):
        self.__draw_simulation_result()

        if prediction_round > 0:
            for _ in range(prediction_round):
                self.__calculate_prediction()
            self.__draw_prediction_result()

    def __draw_prediction_result(self):
        feader_names = [feader.name for feader in self.feaders]

        plt.xlabel('time step')
        plt.ylabel('number of ants')

        for feader_name in feader_names:
            prediction = [prediction[feader_name]
                          for prediction in self.predictions]
            plt.plot(prediction, label=feader_name + ' prediction')

        plt.legend()
        plt.savefig(f'./part1_result/ants_prediction_{time.time()}.png')
        plt.close()

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
