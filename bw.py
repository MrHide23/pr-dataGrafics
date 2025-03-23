#%%
import pandas as pd

# Leer el archivo como texto sin encabezados automáticos
with open("data/data_all.csv", "r") as file:
    lines = file.readlines()

# Inicializar listas para almacenar datos
data = []

# Recorrer líneas y procesar solo las de tipo "vector"
for line in lines:
    parts = line.strip().split(",")  # Dividir por comas
    if parts[1] == "vector":  # Filtrar solo líneas con datos útiles
        nodo = parts[2]  # Identificar el nodo (ejemplo: ConfiguratorA.host0.app[1])
        tiempo = list(map(float, parts[-2].strip('"').split()))  # Extraer tiempos
        throughput = list(map(float, parts[-1].strip('"').split()))  # Extraer valores de throughput

        # Guardar cada punto de tiempo con su valor
        for t, thr in zip(tiempo, throughput):
            data.append([nodo, t, thr])

# Convertir a DataFrame
df = pd.DataFrame(data, columns=["Nodo", "Tiempo", "Throughput"])

# Mostrar primeras filas para verificar
print(df.head())

# Guardar en un CSV limpio
df.to_csv("data/throughput_limpio.csv", index=False)

#%%
import pandas as pd

# Cargar los datos de throughput
df = pd.read_csv("data/throughput_limpio.csv")

# Lista para almacenar resultados
resultados = []

# Calcular el bandwidth para cada nodo
for nodo in df["Nodo"].unique():
    df_nodo = df[df["Nodo"] == nodo]  # Filtrar datos por nodo
    tiempo_total = df_nodo["Tiempo"].max() - df_nodo["Tiempo"].min()  # Duración total
    throughput_total = df_nodo["Throughput"].sum()  # Suma de throughput

    # Evitar división entre cero
    bandwidth = throughput_total / tiempo_total if tiempo_total > 0 else 0

    resultados.append([nodo, bandwidth])

# Convertir a DataFrame
df_bandwidth = pd.DataFrame(resultados, columns=["Nodo", "Bandwidth (bps)"])

# Mostrar resultados
print(df_bandwidth)

# Guardar en un archivo CSV
df_bandwidth.to_csv("bandwidth_por_nodo.csv", index=False)
# %%
