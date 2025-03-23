import pandas as pd
import re
import matplotlib.pyplot as plt


key=["data_0_5","data_1","data_5","data_10","data_50","data_100","data_150","data_200","data_250", "data_300", "data_500", "data_800"]
thr_tot=[]
off_tot=[]

for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    thr={}
    off=[]

    

    for i in range(0,9):
      filter = data.loc[(data["type"] == "vector") & (data["module"] == f"ConfiguratorA.host{i}.app[1]"), ["vectime", "vecvalue"]]
      s:str = data.loc[(data["type"] == "param") & (data["module"] == f"ConfiguratorA.host0.app[0]") & (data["name"] == "sendInterval"), "value"].iloc[0]
      m:str = data.loc[(data["type"] == "param") & (data["module"] == f"ConfiguratorA.host0.app[0]") & (data["name"] == "messageLength"), "value"].iloc[0]
      header = 46 # UDP+IPv4+Ethernet=46 bytes
      send_int = float(re.sub(r"[^\d.]", "", s))  # Elimina todo excepto números y puntos
      mess_len = float(re.sub(r"[^\d.]", "", m))  # Elimina unidades como 'B' o 's'
      off.append((mess_len + header)*8 / send_int) 
      
      if not filter.empty:
         # Convertir vectime y vecvalue de strings a listas de floats
         vectime = list(map(float, filter["vectime"].iloc[0].strip("\"").split()))
         vecvalue = list(map(float, filter["vecvalue"].iloc[0].strip("\"").split()))
         # Almacenar los datos en un diccionario
         thr[f"ConfiguratorA.host{i}.app[1]"] = {"vectime": vectime, "vecvalue": vecvalue}
    thr_tot.append(sum(len(values["vectime"]) for values in thr.values()) / len(thr))
    off_tot.append(sum(off))
    
# Graficar el throughput total
# plt.plot(off_tot, thr_tot, label="Throughput All", color="blue")
# plt.xlabel("pq/sec")
# plt.ylabel("Throughput (bps)")
# plt.title("Throughput of the NET")
# plt.legend()
# plt.grid(True)
plt.show()
plt.plot( off_tot, thr_tot, label="Throughput All", color="blue")
plt.xlabel("Offered Trafic")
plt.ylabel("Throughput (bps)")
plt.title("Throughput of the NET")
plt.legend()
plt.grid(True)
plt.show()


# %%
