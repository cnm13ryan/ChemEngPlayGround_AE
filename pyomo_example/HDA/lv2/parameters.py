class Parameters:
    def __init__(self):
        self.params = {
            
            # Molar flow rate of Stream 8 (Hydrogen Feed inlet)
            'S8': 2543.1684 * 5, # to the power of 10**6 [kmol / hr] (5:1 ratio of H2 to Toluene)
            
            # Molar flow rate of Stream 9 (combined flow rate of Stream 4 and Stream 6) (Toluene Feed inlet)
            'S9': 2543.1684, # to the power of 10**6 [kmol / hr]
            
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
            'S9_Benzene': 0.91/100,
            'S9_Toluene': 99.09/100 ,
            'S9_ParaXylene': 0.0, # Trace (Ignore this)
            'S9_Diphenyl': 0.0,
            
            # Fractional recoveries of HK/LK
            'FR_S11_LK': 0.98,
            'FR_S12_HK': 0.95,
            'FR_S15_LK': 0.98,
            'FR_S16_HK': 0.95,
            'FR_S17_LK': 0.98,
            'FR_S18_HK': 0.95
            
        }