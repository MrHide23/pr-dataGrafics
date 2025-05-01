import pandas as pd
import re
import matplotlib.pyplot as plt

key=["data_10","data_100","data_350", "data_500", "data_800", "data_1000","data_1200","data_1300","data_1500"]
thr_tot=[]
off_tot=[]
for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    thr:float=0.0
    off:float=0.0
    for j in range(0,10): 
      # Obtenr Throughput de medio de cada elemento ConfiguratorA.host0.ethg$o[0].channel
      thrmean:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.ethg$o[0].channel"), "value"].iloc[0] #bps
      thr+=(float(thrmean)/1000)# Convertir a Kbps

    thr_tot.append((thr/10)) # Promedio de throughput
    
   
# Graficar el throughput total
plt.plot(["10","100", "350", "500", "800","1200", "1000", "1300", "1500"],thr_tot, label="Throughput All", color="red")
plt.xlabel("Offload - pps")
plt.ylabel("Throughput - kbps")
plt.title("Capacity")
plt.legend()
plt.grid(True)
plt.show()


