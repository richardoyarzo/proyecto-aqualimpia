import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard AquaLimpia S.A.",
    layout="wide"
)

st.title("Dashboard exploratorio AquaLimpia S. A.")
st.write("Análisis del desempeño de plantas de tratamiento de aguas residuales.")

df = pd.read_excel("data/dataset_set_A_aguas_residuales.xlsx")

df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])

df["eficiencia_DBO"] = (
    (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"])
    / df["DBO_entrada_mg_L"]
) * 100

df["estado_cumplimiento"] = df["cumplimiento_norma"].map({
    1: "Cumple",
    0: "No cumple"
})

plantas = st.multiselect(
    "Seleccionar planta",
    options=df["planta"].unique(),
    default=df["planta"].unique()
)

df_filtrado = df[df["planta"].isin(plantas)]

total_registros = len(df_filtrado)
cumplimiento_general = df_filtrado["cumplimiento_norma"].mean() * 100
dbo_salida_promedio = df_filtrado["DBO_salida_mg_L"].mean()
eficiencia_promedio = df_filtrado["eficiencia_DBO"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total registros", total_registros)
col2.metric("Cumplimiento general", f"{cumplimiento_general:.1f}%")
col3.metric("DBO salida promedio", f"{dbo_salida_promedio:.2f} mg/L")
col4.metric("Eficiencia promedio", f"{eficiencia_promedio:.2f}%")

resumen = df_filtrado.groupby("planta").agg(
    cumplimiento=("cumplimiento_norma", "mean"),
    dbo_salida_promedio=("DBO_salida_mg_L", "mean"),
    eficiencia_promedio=("eficiencia_DBO", "mean")
).reset_index()

resumen["cumplimiento"] = resumen["cumplimiento"] * 100

st.subheader("Cumplimiento normativo por planta")

fig1 = px.bar(
    resumen,
    x="planta",
    y="cumplimiento",
    text="cumplimiento",
    title="Porcentaje de cumplimiento por planta"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("DBO de salida en el tiempo")

fig2 = px.line(
    df_filtrado.sort_values("fecha_registro"),
    x="fecha_registro",
    y="DBO_salida_mg_L",
    color="planta",
    title="Evolución de DBO de salida"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Relación entre caudal de entrada y DBO de salida")

fig3 = px.scatter(
    df_filtrado,
    x="caudal_entrada_m3_d",
    y="DBO_salida_mg_L",
    color="estado_cumplimiento",
    hover_data=["planta", "fecha_registro"],
    title="Caudal de entrada vs DBO de salida"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Eficiencia promedio por planta")

fig4 = px.bar(
    resumen,
    x="planta",
    y="eficiencia_promedio",
    text="eficiencia_promedio",
    title="Eficiencia promedio de remoción de DBO"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Datos filtrados")
st.dataframe(df_filtrado)
