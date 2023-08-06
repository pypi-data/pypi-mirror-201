
#%%
import mqtt_SSOP.clientPublisher as Pub
from datetime import datetime



date = datetime.now()

date = str(date)

data = {

    "credentials" : {
        "ID" : "pedro",
        "password" : "passss"
    },
    "dataType" : "invertorData",
    "data" : 
        {       
            'Service': 'Self_Consumption',
            'time': date,
            'Begin': date,
            'PCon': "1",
            'PPV': "1",
            'PReqInv': "1",
            'PMeaInv': "1",
            'PReqBat': "1",
            'PMeaBat': "1",
            'SoC': "1",
            'PCMax': "1",
            'PDMax': "1",
    },  
}
#%%
status = Pub.publish("ssop/123",data, "Client number 10")
if status == 0:
    print("sent!")
else:
    print(f"not sent! ERROR: {status}")

# %%
