
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import numpy as np

route="data" #sys.argv[1] # Ruta de la carpeta que contiene los archivos CSV
key=os.listdir(route)
key.sort(key=lambda x: int(re.search(r'\d+', x).group())) # Ordenar por el número en el nombre del archivo
print(key)
dely_tot=[]
off_tot=[]


for i in key:
    data = pd.read_csv(f"{route}/{i}")
    dely=[]
    packetSent=[]

    #Cada Host
    for j in range(0,10):
      d_mean=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.app[1]") & (data["name"] == "endToEndDelay:mean"), "value"].iloc[0] )
      pack=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.app[0]") & (data["name"] == "packetSent:count"), "value"].iloc[0] )
       #paquete enviado por host
      if (np.isnan(d_mean)!=True and pack!=0):
        dely.append(d_mean) 
        packetSent.append(pack*1024*8)
    
    # #switches
    for j in [0,1,3,4,5]:
      l_s=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.switch{j}.eth[1].queue") & (data["name"] == "queueingTime:mean"), "value"].iloc[0]) #s
      if l_s!=0:
        dely.append(float(l_s))

    for j in range(0,6):
      l_s=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.router{j}.eth[1].queue") & (data["name"] == "queueingTime:mean"), "value"].iloc[0] #s
      if l_s!=0:
        dely.append(float(l_s))
          
    dely_tot.append(sum(dely)/len(dely)) # Promedio de throughput all red
    off_tot.append(sum(packetSent)/len(packetSent)/100) # Promedio de throughput all red
    #off_tot.append(int(re.search(r'\d+', i).group())*1024*8)

 

plt.figure(1)
plt.plot(off_tot,dely_tot, label="Latency", color="blue")
plt.xlabel("Offered Load - bits/s")
plt.ylabel("Latency - s")
plt.title("Latency of the NET")
plt.legend()
plt.grid(True)
plt.show()

