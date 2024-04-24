
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn
import time
import math

from env import ENV

matplotlib.use('Agg')


class Analyze:
    def __init__(self, record_name: str) -> None:
        self.records = {}

        report_file = open(record_name, 'r')
        for row in report_file.readlines():
            [time_step, state, commit_method, x, y] = row[:-1].split(' ')

            if not int(time_step) in self.records:
                self.records[int(time_step)] = []

            self.records[int(time_step)].append(
                (state, commit_method, (int(x), int(y))))
        report_file.close()

    def get_ant_distribution_before(self, time_step: int, start_at: int = 0):
        statistical = {}
        for cur_time_step, ants_info in self.records.items():
            if cur_time_step < start_at or cur_time_step > time_step:
                continue

            for _, _, position in ants_info:
                if not position in statistical:
                    statistical[position] = 0

                statistical[position] += 1

        return self.generate_ant_distribution(statistical=statistical)

    def generate_ant_distribution(self, statistical):
        ant_distribution = []

        for y in range(ENV.get('NATURE_BOUNDARY_Y')):
            cur_row = []
            for x in range(ENV.get('NATURE_BOUNDARY_X')):
                if (x, y) in statistical:
                    cur_row.append(min(statistical[(x, y)], 90))
                else:
                    cur_row.append(0)
            ant_distribution.append(cur_row)

        return ant_distribution

    def plot_heat_map(self, ant_distribution, file_name):
        plt.figure(figsize=(10, 10))
        hm = seaborn.heatmap(ant_distribution, cmap='Blues')
        hm.xaxis.tick_top()
        hm.add_patch(
            Rectangle((25, 5), 1, 1, fill=False, edgecolor='green', lw=3))
        hm.add_patch(
            Rectangle((10, 40), 1, 1, fill=False, edgecolor='red', lw=3))
        hm.add_patch(
            Rectangle((40, 40), 1, 1, fill=False, edgecolor='orange', lw=3))
        plt.savefig(file_name)
        plt.close()


if __name__ == '__main__':
    ENV.load_env()
    analyze = Analyze('./reports/normal2')
    # for time_step in range(500, 800, 50):
    #     ant_distribution = analyze.get_ant_distribution_before(
    #         time_step=time_step)
    #     analyze.plot_heat_map(ant_distribution=ant_distribution,
    #                           file_name=f'./part1_result/too_long/ants_distribution_{time_step}.png')

    # for time_step in range(600, 900, 100):
    #     ant_distribution = analyze.get_ant_distribution_before(
    #         time_step=time_step, start_at=time_step - 100)
    #     analyze.plot_heat_map(ant_distribution=ant_distribution,
    #                           file_name=f'./part1_result/normal2/ants_distribution_{time_step - 100}-{time_step}.png')

    # recruite_count = 0
    # direct_count = 0
    # for time_step in range(1, 800):
    #     for index, info in enumerate(analyze.records[time_step]):
    #         if analyze.records[time_step - 1][index][0] != "recruited_Feader_A" and info[0] == "recruited_Feader_A":
    #             recruite_count += 1
    #         if analyze.records[time_step - 1][index][0] != "directly_Feader_A" and info[0] == "directly_Feader_A":
    #             direct_count += 1

    # print(recruite_count)
    # print(direct_count)

    statistical = {}
    for time_step in range(300, 800):
        for index, info in enumerate(analyze.records[time_step]):
            if info[0] == "recruited_Feader_A" or info[0] == "directly_Feader_A":
                if not info[2] in statistical:
                    statistical[info[2]] = 0

                statistical[info[2]] = min(1, statistical[info[2]] + 1)

    ant_distribution = analyze.generate_ant_distribution(statistical)
    analyze.plot_heat_map(ant_distribution=ant_distribution,
                          file_name='./part1_result/normal2/commit_a_location2.png')
