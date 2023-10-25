from pyomo.environ import *

def define_sets(model):
    model.stm = Set(initialize=[
        'S8', 'S9', 'S10', 'S11', 'S12',
        'S13', 'S14', 'S115', 'S16', 'S17', 
        'S18'
    ], doc='Process Streams')
    
    model.comp = Set(initialize=[
        'Hydrogen', 'Methane', 'Benzene', 
        'Toluene', 'ParaXylene', 'Diphenyl'
    ], doc='Process Components')
    
    return model  
