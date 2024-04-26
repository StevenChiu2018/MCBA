from ABM import ABM, Ant, Feader, Nature, Nest, Position, Status
from env import ENV

ENV.load_env()

# time_steps_list = []

# for round in range(50):
#     print(f'{round} round', end='\r')
#     feader_a = Feader(name='Feader_A', position=Position(10, 40), discover_possibility=ENV.get('ALPHA_A'),
#                       attrition_possibility=ENV.get('LAMBDA_A'), recuitment_possibility=ENV.get('BETA_A'), unit=100)
#     feader_b = Feader(name='Feader_B', position=Position(40, 40), discover_possibility=ENV.get('ALPHA_B'),
#                       attrition_possibility=ENV.get('LAMBDA_B'), recuitment_possibility=ENV.get('BETA_B'), unit=100)
#     feaders = [feader_a, feader_b]

#     nest = Nest(position=Position(25, 5))
#     nature = Nature(feaders=feaders, nest=nest)

#     ants = [Ant(initial_position=Position(25, 5), nature=nature)
#             for _ in range(100)]

#     abm = ABM(ants=ants, feaders=feaders, nest=nest, need_report=False)

#     time_steps = abm.execute()
#     time_steps_list.append(time_steps)

# print("")
# print("restriction")
# print(sum(time_steps_list) / 50)
# print(max(time_steps_list))
# print(min(time_steps_list))
# print(abm.statistic.first_commit)


feader_a = Feader(name='Feader_A', position=Position(10, 40), discover_possibility=ENV.get('ALPHA_A'),
                  attrition_possibility=ENV.get('LAMBDA_A'), recuitment_possibility=ENV.get('BETA_A'), unit=100)
feader_b = Feader(name='Feader_B', position=Position(40, 40), discover_possibility=ENV.get('ALPHA_B'),
                  attrition_possibility=ENV.get('LAMBDA_B'), recuitment_possibility=ENV.get('BETA_B'), unit=100)
feaders = [feader_a, feader_b]

nest = Nest(position=Position(25, 5))
nature = Nature(feaders=feaders, nest=nest)

ants = [Ant(initial_position=Position(25, 5), nature=nature)
        for _ in range(100)]

abm = ABM(ants=ants, feaders=feaders, nest=nest, need_report=False)

abm.execute()

abm.statistic.draw_status_line_graph()
