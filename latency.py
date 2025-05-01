
import pandas as pd
import re
import matplotlib.pyplot as plt


 #Cada Switch
    
key=["data_10","data_100","data_350", "data_500", "data_800", "data_1000","data_1200","data_1300","data_1500"]
dely_tot=[]
off_tot=[]


for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    dely=[]
    #Cada Host
    for j in range(0,10):
      d_mean=float(data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.app[1]") & (data["name"] == "endToEndDelay:mean"), "value"].iloc[0] )
      dely.append(d_mean) 
    
    # #switches
    # for j in [0,1,3,4,5]:
    #   l_s=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.switch{j}.eth[1].queue") & (data["name"] == "queueingTime:mean"), "value"].iloc[0] #s
    #   dely.append(float(l_s))

    # for j in range(0,6):
    #   l_s=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.router{j}.eth[1].queue") & (data["name"] == "queueingTime:mean"), "value"].iloc[0] #s
    #   dely.append(float(l_s))
          
    dely_tot.append(sum(dely)/len(dely)) # Promedio de throughput all red
    off_tot.append(int(re.search(r'\d+', i).group())*1024*8)

 

plt.figure(1)
plt.plot(off_tot,dely_tot, label="Latency", color="blue")
plt.xlabel("Offered Load - bits/s")
plt.ylabel("Latency - s")
plt.title("Latency of the NET")
plt.legend()
plt.grid(True)
plt.show()

