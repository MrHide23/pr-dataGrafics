
import pandas as pd
import re
import matplotlib.pyplot as plt


key=["data_0_5","data_1","data_5","data_10","data_50","data_100","data_150","data_200","data_250", "data_300", "data_500"]
thr_tot=[]
off_tot=[]

for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    thr=[]
    off=[]

    for i in range(0,9):
      filter:str=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{i}.ethg$o[0].channel"), "value"].iloc[0] 

      s:str = data.loc[(data["type"] == "param") & (data["module"] == f"ConfiguratorA.host0.app[0]") & (data["name"] == "sendInterval"), "value"].iloc[0]
      m:str = data.loc[(data["type"] == "param") & (data["module"] == f"ConfiguratorA.host0.app[0]") & (data["name"] == "messageLength"), "value"].iloc[0]
      header = 46 # UDP+IPv4+Ethernet=46 bytes
      
      send_int = float(re.sub(r"[^\d.]", "", s))  # Elimina todo excepto números y puntos
      mess_len = float(re.sub(r"[^\d.]", "", m))  # Elimina unidades como 'B' o 's'
      off.append((mess_len + header)*8 / send_int) 
      thr.append(float(re.sub(r"[^\d.]", "", filter))/off[i])

    thr_tot.append(sum(thr)/len(thr))
    
# Graficar el throughput total
plt.show()
plt.plot(key, thr_tot, label="Throughput All", color="red")
plt.xlabel("Nº pq/seq")
plt.ylabel("Throughput/Offed Trafic")
plt.title("Throughput of the NET")
plt.legend()
plt.grid(True)
plt.show()


# %%
