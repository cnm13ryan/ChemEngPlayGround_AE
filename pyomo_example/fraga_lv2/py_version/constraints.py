from pyomo.environ import Constraint
from math import log

class Constraints:
    def __init__(self, model, parameters):
        self.define_constraints(model, parameters)

    def define_constraints(self, model, parameters):
        model.selectivitydependence = Constraint(rule=self.selectivitydependence_rule)
        model.conversiondependence = Constraint(rule=self.conversiondependence_rule)
        # Define other constraints similarly

    def selectivitydependence_rule(self, model):
        return model.params['t'] * (model.S - 0.06397) == 371.6

    def conversiondependence_rule(self, model):
        return model.x + 0.6624 == 0.23303 * log(model.params['t'])
        
    def selectivitydefinition_rule(self, model):
        """Defines the selectivity definition rule."""
        return model.S * model.xi2 == model.xi1 - model.xi2 + model.xi3

    def conversiondefinition_rule(self, model):
        """Defines the conversion definition rule."""
        return model.x * (model.F2 + model.F1) == (model.params['yPE'] + model.yPBz) * model.PG

    def balanceTu_rule(self, model):
        """Defines the balance Tu rule."""
        return model.F2 * model.params['yTu'] == model.xi3

    def balanceBz_rule(self, model):
        """Defines the balance Bz rule."""
        return model.F2 * (1 - model.params['yTu']) - model.xi1 == model.yPBz * model.PG

    def balanceE_rule(self, model):
        """Defines the balance E rule."""
        return model.F1 * model.params['yFE'] - model.xi1 - model.xi2 - 2 * model.xi3 == model.params['yPE'] * model.PG

    def balanceP_rule(self, model):
        """Defines the balance P rule."""
        return model.xi3 == (1 - model.params['yPE'] - model.yPBz) * model.PG

    def balanceDEB_rule(self, model):
        """Defines the balance DEB rule."""
        return model.xi2 == model.params['yDEB'] * model.BPD + (1 - model.params['yEB']) * model.params['PD']

    def balanceEB_rule(self, model):
        """Defines the balance EB rule."""
        return model.xi1 - model.xi2 + model.xi3 == model.params['yEB'] * model.params['PD'] + (1 - model.params['yDEB']) * model.BPD

    def matbal_rule(self, model):
        """Defines the matbal rule."""
        return model.F == model.PG + model.params['PD'] + model.BPD

    def Ecomp_rule(self, model):
        """Defines the Ecomp rule."""
        return model.F * model.z['E'] == model.params['yPE'] * model.PG

    def Pcomp_rule(self, model):
        """Defines the Pcomp rule."""
        return model.F * model.z['P'] == (1 - model.params['yPE'] - model.yPBz) * model.PG

    def Bzcomp_rule(self, model):
        """Defines the Bzcomp rule."""
        return model.F * model.z['Bz'] == model.yPBz * model.PG

    def EBcomp_rule(self, model):
        """Defines the EBcomp rule."""
        return model.F * model.z['EB'] == model.params['yEB'] * model.params['PD'] + (1 - model.params['yDEB']) * model.BPD

    def DEBcomp_rule(self, model):
        """Defines the DEBcomp rule."""
        return model.F * model.z['DEB'] == model.params['yDEB'] * model.BPD + (1 - model.params['yEB']) * model.params['PD']

    def Tucomp_rule(self, model):
        """Defines the Tucomp rule."""
        return model.z['Tu'] == 0
