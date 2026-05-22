from pathlib import Path
from scripts.funciones_aqualimpia import (
    cargar_datos,
    calcular_eficiencia_dbo,
    agregar_estado_cumplimiento,
    resumen_por_planta,
    detectar_outliers_dbo_salida,
    guardar_resultado_joblib
)

ruta_datos = Path("data/dataset_set_A_aguas_residuales.xlsx")
ruta_outputs = Path("outputs")

ruta_outputs.mkdir(exist_ok=True)

df = cargar_datos(ruta_datos)

df = calcular_eficiencia_dbo(df)
df = agregar_estado_cumplimiento(df)
df = detectar_outliers_dbo_salida(df)

resumen = resumen_por_planta(df)

df.to_csv(
    ruta_outputs / "dataset_procesado_modular.csv",
    index=False,
    encoding="utf-8"
)

resumen.to_csv(
    ruta_outputs / "resumen_por_planta_modular.csv",
    index=False,
    encoding="utf-8"
)

guardar_resultado_joblib(
    resumen,
    ruta_outputs / "resumen_por_planta.joblib"
)

print("Resumen por planta:")
print(resumen)

print("\nCantidad de posibles outliers en DBO de salida:")
print(df["outlier_DBO_salida"].sum())

print("\nAnálisis modular finalizado correctamente.")
