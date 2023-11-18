from pyomo.environ import Constraint, RangeSet
from math import log
from functools import partial

class Constraints:
    components = ["Benzene", "Toluene", "OrthoXylene", "MetaXylene", "ParaXylene"]
    
    def __init__(self, model, parameters=None):
        self.model = model
        if parameters:
            self.define_constraints(model, parameters)

    def define_constraints(self, model, parameters):
        
        # Check and delete existing components before redefining
        if hasattr(model, 'streams'):
            model.del_component(model.streams)
        model.streams = RangeSet(2, 11)
        
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
            'Eq12': self.Eq12,
            'Eq13': self.Eq13,
            'Eq14': self.Eq14,
            'Eq15': self.Eq15,
            'Eq16': self.Eq16           
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
    
    # D1
    def Eq1(self, model):
        return model.params['FR_S2_LK'] * model.params['S1'] * model.params['S1_Benzene'] == model.s2['Benzene']
    
    def Eq2(self, model):
        return (1 - model.params['FR_S2_LK']) * model.params['S1'] * model.params['S1_Benzene'] == model.s3['Benzene']
    
    def Eq3(self, model):
        return model.params['FR_S3_HK'] * model.params['S1'] * model.params['S1_Toluene'] == model.s3['Toluene']
    
    def Eq4(self, model):
        return (1 - model.params['FR_S3_HK']) * model.params['S1'] * model.params['S1_Toluene'] == model.s2['Toluene']
    
    # D2
    def Eq5(self, model):
        return model.params['FR_S4_LK'] * model.s3['Toluene'] == model.s4['Toluene']
    
    def Eq6(self, model):
        return (1 - model.params['FR_S4_LK']) * model.s3['Toluene'] == model.s5['Toluene']
    
    def Eq7(self, model):
        return model.params['FR_S5_HK'] * model.s3['ParaXylene'] == model.s5['ParaXylene']
    
    def Eq8(self, model):
        return (1 - model.params['FR_S5_HK']) * model.s3['ParaXylene'] == model.s4['ParaXylene']
    
    # D3
    def Eq9(self, model):
        return model.params['FR_S6_LK'] * model.s5['Toluene'] == model.s6['Toluene']
    
    def Eq10(self, model):
        return (1 - model.params['FR_S6_LK']) * model.s5['Toluene'] == model.s7['Toluene']
    
    def Eq11(self, model):
        return model.params['FR_S7_HK'] * model.s5['ParaXylene'] == model.s7['ParaXylene'] 
    
    def Eq12(self, model):
        return (1 - model.params['FR_S7_HK']) * model.s5['ParaXylene'] ==  model.s6['ParaXylene']
    
    # D4
    def Eq13(self, model):
        return model.params['FR_S9_LK'] * model.s8['Toluene'] == model.s9['Toluene']
    
    def Eq14(self, model):
        return (1 - model.params['FR_S9_LK']) * model.s8['Toluene'] == model.s10['Toluene']
    
    def Eq15(self, model):
        return model.params['FR_S10_HK'] * model.s8['ParaXylene'] == model.s10['ParaXylene'] 
    
    def Eq16(self, model):
        return (1 - model.params['FR_S10_HK']) * model.s8['ParaXylene'] ==  model.s9['ParaXylene']



    
    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_Benzene'] ==  model.s2['Benzene'] + model.s3['Benzene']

    def Benzene_comp_rule2(self, model):
        return model.s3['Benzene'] ==  model.s4['Benzene'] + model.s5['Benzene']
    
    def Benzene_comp_rule3(self, model):
        return model.s5['Benzene'] == model.s6['Benzene'] + model.s7['Benzene']
    
    def Benzene_comp_rule4(self, model):
        return model.s8['Benzene']  == model.s4['Benzene'] + model.s6['Benzene']
    
    def Benzene_comp_rule5(self, model):
        return model.s8['Benzene']  == model.s9['Benzene'] + model.s10['Benzene']
    
    def Benzene_comp_rule6(self, model):
        return model.s5['Benzene'] + model.s6['Benzene'] + model.s7['Benzene'] + model.s10['Benzene'] == 0
    
    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_Toluene'] ==  model.s2['Toluene'] + model.s3['Toluene']
    
    def Toluene_comp_rule2(self, model):
        return model.s3['Toluene'] ==  model.s4['Toluene']  + model.s5['Toluene']
    
    def Toluene_comp_rule3(self, model):
        return model.s5['Toluene'] == model.s6['Toluene'] + model.s7['Toluene']

    def Toluene_zero_rule4(self, model):
        return model.s8['Toluene'] == model.s4['Toluene'] + model.s6['Toluene']
    
    def Toluene_zero_rule5(self, model):
        return model.s8['Toluene'] == model.s9['Toluene'] + model.s10['Toluene']
    
    
    # Ortho-Xylene (Individual Component material balance)
    def OrthoXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_OrthoXylene'] == model.s3['OrthoXylene'] + model.s2['OrthoXylene']
    
    def OrthoXylene_comp_rule2(self, model):
        return model.s2['OrthoXylene'] + model.s4['OrthoXylene'] + model.s6['OrthoXylene'] + model.s8['OrthoXylene'] + model.s9['OrthoXylene'] + model.s10['OrthoXylene']== 0
    
    def OrthoXylene_comp_rule3(self, model):
        return model.s3['OrthoXylene'] == model.s4['OrthoXylene'] + model.s5['OrthoXylene']

    def OrthoXylene_comp_rule4(self, model):
        return model.s5['OrthoXylene'] == model.s6['OrthoXylene'] + model.s7['OrthoXylene']
    
    def OrthoXylene_comp_rule5(self, model):
        return model.s8['OrthoXylene'] == model.s4['OrthoXylene'] + model.s6['OrthoXylene']
    
    def OrthoXylene_comp_rule6(self, model):
        return model.s8['OrthoXylene'] == model.s9['OrthoXylene'] + model.s10['OrthoXylene']
    
    
    # MetaXylene (Individual Component material balance)
    def MetaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_MetaXylene'] == model.s3['MetaXylene'] + model.s2['MetaXylene']
    
    def MetaXylene_comp_rule2(self, model):
        return model.s2['MetaXylene'] + model.s4['MetaXylene'] + model.s6['MetaXylene'] + model.s8['MetaXylene'] + model.s9['MetaXylene'] + model.s10['MetaXylene']== 0
    
    def MetaXylene_comp_rule3(self, model):
        return model.s3['MetaXylene'] == model.s5['MetaXylene'] + model.s4['MetaXylene']

    def MetaXylene_comp_rule4(self, model):
        return model.s5['MetaXylene'] == model.s7['MetaXylene'] + model.s6['MetaXylene']
    
    def MetaXylene_comp_rule5(self, model):
        return model.s8['MetaXylene'] == model.s4['MetaXylene'] + model.s6['MetaXylene']
    
    def MetaXylene_comp_rule6(self, model):
        return model.s8['MetaXylene'] == model.s9['MetaXylene'] + model.s10['MetaXylene']

    
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['S1_ParaXylene'] == model.s3['ParaXylene'] + model.s2['ParaXylene']
    
    def ParaXylene_comp_rule2(self, model):
        return model.s2['ParaXylene'] == 0
    
    def ParaXylene_comp_rule3(self, model):
        return model.s3['ParaXylene']  ==  model.s4['ParaXylene'] + model.s5['ParaXylene']

    def ParaXylene_comp_rule4(self, model):
        return model.s8['ParaXylene']  == model.s4['ParaXylene'] + model.s6['ParaXylene']
    
    def ParaXylene_comp_rule5(self, model):
        return model.s5['ParaXylene']  == model.s6['ParaXylene'] + model.s7['ParaXylene']
    
    def ParaXylene_comp_rule6(self, model):
        return model.s8['ParaXylene']  == model.s9['ParaXylene'] + model.s10['ParaXylene']    
