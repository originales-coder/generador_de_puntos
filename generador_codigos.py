import datetime
import json
import os
import streamlit as st

st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="wide"
)

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
        max-width: 100% !important;
    }
    
    [data-testid="column"] {
        padding: 0px 2px !important;
    }
    
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0px;
        font-size: 14px;
        font-weight: bold;
        height: 28px;
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

# Título y mes en una misma línea horizontal
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h3 style='margin: 0; font-size: 1.2rem; display: inline-block;'>Control de Puntos</h3>
        <span style='color: gray; font-size: 0.85rem; margin-left: 6px;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos en 2 columnas principales, y cada una con una línea compacta
for i in range(0, len(jugadoras), 2):
  col_principal1, col_principal2 = st.columns(2)

  # --- Jugadora Izquierda ---
  with col_principal1:
    jugadora_1 = jugadoras[i]
    # Subcolumnas ultra juntas en una sola fila: [Nombre, Puntos, Botón -, Botón +]
    c1, c2, c3, c4 = st.columns([2.2, 1, 0.7, 0.7])
    with c1:
      st.markdown(
          f"<div style='font-size: 0.85rem; font-weight: bold; padding-top: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{jugadora_1}</div>",
          unsafe_allow_html=True,
      )
    with c2:
      st.markdown(
          f"<div style='font-size: 0.85rem; padding-top: 5px; text-align: center;'><b>{puntos_mes[jugadora_1]}</b></div>",
          unsafe_allow_html=True,
      )
    with c3:
      if st.button("-", key=f"menos_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) - 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    with c4:
      if st.button("+", key=f"mas_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) + 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()

  # --- Jugadora Derecha ---
  if i + 1 < len(jugadoras):
    with col_principal2:
      jugadora_2 = jugadoras[i + 1]
      c5, c6, c7, c8 = st.columns([2.2, 1, 0.7, 0.7])
      with c5:
        st.markdown(
            f"<div style='font-size: 0.85rem; font-weight: bold; padding-top: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{jugadora_2}</div>",
            unsafe_allow_html=True,
        )
      with c6:
        st.markdown(
            f"<div style='font-size: 0.85rem; padding-top: 5px; text-align: center;'><b>{puntos_mes[jugadora_2]}</b></div>",
            unsafe_allow_html=True,
        )
      with c7:
        if st.button("-", key=f"menos_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) - 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
      with c8:
        if st.button("+", key=f"mas_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) + 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
