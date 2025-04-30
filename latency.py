
import pandas as pd
import re
import matplotlib.pyplot as plt


 #Cada Switch
    
key=["data_1000"]
dely_tot=[]
off_tot=[]


for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    dely=[]
    off=[]
    
    #Cada Host
    for j in range(0,10):
      d_mean=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.app[1]") & (data["name"] == "endToEndDelay:mean"), "value"].iloc[0] )
      
      dely.append(d_mean) 
    
    #switches
    for j in [0,1,3,4,5]:
        l_s=data.loc[(data["type"] == "vector") & (data["module"] == f"ConfiguratorA.switch{j}.eth[1].queue") & (data["name"] == "queueingTime:vector"), "vecvalue"]
    
        print(l_s)
        #vector,ConfiguratorA.router0.eth[0].queue,queueingTime:vector
         
    dely_tot.append((sum(dely)/len(dely)))

 

plt.figure(1)
plt.plot(["0,5","1","5","10","50","100","150","200","250", "300", "500", "800"], dely_tot, label="Latency  ", color="blue")
plt.xlabel("Nº of pq/s")
plt.ylabel("Latency (ms)")
for i in range(0,10): plt.text(i, dely_tot[i], f"Host {i}: {dely_tot[i]:.8f}", fontsize=8, ha='left', va='bottom')
plt.title("Latency of the NET")
plt.legend()
plt.grid(True)
plt.show()

