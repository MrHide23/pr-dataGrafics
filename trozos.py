import pandas as pd
import matplotlib.pyplot as plt

def calculate_network_throughput(df):
    # Filter relevant rows (e.g., outgoing packets from the queue)
    df_queue = df[(df['type'] == 'vector') & (df['name'].str.contains('outgoingDataRate'))]

    # Convert vectime and vecvalue to lists of floats
    df_queue['vectime'] = df_queue['vectime'].apply(lambda x: list(map(float, x.split())))
    df_queue['vecvalue'] = df_queue['vecvalue'].apply(lambda x: list(map(float, x.split())))

    # Explode the vectors into individual rows
    df_exploded = df_queue.explode(['vectime', 'vecvalue'])
    df_exploded['vectime'] = pd.to_numeric(df_exploded['vectime'])
    df_exploded['vecvalue'] = pd.to_numeric(df_exploded['vecvalue'])

    # Calculate throughput (sum of data rates over time)
    throughput = df_exploded.groupby('vectime')['vecvalue'].sum().reset_index()
    throughput.rename(columns={'vectime': 'time', 'vecvalue': 'throughput_bps'}, inplace=True)
    
    return throughput

# Load the CSV data
df = pd.read_csv('results.csv')

# Calculate throughput
throughput_df = calculate_network_throughput(df)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(throughput_df['time'], throughput_df['throughput_bps'], label='Network Throughput')
plt.xlabel('Time (s)')
plt.ylabel('Throughput (bps)')
plt.title('Network Throughput Over Time')
plt.legend()
plt.grid(True)
plt.show()

#%% 
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
df = pd.read_csv("data_all.csv")

# Filtrar las filas con métricas de throughput (ej: outgoingDataRate)
throughput_data = df[
    (df["type"] == "vector") 
    & (df["name"].str.contains("outgoingDataRate:vector"))
    & (df["module"] == "ConfiguratorA.host0.eth[0].queue")  # Filtra por dispositivo/interfaz específica
]

vectime_str = throughput_data["vectime"].iloc[0].strip("\"")
vecvalue_str = throughput_data["vecvalue"].iloc[0].strip("\"")

vectime = list(map(float, vectime_str.split()))
vecvalue = list(map(float, vecvalue_str.split()))

throughput_promedio = sum(vecvalue) / len(vecvalue)
tiempo_total = vectime[-1] - vectime[0]

# Throughput total (bits transferidos)
throughput_total = sum(vecvalue) * (vectime[1] - vectime[0])  # Asume intervalos regulares

print(f"Throughput total: {throughput_total:.2f} bits")
print(f"Throughput promedio: {throughput_promedio:.2f} bps")

plt.figure(figsize=(12, 6))
plt.plot(vectime, vecvalue, label="Throughput", color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("Throughput (bps)")
plt.title("Throughput de la red a lo largo del tiempo")
plt.legend()
plt.grid(True)
plt.show()

#%% thr apquetes

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
df = pd.read_csv("results.csv")

# Filtrar solo los vectores de paquetes transmitidos (txPk)
tx_packets = df[
    (df["type"] == "vector") 
    & (df["name"].str.contains("txPk:vector"))
]

# Convertir las cadenas de vectime a listas de números
tx_packets["vectime"] = tx_packets["vectime"].apply(
    lambda x: list(map(float, x.strip("\"").split()))
)

# Explotar los tiempos en filas individuales
tx_times = tx_packets.explode("vectime")[["vectime"]].copy()
tx_times["vectime"] = pd.to_numeric(tx_times["vectime"])

# Calcular el segundo correspondiente a cada paquete
tx_times["second"] = tx_times["vectime"].astype(int)

# Contar paquetes por segundo
packet_counts = tx_times.groupby("second").size().reset_index(name="packets")

# Calcular la tasa (paquetes/segundo)
packet_counts["tasa_paquetes_por_segundo"] = packet_counts["packets"]

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(packet_counts["second"], packet_counts["tasa_paquetes_por_segundo"], color="blue")
plt.xlabel("Tiempo (segundos)")
plt.ylabel("Paquetes enviados por segundo")
plt.title("Tasa de Paquetes Transmitidos por Segundo")
plt.grid(True)
plt.show()

#& A<ny 
import numpy as np
import matplotlib.pyplot as plt

# Datos de ejemplo para el tráfico ofrecido y el throughput
offered_traffic = np.linspace(0, 1, 100)  # Tráfico ofrecido (fracción de la capacidad)
throughput_stable = np.minimum(offered_traffic, 0.43)  # Throughput para una red estable
throughput_unstable = np.where(offered_traffic <= 0.43, offered_traffic, 0.43 - 0.2 * (offered_traffic - 0.43))  # Throughput para una red inestable

# Configuración de la gráfica
plt.figure(figsize=(10, 6))
plt.style.use("seaborn")  # Estilo de la gráfica (opcional)

# Graficar throughput para una red estable
plt.plot(offered_traffic, throughput_stable, label="Red Estable", linewidth=2, color="blue")

# Graficar throughput para una red inestable
plt.plot(offered_traffic, throughput_unstable, label="Red Inestable", linewidth=2, color="red", linestyle="--")

# Configuración de ejes y título
plt.xlabel("Tráfico Ofrecido (fracción de la capacidad)", fontsize=12)
plt.ylabel("Throughput (fracción de la capacidad)", fontsize=12)
plt.title("Throughput vs. Tráfico Ofrecido", fontsize=14, fontweight="bold")

# Leyenda y cuadrícula
plt.legend(loc="upper left", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7)

# Línea vertical para indicar el punto de saturación
plt.axvline(x=0.43, color="gray", linestyle=":", linewidth=1.5, label="Punto de Saturación (43%)")

# Ajustar márgenes
plt.tight_layout()

# Mostrar la gráfica
plt.show()