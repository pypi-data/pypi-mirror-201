#%%
import SSOPInvertorDataBase.gCentralComponentDB as CC
from datetime import datetime

#Test to run and examples of data to be sent into the functions 
#
#%%
date = datetime.now().isoformat()

data = {
    'Service': "Self_Consumption",
    'time': date,
    'Begin': date,
    'PCon': 1,
    'PPV': 1,
    'PReqInv': 1,
    'PMeaInv': 1,
    'PReqBat': 1,
    'PMeaBat': 1,
    'SoC': 1,
    'PCMax': 1,
    'PDMax': 1,
}



print(CC.table2dict( CC.listData()))
