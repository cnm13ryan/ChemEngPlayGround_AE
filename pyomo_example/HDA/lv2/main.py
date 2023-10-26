from chemical_model import ChemicalModel
import pandas as pd

if __name__ == "__main__":
    chemical_model = ChemicalModel()
    num_eq, num_var = chemical_model.count_equations_and_unknowns()
        
#     chemical_model.solve()
#     chemical_model.display_results()
#     chemical_model.generate_stream_table()
        
    chemical_model.solve_with_tearing()
    chemical_model.display_results()
    chemical_model.generate_stream_table()
    
    
    if (num_eq == num_var):
        print("DOF = 0")
        
    if (num_eq != num_var):
        print(f"DOF = {num_var - num_eq}")
        chemical_model.identify_redundant_constraints_sensitivity()
        chemical_model.identify_redundant_constraints_deactivation()