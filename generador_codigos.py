import datetime
import json
import os
import streamlit as st

st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="centered"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 650px !important;
    }
    
    /* Tarjeta grande y clara para cada jugadora */
    .tarjeta-grande {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #f8f9fa;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }
    
    .texto-jugadora {
        font-size: 1.2rem;
        font-weight: bold;
        color: #111;
    }
    
    .puntos-jugadora {
        font-size: 1.2rem;
        font-weight: bold;
        color: #800020;
    }
    
    /* Botones grandes y cómodos */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        font-size: 20px;
        font-weight: bold;
        height: 40px;
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

# Título y mes grandes y unidos en una sola línea
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; font-size: 1.8rem; display: inline-block; color: #111;'>Control de Puntos</h2>
        <span style='color: #555; font-size: 1.1rem; margin-left: 10px; font-weight: bold;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos en una lista vertical limpia con elementos grandes
for jugadora in jugadoras:
  puntos = puntos_mes[jugadora]

  st.markdown(
      f"""
        <div class='tarjeta-grande'>
            <span class='texto-jugadora'>{jugadora}</span>
            <span class='puntos-jugadora'>{puntos} pts</span>
    """,
      unsafe_allow_html=True,
  )

  # Columnas para los botones pegados a la derecha de cada tarjeta
  col_b1, col_b2 = st.columns(2)
  with col_b1:
    if st.button("-", key=f"menos_{jugadora}"):
      st.session_state.historial[mes_actual][jugadora] = (
          int(st.session_state.historial[mes_actual].get(jugadora, 0)) - 1
      )
      guardar_datos(st.session_state.historial)
      st.rerun()
  with col_b2:
    if st.button("+", key=f"mas_{jugadora}"):
      st.session_state.historial[mes_actual][jugadora] = (
          int(st.session_state.historial[mes_actual].get(jugadora, 0)) + 1
      )
      guardar_datos(st.session_state.historial)
      st.rerun()

  st.markdown("</div>", unsafe_allow_html=True)
