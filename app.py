import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# CONFIGURACIÓN
st.set_page_config(page_title="Simulador ARnD", layout="wide")

st.title("🚛 Simulador Sistema de Tratamiento ARnD")
st.markdown("Lavadero de Vehículos de Carga Pesada")

# =========================
# ENTRADAS
# =========================
st.sidebar.header("⚙️ Parámetros de operación")

N = st.sidebar.slider("Vehículos/día", 1, 100, 20)
C = st.sidebar.slider("Consumo (L/vehículo)", 100, 1500, 800)
