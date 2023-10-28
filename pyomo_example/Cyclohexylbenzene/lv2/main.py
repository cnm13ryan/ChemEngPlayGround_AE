from chemical_model import ChemicalModel
import pandas as pd

if __name__ == "__main__":
    chemical_model = ChemicalModel()
    num_eq, num_var = chemical_model.count_equations_and_unknowns()
    
    
    
    
#     s22_range = [i for i in range(10, 100, 10)]  # Example range: 10, 20, ..., 90
#     s23_range = [i for i in range(10, 100, 10)]  # Example range: 10, 20, ..., 90

#     successful, failed = chemical_model.test_initial_values(s22_range, s23_range)

#     print("Successful initializations:", successful)
#     print("Failed initializations:", failed)
    chemical_model.identify_redundant_constraints_sensitivity()
    chemical_model.identify_redundant_constraints_deactivation()        
    #chemical_model.solve_with_tearing()
    #chemical_model.display_results()
    #chemical_model.generate_stream_table()
    
    
    if (num_eq == num_var):
        print("DOF = 0")
        
    if (num_eq != num_var):
        print(f"DOF = {num_var - num_eq}")
#         chemical_model.identify_redundant_constraints_sensitivity()
#         chemical_model.identify_redundant_constraints_deactivation()