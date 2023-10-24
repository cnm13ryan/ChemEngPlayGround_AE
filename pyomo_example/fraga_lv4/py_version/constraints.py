from pyomo.environ import Constraint

def define_constraints(model):
    # 1. Feed2 Stoichiometric Ratio Constraint
    def feed2_ratio_rule(model):
        return model.f['Feed2', 'Bz'] == 19 * model.f['Feed2', 'Tu']
    model.feed2_ratio_constraint = Constraint(rule=feed2_ratio_rule)
    
    # 2. Mixer Material Balance Constraint
    def mixermb_rule(model, comp):
        return model.f['Mixeff', comp] == model.f['Feed1', comp] + model.f['Feed2', comp] + model.f['LiqRecycle', comp]
    model.mixermb_constraint = Constraint(model.comp, rule=mixermb_rule)
    
    # 3. Reactor Feed Constraint
    def reactor_feed_rule(model):
        return model.f['Mixeff', 'Bz'] >= model.f['Mixeff', 'E']
    model.reactor_feed_constraint = Constraint(rule=reactor_feed_rule)
    
    # 4. Selectivity and Conversion Definitions
    def selectivitydef_rule(model):
        return model.S * model.xi2 == model.xi1 - model.xi2 + model.xi3
    model.selectivitydef_constraint = Constraint(rule=selectivitydef_rule)
    
    def conversiondef_rule(model):
        return model.x * model.f['Mixeff', 'Bz'] == model.xi1
    model.conversiondef_constraint = Constraint(rule=conversiondef_rule)

    # 5. Reactor Material Balances
    def reactor_material_balance_rules(model, comp):
        if comp == 'E':
            return model.f['Mixeff', 'E'] - model.xi1 - model.xi2 - 2 * model.xi3 == model.f['Reacteff', 'E']
        if comp == 'P':
            return model.f['Mixeff', 'P'] + model.xi3 == model.f['Reacteff', 'P']
        if comp == 'Tu':
            return model.f['Mixeff', 'Tu'] == model.xi3
        if comp == 'Bz':
            return model.f['Mixeff', 'Bz'] - model.xi1 == model.f['Reacteff', 'Bz']
        if comp == 'EB':
            return model.f['Mixeff', 'EB'] + model.xi1 - model.xi2 + model.xi3 == model.f['Reacteff', 'EB']
        if comp == 'DEB':
            return model.f['Mixeff', 'DEB'] + model.xi2 == model.f['Reacteff', 'DEB']
    model.reactor_material_balance = Constraint(model.comp, rule=reactor_material_balance_rules)
    
    # 6. Distillation Presence Constraints
    def distillation_presence_rules(model, col, comp):
        if col == 1:
            if comp in {'Bz', 'EB'}:
                return model.aD1[comp] == model.r1 if comp == 'Bz' else 1 - model.r1
        if col == 2:
            if comp in {'P', 'Bz'}:
                return model.aD2[comp] == model.r2 if comp == 'P' else 1 - model.r2
        if col == 3:
            if comp in {'EB', 'DEB'}:
                return model.aD3[comp] == model.r3 if comp == 'EB' else 1 - model.r3
    model.distillation_presence = Constraint([(col, comp) for col in range(1, 4) for comp in model.comp], rule=distillation_presence_rules)

    # 7. Material Balance for Distillation Columns
    def material_balance_rules(model, stm, comp):
        if stm == 'Dist1top':
            return model.aD1[comp] * model.f['Reacteff', comp] == model.f[stm, comp]
        if stm == 'Dist1bot':
            return (1 - model.aD1[comp]) * model.f['Reacteff', comp] == model.f[stm, comp]
        if stm == 'Purge':
            return model.aD2[comp] * model.f['Dist1top', comp] == model.f[stm, comp]
        if stm == 'LiqRecycle':
            return (1 - model.aD2[comp]) * model.f['Dist1top', comp] == model.f[stm, comp]
        if stm == 'Prod':
            return model.aD3[comp] * model.f['Dist1bot', comp] == model.f[stm, comp]
        if stm == 'Byprod':
            return (1 - model.aD3[comp]) * model.f['Dist1bot', comp] == model.f[stm, comp]
    model.material_balance = Constraint([(stm, comp) for stm in model.stm for comp in model.comp], rule=material_balance_rules)

    # 8. Error Calculation and Dummy Constraints
    def error_calculation_rule(model):
        return model.Err == sum((model.tearLiqRecycle[comp] - model.f['LiqRecycle', comp]) for comp in model.comp)
    model.error_calculation = Constraint(rule=error_calculation_rule)

    def dummy_eq_rule(model):
        return model.error == model.Err
    model.dummy_eq = Constraint(rule=dummy_eq_rule)

    # 9. Cost-Related Constraints
    def cost_price_rule(model):
        return model.feed_cost * 1e6 / model.convfact / model.OSPY == sum(model.f['Feed1', comp] * model.Price['E'] for comp in model.comp) + sum(model.f['Feed2', comp] * model.Price['Bz'] for comp in model.comp)
    model.cost_price = Constraint(rule=cost_price_rule)
    
    def sales_price_rule(model):
        return model.output_sales * 1e6 / model.convfact / model.OSPY == sum(model.f['Byprod', comp] * model.Price['DEB'] for comp in model.comp) + sum(model.f['Prod', comp] * model.Price)
