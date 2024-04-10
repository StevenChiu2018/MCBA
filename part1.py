from ABM import ABM, Ant, Feader, Nature, Nest, Position
from env import ENV

ENV.load_env()

feader_a = Feader(position=Position(10, 40), discover_possibility=ENV.get('ALPHA_A'),
                  attrition_possibility=ENV.get('LAMBDA_A'), recuitment_possibility=ENV.get('BETA_A'), unit=100)
feader_b = Feader(position=Position(40, 40), discover_possibility=ENV.get('ALPHA_B'),
                  attrition_possibility=ENV.get('LAMBDA_B'), recuitment_possibility=ENV.get('BETA_B'), unit=100)
feaders = [feader_a, feader_b]

nest = Nest(position=Position(25, 5))
nature = Nature(feaders=feaders, nest=nest)

ants = [Ant(initial_position=Position(25, 5), nature=nature)
        for _ in range(100)]

abm = ABM(ants=ants, feaders=feaders, nest=nest)

result = abm.execute()

print(result)
