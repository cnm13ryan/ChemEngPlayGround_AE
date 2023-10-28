from pyomo.environ import Constraint, RangeSet
from math import log
from functools import partial

class Constraints:
    components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']

    def __init__(self, model, parameters=None):
        self.model = model
        if parameters:
            self.define_constraints(model, parameters)

    def define_constraints(self, model, parameters):
        
        # Check and delete existing components before redefining
        if hasattr(model, 'streams'):
            model.del_component(model.streams)
        model.streams = RangeSet(22, 34)
        
        model.composition_sum_constraint = Constraint(model.streams, rule=self.composition_sum_rule)
        
        
        # Add overall material balance constraints for streams S22 to S33
        for i in model.streams:  # For streams S22 to S33
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
            'Eq16': self.Eq16,            
            'selectivity_1_relation': self.selectivity_1_relation,
            'selectivity_2_relation': self.selectivity_2_relation,
            'conversion_1_def_rule': self.conversion_1_def_rule,
            'conversion_2_def_rule': self.conversion_2_def_rule
            
        }

        for component in self.components:
            # Dynamically create constraint name based on the component
            for i in range(1, 12):
                rule_name = f'{component}_comp_rule{i}'
                if hasattr(self, rule_name):
                    constraints_mapping[rule_name] = getattr(self, rule_name)

        # Dynamically add each constraint to the model
        for constraint_name, rule_function in constraints_mapping.items():
            setattr(model, constraint_name, Constraint(rule=rule_function))
                
                
    
    # Overall Material Balance
    def overall_material_balance(self, model, stream):
        if stream == 22:
            return model.aux_S22 == sum(getattr(model, f's{stream}')[component] for component in self.components)
        elif stream == 23:
            return model.aux_S23 == sum(getattr(model, f's{stream}')[component] for component in self.components)
        else:
            return getattr(model, f'S{stream}') == sum(getattr(model, f's{stream}')[component] for component in self.components)

    # Physical condition 
    def component_molar_composition(self, model, stream, component):
        return model.x[stream, component] == getattr(model, f's{stream}')[component] / getattr(model, f'S{stream}')

    # Physical condition (composition within a stream should add up to 1)
    def composition_sum_rule(self, model, stream):
        return sum(model.x[stream, component] for component in self.components) == 1.0

    
                
    # Fractional Recovery (HK/LK) Equations   
    
 
    def Eq1(self, model):
        return model.params['FR_S24_LK'] * model.aux_S22 * model.x[22, 'Hydrogen'] == model.s24['Hydrogen'] 

    def Eq2(self, model):
        return (1 - model.params['FR_S24_LK']) * model.aux_S22 * model.x[22, 'Hydrogen'] == model.aux_S23 * model.x[23, 'Hydrogen']

    def Eq3(self, model):
        return model.params['FR_S23_HK'] * model.aux_S22 * model.x[22, 'Methane'] == model.aux_S23 * model.x[23, 'Methane']

    def Eq4(self, model):
        return (1 - model.params['FR_S23_HK']) * model.aux_S22 * model.x[22, 'Methane'] == model.s24['Methane']

    def Eq5(self, model):
        return model.params['FR_S29_LK'] * model.s27['Cyclohexene'] == model.s29['Cyclohexene']
    
    def Eq6(self, model):
        return (1 - model.params['FR_S29_LK']) * model.s27['Cyclohexene']  == model.s28['Cyclohexene'] 
    
    def Eq7(self, model):
        return model.params['FR_S28_HK'] * model.s27['Cyclohexylbenzene'] == model.s28['Cyclohexylbenzene']
    
    def Eq8(self, model):
        return (1 - model.params['FR_S28_HK']) * model.s27['Cyclohexylbenzene'] == model.s29['Cyclohexylbenzene'] 
    
    def Eq9(self, model):
        return model.params['FR_S31_LK'] * model.s29['Cyclohexane']  == model.s31['Cyclohexane'] 
    
    def Eq10(self, model):
        return (1 - model.params['FR_S31_LK']) * model.s29['Cyclohexane']  == model.s30['Cyclohexane'] 
    
    def Eq11(self, model):
        return model.params['FR_S30_HK'] * model.s29['Cyclohexene']  == model.s30['Cyclohexene'] 
    
    def Eq12(self, model):
        return (1 - model.params['FR_S30_HK']) * model.s29['Cyclohexene']  == model.s31['Cyclohexene'] 

    def Eq13(self, model):
        return model.params['FR_S33_LK'] * model.s31['Benzene']  == model.s33['Benzene'] 
    
    def Eq14(self, model):
        return (1 - model.params['FR_S33_LK']) * model.s31['Benzene']  == model.s32['Benzene'] 
    
    def Eq15(self, model):
        return model.params['FR_S32_HK'] * model.s31['Cyclohexane']  == model.s32['Cyclohexane'] 
    
    def Eq16(self, model):
        return (1 - model.params['FR_S32_HK']) * model.s31['Cyclohexane']  == model.s33['Cyclohexane'] 
    
    
      
    # Selectivity S1 relation
    def selectivity_1_relation(self, model):
        return (model.zeta_1 + model.zeta_2) * model.params['S1'] == model.aux_S22 * model.x[22, 'Cyclohexene']
    
    # Selectivity S2 relation
    def selectivity_2_relation(self, model):
        return model.zeta_3 * model.params['S2'] == model.s27['Cyclohexylbenzene']
    
      
    # Conversion X1 Definition
    def conversion_1_def_rule(self, model):
        return model.params['X1'] * (model.params['S20'] * model.params['S20_Benzene'] + model.params['S21'] * model.params['S21_Benzene']) ==  model.zeta_1 + model.zeta_2 
    
    
    # Conversion X2 Definition
    def conversion_2_def_rule(self, model):
        return model.params['X2'] * model.aux_S23 * model.x[23, 'Cyclohexene'] ==  model.zeta_3
      
    
    # Hydrogen (Individual Component material balance)

    def Hydrogen_comp_rule1(self, model):
        return model.params['S21'] * model.params['S21_Hydrogen'] + model.params['S20'] * model.params['S20_Hydrogen'] + model.s33['Hydrogen'] + model.s25['Hydrogen'] == model.aux_S22 * model.x[22, 'Hydrogen'] + model.zeta_1 + model.zeta_2

    def Hydrogen_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Hydrogen'] == model.aux_S23 * model.x[23, 'Hydrogen'] + model.s24['Hydrogen']
    
    def Hydrogen_comp_rule3(self, model):
        return model.s24['Hydrogen']  ==  model.s25['Hydrogen'] + model.s26['Hydrogen']   
    
    def Hydrogen_comp_rule4(self, model): # Assume it is in trace such that it does not react with other components
        return model.aux_S23 * model.x[23, 'Hydrogen']  ==  model.s27['Hydrogen'] 
    
    def Hydrogen_comp_rule5(self, model): # Assume it is in trace such that it does not react with other components
        return model.s27['Hydrogen']  ==  model.s29['Hydrogen'] 
  
    def Hydrogen_comp_rule6(self, model): # Assume it is in trace such that it does not react with other components
        return model.s29['Hydrogen']  ==  model.s31['Hydrogen'] 

    def Hydrogen_comp_rule7(self, model): # Assume it is in trace such that it does not react with other components
        return model.s31['Hydrogen']  ==  model.s33['Hydrogen']   
    
    def Hydrogen_comp_rule8(self, model):
        return model.s28['Hydrogen'] == 0
    
    def Hydrogen_comp_rule9(self, model):
        return model.s30['Hydrogen'] == 0
    
    def Hydrogen_comp_rule10(self, model):
        return model.s32['Hydrogen'] == 0
    
    def Hydrogen_comp_rule11(self, model): # Splitter fraction
        return model.s25['Hydrogen'] == 5 * model.s26['Hydrogen']    
    
       
    # Methane (Individual Component material balance)
    def Methane_comp_rule1(self, model):
        return model.params['S21'] * model.params['S21_Methane'] + model.params['S20'] * model.params['S20_Methane'] + model.s33['Methane'] + model.s25['Methane'] == model.aux_S22 * model.x[22, 'Methane']
    
    
    def Methane_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Methane']  ==  model.aux_S23 * model.x[23, 'Methane'] + model.s24['Methane']
    
    def Methane_comp_rule3(self, model):
        return model.s24['Methane']  ==  model.s25['Methane'] + model.s26['Methane']   
    
    def Methane_comp_rule4(self, model): # Assume it is in trace such that it does not react with other components
        return model.aux_S23 * model.x[23, 'Methane'] ==  model.s27['Methane'] 
    
    def Methane_comp_rule5(self, model): # Assume it is in trace such that it does not react with other components
        return model.s27['Methane']  ==  model.s29['Methane'] 
  
    def Methane_comp_rule6(self, model): # Assume it is in trace such that it does not react with other components
        return model.s29['Methane']  ==  model.s31['Methane'] 

    def Methane_comp_rule7(self, model): # Assume it is in trace such that it does not react with other components
        return model.s31['Methane']  ==  model.s33['Methane']   
    
    def Methane_comp_rule8(self, model):
        return model.s28['Methane'] == 0
    
    def Methane_comp_rule9(self, model):
        return model.s30['Methane'] == 0
    
    def Methane_comp_rule10(self, model):
        return model.s32['Methane'] == 0
    
    def Methane_comp_rule11(self, model): # Splitter fraction
        return model.s25['Methane'] == 5 * model.s26['Methane']      
    
    
    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S21'] * model.params['S21_Benzene'] + model.params['S20'] * model.params['S20_Benzene'] + model.s33['Benzene'] + model.s25['Benzene'] == model.aux_S22 * model.x[22, 'Benzene'] + model.zeta_1 + model.zeta_2
    
    def Benzene_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Benzene']  ==  model.aux_S23 * model.x[23, 'Benzene']
    
    def Benzene_comp_rule3(self, model):
        return model.aux_S23 * model.x[23, 'Benzene'] - model.zeta_3  ==  model.s27['Benzene'] 
    
    def Benzene_comp_rule4(self, model): 
        return model.s27['Benzene']  ==  model.s29['Benzene'] 
  
    def Benzene_comp_rule5(self, model): 
        return model.s29['Benzene']  ==  model.s31['Benzene'] 

    def Benzene_comp_rule6(self, model): 
        return model.s31['Benzene']  ==  model.s32['Benzene'] + model.s33['Benzene']  
    
    def Benzene_comp_rule7(self, model):
        return model.s28['Benzene'] == 0
    
    def Benzene_comp_rule8(self, model):
        return model.s30['Benzene'] == 0 
    
    
    # Cyclohexane (Individual Component material balance)
    def Cyclohexane_comp_rule1(self, model):
        return model.params['S21'] * model.params['S21_Cyclohexane'] + model.params['S20'] * model.params['S20_Cyclohexane'] + model.s33['Cyclohexane'] + model.s25['Cyclohexane'] == model.aux_S22 * model.x[22, 'Cyclohexane'] - model.zeta_2
        
    def Cyclohexane_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Cyclohexane']  ==  model.aux_S23 * model.x[23, 'Cyclohexane']
    
    def Cyclohexane_comp_rule3(self, model): # Assume it does not react here
        return model.aux_S23 * model.x[23, 'Cyclohexane']  ==  model.s27['Cyclohexane'] 
    
    def Cyclohexane_comp_rule4(self, model): 
        return model.s27['Cyclohexane']  ==  model.s29['Cyclohexane'] 
  
    def Cyclohexane_comp_rule5(self, model): 
        return model.s29['Cyclohexane']  ==  model.s30['Cyclohexane'] + model.s31['Cyclohexane'] 

    def Cyclohexane_comp_rule6(self, model): 
        return model.s31['Cyclohexane']  ==  model.s32['Cyclohexane'] + model.s33['Cyclohexane']  
    
    def Cyclohexane_comp_rule7(self, model):
        return model.s28['Cyclohexane'] == 0
      
    
    # Cyclohexene (Individual Component material balance)
    def Cyclohexene_comp_rule1(self, model):
        return model.params['S21'] * model.params['S21_Cyclohexene'] + model.params['S20'] * model.params['S20_Cyclohexene'] + model.s33['Cyclohexene'] + model.s25['Cyclohexene'] == model.aux_S22 * model.x[22, 'Cyclohexene'] - model.zeta_1
        
    def Cyclohexene_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Cyclohexene']  ==  model.aux_S23 * model.x[23, 'Cyclohexene']
    
    def Cyclohexene_comp_rule3(self, model): 
        return model.aux_S23 * model.x[23, 'Cyclohexene'] - model.zeta_3  ==  model.s27['Cyclohexene'] 
    
    def Cyclohexene_comp_rule4(self, model): 
        return model.s27['Cyclohexene']  ==  model.s29['Cyclohexene'] + model.s28['Cyclohexene'] 
  
    def Cyclohexene_comp_rule5(self, model): 
        return model.s29['Cyclohexene']  ==  model.s30['Cyclohexene'] + model.s31['Cyclohexene'] 

    def Cyclohexene_comp_rule6(self, model): 
        return model.s31['Cyclohexene']  ==  model.s32['Cyclohexene']
    
    def Cyclohexene_comp_rule7(self, model):
        return model.s33['Cyclohexene'] == 0
    

    # Cyclohexylbenzene (Individual Component material balance)
    
    def Cyclohexylbenzene_comp_rule1(self, model): # Assume Cyclohexylbenzene does not react here
        return model.params['S21'] * model.params['S21_Cyclohexylbenzene'] + model.params['S20'] * model.params['S20_Cyclohexylbenzene'] + model.s33['Cyclohexylbenzene'] + model.s25['Cyclohexylbenzene'] == model.aux_S22 * model.x[22, 'Cyclohexylbenzene']
        
    def Cyclohexylbenzene_comp_rule2(self, model):
        return model.aux_S22 * model.x[22, 'Cyclohexylbenzene']  ==  model.aux_S23 * model.x[23, 'Cyclohexylbenzene']
    
    def Cyclohexylbenzene_comp_rule3(self, model): 
        return model.aux_S23 * model.x[23, 'Cyclohexylbenzene'] + model.zeta_3  ==  model.s27['Cyclohexylbenzene'] 
    
    def Cyclohexylbenzene_comp_rule4(self, model): 
        return model.s27['Cyclohexylbenzene']  ==  model.s29['Cyclohexylbenzene'] + model.s28['Cyclohexylbenzene'] 
  
    def Cyclohexylbenzene_comp_rule5(self, model): 
        return model.s29['Cyclohexylbenzene']  ==  model.s30['Cyclohexylbenzene'] + model.s31['Cyclohexylbenzene'] 

    def Cyclohexylbenzene_comp_rule6(self, model): 
        return model.s31['Cyclohexylbenzene']  ==  model.s32['Cyclohexylbenzene']
    
    def Cyclohexylbenzene_comp_rule7(self, model):
        return model.s33['Cyclohexylbenzene'] == 0