import pandas as pd
import numpy as np
from scipy import stats
import joblib


def cargar_datos(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    return df


def calcular_eficiencia_dbo(df):
    df = df.copy()

    df["eficiencia_DBO"] = (
        (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"])
        / df["DBO_entrada_mg_L"]
    ) * 100

    return df


def agregar_estado_cumplimiento(df):
    df = df.copy()

    df["estado_cumplimiento"] = np.where(
        df["cumplimiento_norma"] == 1,
        "Cumple",
        "No cumple"
    )

    return df


def resumen_por_planta(df):
    resumen = df.groupby("planta").agg(
        total_registros=("planta", "count"),
        dbo_entrada_promedio=("DBO_entrada_mg_L", "mean"),
        dbo_salida_promedio=("DBO_salida_mg_L", "mean"),
        eficiencia_promedio=("eficiencia_DBO", "mean"),
        cumplimiento_promedio=("cumplimiento_norma", "mean"),
        caudal_promedio=("caudal_entrada_m3_d", "mean"),
        energia_promedio=("energia_aeracion_kWh", "mean"),
        lodos_promedio=("lodos_generados_kg_d", "mean")
    ).reset_index()

    resumen["cumplimiento_porcentaje"] = resumen["cumplimiento_promedio"] * 100

    return resumen


def detectar_outliers_dbo_salida(df):
    df = df.copy()

    z_scores = np.abs(stats.zscore(df["DBO_salida_mg_L"]))
    df["outlier_DBO_salida"] = z_scores > 3

    return df


def guardar_resultado_joblib(objeto, ruta_salida):
    joblib.dump(objeto, ruta_salida)