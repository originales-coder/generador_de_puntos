import datetime
import json
import os
import streamlit as st

# Configuración optimizada para aprovechar el ancho en el S23
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="wide"
)

# Estilos CSS para compactar al máximo y eliminar espacios muertos
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    /* Estilo para los botones granates y compactos */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 2px 0px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        min-height: 34px;
    }
    .stButton > button:hover {
        background-color: #5a0017;
        color: white;
    }
    /* Reducir tamaño y márgenes del título */
    h1 {
        font-size: 1.5rem !important;
        text-align: center;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Archivo de persistencia de datos
JSON_FILE = "historial_puntos.json"
mes_actual = datetime.datetime.now().strftime("%Y-%m")


def cargar_datos():
  if os.path.exists(JSON_FILE):
    try:
      with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    except Exception:
      data = {}
  else:
    data = {}

  if mes_actual not in data or not isinstance(data.get(mes_actual), dict):
    jugadoras_nombres = [
        "Alma",
        "Greta",
        "Iria",
        "Laia",
        "Lia",
        "Marina",
        "Marta",
        "Martina",
        "Mireia",
        "Nerea",
        "Ona Franquet",
        "Ona Orri",
        "Silvia",
        "Txell",
        "Valen",
        "Vega",
    ]
    data[mes_actual] = {j: 0 for j in jugadoras_nombres}
  return data


def guardar_datos(datos):
  with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=4)


if "historial" not in st.session_state:
  st.session_state.historial = cargar_datos()

if mes_actual not in st.session_state.historial:
  st.session_state.historial[mes_actual] = {
      f"Jugadora {i+1}": 0 for i in range(16)
  }

# Título limpio sin iconos y subtítulo integrado en una línea pequeña
st.markdown("<h1>Control de Puntos</h1>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 0.85rem; margin-top: 0px;'>Mes: {mes_actual}</p>",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Cuadrícula en 2 columnas principales
cols = st.columns(2)

for i, jugadora in enumerate(jugadoras):
  col_actual = cols[i % 2]
  with col_actual:
    with st.container():
      st.markdown(
          f"<div style='font-size: 0.95rem; font-weight: bold; margin-bottom: 2px;'>{jugadora}</div>",
          unsafe_allow_html=True,
      )

      # Sub-columnas ajustadas: [Puntos] [-] [+]
      col_puntos, col_menos, col_mas = st.columns([1.5, 1, 1])

      with col_puntos:
        st.markdown(
            f"<div style='text-align: center; font-size: 0.9rem; padding-top: 6px;'>Pts: <b>{puntos_mes[jugadora]}</b></div>",
            unsafe_allow_html=True,
        )

      with col_menos:
        if st.button("-", key=f"menos_{jugadora}"):
          st.session_state.historial[mes_actual][jugadora] = (
              int(st.session_state.historial[mes_actual].get(jugadora, 0)) - 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()

      with col_mas:
        if st.button("+", key=f"mas_{jugadora}"):
          st.session_state.historial[mes_actual][jugadora] = (
              int(st.session_state.historial[mes_actual].get(jugadora, 0)) + 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()

      st.markdown(
          "<hr style='margin: 4px 0px; opacity: 0.15;'>", unsafe_allow_html=True
      )
