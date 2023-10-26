from pyomo.environ import Constraint, RangeSet
from math import log
from functools import partial

class Constraints:
    components = ["Benzene", "Toluene", "OrthoXylene", "MetaXylene", "Ethylbenzene", "ParaXylene", "TwoMethylbutane"]
    
    def __init__(self, model, parameters=None):
        self.model = model
        if parameters:
            self.define_constraints(model, parameters)

    def define_constraints(self, model, parameters):
        
        # Check and delete existing components before redefining
        if hasattr(model, 'streams'):
            model.del_component(model.streams)
        model.streams = RangeSet(2, 8)
        
        model.composition_sum_constraint = Constraint(model.streams, rule=self.composition_sum_rule)
        
        
        # Add overall material balance constraints for streams S2 to S7
        for i in model.streams:  # For streams S2 to S7
            setattr(model, f'Eq0_S{i}', Constraint(expr=self.overall_material_balance(model, i)))

            
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

        for component in self.components:
            # Dynamically create constraint name based on the component
            for i in range(1, 11):
                rule_name = f'{component}_comp_rule{i}'
                if hasattr(self, rule_name):
                    constraints_mapping[rule_name] = getattr(self, rule_name)

        # Dynamically add each constraint to the model
        for constraint_name, rule_function in constraints_mapping.items():
            setattr(model, constraint_name, Constraint(rule=rule_function))
                
    # Overall Material Balance/
    def overall_material_balance(self, model, stream):
        return getattr(model, f'S{stream}') == sum(getattr(model, f's{stream}')[component] for component in self.components)

    # Physical condition 
    def component_molar_composition(self, model, stream, component):
        return model.x[stream, component] == getattr(model, f's{stream}')[component] / getattr(model, f'S{stream}')

    # Physical condition (composition within a stream should add up to 1)
    def composition_sum_rule(self, model, stream):
        return sum(model.x[stream, component] for component in self.components) == 1.0
    
    
    # Fractional Recovery Equations   
    def Eq1(self, model):
        return model.params['FR_S2_LK'] * model.params['S1'] * model.params['S1_Benzene'] == model.s2['Benzene']
    
    def Eq2(self, model):
        return (1 - model.params['FR_S2_LK']) * model.params['S1'] * model.params['S1_Benzene'] == model.s3['Benzene']
    
    def Eq3(self, model):
        return model.params['FR_S3_HK'] * model.params['S1'] * model.params['S1_Toluene'] == model.s3['Toluene']
    
    def Eq4(self, model):
        return (1 - model.params['FR_S3_HK']) * model.params['S1'] * model.params['S1_Toluene'] == model.s2['Toluene']
    
    def Eq5(self, model):
        return model.params['FR_S4_LK'] * model.s3['Toluene'] == model.s4['Toluene']
    
    def Eq6(self, model):
        return (1 - model.params['FR_S4_LK']) * model.s3['Toluene'] == model.s5['Toluene']
    
    def Eq7(self, model):
        return model.params['FR_S5_HK'] * model.s3['Ethylbenzene'] == model.s5['Ethylbenzene']
    
    def Eq8(self, model):
        return (1 - model.params['FR_S5_HK']) * model.s3['Ethylbenzene'] == model.s4['Ethylbenzene']
    
    def Eq9(self, model):
        return model.params['FR_S6_LK'] * model.s5['Ethylbenzene'] == model.s6['Ethylbenzene']
    
    def Eq10(self, model):
        return (1 - model.params['FR_S6_LK']) * model.s5['Ethylbenzene'] == model.s7['Ethylbenzene']
    
    def Eq11(self, model):
        return model.params['FR_S7_HK'] * model.s5['ParaXylene'] == model.s7['ParaXylene'] 
    
    def Eq12(self, model):
        return (1 - model.params['FR_S7_HK']) * model.s5['ParaXylene'] ==  model.s6['ParaXylene']


    
    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_Benzene'] ==  model.s2['Benzene'] + model.s3['Benzene']

    def Benzene_comp_rule2(self, model):
        return model.s3['Benzene'] ==  model.s4['Benzene']
    
    def Benzene_comp_rule3(self, model):
        return model.s5['Benzene'] == 0
    
    def Benzene_comp_rule4(self, model):
        return model.s6['Benzene'] == 0
    
    def Benzene_comp_rule5(self, model):
        return model.s7['Benzene'] == 0
    
    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_Toluene'] ==  model.s2['Toluene'] + model.s3['Toluene']
    
    def Toluene_comp_rule2(self, model):
        return model.s3['Toluene'] ==  model.s4['Toluene']  + model.s5['Toluene']
    
    def Toluene_comp_rule3(self, model):
        return model.s5['Toluene'] ==  model.s6['Toluene']

    def Toluene_zero_rule4(self, model):
        return model.s7['Toluene'] == 0

    
    # Ortho-Xylene (Individual Component material balance)
    def OrthoXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_OrthoXylene'] == model.s3['OrthoXylene']
    
    def OrthoXylene_comp_rule2(self, model):
        return model.s2['OrthoXylene'] == 0
    
    def OrthoXylene_comp_rule3(self, model):
        return model.s3['OrthoXylene'] == model.s5['OrthoXylene']
    
    def OrthoXylene_comp_rule4(self, model):
        return model.s4['OrthoXylene'] == 0

    def OrthoXylene_comp_rule5(self, model):
        return model.s5['OrthoXylene'] == model.s7['OrthoXylene']

    def OrthoXylene_comp_rule6(self, model):
        return model.s6['OrthoXylene'] == 0

    
    # Ethylbenzene (Individual Component material balance)
    def Ethylbenzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_Ethylbenzene'] == model.s3['Ethylbenzene']
    
    def Ethylbenzene_comp_rule2(self, model):
        return model.s3['Ethylbenzene']  == model.s4['Ethylbenzene'] + model.s5['Ethylbenzene']

    def Ethylbenzene_comp_rule3(self, model):
        return model.s5['Ethylbenzene']  == model.s6['Ethylbenzene']+ model.s7['Ethylbenzene']

    def Ethylbenzene_comp_rule4(self, model):
        return model.s2['Ethylbenzene'] == 0

    
    # MetaXylene (Individual Component material balance)
    def MetaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_MetaXylene'] == model.s3['MetaXylene']
    
    def MetaXylene_comp_rule2(self, model):
        return model.s2['MetaXylene'] == 0
    
    def MetaXylene_comp_rule3(self, model):
        return model.s3['MetaXylene'] == model.s5['MetaXylene']
    
    def MetaXylene_comp_rule4(self, model):
        return model.s4['MetaXylene'] == 0

    def MetaXylene_comp_rule5(self, model):
        return model.s5['MetaXylene'] == model.s7['MetaXylene']

    def MetaXylene_comp_rule6(self, model):
        return model.s6['MetaXylene'] == 0


    
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_ParaXylene'] == model.s3['ParaXylene']
    
    def ParaXylene_comp_rule2(self, model):
        return model.s2['ParaXylene'] == 0
    
    def ParaXylene_comp_rule3(self, model):
        return model.s3['ParaXylene']  ==  model.s5['ParaXylene']
    
    def ParaXylene_comp_rule4(self, model):
        return model.s4['ParaXylene'] == 0

    def ParaXylene_comp_rule5(self, model):
        return model.s5['ParaXylene']  == model.s6['ParaXylene'] + model.s7['ParaXylene']


    # TwoMethylbutane (Individual Component material balance)
    def TwoMethylbutane_comp_rule1(self, model):
        return model.s2['TwoMethylbutane'] == 0
    
    def TwoMethylbutane_comp_rule1(self, model):
        return model.s3['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule2(self, model):
        return model.s4['TwoMethylbutane'] == 0
        
    def TwoMethylbutane_comp_rule3(self, model):
        return model.s5['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule4(self, model):
        return model.s6['TwoMethylbutane'] == 0

    def TwoMethylbutane_comp_rule5(self, model):
        return model.s7['TwoMethylbutane'] == 0
