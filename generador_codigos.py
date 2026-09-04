import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", layout="centered"
)

# Estilos CSS para tarjetas grandes y táctiles optimizadas para el S23
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        max-width: 700px !important;
    }
    
    /* Tarjeta individual grande y clara para cada jugadora */
    .tarjeta-jugadora {
        background-color: #fcfcfc;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 8px 10px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Botones grandes, granates y muy fáciles de pulsar */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 4px 0px;
        font-size: 18px;
        font-weight: bold;
        min-height: 38px;
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

# Título y mes limpios y legibles
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 12px;'>
        <h2 style='margin: 0; font-size: 1.5rem; color: #111;'>Control de Puntos</h2>
        <span style='color: #666; font-size: 0.9rem;'>Mes: {mes_actual}</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos en 2 columnas con tarjetas claras y de tamaño grande
for i in range(0, len(jugadoras), 2):
  col1, col2 = st.columns(2)

  # Jugadora Izquierda
  with col1:
    jugadora_1 = jugadoras[i]
    st.markdown(
        f"""
        <div class='tarjeta-jugadora'>
            <div style='font-size: 1rem; font-weight: bold; color: #222; margin-bottom: 4px;'>{jugadora_1}</div>
    """,
        unsafe_allow_html=True,
    )

    sc1, sc2, sc3 = st.columns([1.2, 1, 1])
    with sc1:
      st.markdown(
          f"<div style='font-size: 1rem; font-weight: bold; padding-top: 8px;'>{puntos_mes[jugadora_1]} pts</div>",
          unsafe_allow_html=True,
      )
    with sc2:
      if st.button("-", key=f"menos_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) - 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    with sc3:
      if st.button("+", key=f"mas_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) + 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

  # Jugadora Derecha
  if i + 1 < len(jugadoras):
    with col2:
      jugadora_2 = jugadoras[i + 1]
      st.markdown(
          f"""
            <div class='tarjeta-jugadora'>
                <div style='font-size: 1rem; font-weight: bold; color: #222; margin-bottom: 4px;'>{jugadora_2}</div>
        """,
          unsafe_allow_html=True,
      )

      dc1, dc2, dc3 = st.columns([1.2, 1, 1])
      with dc1:
        st.markdown(
            f"<div style='font-size: 1rem; font-weight: bold; padding-top: 8px;'>{puntos_mes[jugadora_2]} pts</div>",
            unsafe_allow_html=True,
        )
      with dc2:
        if st.button("-", key=f"menos_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) - 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
      with dc3:
        if st.button("+", key=f"mas_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) + 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()

      st.markdown("</div>", unsafe_allow_html=True)
