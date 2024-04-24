import math
import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import Feader, Position
from env import ENV

ENV.load_env()


matplotlib.use('Agg')


class ODE:
    def __init__(self, ant_amount: int, feaders: [Feader], time_steps: int):
        self.feaders = feaders
        self.predictions = [{feader.name: 0 for feader in feaders}]

        for _ in range(time_steps):
            last_prediction = self.predictions[-1]
            uncommitted_ants = max(0, ant_amount -
                                   sum(last_prediction.values()))
            next_prediction = {feader.name: 0 for feader in feaders}

            for feader in feaders:
                diff = feader.discover_possibility * uncommitted_ants + \
                    feader.recuitment_possibility * \
                    last_prediction[feader.name] * uncommitted_ants - \
                    feader.attrition_possibility * last_prediction[feader.name]

                next_prediction[feader.name] = max(
                    0, last_prediction[feader.name] + math.ceil(diff))

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

    ode = ODE(ant_amount=100, feaders=[feader_a, feader_b], time_steps=70)

    ode.draw_prediction_result()
