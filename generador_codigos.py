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
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 800px !important;
    }
    
    /* Botones ajustados y cómodos */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        font-size: 24px;
        font-weight: bold;
        height: 50px;
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

# Título y mes compactos en la misma línea
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; align-items: baseline; gap: 8px; margin-bottom: 8px;'>
        <h2 style='margin: 0; font-size: 1.8rem; color: #111;'>Control de Puntos</h2>
        <span style='color: #555; font-size: 1.1rem; font-weight: bold;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

for jugadora in jugadoras:
  puntos = puntos_mes[jugadora]

  # Tarjeta con fuente a 5rem exactos
  st.markdown(
      """
        <div style='background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 6px; padding: 4px 8px; margin-bottom: 2px;'>
    """,
      unsafe_allow_html=True,
  )

  c1, c2, c3, c4 = st.columns([2.5, 1.2, 0.8, 0.8])

  with c1:
    st.markdown(
        f"<div style='font-size: 5rem; font-weight: bold; color: #111; line-height: 1.1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{jugadora}</div>",
        unsafe_allow_html=True,
    )
  with c2:
    st.markdown(
        f"<div style='font-size: 5rem; font-weight: bold; color: #800020; line-height: 1.1; text-align: center;'>{puntos}</div>",
        unsafe_allow_html=True,
    )
  with c3:
    if st.button("-", key=f"menos_{jugadora}"):
      st.session_state.historial[mes_actual][jugadora] = (
          int(st.session_state.historial[mes_actual].get(jugadora, 0)) - 1
      )
      guardar_datos(st.session_state.historial)
      st.rerun()
  with c4:
    if st.button("+", key=f"mas_{jugadora}"):
      st.session_state.historial[mes_actual][jugadora] = (
          int(st.session_state.historial[mes_actual].get(jugadora, 0)) + 1
      )
      guardar_datos(st.session_state.historial)
      st.rerun()

  st.markdown("</div>", unsafe_allow_html=True)
