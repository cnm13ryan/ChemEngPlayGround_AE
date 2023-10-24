from pyomo.environ import Constraint
from math import log

class Constraints:
    def __init__(self, model, parameters):
        self.define_constraints(model, parameters)
        self.add_composition_constraints(model)

    def define_constraints(self, model, parameters):
        # Map each constraint to its corresponding function
        constraints_mapping = {
            'FR_LK_d1': self.FR_LK_d1,
            'FR_HK_b1': self.FR_HK_b1,
            'FR_LK_d2': self.FR_LK_d2,
            'FR_HK_b2': self.FR_HK_b2,
            'FR_LK_d3': self.FR_LK_d3,
            'FR_HK_b3': self.FR_HK_b3,
            'matbal_rule1': self.matbal_rule1,
            'matbal_rule2': self.matbal_rule2,
            'matbal_rule3': self.matbal_rule3
        }

        components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']

        for component in components:
            # Dynamically create constraint name based on the component
            for i in range(1, 7):
                rule_name = f'{component}_comp_rule{i}'
                if rule_name in dir(self):
                    constraints_mapping[rule_name] = getattr(self, rule_name)

        # Dynamically add each constraint to the model
        for constraint_name, rule_function in constraints_mapping.items():
            setattr(model, constraint_name, Constraint(rule=rule_function))

    def add_composition_constraints(self, model):
        components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']

        for comp in ['b1', 'b2', 'b3', 'd1', 'd2', 'd3']:
            constraint_name = f'{comp}_sum_constraint'
            setattr(model, constraint_name, Constraint(expr=sum(getattr(model, comp)[component] for component in components) == 1))

          
    # Fractional Recoveries Equations    
    def FR_LK_d1(self, model):
        return model.params['FR_S2_LK'] * model.params['S1'] * model.params['z1_Benzene'] == model.d1['Benzene'] * model.S2
    
    def FR_HK_b1(self, model):
        return model.params['FR_S3_HK'] * model.params['S1'] * model.params['z1_Toluene'] == model.b1['Toluene'] * model.S3
    
    def FR_LK_d2(self, model):
        return model.params['FR_S4_LK'] * model.S3 * model.b1['Toluene'] - model.d2['Toluene'] * model.S4 == 0
    
    def FR_HK_b2(self, model):
        return model.params['FR_S5_HK'] * model.S3 * model.b1['Ethylbenzene'] - model.b2['Ethylbenzene'] * model.S5 == 0
    
    def FR_LK_d3(self, model):
        return model.params['FR_S6_LK'] * model.S5 * model.b2['Ethylbenzene'] - model.d3['Ethylbenzene'] * model.S6 == 0
    
    def FR_HK_b3(self, model):
        return model.params['FR_S7_HK'] * model.S5 * model.b2['ParaXylene'] - model.b3['ParaXylene'] * model.S7 == 0


    # Overall Material Balance
    def matbal_rule1(self, model):
        return model.params['S1'] == model.S2 + model.S3
    
    def matbal_rule2(self, model):
        return model.S3 == model.S4 + model.S5 
    
    def matbal_rule3(self, model):
        return model.S5 == model.S6 + model.S7 
    

    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Benzene'] ==  model.d1['Benzene'] * model.S2 + model.b1['Benzene'] * model.S3

    def Benzene_comp_rule2(self, model):
        return model.S3 * model.b1['Benzene'] ==  model.S4 * model.d2['Benzene']
    
#     def Benzene_comp_rule3(self, model):
#         return model.b2['Benzene'] == 0
    
#     def Benzene_comp_rule4(self, model):
#         return model.d3['Benzene'] == 0
    
#     def Benzene_comp_rule5(self, model):
#         return model.b3['Benzene'] == 0

    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Toluene'] ==  model.d1['Toluene'] * model.S2 + model.b1['Toluene'] * model.S3
    
    def Toluene_comp_rule2(self, model):
        return model.b1['Toluene'] * model.S3 ==  model.d2['Toluene'] * model.S4 + model.b2['Toluene'] * model.S5
    
    def Toluene_comp_rule3(self, model):
        return model.b2['Toluene'] * model.S5 ==  model.d3['Toluene'] * model.S6

    def Toluene_zero_rule4(self, model):
        return model.b3['Toluene'] == 0

    
    
    # Ortho-Xylene (Individual Component material balance)
    def OrthoXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_OrthoXylene'] == model.b1['OrthoXylene'] * model.S3
    
    def OrthoXylene_comp_rule2(self, model):
        return model.b1['OrthoXylene'] * model.S3 == model.b2['OrthoXylene'] * model.S5

    def OrthoXylene_comp_rule3(self, model):
        return model.b2['OrthoXylene'] * model.S5 == model.b3['OrthoXylene'] * model.S7
    
