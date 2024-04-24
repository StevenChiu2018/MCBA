from typing import List
import math
import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import Feader, Position
from env import ENV

ENV.load_env()


matplotlib.use('Agg')


class ODE:
    def __init__(self, ant_amount: int, feaders: List[Feader], time_steps: int):
        self.feaders = feaders
        self.predictions = [{feader.name: 0 for feader in feaders}]

        uncommitted_ants = ant_amount
        for _ in range(time_steps):
            last_prediction = self.predictions[-1]
            next_prediction = {feader.name: 0 for feader in feaders}

            for feader in feaders:
                feader_amount = last_prediction[feader.name]

                discoveries_ants = math.ceil(
                    feader.discover_possibility * uncommitted_ants)
                uncommitted_ants = max(0, uncommitted_ants - discoveries_ants)

                recruited_ants = math.ceil(feader.recuitment_possibility *
                                           feader_amount * uncommitted_ants)
                uncommitted_ants = max(0, uncommitted_ants - recruited_ants)

                dismissed_ants = math.ceil(
                    feader.attrition_possibility * feader_amount)
                uncommitted_ants += dismissed_ants

                next_prediction[feader.name] = max(
                    0, feader_amount + discoveries_ants + recruited_ants - dismissed_ants)

            self.predictions.append(next_prediction)

    def draw_prediction_result(self):
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


if __name__ == '__main__':
    feader_a = Feader(name='Feader_A', position=Position(10, 40), discover_possibility=ENV.get('ALPHA_A'),
                      attrition_possibility=ENV.get('LAMBDA_A'), recuitment_possibility=ENV.get('BETA_A'), unit=100)
    feader_b = Feader(name='Feader_B', position=Position(40, 40), discover_possibility=ENV.get('ALPHA_B'),
                      attrition_possibility=ENV.get('LAMBDA_B'), recuitment_possibility=ENV.get('BETA_B'), unit=100)

    # feader_a = Feader(name='Feader_A', position=Position(10, 40), discover_possibility=0.0125,
    #                   attrition_possibility=0.009, recuitment_possibility=0.015, unit=100)
    # feader_b = Feader(name='Feader_B', position=Position(40, 40), discover_possibility=0.0125,
    #                   attrition_possibility=0.038, recuitment_possibility=0.006, unit=100)

    ode = ODE(ant_amount=100, feaders=[feader_a, feader_b], time_steps=30)

    ode.draw_prediction_result()
