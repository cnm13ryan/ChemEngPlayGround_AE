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
        solver = SolverFactory('ipopt')
        solver.options['constr_viol_tol'] = 1e-8
        solver.options['acceptable_constr_viol_tol'] = 1e-8

        solver.solve(self.model, tee=True)

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
                f"S1: {model.params['S1']}",
                f"S2: {fetch_value(model.S2)}",
                f"S3: {fetch_value(model.S3)}",
                f"S4: {fetch_value(model.S4)}",
                f"S5: {fetch_value(model.S5)}",
                f"S6: {fetch_value(model.S6)}",
                f"S7: {fetch_value(model.S7)}"
            ]
            display_and_write(file, "\nStream S Results:", s_results)

            # d Composition Results
            components = ['Benzene', 'Toluene', 'OrthoXylene', 'MetaXylene', 'Ethylbenzene', 'ParaXylene', 'TwoMethylbutane']
            d_results = [
                f"d1[{component}]: {fetch_value(model.d1[component])}" for component in components
            ] + [
                f"d2[{component}]: {fetch_value(model.d2[component])}" for component in components
            ] + [
                f"d3[{component}]: {fetch_value(model.d3[component])}" for component in components
            ]
            display_and_write(file, "\nd Composition Results:", d_results)

            # b Composition Results
            b_results = [
                f"b1[{component}]: {fetch_value(model.b1[component])}" for component in components
            ] + [
                f"b2[{component}]: {fetch_value(model.b2[component])}" for component in components
            ] + [
                f"b3[{component}]: {fetch_value(model.b3[component])}" for component in components
            ]
            display_and_write(file, "\nb Composition Results:", b_results)

            # Generate the stream table
            stream_table_df = self.generate_stream_table()
            stream_table_str = stream_table_df.to_string()

            # Write the stream table to the file
            file.write("\nStream Table:\n")
            file.write(stream_table_str)
            file.write("\n")

        # Print to console that results are written to the file
        print(f"\nResults have been written to {filename}")


    def generate_stream_table(self):
        """Generate a table with molar flow rates of each component in each stream."""

        def fetch_value(var):
            val = var.value
            if val is None or val < 0:
                return 0.0
            return round(val, 4)  # Rounding to 4 decimal digits

        components = self.components
        data = []  # This will store rows of data which will be used to create DataFrame

        # For S1 (since it's defined in parameters)
        s1_flow = self.model.params['S1']
        s1_compositions = [self.model.params[f'z1_{component}'] for component in components]
        s1_molar_flow_rates = [s1_flow * comp for comp in s1_compositions]
        data.append(s1_molar_flow_rates)

        # For other S streams
        for i in range(2, 8):  # Start from S2 since we've already handled S1
            stream_name = "S" + str(i)
            s_flow = fetch_value(getattr(self.model, stream_name))

            if i % 2 == 0:  # Even numbered S streams
                stream_name = "d" + str(i//2)
                compositions = [fetch_value(getattr(self.model, stream_name)[component]) for component in components]
            else:  # Odd numbered S streams
                stream_name = "b" + str(i//2)
                compositions = [fetch_value(getattr(self.model, stream_name)[component]) for component in components]

            molar_flow_rates = [s_flow * comp for comp in compositions]
            data.append(molar_flow_rates)

        # Creating DataFrame
        stream_names = [f'S{i}' for i in range(1, 8)]
        df = pd.DataFrame(data, columns=components, index=stream_names)
        print(df)

        return df
