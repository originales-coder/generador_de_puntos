import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="centered"
)

# Estilos CSS para compactar al máximo los espacios y alinear título y mes
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 0.3rem;
        padding-bottom: 2rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;
        max-width: 600px !important; /* Limitar ancho para que no se separe tanto en pantallas grandes */
    }
    
    /* Botones cuadrados compactos */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 2px 0px;
        font-size: 13px;
        font-weight: bold;
        min-height: 24px;
        min-width: 24px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #5a0017;
        color: white;
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

# Título y mes juntos en una sola línea horizontal
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; align-items: baseline; gap: 10px; margin-bottom: 8px;'>
        <h3 style='margin: 0; font-size: 1rem;'>Control de Puntos</h3>
        <span style='color: gray; font-size: 0.75rem;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos las 16 jugadoras en dos columnas muy compactas
for i in range(0, len(jugadoras), 2):
  col1, col2 = st.columns(2)

  # Columna Izquierda
  with col1:
    jugadora_1 = jugadoras[i]
    nc1, nc2, nc3, nc4 = st.columns([2.2, 1, 0.9, 0.9])
    with nc1:
      st.markdown(
          f"<div style='font-size: 0.75rem; font-weight: bold; padding-top: 5px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'>{jugadora_1}</div>",
          unsafe_allow_html=True,
      )
    with nc2:
      st.markdown(
          f"<div style='font-size: 0.75rem; padding-top: 5px; text-align: center;'><b>{puntos_mes[jugadora_1]}</b></div>",
          unsafe_allow_html=True,
      )
    with nc3:
      if st.button("-", key=f"menos_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) - 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    with nc4:
      if st.button("+", key=f"mas_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) + 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()

  # Columna Derecha
  if i + 1 < len(jugadoras):
    with col2:
      jugadora_2 = jugadoras[i + 1]
      dc1, dc2, dc3, dc4 = st.columns([2.2, 1, 0.9, 0.9])
      with dc1:
        st.markdown(
            f"<div style='font-size: 0.75rem; font-weight: bold; padding-top: 5px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'>{jugadora_2}</div>",
            unsafe_allow_html=True,
        )
      with dc2:
        st.markdown(
            f"<div style='font-size: 0.75rem; padding-top: 5px; text-align: center;'><b>{puntos_mes[jugadora_2]}</b></div>",
            unsafe_allow_html=True,
        )
      with dc3:
        if st.button("-", key=f"menos_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) - 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
      with dc4:
        if st.button("+", key=f"mas_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) + 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
