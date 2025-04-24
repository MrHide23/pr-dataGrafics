
import pandas as pd
import re
import matplotlib.pyplot as plt


key=["data_0_5","data_1","data_5","data_10","data_50","data_100","data_150","data_200","data_250", "data_300", "data_500"]
thr_tot=[]
off_tot=[]
for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    thr:float=0.0
    off:float=0.0
    for j in range(0,10): 
      # Obtenr Throughput de medio de cada elemento ConfiguratorA.host0.ethg$o[0].channel
      thrmean:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.ethg$o[0].channel"), "value"].iloc[0] 
      sent_total:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.eth[0].mac") & (data["name"] == "bits/sec sent"), "value"].iloc[0]
      thr+=float(thrmean)/1000# Convertir a Kbps
      off+=(float(sent_total)/8)/1000 # Convertir a Kbps

      off_tot.append(off/9) # Promedio de offed traffic
      thr_tot.append((thr/9)) # Promedio de throughput
    # off_tot.append(off/9) # Promedio de offed traffic
    # thr_tot.append((off/9)/(thr/9)) # Promedio de throughput
   



# Graficar el throughput total
plt.show()
#plt.plot(key, thr_tot, label="Throughput All", color="red")
plt.plot(off_tot, thr_tot, label="Throughput All", color="red")
plt.xlabel("Nº pq/seq")
plt.ylabel("Throughput/Offed Trafic")
plt.title("Throughput of the NET")
plt.legend()
plt.grid(True)
plt.show()


