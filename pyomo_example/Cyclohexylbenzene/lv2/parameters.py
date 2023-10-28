class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 20 (Benzene and Methane)
            'S20': 38.3, # to the power of 10**6 [kmol / hr]
            
            # Molar flow rate of Stream 21 (Hydrogen feed stream) Ratio of H:B = 1:5
            'S21': 7.66, # to the power of 10**6 [kmol / hr] 
            
            # Molar Composition of Stream 20
            'S20_Hydrogen': 0.0,
            'S20_Methane': 0.001,
            'S20_Benzene': 0.999,
            'S20_Cyclohexane': 0.0 ,
            'S20_Cyclohexene': 0.0,
            'S20_Cyclohexylbenzene': 0.0,            
            
            # Molar composition of Stream 21
            'S21_Hydrogen': 1.0,
            'S21_Methane': 0.0,
            'S21_Benzene': 0.0,
            'S21_Cyclohexane': 0.0 ,
            'S21_Cyclohexene': 0.0,
            'S21_Cyclohexylbenzene': 0.0,  
            
            # Fractional recoveries of HK/LK
            'FR_S24_LK': 0.98,
            'FR_S23_HK': 0.95,
            
            'FR_S29_LK': 0.98,
            'FR_S28_HK': 0.95,
            
            'FR_S31_LK': 0.98,
            'FR_S30_HK': 0.95,
      
            'FR_S33_LK': 0.98,
            'FR_S32_HK': 0.95,           
            
            
            # Conversion of benzene at PFR (at the maximum yield of CHE):
            'X1': 0.646,
            
            # Conversion of Cyclohexene at PBR:
            'X2': 0.468,            
            
            # Selectivity of Cyclohexene (CHE) (at the maximum yield of CHE): 
            'S1': 0.669,
            
            # Selectivity of Cyclohexylbenzene (CHB):
            'S2': 0.984            
            
        }