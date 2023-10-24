class Parameters:
    def __init__(self):
        self.params = {
            # Molar flow rate of Stream 1 (Feed inlet)
            'S1': 288.2,
            
            # Molar composition of Stream 1 (Feed inlet)
            'z1_Benzene': 0.2540,
            'z1_Toluene': 0.5840,
            'z1_OrthoXylene': 0.1374,
            'z1_MetaXylene': 0.0244,
            'z1_Ethylbenzene': 0.0,
            'z1_ParaXylene': 0.0001,
            'z1_TwoMethylbutane': 0.0001,
            
            # Fractional recoveries of HK/LK
            'FR_S2_LK': 0.98,
            'FR_S3_HK': 0.95,
            'FR_S4_LK': 0.98,
            'FR_S5_HK': 0.95,
            'FR_S6_LK': 0.98,
            'FR_S7_HK': 0.95,
            
        }