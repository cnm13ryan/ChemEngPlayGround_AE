from pyomo.environ import Constraint, RangeSet
from math import log
from functools import partial

class Constraints:
    components = ['Hydrogen', 'Methane', 'Benzene', 'Toluene', 'ParaXylene', 'Diphenyl']

    def __init__(self, model, parameters=None):
        self.model = model
        if parameters:
            self.define_constraints(model, parameters)

    def define_constraints(self, model, parameters):
        self._initialize_streams(model)
        self._add_composition_sum_constraint(model)
        self._add_material_balance_constraints(model)
        self._add_component_molar_composition_constraints(model)
        self._add_dynamic_constraints(model)

    def _initialize_streams(self, model):
        if hasattr(model, 'streams'):
            model.del_component(model.streams)
        model.streams = RangeSet(10, 18)

    def _add_composition_sum_constraint(self, model):
        model.composition_sum_constraint = Constraint(model.streams, rule=self.composition_sum_rule)

    def _add_material_balance_constraints(self, model):
        for i in model.streams:
            setattr(model, f'Eq0_S{i}', Constraint(expr=self.overall_material_balance(model, i)))

    def _add_component_molar_composition_constraints(self, model):
        for s in model.streams:
            for c in self.components:
                constraint_name = f'component_molar_composition_S{s}_{c}'
                setattr(model, constraint_name, Constraint(expr=self.component_molar_composition(model, s, c)))

    def _add_dynamic_constraints(self, model):
        constraints_mapping = self._get_constraints_mapping()
        for constraint_name, rule_function in constraints_mapping.items():
            setattr(model, constraint_name, Constraint(rule=rule_function))

    def _get_constraints_mapping(self):
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
            'selectivity_def_constraint': self.selectivity_def_rule,
            'selectivity_relation': self.selectivity_relation,
            'conversion_def_rule': self.conversion_def_rule
        }
        for component in self.components:
            for i in range(1, 8):
                rule_name = f'{component}_comp_rule{i}'
                if hasattr(self, rule_name):
                    constraints_mapping[rule_name] = getattr(self, rule_name)
        return constraints_mapping

    # Overall Material Balance
    def overall_material_balance(self, model, stream):
        return getattr(model, f'S{stream}') == sum(getattr(model, f's{stream}')[component] for component in self.components)

    # Physical condition 
    def component_molar_composition(self, model, stream, component):
        return model.x[stream, component] == getattr(model, f's{stream}')[component] / getattr(model, f'S{stream}')

    # Physical condition (composition within a stream should add up to 1)
    def composition_sum_rule(self, model, stream):
        return sum(model.x[stream, component] for component in self.components) == 1.0


    # Fractional Recovery (HK/LK) Equations   
    def Eq1(self, model):
        return model.params['FR_S11_LK'] * model.s10['Methane'] == model.s11['Methane'] 
    
    def Eq2(self, model):
        return (1 - model.params['FR_S11_LK']) * model.s10['Methane'] == model.s12['Methane']
    
    def Eq3(self, model):
        return model.params['FR_S12_HK'] * model.s10['Benzene'] == model.s12['Benzene'] 
    
    def Eq4(self, model):
        return (1 - model.params['FR_S12_HK']) * model.s10['Benzene'] == model.s11['Benzene'] 
    
    def Eq5(self, model):
        return model.params['FR_S15_LK'] * model.s12['Benzene'] == model.s15['Benzene']
    
    def Eq6(self, model):
        return (1 - model.params['FR_S15_LK']) * model.s12['Benzene']  == model.s16['Benzene'] 
    
    def Eq7(self, model):
        return model.params['FR_S16_HK'] * model.s12['Toluene'] == model.s16['Toluene']
    
    def Eq8(self, model):
        return (1 - model.params['FR_S16_HK']) * model.s12['Toluene'] == model.s15['Toluene'] 
    
    def Eq9(self, model):
        return model.params['FR_S17_LK'] * model.s16['Toluene']  == model.s17['Toluene'] 
    
    def Eq10(self, model):
        return (1 - model.params['FR_S17_LK']) * model.s16['Toluene']  == model.s18['Toluene'] 
    
    def Eq11(self, model):
        return model.params['FR_S18_HK'] * model.s16['ParaXylene']  == model.s18['ParaXylene'] 
    
    def Eq12(self, model):
        return (1 - model.params['FR_S18_HK']) * model.s16['ParaXylene']  == model.s17['ParaXylene'] 
    
    
    # Selectivity Definition
    def selectivity_def_rule(self, model):
        return model.S * (1 - model.X)**(1.544) == (1 - model.X)**(1.544) - 0.0036 
    
    # Selectivity relation
    def selectivity_relation(self, model):
        return model.zeta_1 * model.S == model.s10['Benzene']
    
    # Conversion Definition
    def conversion_def_rule(self, model):
        return model.X * (model.params['S9'] * model.params['S9_Benzene'] + model.s13['Benzene'] + model.s17['Benzene']) ==  model.zeta_1 - 2 * model.zeta_2 
    
    # Hydrogen (Individual Component material balance)
    def Hydrogen_comp_rule1(self, model):
        return model.params['S9'] * model.params['S9_Hydrogen'] + model.params['S8'] * model.params['S8_Hydrogen'] + model.s13['Hydrogen'] + model.s17['Hydrogen'] - model.zeta_1 + model.zeta_2 == model.s10['Hydrogen'] 

    def Hydrogen_comp_rule2(self, model):
        return model.s10['Hydrogen']  ==  model.s11['Hydrogen'] + model.s12['Hydrogen']
    
    def Hydrogen_comp_rule3(self, model):
        return model.s11['Hydrogen'] == model.s13['Hydrogen'] + model.s14['Hydrogen']
    
    def Hydrogen_comp_rule4(self, model):
        return model.s12['Hydrogen'] + model.s15['Hydrogen'] + model.s16['Hydrogen'] + model.s17['Hydrogen'] + model.s18['Hydrogen'] == 0
    
    def Hydrogen_comp_rule5(self, model):
        return model.s13['Hydrogen'] == 5 * model.s14['Hydrogen'] 
    
    # Methane (Individual Component material balance)
    def Methane_comp_rule1(self, model):
        return model.params['S9']*model.params['S9_Methane'] + model.params['S8']*model.params['S8_Methane'] + model.s13['Methane'] + model.s17['Methane'] + model.zeta_1 == model.s10['Methane']
    
    def Methane_comp_rule2(self, model):
        return model.s10['Methane'] == model.s11['Methane'] + model.s12['Methane']
   
    def Methane_comp_rule3(self, model):
        return model.s11['Methane'] == model.s13['Methane'] + model.s14['Methane']
       
    def Methane_comp_rule4(self, model):
        return model.s12['Methane'] == model.s15['Methane']
    
    def Methane_comp_rule5(self, model):
        return model.s16['Methane']+model.s17['Methane']+model.s18['Methane'] == 0
    
    def Methane_comp_rule6(self, model):
        return model.s13['Methane'] == 5 * model.s14['Methane']   
      
    
    
    # Benzene (Individual Component material balance)
    def Benzene_comp_rule1(self, model):
        return model.params['S9']*model.params['S9_Benzene'] + model.params['S8']*model.params['S8_Benzene'] + model.s13['Benzene'] + model.s17['Benzene'] + model.zeta_1 - 2 * model.zeta_2 == model.s10['Benzene']                                                           
    def Benzene_comp_rule2(self, model):
        return model.s10['Benzene'] == model.s11['Benzene'] + model.s12['Benzene']
   
    def Benzene_comp_rule3(self, model):
        return model.s11['Benzene'] == model.s13['Benzene'] + model.s14['Benzene'] 
    
    def Benzene_comp_rule4(self, model):
        return model.s12['Benzene'] == model.s15['Benzene'] + model.s16['Benzene']
    
    def Benzene_comp_rule5(self, model):
        return model.s16['Benzene'] == model.s17['Benzene']
    
    def Benzene_comp_rule6(self, model):
        return model.s18['Benzene'] == 0  
    
    def Benzene_comp_rule7(self, model):
        return model.s13['Benzene'] == 5 * model.s14['Benzene']
    
    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S9']*model.params['S9_Toluene'] + model.params['S8'] * model.params['S8_Toluene'] + model.s13['Toluene'] + model.s17['Toluene'] - model.zeta_1 == model.s10['Toluene']
       
    def Toluene_comp_rule2(self, model):
        return model.s10['Toluene'] ==  model.s12['Toluene']
   
    def Toluene_comp_rule3(self, model):
        return model.s12['Toluene'] == model.s15['Toluene'] + model.s16['Toluene']
    
    def Toluene_comp_rule4(self, model):
        return model.s16['Toluene'] == model.s17['Toluene'] + model.s18['Toluene']
    
    def Toluene_comp_rule5(self, model):
        return model.x[11, 'Toluene'] + model.x[13, 'Toluene'] + model.x[14, 'Toluene'] == 0
    def Toluene_comp_rule6(self, model):
        return model.s15['Toluene'] == 0
     
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S9']*model.params['S9_ParaXylene'] + model.params['S8']*model.params['S8_ParaXylene'] + model.s13['ParaXylene'] + model.s17['ParaXylene'] == model.s10['ParaXylene']
    
    def ParaXylene_comp_rule2(self, model):
        return model.s10['ParaXylene'] ==  model.s12['ParaXylene']
   
    def ParaXylene_comp_rule3(self, model):
        return model.s12['ParaXylene'] == model.s16['ParaXylene']
    
    def ParaXylene_comp_rule4(self, model):
        return model.s15['ParaXylene'] + model.s16['ParaXylene'] + model.s17['ParaXylene'] + model.s18['ParaXylene'] + model.s11['ParaXylene'] + model.s13['ParaXylene'] + model.s14['ParaXylene'] == 0
    

    # Diphenyl (Individual Component material balance)
    def Diphenyl_comp_rule1(self, model):
        return model.params['S9']*model.params['S9_Diphenyl'] + model.params['S8']*model.params['S8_Diphenyl'] + model.s13['Diphenyl'] + model.s17['Diphenyl']  + model.zeta_2 == model.s10['Diphenyl']
    
    def Diphenyl_comp_rule2(self, model):
        return model.s10['Diphenyl'] ==  model.s12['Diphenyl']
   
    def Diphenyl_comp_rule3(self, model):
        return model.s12['Diphenyl'] == model.s16['Diphenyl']
    
    def Diphenyl_comp_rule4(self, model):
        return model.s16['Diphenyl']  == model.s18['Diphenyl']
    
    def Diphenyl_comp_rule5(self, model):
        return model.s11['Diphenyl'] + model.s13['Diphenyl'] + model.s14['Diphenyl'] + model.s15['Diphenyl'] + model.s17['Diphenyl']== 0
           
    