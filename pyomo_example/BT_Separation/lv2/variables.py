from pyomo.environ import Var, NonNegativeReals, RangeSet

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):
        initial_value = 0.00001

        # Define a set for the streams (10 streams only)
        model.streams = RangeSet(2, 11)

        for i in model.streams:
            # Overall Stream molar flow rates
            setattr(model, f'S{i}', Var(within=NonNegativeReals, initialize=1000))

            # Individual component stream flow rates
            setattr(model, f's{i}', Var(components, within=NonNegativeReals, initialize=initial_value))

        # Individual component molar composition for all streams
        model.x = Var(model.streams, components, within=NonNegativeReals, bounds=[0, 1])
