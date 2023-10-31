class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 15 (Hydrogen, Methane, and Benzene)
            'S15': 39.1038, # [kmol / hr]
            
            # Molar Composition of Stream 15
            'S15_Hydrogen': 0.0,
            'S15_Methane': 0.8519,
            'S15_Benzene': 0.1481,
            'S15_Cyclohexane': 0.0 ,
            'S15_Cyclohexene': 0.0,
            'S15_Cyclohexylbenzene': 0.0,  
            
            # Molar Composition of Stream 21
            'S21_Hydrogen': 1.0,
            'S21_Methane': 0.0,
            'S21_Benzene': 0.0,
            'S21_Cyclohexane': 0.0 ,
            'S21_Cyclohexene': 0.0,
            'S21_Cyclohexylbenzene': 0.0,              
                        
            
            # Fractional recoveries of HK/LK (Distillation Column 7)
            'FR_S19_LK': 0.98,
            'FR_S20_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 8)
            'FR_S25_LK': 0.98,
            'FR_S29_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 9)
            'FR_S32_LK': 0.98,
            'FR_S33_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 10)
            'FR_S34_LK': 0.98,
            'FR_S35_HK': 0.95,
            
            # Fractional recoveries of HK/LK (Distillation Column 11)
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