#     def OrthoXylene_comp_rule4(self, model):
#         return model.d1['OrthoXylene'] == 0

#     def OrthoXylene_comp_rule5(self, model):
#         return model.d2['OrthoXylene'] == 0

#     def OrthoXylene_comp_rule6(self, model):
#         return model.d3['OrthoXylene'] == 0

    
    # Ethylbenzene (Individual Component material balance)
    def Ethylbenzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Ethylbenzene'] == model.b1['Ethylbenzene'] * model.S3  
    
    def Ethylbenzene_comp_rule2(self, model):
        return model.b1['Ethylbenzene'] * model.S3  == model.d2['Ethylbenzene'] * model.S4 + model.b2['Ethylbenzene'] * model.S5

    def Ethylbenzene_comp_rule3(self, model):
        return model.b2['Ethylbenzene'] * model.S5  == model.d3['Ethylbenzene'] * model.S6 + model.b3['Ethylbenzene'] * model.S7

    def Ethylbenzene_comp_rule4(self, model):
        return model.d1['Ethylbenzene'] == 0

    
    # MetaXylene (Individual Component material balance)
    def MetaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_MetaXylene'] == model.b1['MetaXylene'] * model.S3
    
    def MetaXylene_comp_rule2(self, model):
        return model.b1['MetaXylene'] * model.S3 == model.b2['MetaXylene'] * model.S5

    def MetaXylene_comp_rule3(self, model):
        return model.b2['MetaXylene'] * model.S5 == model.b3['MetaXylene'] * model.S7
    
#     def MetaXylene_comp_rule4(self, model):
#         return model.d1['MetaXylene'] == 0

#     def MetaXylene_comp_rule5(self, model):
#         return model.d2['MetaXylene'] == 0

#     def MetaXylene_comp_rule6(self, model):
#         return model.d3['MetaXylene'] == 0


    
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_ParaXylene'] == model.b1['ParaXylene'] * model.S3  
    
    def ParaXylene_comp_rule2(self, model):
        return model.b1['ParaXylene'] * model.S3  ==  model.b2['ParaXylene'] * model.S5

    def ParaXylene_comp_rule3(self, model):
        return model.b2['ParaXylene'] * model.S5  == model.d3['ParaXylene'] * model.S6 + model.b3['ParaXylene'] * model.S7

#     def ParaXylene_comp_rule4(self, model):
#         return model.d1['ParaXylene'] == 0

#     def ParaXylene_comp_rule5(self, model):
#         return model.d2['ParaXylene'] == 0

    # TwoMethylbutane (Individual Component material balance)
    def TwoMethylbutane_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_TwoMethylbutane'] == model.d1['TwoMethylbutane'] * model.S2
    
#     def TwoMethylbutane_comp_rule2(self, model):
#         return model.b1['TwoMethylbutane'] == 0

#     def TwoMethylbutane_comp_rule3(self, model):
#         return model.d2['TwoMethylbutane'] == 0
        
#     def TwoMethylbutane_comp_rule4(self, model):
#         return model.b2['TwoMethylbutane'] == 0

#     def TwoMethylbutane_comp_rule5(self, model):
#         return model.d3['TwoMethylbutane'] == 0

#     def TwoMethylbutane_comp_rule6(self, model):
#         return model.b3['TwoMethylbutane'] == 0

    
    def add_composition_constraints(self, model):
        components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']

        # Ensure total composition for b1 is 1
        model.b1_sum_constraint = Constraint(expr=sum(model.b1[component] for component in components) == 1)
        
        # Ensure total composition for b2 is 1
        model.b2_sum_constraint = Constraint(expr=sum(model.b2[component] for component in components) == 1)
        
        # Ensure total composition for b3 is 1
        model.b3_sum_constraint = Constraint(expr=sum(model.b3[component] for component in components) == 1)
        
        # Ensure total composition for d1 is 1
        model.d1_sum_constraint = Constraint(expr=sum(model.d1[component] for component in components) == 1)

        # Ensure total composition for d2 is 1
        model.d2_sum_constraint = Constraint(expr=sum(model.d2[component] for component in components) == 1)

        # Ensure total composition for d3 is 1
        model.d3_sum_constraint = Constraint(expr=sum(model.d3[component] for component in components) == 1)
