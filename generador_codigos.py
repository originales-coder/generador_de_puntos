import streamlit as st
import json
import os
from datetime import datetime

# Configuración inicial optimizada para móvil
st.set_page_config(page_title="Control de Puntos", page_icon="📊", layout="centered")

# Estilos CSS idénticos a tu referencia y optimizados para velocidad
st.markdown("""
    <style>
    .stButton > button {
        background-color: #7A1C4F !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: bold !important;
        height: 38px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #9A2463 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

ARCHIVO_DATOS = "historial_puntos.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

st.title("📊 Control de Puntos")

mes_actual = datetime.now().strftime("%Y-%m")

if "datos_historicos" not in st.session_state:
    st.session_state.datos_historicos = cargar_datos()

if "meses" not in st.session_state.datos_historicos:
    st.session_state.datos_historicos["meses"] = {}

if mes_actual not in st.session_state.datos_historicos["meses"]:
    nombres_iniciales = [
        "Alma", "Greta", "Iria", "Laia", "Lia", 
        "Marina", "Marta", "Martina", "Mireia", "Nerea", 
        "Ona Franquet", "Ona Orri", "Silvia", "Txell", "Valen", "Vega"
    ]
    st.session_state.datos_historicos["meses"][mes_actual] = {nombre: 0 for nombre in sorted(nombres_iniciales)}
    guardar_datos(st.session_state.datos_historicos)

jugadoras_mes = st.session_state.datos_historicos["meses"][mes_actual]

# Barra lateral para añadir jugadoras
st.sidebar.header("Añadir Jugadora")
nueva_jugadora = st.sidebar.text_input("Nombre")
if st.sidebar.button("Añadir"):
    if nueva_jugadora and nueva_jugadora not in jugadoras_mes:
        jugadoras_mes[nueva_jugadora] = 0
        guardar_datos(st.session_state.datos_historicos)
        st.success(f"¡{nueva_jugadora} añadida!")
        st.rerun()

pestana_control, pestana_stats = st.tabs(["🎮 Control", "📈 Estadísticas"])

with pestana_control:
    st.subheader(f"Mes: {mes_actual}")
    st.markdown("---")

    jugadoras_ordenadas = sorted(jugadoras_mes.keys())

    # Generamos la lista de forma directa y limpia para agilizar la respuesta
    for jugadora in jugadoras_ordenadas:
        col1, col2, col3, col4, col5 = st.columns([2.5, 1, 1, 1, 0.5])
        
        with col1:
            st.write(f"**{jugadora}**")
        with col2:
            st.write(f"{jugadoras_mes[jugadora]}")
        with col3:
            if st.button("-1", key=f"menos_{jugadora}"):
                jugadoras_mes[jugadora] -= 1
                guardar_datos(st.session_state.datos_historicos)
                st.rerun()
        with col4:
            if st.button("+1", key=f"mas_{jugadora}"):
                jugadoras_mes[jugadora] += 1
                guardar_datos(st.session_state.datos_historicos)
                st.rerun()
        with col5:
            st.write("...")
            
        st.divider()

with pestana_stats:
    st.subheader("📋 Resumen Estadístico")
    
    totales_historicos = {}
    for mes, jugadoras in st.session_state.datos_historicos["meses"].items():
        for jugadora, pts in jugadoras.items():
            totales_historicos[jugadora] = totales_historicos.get(jugadora, 0) + pts

    st.markdown(f"### 📅 Cómputo del Mes ({mes_actual})")
    for j in sorted(jugadoras_mes.keys()):
        st.text(f"• {j}: {jugadoras_mes[j]} puntos")

    st.markdown("---")
    st.markdown("### 🏆 Cómputo Total Histórico")
    for j in sorted(totales_historicos.keys()):
        st.markdown(f"**{j}**: 🎯 {totales_historicos[j]} puntos acumulados")