import matplotlib
import matplotlib.pyplot as plt
import time

from ABM import ABM, Ant, Feader, Nature, Nest, Position, Status
from env import ENV

matplotlib.use('Agg')

ENV.load_env()

position_b = Position(37, 31)
feaderAResult = []
feaderBResult = []

for shift in [100, 50, 25, 5]:
    commit_status = {'Feader_A': 0, 'Feader_B': 0, '': 0}
    for running_round in range(50):
        print(f'{running_round} round', end='\r')
        feader_a = Feader(name='Feader_A', position=Position(10, 40), discover_possibility=ENV.get('ALPHA_A'),
                          attrition_possibility=ENV.get('LAMBDA_A'), recuitment_possibility=ENV.get('BETA_A'), unit=shift)
        feader_b = Feader(name='Feader_B', position=position_b, discover_possibility=ENV.get('ALPHA_B'),
                          attrition_possibility=ENV.get('LAMBDA_B'), recuitment_possibility=ENV.get('BETA_B'), unit=100)
        feaders = [feader_a, feader_b]

        nest = Nest(position=Position(25, 5))
        nature = Nature(feaders=feaders, nest=nest)

        ants = [Ant(initial_position=Position(25, 5), nature=nature)
                for _ in range(100)]

        abm = ABM(ants=ants, feaders=feaders, nest=nest, need_report=False)

        result = abm.execute()

        commit_status[result] += 1

    print("")
    print(shift)
    feaderAResult.append(commit_status['Feader_A'])
    feaderBResult.append(commit_status['Feader_B'])
    print('Feader_A: ' + str(commit_status['Feader_A']))
    print('Feader_B: ' + str(commit_status['Feader_B']))

plt.xlabel('round')
plt.ylabel('number of ants')

plt.plot(feaderAResult, label='Feeder A')
plt.plot(feaderBResult, label='Feeder B')
plt.xticks([0, 1, 2, 3], [100, 50, 25, 5])

plt.legend()
plt.savefig(f'./part2_result/food_a{time.time()}.png')
plt.close()
