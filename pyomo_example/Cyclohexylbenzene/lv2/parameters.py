class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 15 (Hydrogen, Methane, and Benzene)
            'S15': 345.14, # [kmol / hr]
            
            # Molar Composition of Stream 15
            'S15_Hydrogen': 0.8867,
            'S15_Methane': 0.0965,
            'S15_Benzene': 0.01677,
            'S15_Cyclohexane': 0.0 ,
            'S15_Cyclohexene': 0.0,
            'S15_Cyclohexylbenzene': 0.0,            
                        
            
            # Fractional recoveries of HK/LK (Distillation Column 7)
            'FR_S21_LK': 0.98,
            'FR_S20_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 8)
            'FR_S22_LK': 0.98,
            'FR_S23_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 9)
            'FR_S25_LK': 0.98,
            'FR_S26_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 10)
            'FR_S32_LK': 0.98,
            'FR_S33_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 11)
            'FR_S34_LK': 0.98,
            'FR_S35_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 12)
            'FR_S36_LK': 0.98,
            'FR_S37_HK': 0.95,
                    
            
            # Conversion of benzene at PFR (at the maximum yield of CHE):
            'X1': 0.646,
            
            # Conversion of Cyclohexene at PBR:
            'X2': 0.468,            
            
            # Selectivity of Cyclohexene (CHE) (at the maximum yield of CHE): 
            'S1': 0.669,
            
            # Selectivity of Cyclohexylbenzene (CHB):
            'S2': 0.984            
            
        }