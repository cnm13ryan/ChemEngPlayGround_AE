class Parameters:
    def __init__(self):
        self.params = {
            # Molar flow rate of Stream 1 (Feed inlet)
            'S1': 4542.305, # to the power of 10**6 [kmol / hr]
            
            # Molar composition of Stream 1 (Feed inlet)
            'S1_Benzene': 0.2540,
            'S1_Toluene': 0.5840,
            'S1_OrthoXylene': 0.1374,
            'S1_MetaXylene': 0.0244,
            'S1_Ethylbenzene': 0.0,
            'S1_ParaXylene': 0.0001,
            'S1_TwoMethylbutane': 0.0,
            
            # Fractional recoveries of HK/LK
            'FR_S2_LK': 0.98,
            'FR_S3_HK': 0.95,
            'FR_S4_LK': 0.98,
            'FR_S5_HK': 0.95,
            'FR_S6_LK': 0.98,
            'FR_S7_HK': 0.95,
            
        }
