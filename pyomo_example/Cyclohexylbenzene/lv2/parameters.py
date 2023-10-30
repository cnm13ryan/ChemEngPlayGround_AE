class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 15 (Hydrogen, Methane, and Benzene)
            'S15': 1779.1836, # to the power of 10**6 [kmol / hr]
            
            # Molar flow rate of Stream 14 (Hydrogen and Methane)
            'S14': 13688.5771, # to the power of 10**6 [kmol / hr] 
            
            # Molar Composition of Stream 15
            'S15_Hydrogen': 0.82,
            'S15_Methane': 0.15,
            'S15_Benzene': 0.03,
            'S15_Cyclohexane': 0.0 ,
            'S15_Cyclohexene': 0.0,
            'S15_Cyclohexylbenzene': 0.0,            
            
            # Molar composition of Stream 14
            'S14_Hydrogen': 0.84,
            'S14_Methane': 0.16,
            'S14_Benzene': 0.0,
            'S14_Cyclohexane': 0.0 ,
            'S14_Cyclohexene': 0.0,
            'S14_Cyclohexylbenzene': 0.0,  
            
            # Fractional recoveries of HK/LK
            'FR_S19_LK': 0.98,
            'FR_S20_HK': 0.95,
            
            'FR_S22_LK': 0.98,
            'FR_S24_HK': 0.95,
            
            'FR_S25_LK': 0.98,
            'FR_S26_HK': 0.95,
            
            'FR_S28_LK': 0.98,
            'FR_S32_HK': 0.95,
            
            'FR_S36_LK': 0.98,
            'FR_S35_HK': 0.95,
            
            'FR_S37_LK': 0.98,
            'FR_S38_HK': 0.95,
      
            'FR_S40_LK': 0.98,
            'FR_S39_HK': 0.95,           
            
            
            # Conversion of benzene at PFR (at the maximum yield of CHE):
            'X1': 0.646,
            
            # Conversion of Cyclohexene at PBR:
            'X2': 0.468,            
            
            # Selectivity of Cyclohexene (CHE) (at the maximum yield of CHE): 
            'S1': 0.669,
            
            # Selectivity of Cyclohexylbenzene (CHB):
            'S2': 0.984            
            
        }