from pyomo.environ import ConcreteModel, SolverFactory
from parameters import Parameters
from variables import Variables
from constraints import Constraints
import pandas as pd
from pyomo.environ import Objective, maximize

class ChemicalModel:
    
    def __init__(self):
        self.model = ConcreteModel()
        self.components = ['Hydrogen', 'Methane', 'Benzene', 'Toluene', 'ParaXylene', 'Diphenyl']
        self.parameters = Parameters()
        
        
        # Set params as an attribute of model
        self.model.params = self.parameters.params
        
        self.variables = Variables(self.model, self.components, self.model.params)
        self.constraints = Constraints(self.model, self.model.params)
        
        # Set up the objective function
        self.set_objective()
        
        # Initialize tearing variables for s13 and s17
        self.tearing_streams = ['s13', 's17', 'S13', 'S17']
        self.tearing_values = {
            's13': {component: 0.00001 for component in self.components},
            's17': {component: 0.00001 for component in self.components},
            'S13': 1000,
            'S17': 200
        }

        
    def solve_with_tearing(self):
        # Initial solve
        self.solve()

        # Define the tearing streams and initialize their values
        self.tearing_streams = ['s13', 's17']
        self.tearing_values = {
            's13': {component: 500 for component in self.components},
            's17': {component: 50 for component in self.components}
        }

        # Define a tolerance for the difference between successive values
        tolerance = 1e-4

        # Maximum number of iterations
        max_iterations = 100

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



    def set_objective(self):
        """Define the objective function for the model."""
        self.model.objective = Objective(expr=self.model.s13['Hydrogen'], sense=maximize)
        self.model.objective = Objective(expr=self.model.s15['Benzene'], sense=maximize)
        
    def solve(self):
        solver = SolverFactory('ipopt')
        solver.options['constr_viol_tol'] = 1e-8
        solver.options['acceptable_constr_viol_tol'] = 1e-8

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

        if stream_name in ['s8', 's9']:
            s_flow = self.model.params[stream_name.upper()]
            molar_flow_rates = [s_flow * self.model.params[f'{stream_name.upper()}_{component}'] for component in self.components]
        else:
            molar_flow_rates = [self.fetch_value(getattr(self.model, f's{stream_index}')[component]) for component in self.components]

        return molar_flow_rates

    def generate_stream_table(self):
        """Generate a table with molar flow rates of each component in each stream."""
        data = []  # This will store rows of data which will be used to create DataFrame

        # For each stream
        for i in range(8, 19):  # Adjusted the range to start from S8
            stream_name = f's{i}'
            data.append(self.generate_stream_data(stream_name))

        # Creating DataFrame
        stream_names = [f's{i}' for i in range(8, 19)]  # Adjusted the range to start from S8
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
                f"S{i}: {fetch_value(getattr(model, f'S{i}'))}" for i in range(10, 19)
            ]
            # Add results for S8 and S9 from parameters
            s_results.insert(0, f"S8: {model.params['S8']}")
            s_results.insert(1, f"S9: {model.params['S9']}")
            display_and_write(file, "\nStream S Results:", s_results)

            # Component molar flow rate results for Streams S10 to S18
            components = ['Hydrogen', 'Methane', 'Benzene', 'Toluene', 'ParaXylene', 'Diphenyl']
            molar_flowRate_results = [
                f"Molar Flow rate of[{component}] in S{i}: {fetch_value(getattr(model, f's{i}')[component])}" 
                for i in range(10, 19) for component in components
            ]
            # Add composition results for S8 and S9 from parameters
            for component in components:
                molar_flowRate_results.insert(0, f"Molar Flow rate of[{component}] in S8: {model.params['S8'] * model.params[f'S8_{component}']}")
                molar_flowRate_results.insert(1, f"Molar Flow rate of[{component}] in S9: {model.params['S9'] * model.params[f'S9_{component}']}")
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
