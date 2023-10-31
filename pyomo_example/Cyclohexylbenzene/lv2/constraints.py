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
        model.streams = RangeSet(20, 39)
        
        model.composition_sum_constraint = Constraint(model.streams, rule=self.composition_sum_rule)
        
        
        # Add overall material balance constraints for streams S19 to S41
        for i in model.streams:  # For streams S19 to S41
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
            'Eq17': self.Eq17,
            'Eq18': self.Eq18,
            'Eq19': self.Eq19,
            'Eq20': self.Eq20,
            
            'selectivity_1_relation': self.selectivity_1_relation,
            'selectivity_2_relation': self.selectivity_2_relation,
            'conversion_1_def_rule': self.conversion_1_def_rule,
            'conversion_2_def_rule': self.conversion_2_def_rule
            
        }

        for component in self.components:
            # Dynamically create constraint name based on the component
            for i in range(1, 14):
                rule_name = f'{component}_comp_rule{i}'
                if hasattr(self, rule_name):
                    constraints_mapping[rule_name] = getattr(self, rule_name)

        # Dynamically add each constraint to the model
        for constraint_name, rule_function in constraints_mapping.items():
            setattr(model, constraint_name, Constraint(rule=rule_function))
                
                
    
    # Overall Material Balance
    def overall_material_balance(self, model, stream):
        return getattr(model, f'S{stream}') == sum(getattr(model, f's{stream}')[component] for component in self.components)

    # Physical condition 
    def component_molar_composition(self, model, stream, component):
        return model.x[stream, component] == getattr(model, f's{stream}')[component] / getattr(model, f'S{stream}')

    # Physical condition (composition within a stream should add up to 1)
    def composition_sum_rule(self, model, stream):
        return sum(model.x[stream, component] for component in self.components) == 1.0
    
              
    # Fractional recoveries of HK/LK (Distillation Column 7)    
    def Eq1(self, model):
        return model.params['FR_S19_LK'] * model.params['S15'] * model.params['S15_Methane'] == model.s19['Methane'] 

    def Eq2(self, model):
        return (1 - model.params['FR_S19_LK']) * model.params['S15'] * model.params['S15_Methane'] == model.s20['Methane'] 
    
    def Eq3(self, model):
        return model.params['FR_S20_HK'] * model.params['S15'] * model.params['S15_Benzene'] == model.s20['Benzene'] 

    def Eq4(self, model):
        return (1 - model.params['FR_S20_HK']) * model.params['S15'] * model.params['S15_Benzene'] == model.s19['Benzene'] 
        
        
    # Fractional recoveries of HK/LK (Distillation Column 8)       
    def Eq5(self, model):
        return model.params['FR_S25_LK'] * model.s24['Hydrogen']  == model.s25['Hydrogen'] 
    
    def Eq6(self, model):
        return (1 - model.params['FR_S25_LK']) * model.s24['Hydrogen']  == model.s29['Hydrogen'] 
    
    def Eq7(self, model):
        return model.params['FR_S29_HK'] * model.s24['Methane']  == model.s29['Methane'] 
    
    def Eq8(self, model):
        return (1 - model.params['FR_S29_HK']) * model.s24['Methane']  == model.s25['Methane'] 
    
    
    # Fractional recoveries of HK/LK (Distillation Column 9)  
    def Eq9(self, model):
        return model.params['FR_S32_LK'] * model.s31['Cyclohexene']  == model.s32['Cyclohexene'] 
    
    def Eq10(self, model):
        return (1 - model.params['FR_S32_LK']) * model.s31['Cyclohexene']  == model.s33['Cyclohexene'] 
    
    def Eq11(self, model):
        return model.params['FR_S33_HK'] * model.s31['Cyclohexylbenzene']  == model.s33['Cyclohexylbenzene'] 
    
    def Eq12(self, model):
        return (1 - model.params['FR_S33_HK']) * model.s31['Cyclohexylbenzene']  == model.s32['Cyclohexylbenzene'] 

    
    # Fractional recoveries of HK/LK (Distillation Column 10)   
    def Eq13(self, model):
        return model.params['FR_S34_LK'] * model.s31['Cyclohexane']  == model.s34['Cyclohexane'] 
    
    def Eq14(self, model):
        return (1 - model.params['FR_S34_LK']) * model.s31['Cyclohexane']  == model.s35['Cyclohexane']   

    def Eq15(self, model):
        return model.params['FR_S35_HK'] * model.s31['Cyclohexene']  == model.s35['Cyclohexene'] 
    
    def Eq16(self, model):
        return (1 - model.params['FR_S35_HK']) * model.s31['Cyclohexene']  == model.s34['Cyclohexene']  
    
    
    # Fractional recoveries of HK/LK (Distillation Column 11)
    def Eq17(self, model):
        return model.params['FR_S36_LK'] * model.s34['Benzene']  == model.s36['Benzene']     
    
    def Eq18(self, model):
        return (1 - model.params['FR_S36_LK']) * model.s34['Benzene']  == model.s37['Benzene']     
    
    def Eq19(self, model):
        return model.params['FR_S37_HK'] * model.s34['Cyclohexane']  == model.s37['Cyclohexane'] 
    
    def Eq20(self, model):
        return (1 - model.params['FR_S37_HK']) * model.s34['Cyclohexane']  == model.s36['Cyclohexane']   
 

    
      
    # Selectivity S1 relation
    def selectivity_1_relation(self, model):
        return (model.zeta_1 + model.zeta_2) * model.params['S1'] == model.s24['Cyclohexene']
    
    # Selectivity S2 relation
    def selectivity_2_relation(self, model):
        return model.zeta_3 * model.params['S2'] == model.s31['Cyclohexylbenzene']
    
      
    # Conversion X1 Definition
    def conversion_1_def_rule(self, model):
        return model.params['X1'] * (model.s20['Benzene'] + model.s38['Benzene']) ==  model.zeta_1 + model.zeta_2 
    
    
    # Conversion X2 Definition
    def conversion_2_def_rule(self, model):
        return model.params['X2'] * model.s30['Cyclohexene'] ==  model.zeta_3
      
    
    
    # Hydrogen (Individual Component material balance)
    
    def Hydrogen_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Hydrogen'] == model.s19['Hydrogen'] + model.s20['Hydrogen']
    
    def Hydrogen_comp_rule2(self, model):
        return model.s20['Hydrogen'] + model.s21['Hydrogen'] + model.s38['Hydrogen'] - model.zeta_1 - model.zeta_2 == model.s24['Hydrogen']

    def Hydrogen_comp_rule3(self, model):
        return model.s24['Hydrogen'] == model.s25['Hydrogen'] + model.s29['Hydrogen']
        
    def Hydrogen_comp_rule4(self, model):
        return model.s25['Hydrogen'] == model.s26['Hydrogen'] + model.s27['Hydrogen']
    
    def Hydrogen_comp_rule5(self, model):
        return model.s29['Hydrogen'] + model.s35['Hydrogen'] == model.s30['Hydrogen']  

    def Hydrogen_comp_rule6(self, model):
        return model.s26['Hydrogen'] + model.s36['Hydrogen'] == model.s38['Hydrogen']

    def Hydrogen_comp_rule7(self, model): # Assume no reaction
        return model.s30['Hydrogen'] == model.s31['Hydrogen']

    def Hydrogen_comp_rule8(self, model):
        return model.s31['Hydrogen'] == model.s32['Hydrogen'] + model.s33['Hydrogen']
    
    
