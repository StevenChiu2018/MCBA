from typing import List
import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import Ant, Feader, Status


matplotlib.use('Agg')


class TimeBase:
    def __init__(self, feaders: List[Feader]) -> None:
        self.feaders: List[Feader] = feaders
        self.records = []
        self.status = []
        self.predictions = [{feader.name: 0 for feader in self.feaders}]

    def add_records(self, ants: List[Ant]):
        self.records.extend(ants)

        cur_status = {feader.name: 0 for feader in self.feaders}
        cur_status['uncommitted'] = 0
        for ant in ants:
            if ant.state == Status.UNCOMMITTED:
                cur_status['uncommitted'] += 1
            else:
                cur_status[ant.committed_to.name] += 1

        self.__calculate_prediction(cur_status=cur_status)
        self.status.append(cur_status)

    def __calculate_prediction(self, cur_status):
        uncommitted_ants = cur_status['uncommitted']

        next_prediction = {}
        for feader in self.feaders:
            prediction = feader.discover_possibility * uncommitted_ants + \
                feader.recuitment_possibility * \
                cur_status[feader.name] * uncommitted_ants - \
                feader.attrition_possibility * uncommitted_ants

            next_prediction[feader.name] = prediction

        self.predictions.append(next_prediction)

    def draw_status_line_graph(self, need_prediction: bool = False):
        feader_names = [feader.name for feader in self.feaders]
        feader_names.append('uncommitted')

        plt.xlabel('time step')
        plt.ylabel('number of ants')

        for feader_name in feader_names:
            state_track = [status[feader_name] for status in self.status]
            if need_prediction and feader_name != 'uncommitted':
                prediction = [prediction[feader_name]
                              for prediction in self.predictions]
                plt.plot(prediction, label=feader_name + 'prediction')
            plt.plot(state_track, label=feader_name)

        plt.legend()
        plt.savefig(f'./part1_result/ants_status{time.time()}.png')
