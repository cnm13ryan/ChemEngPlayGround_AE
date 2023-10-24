from pyomo.environ import *

def define_sets(model):
    model.stm = Set(initialize=[
        'Feed1', 'Feed2', 'Mixeff', 'Reacteff', 'Dist1top',
        'Dist1bot', 'Purge', 'LiqRecycle', 'Prod', 'Byprod'
    ], doc='Process Streams')
    
    model.comp = Set(initialize=[
        'E', 'P', 'Bz', 'Tu', 'EB', 'DEB'
    ], doc='Process Components')
    
    return model  # Ensure you return the model
