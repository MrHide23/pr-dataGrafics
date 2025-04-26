
import pandas as pd
import re
import matplotlib.pyplot as plt


key=["data_0_5","data_1","data_5","data_10","data_50","data_100","data_150","data_200","data_250", "data_300", "data_500", "data_800"]
thr_tot=[]
off_tot=[]
off_recv_tot=[]
for i in key:
    data = pd.read_csv(f"data/{i}.csv")
    thr:float=0.0
    off:float=0.0
    off_recv:float=0.0
    for j in range(0,10): 
      # Obtenr Throughput de medio de cada elemento ConfiguratorA.host0.ethg$o[0].channel
      thrmean:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.ethg$o[0].channel"), "value"].iloc[0] 
      sent_total:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.eth[0].mac") & (data["name"] == "bits/sec sent"), "value"].iloc[0]
      recived_bits:float=data.loc[(data["type"] == "scalar") & (data["module"] == f"ConfiguratorA.host{j}.eth[0].mac") & (data["name"] == "bits/sec rcvd"), "value"].iloc[0]
      thr+=float(thrmean)# Convertir a Kbps
      off+=(float(sent_total)/(1000*100)) # Convertir a Kbps
      off_recv+=(float(recived_bits)/(1000*100)) # Convertir a Kbps

    off_tot.append(off/9) # Promedio de offed traffic
    thr_tot.append((off/9)/(thr/9)) # Promedio de throughput
    off_recv_tot.append(off_recv/9) # Promedio de throughput
   
   



# Graficar el throughput total
plt.subplot(2, 1, 1)
plt.plot(key, thr_tot, label="Throughput All", color="red")
plt.xlabel("Iteracion")
plt.ylabel("Offed Trafic/Throughput - kbps")
plt.title("Capacity")
plt.legend()
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(off_recv_tot ,thr_tot, label="Pakets Recived VS Throughput Mean", color="blue")
plt.xlabel("Iteracion")
plt.ylabel("Offed Trafic/Throughput - kbps")
plt.title("Pakets Recived VS Throughput Mean")
plt.legend()
plt.grid(True)
plt.show()


