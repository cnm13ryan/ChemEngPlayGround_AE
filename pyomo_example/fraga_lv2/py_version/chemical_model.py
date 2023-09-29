from pyomo.environ import ConcreteModel, SolverFactory
from parameters import Parameters
from variables import Variables
from constraints import Constraints

class ChemicalModel:
    def __init__(self):
        self.model = ConcreteModel()
        self.components = ['E', 'P', 'Bz', 'Tu', 'EB', 'DEB']
        self.parameters = Parameters()
        
        # Set params as an attribute of model
        self.model.params = self.parameters.params
        
        self.variables = Variables(self.model, self.components, self.model.params)
        self.constraints = Constraints(self.model, self.model.params)

    def solve(self):
        solver = SolverFactory('glpk')
        solver.solve(self.model, tee=True)

    def display_results(self):
        # Specify the filename where you want to store the results
        filename = "model_results.txt"
        model = self.model 
        # Open the file in write mode
        with open(filename, 'w') as file:
            # Write the results to the file
            file.write("Results:\n")
            file.write(f"F2:  {model.F2.value}\n")
            file.write(f"F1:  {model.F1.value}\n")
            file.write(f"xi1: {model.xi1.value}\n")
            file.write(f"xi2: {model.xi2.value}\n")
            file.write(f"xi3: {model.xi3.value}\n")
            file.write(f"BPD: {model.BPD.value}\n")
            file.write(f"PG:  {model.PG.value}\n")
        
        # Print to console that results are written to the file
        print(f"Results have been written to {filename}")

