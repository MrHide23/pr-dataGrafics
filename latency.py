
import pandas as pd
import re
import matplotlib.pyplot as plt


key=["data_0_5","data_1","data_5","data_10","data_50","data_100","data_150","data_200","data_250", "data_300", "data_500", "data_800"]
dely_tot=[]
delyhost=[0,0,0,0,0,0,0,0,0,0]
off_tot=[]

for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    dely=[]
    off=[]
    

    for j in range(0,10):
      d_mean=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.app[1]") & (data["name"] == "endToEndDelay:mean"), "value"].iloc[0] )
      sent_total=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.eth[0].mac") & (data["name"] == "bits/sec sent"), "value"].iloc[0])
      
      off.append(sent_total) # Convertir a Kbps
      dely.append(d_mean) 
      delyhost[j]+=d_mean
    
    dely_tot.append((sum(dely)/len(dely)))
    off_tot.append((sum(off)/len(off))) # Promedio de throughput 


for k in range(0,10): delyhost[k]/=len(delyhost) # Promedio de cada host    

plt.figure(1)
# plt.plot(off_tot, dely_tot, label="Latency  ", color="blue")
# plt.xlabel("Nº of pq/s")
# plt.ylabel("Latency (ms)")
# plt.title("Latency of the NET")
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.figure(2)
plt.plot(delyhost, label="Latency Mean", color="blue")
plt.xlabel(f"Nº of Host")
plt.ylabel("Latency (ms)")
plt.title(f"Latencia Mean Hosts")
plt.legend()
for i in range(0,10): plt.text(i, delyhost[i], f"Host {i}: {delyhost[i]:.5f}", fontsize=8, ha='left', va='bottom')
plt.grid(True)
plt.show()