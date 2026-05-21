import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador ARnD", layout="wide")

st.title("🚛 Simulador Sistema de Tratamiento ARnD")
st.markdown("Lavadero de Vehículos de Carga Pesada")

st.sidebar.header("⚙️ Parámetros de operación")

N = st.sidebar.slider("Vehículos/día", 1, 100, 20)
C = st.sidebar.slider("Consumo (L/vehículo)", 100, 1500, 800)
t = st.sidebar.slider("Horas operación", 1, 24, 8)
Fp = st.sidebar.slider("Factor pico", 1.0, 3.0, 2.0)

st.sidebar.header("💧 Calidad del afluente")

SST = st.sidebar.slider("SST (mg/L)", 0, 5000, 2500)
DQO = st.sidebar.slider("DQO (mg/L)", 0, 5000, 2500)
GyA = st.sidebar.slider("Grasas y aceites (mg/L)", 0, 1000, 400)
SAAM = st.sidebar.slider("SAAM (mg/L)", 0, 100, 20)

Qd = N * C / 1000
Qmh = Qd / t
Qp = Qmh * Fp

st.subheader("📊 Resultados hidráulicos")

col1, col2, col3 = st.columns(3)
col1.metric("Caudal diario", f"{Qd:.2f} m³/día")
col2.metric("Caudal medio", f"{Qmh:.2f} m³/h")
col3.metric("Caudal pico", f"{Qp:.2f} m³/h")

st.subheader("🧪 Eficiencias de remoción (%)")

etapas = [
    "Cribado",
    "Desarenador",
    "Separador coalescente",
    "Ecualización",
    "Coagulación-Floculación",
    "Clarificador lamelar",
    "Filtro de arena",
    "Carbón activado",
    "Desinfección"
]

remociones = []

valores_defecto = {
    "Cribado": [5, 2, 0, 0],
    "Desarenador": [15, 5, 0, 0],
    "Separador coalescente": [10, 10, 65, 5],
    "Ecualización": [0, 0, 0, 0],
    "Coagulación-Floculación": [45, 30, 35, 20],
    "Clarificador lamelar": [60, 25, 20, 10],
    "Filtro de arena": [55, 15, 10, 5],
    "Carbón activado": [10, 35, 25, 50],
    "Desinfección": [0, 0, 0, 0]
}

for e in etapas:
    st.write(f"### {e}")
    col = st.columns(4)

    r1 = col[0].slider(f"{e} - SST", 0, 100, valores_defecto[e][0]) / 100
    r2 = col[1].slider(f"{e} - DQO", 0, 100, valores_defecto[e][1]) / 100
    r3 = col[2].slider(f"{e} - Grasas y aceites", 0, 100, valores_defecto[e][2]) / 100
    r4 = col[3].slider(f"{e} - SAAM", 0, 100, valores_defecto[e][3]) / 100

    remociones.append([r1, r2, r3, r4])

parametros = ["SST", "DQO", "Grasas y aceites", "SAAM"]
valores = np.array([SST, DQO, GyA, SAAM], dtype=float)

historial = [valores.copy()]

for rem in remociones:
    valores = valores * (1 - np.array(rem))
    historial.append(valores.copy())

st.subheader("📈 Evolución del tratamiento")

df = pd.DataFrame(historial, columns=parametros)
df.index = ["Afluente"] + etapas

st.dataframe(df)

fig, ax = plt.subplots(figsize=(10, 5))

for p in parametros:
    ax.plot(df.index, df[p], marker="o", label=p)

ax.set_ylabel("mg/L")
ax.set_title("Evolución de contaminantes por etapa")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

st.subheader("✅ Remoción global")

rem_total = 1 - (df.iloc[-1] / df.iloc[0])
st.write((rem_total * 100).round(2).astype(str) + " %")

st.subheader("♻️ Reuso de agua")

reuso = st.slider("Porcentaje de reuso (%)", 0, 100, 50)
agua_reutilizada = Qd * (reuso / 100)

st.metric("Agua reutilizada", f"{agua_reutilizada:.2f} m³/día")

st.info(
    "Este simulador es preliminar. Las eficiencias deben ajustarse con caracterización real del agua residual y pruebas de jarras."
)
