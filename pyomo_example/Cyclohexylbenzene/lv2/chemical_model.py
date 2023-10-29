from pyomo.environ import ConcreteModel, SolverFactory, Objective, maximize, Constraint, Var, Suffix
from parameters import Parameters
from variables import Variables
from constraints import Constraints
import pandas as pd
from pyomo.opt import TerminationCondition

class ChemicalModel:
    
    def __init__(self):
        self.model = ConcreteModel()
        self.components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']
        self.parameters = Parameters()
        
        # Set params as an attribute of model
        self.model.params = self.parameters.params
        
        self.variables = Variables(self.model, self.components, self.model.params)
        self.constraints = Constraints(self.model, self.model.params)
        
    def solve_with_tearing(self, max_iterations=100, tolerance=1e-6):
        # Define tearing streams
        tearing_streams = ['S22', 'S23']

        # Initial guess for tearing streams
        if not hasattr(self.model, 'S22'):
            self.model.S22 = Var(initialize=10.0)
        if not hasattr(self.model, 'S23'):
            self.model.S23 = Var(initialize=10.0)

        # Solver setup
        solver = SolverFactory('ipopt')
        solver.options["tol"] = 1e-8
        solver.options["max_iter"] =5000
        solver.options["print_level"] = 5

        # Check if dual Suffix already exists, if so, delete it
        if hasattr(self.model, 'dual'):
            self.model.del_component(self.model.dual)

        # Now, add the dual Suffix
        self.model.dual = Suffix(direction=Suffix.IMPORT)

        # Store previous values for convergence check
        previous_values = {stream: getattr(self.model, stream).value for stream in tearing_streams}
        
        # Iterative solution
        for iteration in range(max_iterations):
            results = solver.solve(self.model)

            # Check for solver errors
            if results.solver.termination_condition != TerminationCondition.optimal:
                print(f"Solver error message: {results.solver.message}")
                raise ValueError(f"Solver did not converge in iteration {iteration + 1}!")

            # Feedback mechanism: Update the values of S22 and S23 based on the auxiliary variables
            self.model.S22.set_value(self.model.aux_S22.value)
            self.model.S23.set_value(self.model.aux_S23.value)

            # Check for convergence
            deviations = []
        
            for stream in tearing_streams:
                current_value = getattr(self.model, stream).value
                deviation = abs(current_value - previous_values[stream])
                deviations.append(deviation)

                # Update previous value for next iteration
                previous_values[stream] = current_value

            # If all deviations are below the tolerance, we have converged
            if all(dev < tolerance for dev in deviations):
                print(f"Converged in {iteration + 1} iterations!")
                return

        print("Maximum iterations reached without convergence!")

    def test_initial_values(self, s22_range, s23_range):
            successful_initializations = []
            failed_initializations = []

            for init_s22 in s22_range:
                for init_s23 in s23_range:
                    # Set initial values
                    self.model.S22.set_value(init_s22)
                    self.model.S23.set_value(init_s23)

                    try:
                        self.solve_with_tearing()
                        successful_initializations.append((init_s22, init_s23))
                    except ValueError as e:
                        failed_initializations.append((init_s22, init_s23))

            return successful_initializations, failed_initializations
        
        
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
        self.model.objective = Objective(expr=self.model.s28['Cyclohexylbenzene'], sense=maximize)
        
    def solve(self):
        solver = SolverFactory('glpk')
#         solver.options['constr_viol_tol'] = 1e-8
#         solver.options['acceptable_constr_viol_tol'] = 1e-8

        solver.solve(self.model, tee=True)

    def fetch_value(self, var):
        """Fetch the value of a variable and round it."""
        val = var.value
        if val is None or val < 0:
            return 0.0
        return round(val, 4)  

    
    def generate_stream_data(self, stream_name):
        """Generate molar flow rates for a given stream."""
        stream_index = int(stream_name[1:])  # Extract the integer value from the stream name

        if stream_name in ['s20', 's21']:
            s_flow = self.model.params[stream_name.upper()]
            molar_flow_rates = [s_flow * self.model.params[f'{stream_name.upper()}_{component}'] for component in self.components]
        else:
            molar_flow_rates = [self.fetch_value(getattr(self.model, f's{stream_index}')[component]) for component in self.components]

        return molar_flow_rates

    def generate_stream_table(self):
        """Generate a table with molar flow rates of each component in each stream."""
        data = []  # This will store rows of data which will be used to create DataFrame

        # For each stream
        for i in range(20, 34):  # Adjusted the range to start from S8
            stream_name = f's{i}'
            data.append(self.generate_stream_data(stream_name))

        # Creating DataFrame
        stream_names = [f's{i}' for i in range(20, 34)]  # Adjusted the range to start from S8
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
                f"S{i}: {fetch_value(getattr(model, f'S{i}'))}" for i in range(22, 34)
            ]
            # Add results for S8 and S9 from parameters
            s_results.insert(0, f"S20: {model.params['S20']}")
            s_results.insert(1, f"S21: {model.params['S21']}")
            display_and_write(file, "\nStream S Results:", s_results)

            # Component molar flow rate results for Streams S10 to S18
            components = ['Hydrogen', 'Methane', 'Benzene', 'Cyclohexane', 'Cyclohexene', 'Cyclohexylbenzene']
            molar_flowRate_results = [
                f"Molar Flow rate of[{component}] in S{i}: {fetch_value(getattr(model, f's{i}')[component])}" 
                for i in range(22, 34) for component in components
            ]
            # Add composition results for S8 and S9 from parameters
            for component in components:
                molar_flowRate_results.insert(0, f"Molar Flow rate of[{component}] in S20: {model.params['S20'] * model.params[f'S20_{component}']}")
                molar_flowRate_results.insert(1, f"Molar Flow rate of[{component}] in S21: {model.params['S21'] * model.params[f'S21_{component}']}")
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

