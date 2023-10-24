from pyomo.environ import *

# Assume model is the ConcreteModel object
def define_objective(model):

    # Define feed cost and output sales equations
    model.feed_cost = Expression(expr=sum(model.f['Feed1', comp] * model.Price[comp] for comp in model.comp) +
                                  sum(model.f['Feed2', comp] * model.Price[comp] for comp in model.comp))

    model.output_sales = Expression(expr=sum(model.f['Byprod', comp] * model.Price[comp] for comp in model.comp) +
                                     sum(model.f['Prod', comp] * model.Price[comp] for comp in model.comp))

    # Define unit costs for Distillation Columns, Reactor, and Heat Exchanger
    model.dist1_c = Expression(expr=sqrt(sum(model.f['Reacteff', comp] for comp in model.comp)) * model.convfact * 100 *
                                (1 - model.r1) * (model.alpha1 - 1))

    model.dist2_c = Expression(expr=sqrt(sum(model.f['Dist1top', comp] for comp in model.comp)) * model.convfact * 100 *
                                (1 - model.r2) * (model.alpha2 - 1))

    model.dist3_c = Expression(expr=sqrt(sum(model.f['Dist1bot', comp] for comp in model.comp)) * model.convfact * 100 *
                                (1 - model.r3) * (model.alpha3 - 1))

    model.react_c = Expression(expr=model.t * sum(model.f['Mixeff', comp] for comp in model.comp) * model.convfact * 1000)

    model.hex_c = Expression(expr=9 * (model.A**0.65) * 100)

    # Define Net Value and Unit Costs
    model.netvalue = Expression(expr=model.output_sales - model.feed_cost)
    model.unitcosts = Expression(expr=model.dist1_c + model.dist2_c + model.dist3_c + model.react_c + model.hex_c)

    # Define Economic Potential
    model.EP = Expression(expr=model.netvalue - model.unitcosts)

    # Define Objective: Maximize Economic Potential
    model.objective = Objective(expr=model.EP, sense=maximize)

    return model


