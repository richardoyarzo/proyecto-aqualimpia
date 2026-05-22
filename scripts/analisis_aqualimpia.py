import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

RUTA_DATOS = Path("data/dataset_set_A_aguas_residuales.xlsx")
RUTA_OUTPUTS = Path("outputs")
RUTA_GRAFICOS = RUTA_OUTPUTS / "graficos"

RUTA_OUTPUTS.mkdir(exist_ok=True)
RUTA_GRAFICOS.mkdir(exist_ok=True)

df = pd.read_excel(RUTA_DATOS)

print("Primeros registros del dataset:")
print(df.head())

print("\nInformación general:")
print(df.info())

print("\nValores nulos por columna:")
print(df.isnull().sum())

df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])

df["eficiencia_DBO"] = (
    (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"])
    / df["DBO_entrada_mg_L"]
) * 100

df["estado_cumplimiento"] = np.where(
    df["cumplimiento_norma"] == 1,
    "Cumple",
    "No cumple"
)

df["alerta_operativa"] = np.where(
    df["cumplimiento_norma"] == 0,
    "Revisar",
    "Normal"
)

resumen_planta = df.groupby("planta").agg(
    registros=("planta", "count"),
    caudal_promedio=("caudal_entrada_m3_d", "mean"),
    dbo_entrada_promedio=("DBO_entrada_mg_L", "mean"),
    dbo_salida_promedio=("DBO_salida_mg_L", "mean"),
    eficiencia_promedio=("eficiencia_DBO", "mean"),
    cumplimiento_promedio=("cumplimiento_norma", "mean"),
    energia_promedio=("energia_aeracion_kWh", "mean"),
    lodos_promedio=("lodos_generados_kg_d", "mean")
).reset_index()

resumen_planta["cumplimiento_porcentaje"] = resumen_planta["cumplimiento_promedio"] * 100

print("\nResumen por planta:")
print(resumen_planta)

resumen_planta.to_csv(RUTA_OUTPUTS / "resumen_por_planta.csv", index=False)

salida_operaciones = df[
    [
        "fecha_registro",
        "planta",
        "caudal_entrada_m3_d",
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L",
        "energia_aeracion_kWh",
        "lodos_generados_kg_d",
        "eficiencia_DBO",
        "alerta_operativa"
    ]
]

salida_gestion_ambiental = df[
    [
        "fecha_registro",
        "planta",
        "DBO_salida_mg_L",
        "cumplimiento_norma",
        "estado_cumplimiento"
    ]
]

salida_operaciones.to_csv(RUTA_OUTPUTS / "salida_operaciones.csv", index=False)
salida_gestion_ambiental.to_csv(RUTA_OUTPUTS / "salida_gestion_ambiental.csv", index=False)

plt.figure(figsize=(8, 5))
plt.bar(resumen_planta["planta"], resumen_planta["cumplimiento_porcentaje"])
plt.title("Porcentaje de cumplimiento normativo por planta")
plt.xlabel("Planta")
plt.ylabel("Cumplimiento (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(RUTA_GRAFICOS / "cumplimiento_por_planta.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(resumen_planta["planta"], resumen_planta["eficiencia_promedio"])
plt.title("Eficiencia promedio de remoción de DBO por planta")
plt.xlabel("Planta")
plt.ylabel("Eficiencia DBO (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(RUTA_GRAFICOS / "eficiencia_por_planta.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(df["caudal_entrada_m3_d"], df["DBO_salida_mg_L"])
plt.title("Relación entre caudal de entrada y DBO de salida")
plt.xlabel("Caudal de entrada m3/d")
plt.ylabel("DBO salida mg/L")
plt.tight_layout()
plt.savefig(RUTA_GRAFICOS / "caudal_vs_dbo_salida.png")
plt.close()

print("\nAnálisis finalizado. Archivos generados en la carpeta outputs.")
