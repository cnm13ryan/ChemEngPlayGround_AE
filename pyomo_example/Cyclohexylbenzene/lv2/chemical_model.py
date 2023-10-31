from pyomo.environ import ConcreteModel, SolverFactory, Objective, maximize, Constraint, Var, Suffix
from parameters import Parameters
from variables import Variables
from constraints import Constraints
import pandas as pd
from pyomo.opt import TerminationCondition
#import cplex

class ChemicalModel:
    
    def __init__(self):
        self.model = ConcreteModel()
        self.components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']
        self.parameters = Parameters()
        
        # Set params as an attribute of model
        self.model.params = self.parameters.params
        
        self.variables = Variables(self.model, self.components, self.model.params)
        self.constraints = Constraints(self.model, self.model.params)
        
        # Initialize tearing variables for s25 and s30
        self.tearing_streams = ['s25', 's30', 'S25', 'S30']
        self.tearing_values = {
            's25': {component: 0.00001 for component in self.components},
            's30': {component: 0.00001 for component in self.components},
            'S25': 1000,
            'S30': 1000
        }
        
    def refine_conflict(self):
        # Create a CPLEX instance
        c = cplex.Cplex()

        # Load the model from the Pyomo instance
        c.read_from_stream(self.model.write(format='lp_string'))

        # Refine the conflict
        c.conflict.refine(c.conflict.all_constraints())

        # Get the conflict groups
        conflict_groups = c.conflict.get()

        # Analyze the results
        for idx, conflict in enumerate(conflict_groups):
            if conflict[1] == c.conflict.Status.ConflictMember:
                print(f"Constraint {idx} is part of the conflict.")

        
    def find_optimal_initial_values(self, s25_range, s30_range):
        min_error = float('inf')  # Initialize with a large value
        optimal_initial_values = {'s25': None, 's30': None}

        for s25_init in s25_range:
            for s30_init in s30_range:
                # Set initial values
                for component in self.components:
                    self.model.s25[component].set_value(s25_init)
                    self.model.s30[component].set_value(s30_init)

                # Solve with tearing method
                self.solve_with_tearing()

                # Calculate the error for this iteration
                error = sum(
                    abs(self.tearing_values[stream][component] - self.fetch_value(getattr(self.model, stream)[component]))
                    for stream in ['s25', 's30']
                    for component in self.components
                )

                # Update optimal values if this error is smaller
                if error < min_error:
                    min_error = error
                    optimal_initial_values['s28'] = s28_init
                    optimal_initial_values['s32'] = s32_init

        return optimal_initial_values
        

    def count_equations_and_unknowns(self):
        """
        Count the number of active constraints (equations) and variables (unknowns) in the model.
        """
        # Count active constraints
        num_constraints = sum(1 for c in self.model.component_objects(ctype=Constraint, active=True)
                              for _ in c)

        # Count active variables
        num_variables = sum(1 for v in self.model.component_objects(ctype=Var, active=True)
                            for _ in v)

        return num_constraints, num_variables 
    
    def solve_with_tearing(self):
        # Initial solve
        self.solve()

        # Define the tearing streams and initialize their values
        self.tearing_streams = ['s25', 's30']
        self.tearing_values = {
            's25': {component: 1000 for component in self.components},
            's30': {component: 1000 for component in self.components}
        }

        # Define a tolerance for the difference between successive values
        tolerance = 1e-4

        # Maximum number of iterations
        max_iterations = 500

        # Current iteration counter
        current_iteration = 0

        # List to store the error for each iteration
        errors = []

        # Loop until the tearing streams converge or max iterations reached
        while current_iteration < max_iterations:
            # Store the old values of the tearing streams
            old_values = {
                stream: {component: self.tearing_values[stream][component] for component in self.components}
                for stream in self.tearing_streams
            }

            # Update the tearing_values dictionary with the current values from the model
            for stream in self.tearing_streams:
                for component in self.components:
                    current_value = self.fetch_value(getattr(self.model, stream)[component])
                    self.tearing_values[stream][component] = current_value

            # Calculate the error for the current iteration
            error = sum(
                abs(self.tearing_values[stream][component] - old_values[stream][component])
                for stream in self.tearing_streams
                for component in self.components
            )
            errors.append(error)

            # Check for convergence
            converged = all(e < tolerance for e in errors)

            if converged:
                break

            # If not converged, update the model with the new tearing values and solve again
            for stream in self.tearing_streams:
                for component in self.components:
                    getattr(self.model, stream)[component].set_value(self.tearing_values[stream][component])

            self.solve()

            # Increment the current iteration counter
            current_iteration += 1

        # Print the error for each iteration (optional)
        for i, error in enumerate(errors, 1):
            print(f"Iteration {i}: Error = {error:.6f}")

        # Check if the solution converged within the maximum number of iterations
        if current_iteration == max_iterations and not converged:
            print("Warning: Maximum number of iterations reached without convergence.")

            
    def identify_redundant_constraints_sensitivity(self):
        """Identify potential redundant constraints using sensitivity analysis."""
        self.model.dual = Suffix(direction=Suffix.IMPORT)
        solver = SolverFactory('ipopt')
        result = solver.solve(self.model, tee=True)

        # Check if the solver was successful
        if result.solver.termination_condition != TerminationCondition.optimal:
            print("Solver did not converge. Cannot perform sensitivity analysis.")
            return

        redundant_constraints = []
        for c in self.model.component_objects(ctype=Constraint, active=True):
            for index in c:
                if abs(self.model.dual[c[index]]) < 1e-6:  # Small threshold
                    redundant_constraints.append(c[index])

        print("Potential redundant constraints based on sensitivity analysis:")
        for rc in redundant_constraints:
            print(rc)

 
    def identify_redundant_constraints_deactivation(self):
        """Identify potential redundant constraints by deactivating them one by one."""
        solver = SolverFactory('ipopt')
        original_objective_value = self.model.objective.expr()

        redundant_constraints = []
        for c in self.model.component_objects(ctype=Constraint, active=True):
            for index in c:
                c[index].deactivate()
                solver.solve(self.model)
                if abs(original_objective_value - self.model.objective.expr()) < 1e-6:  # Small threshold
                    redundant_constraints.append(c[index])
                c[index].activate()

        print("Potential redundant constraints based on deactivation method:")
        for rc in redundant_constraints:
            print(rc)

            
    def set_objective(self):
        """Define the objective function for the model."""
        self.model.objective = Objective(expr=self.model.s21['Hydrogen'], sense=minimise)
        
    def solve(self):
        solver = SolverFactory('ipopt')
        solver.options['constr_viol_tol'] = 1e-8
        solver.options['acceptable_constr_viol_tol'] = 1e-8
        solver.solve(self.model, tee=True)
