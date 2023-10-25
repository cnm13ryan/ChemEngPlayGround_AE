from chemical_model import ChemicalModel
import pandas as pd
from sets import define_sets

if __name__ == "__main__":
    chemical_model = ChemicalModel()
    chemical_model.solve()
    chemical_model.display_results()
    chemical_model.generate_stream_table()
    
    chemical_model.solve_with_tearing()
    chemical_model.display_results()
    chemical_model.generate_stream_table()
