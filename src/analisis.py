import pandas as pd
import os

# Asegurar que existe el directorio de resultados
os.makedirs('resultados', exist_ok=True)

# 1. Leer el archivo CSV
df = pd.read_csv('data/sensores_industriales.csv')

# 2. Cantidad de registros y de sensores distintos
total_registros = len(df)
sensores_distintos = df['id_sensor'].nunique()
print(f"Cantidad de registros: {total_registros}")
print(f"Sensores distintos: {sensores_distintos}\n")

# 3. Temperatura promedio de cada planta
print("Temperatura promedio por planta:")
promedios = df.groupby('planta')['temperatura_c'].mean()
print(promedios.round(2).to_string() + "\n")

# 4. Temperatura máxima, sensor y fecha correspondientes
max_temp_idx = df['temperatura_c'].idxmax()
max_temp_row = df.loc[max_temp_idx]
print(f"Temperatura máxima: {max_temp_row['temperatura_c']} °C")
print(f"Sensor: {max_temp_row['id_sensor']}")
print(f"Fecha: {max_temp_row['fecha_hora']}\n")

# 5. Contar las lecturas con temperatura mayor que 85 °C
alertas_df = df[df['temperatura_c'] > 85]
print(f"Lecturas con temperatura mayor a 85 °C: {len(alertas_df)}\n")

# 6. Identificar la planta con más alertas de temperatura
conteo_alertas_planta = alertas_df['planta'].value_counts()
max_alertas = conteo_alertas_planta.max()
plantas_empate = conteo_alertas_planta[conteo_alertas_planta == max_alertas].index.tolist()
print(f"Planta(s) con más alertas ({max_alertas} alertas): {', '.join(plantas_empate)}\n")

# 7. Exportar todas las lecturas con alerta
alertas_df.to_csv('resultados/alertas.csv', index=False)
print("Las alertas han sido exportadas a 'resultados/alertas.csv'.")