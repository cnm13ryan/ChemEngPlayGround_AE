from pyomo.environ import *
from sets import define_sets
from parameters import define_parameters
from variables import define_variables
from constraints import define_constraints
from objective import define_objective
import math

def main():
    model = ConcreteModel()  # Initializing model as a ConcreteModel instance
    
    if model is None:  # Ensuring that the model is not None after initialization
        raise Exception("Model is None after initialization.")
        
    model = define_sets(model)  # Defining sets
    
    if model is None:  # Ensuring that the model is not None after defining sets
        raise Exception("Model is None after defining sets.")
        
    print("Model after defining sets: ", model)
    print("model.stm: ", model.stm)
    print("model.comp: ", model.comp)

    # # Check the existence of required sets before proceeding to define parameters
    # if not hasattr(model, 'comp'):
    #     raise Exception("model.comp is not defined. Please check define_sets function.")
    
    # Define Parameters
    model = define_parameters(model)

    # Define Variables
    model = define_variables(model)

    # Define Constraints
    model = define_constraints(model)

    # Define Objectives
    model = define_objective(model)

    # Open a file to write results
    with open('cengL4EP.data', 'w') as results:
        results.write('#      t      r1       r2      r3      x       S       z      status \n')

        # Iterate over different values of t, the reactor residence time
        for t in range(5, 301):  # equivalent to 'for(t = 5 to 300 by 1,' in GAMS

            # Recalculate the selectivity and conversion for each different value of t
            model.S = 371.60496 / t + 0.06379
            model.x = -0.66214 + 0.23303 * math.log(t)

            # Initialize all stream flows to help get started in the search for the solution
            for stm in model.stm:
                for comp in model.comp:
                    model.f[stm, comp] = 10
            for comp in model.comp:
                model.f['LiqRecycle', comp] = 80 * (1 - model.r2)

            # Invoke the solver
            solver = SolverFactory('ipopt')  # Assuming ipopt is the solver you are using
            results = solver.solve(model, tee=True)

            # Check if the solution is optimal and the economic potential is positive
            if str(results.Solver.Status) == 'ok':
                if model.EP() >= 0:
                    results.write(f"{t} {model.r1()} {model.r2()} {model.r3()} {model.x} {model.S} {model.EP()} ok\n")

    print('Optimization Complete.')

if __name__ == '__main__':
    main()
