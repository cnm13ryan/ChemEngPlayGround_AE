from pyomo.environ import Var, NonNegativeReals, RangeSet

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):

        # Define a set for the streams
        model.streams = RangeSet(10, 18)

        for i in model.streams:
            # Overall Stream molar flow rates
            setattr(model, f'S{i}', Var(within=NonNegativeReals, initialize=200))

            # Individual component stream flow rates
            setattr(model, f's{i}', Var(components, within=NonNegativeReals, initialize=10.0))

        # Individual component molar composition for all streams
        model.x = Var(model.streams, components, within=NonNegativeReals, bounds=[0, 1])
   
        # Extents of Reaction
        model.zeta_1 = Var(within=NonNegativeReals)
        model.zeta_2 = Var(within=NonNegativeReals)
        
        # Selectivity of Benzene
        model.S = Var(within=NonNegativeReals)
        
        # Conversion of Toluene
        model.X = Var(within=NonNegativeReals, bounds=[0, 1], initialize=0.4)
        
#         model.S8 = Var(within=NonNegativeReals, initialize=200)
