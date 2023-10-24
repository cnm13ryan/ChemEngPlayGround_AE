from pyomo.environ import Var, PositiveReals, NonNegativeReals

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):

        initial_value = 0.00001

        # Stream variables
        for i in range(2, 8):  # Streams from S2 to S7
            setattr(model, f'S{i}', Var(within=PositiveReals, initialize=parameters['S1']))

        # molar composition of Feed
        model.z = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value)

        # molar compositions for Distillate and Bottom streams
        for i in range(1, 4):  # 3 sets of Distillate and Bottom streams
            setattr(model, f'd{i}', Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value))
            setattr(model, f'b{i}', Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value))

