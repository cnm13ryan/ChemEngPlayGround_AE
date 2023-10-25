from pyomo.environ import Constraint
from math import log

class Constraints:
    components = ["Benzene", "Toluene", "OrthoXylene", "MetaXylene", "Ethylbenzene", "ParaXylene", "TwoMethylbutane"]

    def __init__(self, model, parameters=None):
        self.model = model
        if parameters:
            self.define_constraints(model, parameters)
        self.generate_all_constraints()

    def generate_all_constraints(self):
        for component in self.components:
            self.material_balance_rule1(component)
            self.material_balance_rule2(component)
            self.material_balance_rule3(component)

    def material_balance_rule1(self, component):
        def rule(model):
            return getattr(model, f'{component}_S1') == getattr(model, f'{component}_S2') + getattr(model, f'{component}_S3')

        # Adding the constraint to the model
        setattr(self.model, f'{component}_rule1_constraint', self.model.Constraint(rule=rule))

    def material_balance_rule2(self, component):
        def rule(model):
            return getattr(model, f'{component}_S3') == getattr(model, f'{component}_S4') + getattr(model, f'{component}_S5')

        # Adding the constraint to the model
        setattr(self.model, f'{component}_rule2_constraint', self.model.Constraint(rule=rule))

    def material_balance_rule3(self, component):
        def rule(model):
            return getattr(model, f'{component}_S5') == getattr(model, f'{component}_S6') + getattr(model, f'{component}_S7')

        # Adding the constraint to the model
        setattr(self.model, f'{component}_rule3_constraint', self.model.Constraint(rule=rule))


    def define_constraints(self, model, parameters):
        # Map each constraint to its corresponding function
        constraints_mapping = {
            'Eq1': self.Eq1,
            'Eq2': self.Eq2,
            'Eq3': self.Eq3,
            'Eq4': self.Eq4,
            'Eq5': self.Eq5,
            'Eq6': self.Eq6,
            'Eq7': self.Eq7,
            'Eq8': self.Eq8,
            'Eq9': self.Eq9,
            'Eq10': self.Eq10,  
            'Eq11': self.Eq11,
            'Eq12': self.Eq12
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

          
    # Equations   
    def Eq1(self, model):
        return model.params['FR_S2_LK'] * model.params['S1'] * model.params['z1_Benzene'] - model.d1['Benzene'] * model.S2 == 0
    
    def Eq2(self, model):
        return (1 - model.params['FR_S2_LK']) * model.params['S1'] * model.params['z1_Benzene'] - model.b1['Benzene'] * model.S3 == 0
    
    def Eq3(self, model):
        return model.params['FR_S3_HK'] * model.params['S1'] * model.params['z1_Toluene'] == model.b1['Toluene'] * model.S3
    
    def Eq4(self, model):
        return (1 - model.params['FR_S3_HK']) * model.params['S1'] * model.params['z1_Toluene'] == model.d1['Toluene'] * model.S2
    
    def Eq5(self, model):
        return model.params['FR_S4_LK'] * model.S3 * model.b1['Toluene'] - model.d2['Toluene'] * model.S4 == 0
    
    def Eq6(self, model):
        return (1 - model.params['FR_S4_LK']) * model.S3 * model.b1['Toluene'] - model.b2['Toluene'] * model.S5 == 0
    
    def Eq7(self, model):
        return model.params['FR_S5_HK'] * model.S3 * model.b1['Ethylbenzene'] - model.b2['Ethylbenzene'] * model.S5 == 0
    
    def Eq8(self, model):
        return (1 - model.params['FR_S5_HK']) * model.S3 * model.b1['Ethylbenzene'] - model.d2['Ethylbenzene'] * model.S5 == 0
    
    def Eq9(self, model):
        return model.params['FR_S6_LK'] * model.S5 * model.b2['Ethylbenzene'] - model.d3['Ethylbenzene'] * model.S6 == 0
    
    def Eq10(self, model):
        return (1 - model.params['FR_S6_LK']) * model.S5 * model.b2['Ethylbenzene'] - model.b3['Ethylbenzene'] * model.S7 == 0
    
    def Eq11(self, model):
        return model.params['FR_S7_HK'] * model.S5 * model.b2['ParaXylene'] - model.b3['ParaXylene'] * model.S7 == 0
    
    def Eq12(self, model):
        return (1 - model.params['FR_S7_HK']) * model.S5 * model.b2['ParaXylene'] - model.d3['ParaXylene'] * model.S6 == 0


    
    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Benzene'] ==  model.d1['Benzene'] * model.S2 + model.b1['Benzene'] * model.S3

    def Benzene_comp_rule2(self, model):
        return model.S3 * model.b1['Benzene'] ==  model.S4 * model.d2['Benzene']
    
    def Benzene_comp_rule3(self, model):
        return model.b2['Benzene'] == 0
    
    def Benzene_comp_rule4(self, model):
        return model.d3['Benzene'] == 0
    
    def Benzene_comp_rule5(self, model):
        return model.b3['Benzene'] == 0
    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Toluene'] ==  model.d1['Toluene'] * model.S2 + model.b1['Toluene'] * model.S3
    
    def Toluene_comp_rule2(self, model):
        return model.S3 * model.b1['Toluene']  ==  model.S4 * model.d2['Toluene']  + model.S5 * model.b2['Toluene']
    
    def Toluene_comp_rule3(self, model):
        return model.b2['Toluene'] * model.S5 ==  model.S6 * model.d3['Toluene']

    def Toluene_zero_rule4(self, model):
        return model.b3['Toluene'] == 0

    
    
    # Ortho-Xylene (Individual Component material balance)
    def OrthoXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_OrthoXylene'] == model.b1['OrthoXylene'] * model.S3
    
    def OrthoXylene_comp_rule2(self, model):
        return model.d1['OrthoXylene'] == 0
    
    def OrthoXylene_comp_rule3(self, model):
        return model.b1['OrthoXylene'] * model.S3 == model.b2['OrthoXylene'] * model.S5
    
    def OrthoXylene_comp_rule4(self, model):
        return model.d2['OrthoXylene'] == 0

    def OrthoXylene_comp_rule5(self, model):
        return model.b2['OrthoXylene'] * model.S5 == model.b3['OrthoXylene'] * model.S7

    def OrthoXylene_comp_rule6(self, model):
        return model.d3['OrthoXylene'] == 0

    
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
        return model.d1['MetaXylene'] == 0
    
    def MetaXylene_comp_rule3(self, model):
        return model.b1['MetaXylene'] * model.S3 == model.b2['MetaXylene'] * model.S5
    
    def MetaXylene_comp_rule4(self, model):
        return model.d2['MetaXylene'] == 0

    def MetaXylene_comp_rule5(self, model):
        return model.b2['MetaXylene'] * model.S5 == model.b3['MetaXylene'] * model.S7

    def MetaXylene_comp_rule6(self, model):
        return model.d3['MetaXylene'] == 0


    
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_ParaXylene'] == model.b1['ParaXylene'] * model.S3 
    
    def ParaXylene_comp_rule2(self, model):
        return model.d1['ParaXylene'] == 0
    
    def ParaXylene_comp_rule3(self, model):
        return model.b1['ParaXylene'] * model.S3  ==  model.b2['ParaXylene'] * model.S5
    
    def ParaXylene_comp_rule4(self, model):
        return model.d2['ParaXylene'] == 0

    def ParaXylene_comp_rule5(self, model):
        return model.b2['ParaXylene'] * model.S5  == model.d3['ParaXylene'] * model.S6 + model.b3['ParaXylene'] * model.S7


    # TwoMethylbutane (Individual Component material balance)
    def TwoMethylbutane_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_TwoMethylbutane'] == model.d1['TwoMethylbutane'] * model.S2
    
    def TwoMethylbutane_comp_rule1(self, model):
        return model.b1['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule2(self, model):
        return model.d2['TwoMethylbutane'] == 0
        
    def TwoMethylbutane_comp_rule3(self, model):
        return model.b2['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule4(self, model):
        return model.d3['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule5(self, model):
        return model.b3['TwoMethylbutane'] == 0
