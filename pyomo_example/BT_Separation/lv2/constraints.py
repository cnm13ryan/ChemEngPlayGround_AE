from pyomo.environ import Constraint
from math import log

class Constraints:
    def __init__(self, model, parameters):
        self.define_constraints(model, parameters)
        self.add_composition_constraints(model)

    def define_constraints(self, model, parameters):
        
        model.FR_LK_d1 = Constraint(rule=self.FR_LK_d1)
        model.FR_HK_b1 = Constraint(rule=self.FR_HK_b1)
        model.FR_LK_d2 = Constraint(rule=self.FR_LK_d2)
        model.FR_HK_b2 = Constraint(rule=self.FR_HK_b2)      
        model.FR_LK_d3 = Constraint(rule=self.FR_LK_d3)
        model.FR_HK_b3 = Constraint(rule=self.FR_HK_b3)
        
        model.matbal_rule1 = Constraint(rule=self.matbal_rule1)
        model.matbal_rule2 = Constraint(rule=self.matbal_rule2)
        model.matbal_rule3 = Constraint(rule=self.matbal_rule3)
        
        model.Benzene_comp_rule1 = Constraint(rule=self.Benzene_comp_rule1)
        model.Benzene_comp_rule2 = Constraint(rule=self.Benzene_comp_rule2)
        
        model.Toluene_comp_rule1 = Constraint(rule=self.Toluene_comp_rule1)
        model.Toluene_comp_rule2 = Constraint(rule=self.Toluene_comp_rule2)
        model.Toluene_comp_rule3 = Constraint(rule=self.Toluene_comp_rule3)
        
        model.OrthoXylene_comp_rule1 = Constraint(rule=self.OrthoXylene_comp_rule1)
        model.OrthoXylene_comp_rule2 = Constraint(rule=self.OrthoXylene_comp_rule2)
        model.OrthoXylene_comp_rule3 = Constraint(rule=self.OrthoXylene_comp_rule3)
        
        model.MetaXylene_comp_rule1 = Constraint(rule=self.MetaXylene_comp_rule1)
        model.MetaXylene_comp_rule2 = Constraint(rule=self.MetaXylene_comp_rule2)
        model.MetaXylene_comp_rule3 = Constraint(rule=self.MetaXylene_comp_rule3)
        
        
        model.Ethylbenzene_comp_rule1 = Constraint(rule=self.Ethylbenzene_comp_rule1)
        model.Ethylbenzene_comp_rule2 = Constraint(rule=self.Ethylbenzene_comp_rule2)
        model.Ethylbenzene_comp_rule3 = Constraint(rule=self.Ethylbenzene_comp_rule3)

        
        model.ParaXylene_comp_rule1 = Constraint(rule=self.ParaXylene_comp_rule1)
        model.ParaXylene_comp_rule2 = Constraint(rule=self.ParaXylene_comp_rule2)
        model.ParaXylene_comp_rule3 = Constraint(rule=self.ParaXylene_comp_rule3)
        
        model.TwoMethylbenzene_comp_rule1 = Constraint(rule=self.TwoMethylbenzene_comp_rule1)
        
          
    # Fractional Recoveries Equations    
    def FR_LK_d1(self, model):
        return model.params['FR_S2_LK'] * model.params['S1'] * model.params['z1_Benzene'] == model.d1['Benzene'] * model.S2
    
    def FR_HK_b1(self, model):
        return model.params['FR_S3_HK'] * model.params['S1'] * model.params['z1_Toluene'] == model.b1['Toluene'] * model.S3
    
    def FR_LK_d2(self, model):
        return model.params['FR_S4_LK'] * model.S3 * model.b1['Toluene'] == model.d2['Toluene'] * model.S4
    
    def FR_HK_b2(self, model):
        return model.params['FR_S5_HK'] * model.S3 * model.b1['Ethylbenzene'] == model.b2['Ethylbenzene'] * model.S5
    
    def FR_LK_d3(self, model):
        return model.params['FR_S6_LK'] * model.S5 * model.b2['Ethylbenzene'] == model.d3['Ethylbenzene'] * model.S6
    
    def FR_HK_b3(self, model):
        return model.params['FR_S7_HK'] * model.S5 * model.b2['ParaXylene'] == model.b3['ParaXylene'] * model.S7


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

    
    # Toluene (Individual Component material balance)
    def Toluene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Toluene'] ==  model.d1['Toluene'] * model.S2 + model.b1['Toluene'] * model.S3
    
    def Toluene_comp_rule2(self, model):
        return model.b1['Toluene'] * model.S3 ==  model.d2['Toluene'] * model.S4 + model.b2['Toluene'] * model.S5
    
    def Toluene_comp_rule3(self, model):
        return model.b2['Toluene'] * model.S5 ==  model.d3['Toluene'] * model.S6
    
    
    # Ortho-Xylene (Individual Component material balance)
    def OrthoXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_OrthoXylene'] == model.b1['OrthoXylene'] * model.S3
    
    def OrthoXylene_comp_rule2(self, model):
        return model.b1['OrthoXylene'] * model.S3 == model.b2['OrthoXylene'] * model.S5

    def OrthoXylene_comp_rule3(self, model):
        return model.b2['OrthoXylene'] * model.S5 == model.b3['OrthoXylene'] * model.S7
    
    
    # Ethylbenzene (Individual Component material balance)
    def Ethylbenzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_Ethylbenzene'] == model.b1['Ethylbenzene'] * model.S3  
    
    def Ethylbenzene_comp_rule2(self, model):
        return model.b1['Ethylbenzene'] * model.S3  == model.d2['Ethylbenzene'] * model.S4 + model.b2['Ethylbenzene'] * model.S5

    def Ethylbenzene_comp_rule3(self, model):
        return model.b2['Ethylbenzene'] * model.S5  == model.d3['Ethylbenzene'] * model.S6 + model.b3['Ethylbenzene'] * model.S7

    
    # MetaXylene (Individual Component material balance)
    def MetaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_MetaXylene'] == model.b1['MetaXylene'] * model.S3
    
    def MetaXylene_comp_rule2(self, model):
        return model.b1['MetaXylene'] * model.S3 == model.b2['MetaXylene'] * model.S5

    def MetaXylene_comp_rule3(self, model):
        return model.b2['MetaXylene'] * model.S5 == model.b3['MetaXylene'] * model.S7

    
    # ParaXylene (Individual Component material balance)
    def ParaXylene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_ParaXylene'] == model.b1['ParaXylene'] * model.S3  
    
    def ParaXylene_comp_rule2(self, model):
        return model.b1['ParaXylene'] * model.S3  ==  model.b2['ParaXylene'] * model.S5

    def ParaXylene_comp_rule3(self, model):
        return model.b2['ParaXylene'] * model.S5  == model.d3['ParaXylene'] * model.S6 + model.b3['ParaXylene'] * model.S7

    # TwoMethylbenzene (Individual Component material balance)
    def TwoMethylbenzene_comp_rule1(self, model):
        return model.params['S1'] * model.params['z1_TwoMethylbenzene'] == model.d1['TwoMethylbenzene'] * model.S2
    
    def add_composition_constraints(self, model):
        components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbenzene']

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
