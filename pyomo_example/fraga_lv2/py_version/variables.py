from pyomo.environ import Var, PositiveReals, NonNegativeReals

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):
        model.S = Var(within=PositiveReals, initialize=0.2)  # selectivity of EB to DEB
        model.x = Var(within=PositiveReals, initialize=0.2)  # Single pass conversion of EB to DEB
        model.F1 = Var(within=PositiveReals, initialize=parameters['PD'])  # feed 1 flow (Pure E) [kmol per h]
        model.F2 = Var(within=PositiveReals, initialize=parameters['PD'])  # feed 2 flow (Bz and Tu) [kmol per h]
        model.PG = Var(within=PositiveReals, initialize=0.2)  # purge gas stream flow [kmol per h]
        model.BPD = Var(within=PositiveReals, initialize=0.2)  # byproduct stream flow [kmol per h]
        model.xi1 = Var(within=PositiveReals, initialize=0.2)  # first extent of reaction [kmol per h]
        model.xi2 = Var(within=PositiveReals, initialize=0.2)  # second extent of reaction [kmol per h]
        model.xi3 = Var(within=PositiveReals, initialize=0.2)  # third extent of reaction [kmol per h]
        model.yPBz = Var(within=PositiveReals, initialize=0.2)  # Bz molar composition in recycle & purge
        model.F = Var(within=PositiveReals, initialize=0.2)  # feed amount [kmol per h]
        model.z = Var(components, within=NonNegativeReals)  # Feed molar composition