#         if self.model.solver.termination_condition == TerminationCondition.infeasible:
#             self.refine_conflict()

    def fetch_value(self, var):
        """Fetch the value of a variable and round it."""
        val = var.value
        if val is None or val < 0:
            return 0.0
        return round(val, 4)  

    def generate_stream_data(self, stream_name):
        """Generate molar flow rates for a given stream."""
        stream_index = int(stream_name[1:])  # Extract the integer value from the stream name

        if stream_name in ['s15']:
            s_flow = self.model.params[stream_name.upper()]
            molar_flow_rates = [s_flow * self.model.params[f'{stream_name.upper()}_{component}'] for component in self.components]
        else:
            molar_flow_rates = [self.fetch_value(getattr(self.model, f's{stream_index}')[component]) for component in self.components]

        return molar_flow_rates

#     def generate_stream_table(self):
#         """Generate a table with molar flow rates of each component in each stream."""
#         data = []  # This will store rows of data which will be used to create DataFrame

#         # For each stream, including s14, s15, and skipping s16 to s18
#         for i in list(range(15, 15)) + list(range(19, 39)):  
#             stream_name = f's{i}'
#             data.append(self.generate_stream_data(stream_name))

#         # Creating DataFrame
#         stream_names = [f's{i}' for i in list(range(15, 15)) + list(range(19, 39))]
#         df = pd.DataFrame(data, columns=self.components, index=stream_names)
#         return df
    def generate_stream_table(self):
        """Generate a table with molar flow rates of each component in each stream."""
        data = []  # This will store rows of data which will be used to create DataFrame

        # For each stream, including s14, s15, and skipping s16 to s18, s22, s23, and s28
        streams_to_skip = [16, 17, 18, 22, 23, 28]
        for i in list(range(15, 15)) + list(range(19, 39)):  
            if i not in streams_to_skip:
                stream_name = f's{i}'
                data.append(self.generate_stream_data(stream_name))

        # Creating DataFrame
        stream_names = [f's{i}' for i in list(range(15, 15)) + list(range(19, 39)) if i not in streams_to_skip]
        df = pd.DataFrame(data, columns=self.components, index=stream_names)
        return df

    def display_results(self):
        # Helper function to fetch the value
        def fetch_value(var):
            val = var.value
            if val is None or val < 0:
                return 0.0
            return val

        # Helper function to display and write a set of results
        def display_and_write(file, header, results):
            file.write(header + '\n')
            print(header)
            for result in results:
                file.write(result + '\n')
                print(result)

        # Specify the filename where you want to store the results
        filename = "model_results.txt"
        model = self.model 

        with open(filename, 'w') as file:
            # Write the header to the file
            file.write("Results:\n")
            print("Results:")

            # Stream S Results
            s_results = [
                f"S{i}: {fetch_value(getattr(model, f'S{i}'))}" for i in range(19, 39)
            ]
            # Add results for S14 and S15 from parameters
            s_results.insert(1, f"S15: {model.params['S15']}")
            display_and_write(file, "\nStream S Results:", s_results)

            # Component molar flow rate results for Streams S19 to S41
#             components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']
#             molar_flowRate_results = [
#                 f"Molar Flow rate of[{component}] in S{i}: {fetch_value(getattr(model, f's{i}')[component])}" 
#                 for i in range(19, 39) for component in components
#             ]
#             # Add composition results for S15 from parameters
#             for component in components:
#                 molar_flowRate_results.insert(1, f"Molar Flow rate of[{component}] in S15: {model.params['S15'] * model.params[f'S15_{component}']}")
#             display_and_write(file, "\nComponent Flow Rate Results:", molar_flowRate_results)

           # Component molar flow rate results for Streams S19 to S41, excluding S22, S23, and S28
            streams_to_skip = [22, 23, 28]
            components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']
            molar_flowRate_results = [
                f"Molar Flow rate of[{component}] in S{i}: {fetch_value(getattr(model, f's{i}')[component])}" 
                for i in range(19, 39) if i not in streams_to_skip for component in components
            ]
            # Add composition results for S15 from parameters
            for component in components:
                molar_flowRate_results.insert(1, f"Molar Flow rate of[{component}] in S15: {model.params['S15'] * model.params[f'S15_{component}']}")
            display_and_write(file, "\nComponent Flow Rate Results:", molar_flowRate_results)

            # Generate the stream table
            stream_table_df = self.generate_stream_table()
            stream_table_str = stream_table_df.to_string()

            # Print the stream table to the terminal
            print("\nStream Table:")
            print(stream_table_str)

            # Write the stream table to the file
            file.write("\nStream Table:\n")
            file.write(stream_table_str)
            file.write("\n")

        # Print to console that results are written to the file
        print(f"\nResults have been written to {filename}")

