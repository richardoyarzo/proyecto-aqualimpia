# Proyecto de Análisis de Datos - AquaLimpia S. A.

## 1. Descripción del proyecto

Este proyecto tiene como objetivo analizar el desempeño de las plantas de tratamiento de aguas residuales de AquaLimpia S. A.

La empresa presenta incumplimientos intermitentes en algunos parámetros de calidad del efluente tratado, principalmente en la DBO de salida y en la eficiencia del tratamiento. Por este motivo, se realiza un análisis exploratorio de datos para apoyar la toma de decisiones.

## 2. Objetivo general

Analizar el comportamiento de las plantas de tratamiento de AquaLimpia S. A. mediante herramientas de ciencia de datos, con el fin de identificar patrones, revisar el cumplimiento normativo y apoyar decisiones operativas y ambientales.

## 3. Objetivos específicos

- Cargar y revisar el dataset entregado.
- Analizar variables como caudal de entrada, DBO de entrada, DBO de salida, energía utilizada y lodos generados.
- Calcular la eficiencia de remoción de DBO.
- Comparar el desempeño entre plantas.
- Generar gráficos y tablas resumen.
- Crear archivos de salida para las áreas de Operaciones y Gestión Ambiental.
- Evaluar la calidad de los datos utilizados.

## 4. Datos utilizados

El dataset utilizado corresponde al archivo:

`dataset_set_A_aguas_residuales.xlsx`

Las principales variables analizadas son:

- `fecha_registro`
- `planta`
- `caudal_entrada_m3_d`
- `DBO_entrada_mg_L`
- `DBO_salida_mg_L`
- `energia_aeracion_kWh`
- `lodos_generados_kg_d`
- `cumplimiento_norma`

## 5. Proceso de análisis

El análisis se desarrolló siguiendo estos pasos:

1. Carga del dataset en Python.
2. Revisión inicial de columnas, tipos de datos y valores nulos.
3. Preparación de los datos para el análisis.
4. Cálculo de la eficiencia de remoción de DBO.
5. Agrupación de resultados por planta de tratamiento.
6. Generación de gráficos exploratorios.
7. Creación de archivos de salida para distintas áreas de la empresa.
8. Interpretación de resultados.

## 6. Indicador calculado

Para medir el desempeño del tratamiento se calculó la eficiencia de remoción de DBO:

```text
eficiencia_DBO = ((DBO_entrada - DBO_salida) / DBO_entrada) * 100