### Splitter fraction
    def Hydrogen_comp_rule9(self, model):
        return model.s26['Hydrogen'] == 5 * model.s27['Hydrogen']   
     
    def Hydrogen_comp_rule10(self, model):
        return model.s32['Hydrogen'] == model.s34['Hydrogen'] + model.s35['Hydrogen']
    
    def Hydrogen_comp_rule11(self, model):
        return model.s34['Hydrogen'] == model.s36['Hydrogen'] + model.s37['Hydrogen']

    ### Zero these streams                 
    def Hydrogen_comp_rule12(self, model): # stream zero hydrogen
        return model.s19['Hydrogen'] + model.s20['Hydrogen'] + model.s33['Hydrogen'] + model.s35['Hydrogen'] + model.s37['Hydrogen'] == 0   

    def Hydrogen_comp_rule13(self, model): 
        return model.s21['Hydrogen'] == model.S21
        
     
    # Methane (Individual Component material balance)
    def Methane_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Methane'] == model.s29['Methane'] + model.s20['Methane']

    def Methane_comp_rule2(self, model):
        return model.s20['Methane'] + model.s21['Methane'] + model.s38['Methane'] == model.s24['Methane']

    def Methane_comp_rule3(self, model):
        return model.s24['Methane'] == model.s25['Methane'] + model.s29['Methane']

    def Methane_comp_rule4(self, model):
        return model.s25['Methane'] == model.s26['Methane'] + model.s27['Methane']

    def Methane_comp_rule5(self, model):
        return model.s26['Methane'] + model.s36['Methane'] == model.s38['Methane']

    def Methane_comp_rule6(self, model):
        return model.s29['Methane'] + model.s35['Methane'] == model.s30['Methane']

    def Methane_comp_rule7(self, model):  # Assume no reaction
        return model.s30['Methane'] == model.s31['Methane']

    def Methane_comp_rule8(self, model):
        return model.s31['Methane'] == model.s32['Methane'] + model.s33['Methane']

    # Splitter fraction
    def Methane_comp_rule9(self, model):
        return model.s26['Methane'] == 5 * model.s27['Methane']

    def Methane_comp_rule10(self, model):
        return model.s32['Methane'] == model.s34['Methane'] + model.s35['Methane']

    def Methane_comp_rule11(self, model):
        return model.s34['Methane'] == model.s36['Methane'] + model.s37['Methane']

    # Zero these streams
    def Methane_comp_rule12(self, model):  # stream zero methane
        return model.s21['Methane'] + model.s33['Methane'] + model.s35['Methane'] + model.s37['Methane'] == 0

     
    
    # Benzene (Individual Component material balance)
    
    def Benzene_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Benzene'] == model.s19['Benzene'] + model.s20['Benzene']

    def Benzene_comp_rule2(self, model):
        return model.s20['Benzene'] + model.s21['Benzene'] + model.s38['Benzene'] - model.zeta_1 - model.zeta_2 == model.s24['Benzene']

    def Benzene_comp_rule3(self, model):
        return model.s24['Benzene'] == model.s25['Benzene'] + model.s29['Benzene']

    def Benzene_comp_rule4(self, model):
        return model.s25['Benzene'] == model.s26['Benzene'] + model.s27['Benzene']

    def Benzene_comp_rule5(self, model):
        return model.s26['Benzene'] + model.s36['Benzene'] == model.s38['Benzene']

    def Benzene_comp_rule6(self, model):
        return model.s29['Benzene'] + model.s35['Benzene'] == model.s30['Benzene']

    def Benzene_comp_rule7(self, model):  
        return model.s30['Benzene'] - model.zeta_3 == model.s31['Benzene']

    def Benzene_comp_rule8(self, model):
        return model.s31['Benzene'] == model.s32['Benzene'] + model.s33['Benzene']

    # Splitter fraction
    def Benzene_comp_rule9(self, model):
        return model.s26['Benzene'] == 5 * model.s27['Benzene']

    def Benzene_comp_rule10(self, model):
        return model.s32['Benzene'] == model.s34['Benzene'] + model.s35['Benzene']

    def Benzene_comp_rule11(self, model):
        return model.s34['Benzene'] == model.s36['Benzene'] + model.s37['Benzene']

    # Zero these streams
    def Benzene_comp_rule12(self, model):  # stream zero benzene
        return model.s21['Benzene'] + model.s25['Benzene'] + model.s26['Benzene'] + model.s27['Benzene'] + model.s29['Benzene'] + model.s33['Benzene'] + model.s35['Benzene'] == 0

    
    # Cyclohexane (Individual Component material balance)

    def Cyclohexane_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Cyclohexane'] == model.s19['Cyclohexane'] + model.s20['Cyclohexane']

    def Cyclohexane_comp_rule2(self, model):
        return model.s20['Cyclohexane'] + model.s21['Cyclohexane'] + model.s38['Cyclohexane'] + model.zeta_2 == model.s24['Cyclohexane']

    def Cyclohexane_comp_rule3(self, model):
        return model.s24['Cyclohexane'] == model.s25['Cyclohexane'] + model.s29['Cyclohexane']

    def Cyclohexane_comp_rule4(self, model):
        return model.s25['Cyclohexane'] == model.s26['Cyclohexane'] + model.s27['Cyclohexane']

    def Cyclohexane_comp_rule5(self, model):
        return model.s26['Cyclohexane'] + model.s36['Cyclohexane'] == model.s38['Cyclohexane']

    def Cyclohexane_comp_rule6(self, model):
        return model.s29['Cyclohexane'] + model.s35['Cyclohexane'] == model.s30['Cyclohexane']

    def Cyclohexane_comp_rule7(self, model):  # Assume no reaction
        return model.s30['Cyclohexane'] == model.s31['Cyclohexane']

    def Cyclohexane_comp_rule8(self, model):
        return model.s31['Cyclohexane'] == model.s32['Cyclohexane'] + model.s33['Cyclohexane']

    # Splitter fraction
    def Cyclohexane_comp_rule9(self, model):
        return model.s26['Cyclohexane'] == 5 * model.s27['Cyclohexane']

    def Cyclohexane_comp_rule10(self, model):
        return model.s32['Cyclohexane'] == model.s34['Cyclohexane'] + model.s35['Cyclohexane']

    def Cyclohexane_comp_rule11(self, model):
        return model.s34['Cyclohexane'] == model.s36['Cyclohexane'] + model.s37['Cyclohexane']

    # Zero these streams
    def Cyclohexane_comp_rule12(self, model):  # stream zero cyclohexane
        return model.s19['Cyclohexane'] + model.s20['Cyclohexane'] + model.s21['Cyclohexane'] + model.s25['Cyclohexane'] + model.s26['Cyclohexane'] + model.s27['Cyclohexane'] + model.s33['Cyclohexane'] == 0

    
    # Cyclohexene (Individual Component material balance)

    def Cyclohexene_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Cyclohexene'] == model.s19['Cyclohexene'] + model.s20['Cyclohexene']

    def Cyclohexene_comp_rule2(self, model):
        return model.s20['Cyclohexene'] + model.s21['Cyclohexene'] + model.s38['Cyclohexene'] + model.zeta_1 == model.s24['Cyclohexene']


    def Cyclohexene_comp_rule3(self, model):
        return model.s24['Cyclohexene'] == model.s25['Cyclohexene'] + model.s29['Cyclohexene']

    def Cyclohexene_comp_rule4(self, model):
        return model.s25['Cyclohexene'] == model.s26['Cyclohexene'] + model.s27['Cyclohexene']

    def Cyclohexene_comp_rule5(self, model):
        return model.s26['Cyclohexene'] + model.s36['Cyclohexene'] == model.s38['Cyclohexene']

    def Cyclohexene_comp_rule6(self, model):
        return model.s29['Cyclohexene'] + model.s35['Cyclohexene'] == model.s30['Cyclohexene']

    def Cyclohexene_comp_rule7(self, model):  # Assume no reaction
        return model.s30['Cyclohexene']  - model.zeta_3 == model.s31['Cyclohexene']

    def Cyclohexene_comp_rule8(self, model):
        return model.s31['Cyclohexene'] == model.s32['Cyclohexene'] + model.s33['Cyclohexene']

    # Splitter fraction
    def Cyclohexene_comp_rule9(self, model):
        return model.s26['Cyclohexene'] == 5 * model.s27['Cyclohexene']

    def Cyclohexene_comp_rule10(self, model):
        return model.s32['Cyclohexene'] == model.s34['Cyclohexene'] + model.s35['Cyclohexene']

    def Cyclohexene_comp_rule11(self, model):
        return model.s34['Cyclohexene'] == model.s36['Cyclohexene'] + model.s37['Cyclohexene']

    # Zero these streams
    def Cyclohexene_comp_rule12(self, model):  # stream zero cyclohexene
        return model.s19['Cyclohexene'] + model.s20['Cyclohexene'] + model.s21['Cyclohexene'] + model.s25['Cyclohexene'] + model.s26['Cyclohexene'] + model.s27['Cyclohexene'] + model.s36['Cyclohexene'] + model.s38['Cyclohexene'] == 0


    # Cyclohexylbenzene (Individual Component material balance)

    def Cyclohexylbenzene_comp_rule1(self, model):
        return model.params['S15'] * model.params['S15_Cyclohexylbenzene'] == model.s19['Cyclohexylbenzene'] + model.s20['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule2(self, model):
        return model.s20['Cyclohexylbenzene'] + model.s21['Cyclohexylbenzene'] + model.s38['Cyclohexylbenzene'] == model.s24['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule3(self, model):
        return model.s24['Cyclohexylbenzene'] == model.s25['Cyclohexylbenzene'] + model.s29['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule4(self, model):
        return model.s25['Cyclohexylbenzene'] == model.s26['Cyclohexylbenzene'] + model.s27['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule5(self, model):
        return model.s26['Cyclohexylbenzene'] + model.s36['Cyclohexylbenzene'] == model.s38['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule6(self, model):
        return model.s29['Cyclohexylbenzene'] + model.s35['Cyclohexylbenzene'] == model.s30['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule7(self, model): 
        return model.s30['Cyclohexylbenzene'] + model.zeta_3 == model.s31['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule8(self, model):
        return model.s31['Cyclohexylbenzene'] == model.s32['Cyclohexylbenzene'] + model.s33['Cyclohexylbenzene']

    # Splitter fraction
    def Cyclohexylbenzene_comp_rule9(self, model):
        return model.s28['Cyclohexylbenzene'] == 5 * model.s27['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule10(self, model):
        return model.s32['Cyclohexylbenzene'] == model.s34['Cyclohexylbenzene'] + model.s35['Cyclohexylbenzene']

    def Cyclohexylbenzene_comp_rule11(self, model):
        return model.s34['Cyclohexylbenzene'] == model.s36['Cyclohexylbenzene'] + model.s37['Cyclohexylbenzene']

    # Zero these streams
    def Cyclohexylbenzene_comp_rule13(self, model):  # stream zero cyclohexylbenzene
        return model.s29['Cyclohexylbenzene'] + model.s20['Cyclohexylbenzene'] + model.s21['Cyclohexylbenzene'] + model.s24['Cyclohexylbenzene'] + model.s25['Cyclohexylbenzene'] + model.s26['Cyclohexylbenzene'] + model.s27['Cyclohexylbenzene'] + model.s28['Cyclohexylbenzene'] + model.s29['Cyclohexylbenzene'] + model.s34['Cyclohexylbenzene'] + model.s36['Cyclohexylbenzene'] + model.s37['Cyclohexylbenzene'] + model.s38['Cyclohexylbenzene'] == 0
    
    
    
    
    
    
    
    
    
    