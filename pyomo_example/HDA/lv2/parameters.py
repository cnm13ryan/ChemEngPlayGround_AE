class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 8 (Hydrogen Feed inlet)
            'S8': 12714.60, # to the power of 10**6 [kmol / hr]
            
            # Molar flow rate of Stream 9 (Toluene Feed inlet)
            'S9': 2542.92, # to the power of 10**6 [kmol / hr]
            
            # Molar Composition of Stream 8 (Pure Hydrogen)
            'S8_Hydrogen': 1,
            'S8_Methane': 0.0,
            'S8_Benzene': 0.0,
            'S8_Toluene': 0.0 ,
            'S8_ParaXylene': 0.0,
            'S8_Diphenyl': 0.0,            
            
            # Molar composition of Stream 9 (Combined Feed inlet of Stream 4 and 6)
            'S9_Hydrogen': 0.0,
            'S9_Methane': 0.0,
            'S9_Benzene': 0.90/100,
            'S9_Toluene': 0.991 ,
            'S9_ParaXylene': 0.0,
            'S9_Diphenyl': 0.0,
            
            # Fractional recoveries of HK/LK
            'FR_S11_LK': 0.98,
            'FR_S12_HK': 0.95,
            'FR_S15_LK': 0.98,
            'FR_S16_HK': 0.95,
            'FR_S17_LK': 0.98,
            'FR_S18_HK': 0.95,
            
            # Purge Composition (Hydrogen + Benzene)
            'yPH': 0.2,
            'yPB': 0.001,
            
            # Conversion: 
            'X': 0.7
            
        }