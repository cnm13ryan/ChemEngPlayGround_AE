from pyomo.environ import *
from math import log, sqrt

def define_parameters(model):
    # Static Parameters
    model.Price = Param(model.comp, initialize={
        'E': 0.05, 'P': 0, 'Tu': 0.10, 'Bz': 0.10, 'EB': 0.25, 'DEB': 0.10},
        doc='Price of each component [Euro per mol]')
    
    model.purityEB = Param(initialize=0.98, doc='Desired purity of product EB')
    model.OHPY = Param(initialize=8150, doc='Operating Hours Per Year')
    model.OSPY = Param(initialize=model.OHPY * 60 * 60, doc='Operating Seconds Per Year')
    model.alpha1 = Param(initialize=7.9323, doc='Relative volatilities wrt (Bz Light Key EB Heavy Key)')
    model.alpha2 = Param(initialize=469.26539, doc='Relative volatilities wrt (P Light Key Bz Heavy Key)')
    model.alpha3 = Param(initialize=8.81191, doc='Relative volatilities wrt (EB Light Key DEB Heavy Key)')
    model.errTol = Param(initialize=0.000001, doc='Error tolerance between LiqRecycle and tearLiqRecycle')
    model.cntTol = Param(initialize=100, doc='Iteration Counter tolerance')
    model.convfact = Param(initialize=1000 / 60 / 60, doc='Conversion factor from [kmol per hr] to [mol per s]')
    model.A = Param(initialize=0, mutable=True, doc='Heat Exchanger Area [sqm]')
    
    # Variable Parameter t
    model.t = Var(initialize=200, within=PositiveReals, doc='Residence time in Reactor [s]')
    
    # Derived Parameters
    def S_rule(model):
        return 371.60496 / model.t + 0.06379
    model.S = Param(initialize=S_rule, mutable=True, doc='Selectivity of EB to DEB [n.d]')
    
    def x_rule(model):
        return -0.66214 + 0.23303 * log(model.t)
    model.x = Param(initialize=x_rule, mutable=True, doc='Single pass conversion of EB [n.d]')
