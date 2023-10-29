from chemical_model import ChemicalModel
import pandas as pd

if __name__ == "__main__":
    chemical_model = ChemicalModel()
    num_eq, num_var = chemical_model.count_equations_and_unknowns()
       
    if (num_eq == num_var):
        print("DOF = 0")
        
    if (num_eq != num_var):
        print(f"DOF = {num_var - num_eq}")   
        
        
#     # Define the range of initial values you want to test
#     s13_range = [i for i in range(0, 50, 10)]  # Example range: 10, 20, ..., 90
#     s17_range = [i for i in range(0, 50, 10)]  # Example range: 10, 20, ..., 90


#     chemical_model = ChemicalModel()
#     optimal_values = chemical_model.find_optimal_initial_values(s13_range, s17_range)
#     print("Optimal initial values:", optimal_values)

        
#     chemical_model.identify_redundant_constraints_sensitivity()
#     chemical_model.identify_redundant_constraints_deactivation()        

    chemical_model.solve()
    chemical_model.display_results()
    chemical_model.generate_stream_table()
        
#     chemical_model.solve_with_tearing()
#     chemical_model.display_results()
#     chemical_model.generate_stream_table()
    
    

