import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import numpy as np

route="data_one" #sys.argv[1] # Ruta de la carpeta que contiene los archivos CSV
key=os.listdir(route)
key.sort(key=lambda x: int(re.search(r'\d+', x).group())) 
thr_tot=[]
off_tot=[]
for i in key:
    data = pd.read_csv(f"{route}/{i}")
    thr:float=0.0
    for j in range(0,10): 
      # Obtenr Throughput de medio de cada elemento ConfiguratorA.host0.ethg$o[0].channel
      thrmean:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.ethg$o[0].channel"), "value"].iloc[0] #bps
      if (np.isnan(thrmean)!=True ):
        thr+=(float(thrmean)/1000)# Convertir a Kbps

    thr_tot.append((thr/10)) # Promedio de throughput
    off_tot.append(int(re.search(r'\d+', i).group())) # Convertir a bps
    
   
# Graficar el throughput total
plt.plot(off_tot,thr_tot, label="Throughput All", color="red")
plt.xlabel("Offload - pps")
plt.ylabel("Throughput - kbps")
plt.title("Capacity")
plt.legend()
plt.grid(True)
plt.show()


