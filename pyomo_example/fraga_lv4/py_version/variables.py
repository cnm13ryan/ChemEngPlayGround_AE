from pyomo.environ import *

def define_variables(model):
    # Component flow rates in each stream
    model.f = Var(model.stm, model.comp, within=NonNegativeReals, doc='Process component flow rates in stream stm [kmol per hr]')
    
    # Extents of Reaction
    model.xi1 = Var(within=NonNegativeReals, doc='Extent of reaction 1')
    model.xi2 = Var(within=NonNegativeReals, doc='Extent of reaction 2')
    model.xi3 = Var(within=NonNegativeReals, doc='Extent of reaction 3')
    
    # Recovery of key components in distillation columns
    model.r1 = Var(bounds=(0.90, 0.998), doc='Recovery of key components in distillation column 1')
    model.r2 = Var(bounds=(0.90, 0.998), doc='Recovery of key components in distillation column 2')
    model.r3 = Var(bounds=(0.90, 0.998), doc='Recovery of key components in distillation column 3')
    
    # Presence of chemical species in distillation columns top stream
    model.aD1 = Var(model.comp, within=Binary, doc='Presence of chemical species in distillation col 1 top stream')
    model.aD2 = Var(model.comp, within=Binary, doc='Presence of chemical species in distillation col 2 top stream')
    model.aD3 = Var(model.comp, within=Binary, doc='Presence of chemical species in distillation col 3 top stream')
    
    # Cost-Related Variables
    model.feed_cost = Var(within=NonNegativeReals, doc='Cost of Feed 1 and Feed 2 [Million Euros per year]')
    model.output_sales = Var(within=NonNegativeReals, doc='Sales of Byproduct and Product [Million Euros per year]')
    model.dist1_c = Var(within=NonNegativeReals, doc='Cost of Distillation column 1 [Millions Euros per year]')
    model.dist2_c = Var(within=NonNegativeReals, doc='Cost of Distillation column 2 [Millions Euros per year]')
    model.dist3_c = Var(within=NonNegativeReals, doc='Cost of Distillation column 3 [Millions Euros per year]')
    model.react_c = Var(within=NonNegativeReals, doc='Cost of Reactor [Millions Euros per year]')
    model.hex_c = Var(within=NonNegativeReals, doc='Cost of Heat Exchanger [Millions Euros per year]')
    model.unitcosts = Var(within=NonNegativeReals, doc='Cost of all processing units [Million Euros per year]')
    model.netvalue = Var(within=Reals, doc='Net value of materials [Million Euros per year]')
    model.EP = Var(within=Reals, doc='Economic Potential [Million of Euros per year]')
    
    # Error Variables
    model.Err = Var(within=Reals, doc='Error between LiqRecycle and tearLiqRecycle')
    model.error = Var(within=Reals, doc='Free variable linked to Err')
    
    # Objective Variable
    model.z = Var(within=Reals, doc='Variable equal to Economic Potential (EP)')
