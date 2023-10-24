from chemical_model import ChemicalModel

if __name__ == "__main__":
    chemical_model = ChemicalModel()
    #print(chemical_model.params)
    chemical_model.solve()
    chemical_model.display_results()

