from pyomo.environ import ConcreteModel, SolverFactory
from parameters import Parameters
from variables import Variables
from constraints import Constraints
import pandas as pd

class ChemicalModel:
    
    def __init__(self):
        self.model = ConcreteModel()
        self.components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']
        self.parameters = Parameters()
        
        # Set params as an attribute of model
        self.model.params = self.parameters.params
        
        self.variables = Variables(self.model, self.components, self.model.params)
        self.constraints = Constraints(self.model, self.model.params)
        
        
        
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

        if stream_name in ['s1']:
            s_flow = self.model.params[stream_name.upper()]
            molar_flow_rates = [s_flow * self.model.params[f'{stream_name.upper()}_{component}'] for component in self.components]
        else:
            molar_flow_rates = [self.fetch_value(getattr(self.model, f's{stream_index}')[component]) for component in self.components]

        return molar_flow_rates

    def generate_stream_table(self):
        """Generate a table with molar flow rates of each component in each stream."""
        data = []  # This will store rows of data which will be used to create DataFrame

        # For each stream
        for i in range(1, 8):  # Adjusted the range to start from S1
            stream_name = f's{i}'
            data.append(self.generate_stream_data(stream_name))

        # Creating DataFrame
        stream_names = [f's{i}' for i in range(1, 8)]  # Adjusted the range to start from S1
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
                f"S{i}: {fetch_value(getattr(model, f'S{i}'))}" for i in range(2, 8)
            ]
            # Add results for S1 from parameters
            s_results.insert(0, f"S1: {model.params['S1']}")
            display_and_write(file, "\nStream S Results:", s_results)

            # Component molar flow rate results for Streams S10 to S18
            components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']
            
            molar_flowRate_results = [
                f"Molar Flow rate of[{component}] in S{i}: {fetch_value(getattr(model, f's{i}')[component])}" 
                for i in range(2, 8) for component in components
            ]
            # Add composition results for S1 from parameters
            for component in components:
                molar_flowRate_results.insert(0, f"Molar Flow rate of[{component}] in S1: {model.params['S1'] * model.params[f'S1_{component}']}")
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
