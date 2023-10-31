from pyomo.environ import Var, NonNegativeReals, RangeSet

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):
        
        # Define a set for the streams
        model.streams = RangeSet(19, 39)

        for i in model.streams:
            # Overall Stream molar flow rates
            setattr(model, f'S{i}', Var(within=NonNegativeReals, initialize=5))

            # Individual component stream flow rates
            setattr(model, f's{i}', Var(components, within=NonNegativeReals, initialize=5))

        # Individual component molar composition for all streams
        model.x = Var(model.streams, components, within=NonNegativeReals, bounds=[0, 1])
   
        # Extents of Reaction
        model.zeta_1 = Var(within=NonNegativeReals, doc='Extent of reaction R1')
        model.zeta_2 = Var(within=NonNegativeReals, doc='Extent of reaction R2')
        model.zeta_3 = Var(within=NonNegativeReals, doc='Extent of reaction R3')
        
        