#%%
#from SSOPDataBase import wGeneralDBService
from SSOPDataBase import gCentralComponentDB as CC
from datetime import datetime

#wGeneralDBService.launchMqttService(topic = "SSOPCloud/1")

# %%

date = datetime.now().isoformat()

data = {
    'Service': "Self_Consumption",
    'timee': date,
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

# %%
CC.newPayload("Oi","ID","inverterData",data)




# %%
