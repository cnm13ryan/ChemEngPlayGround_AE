from pyomo.environ import Var, PositiveReals, NonNegativeReals

class Variables:
    def __init__(self, model, components, parameters):
        self.define_variables(model, components, parameters)

    def define_variables(self, model, components, parameters):
        
        initial_value = 0.0001
        
        model.S2 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 2 molar flow rate  [kmol per h]
        model.S3 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 3 molar flow rate  [kmol per h]
        model.S4 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 4 molar flow rate  [kmol per h]
        model.S5 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 5 molar flow rate  [kmol per h]
        model.S6 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 6 molar flow rate  [kmol per h]
        model.S7 = Var(within=PositiveReals, initialize=parameters['S1'])  # Stream 7 molar flow rate  [kmol per h]
        
        model.z = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of Feed
        model.d1 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S2 (Distillate 1)
        model.d2 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S4 (Distillate 2)
        model.d3 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S6 (Distillate 3)
       
        model.b1 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S3 (Bottom 1)
        model.b2 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S5 (Bottom 2)
        model.b3 = Var(components, within=NonNegativeReals, bounds=(0, 1), initialize=initial_value) # molar composition of S7 (Bottom 3)
        
        
       