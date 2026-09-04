import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="centered"
)

# Estilos CSS optimizados para móvil: tamaño grande y forzar rejilla visible
st.markdown(
    """
    <style>
    /* Ocultar elementos de Streamlit que ocupan espacio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        max-width: 100% !important;
    }
    
    /* Forzar que las columnas de Streamlit se queden lado a lado en móvil */
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0px 4px !important;
    }
    
    /* Tamaño grande y legible para los nombres de las jugadoras */
    .nombre-jugadora {
        font-size: 1.1rem;
        font-weight: bold;
        color: #222;
        margin-bottom: 2px;
    }
    
    /* Tamaño grande para el texto de puntos */
    .puntos-texto {
        font-size: 1rem;
        font-weight: bold;
        color: #444;
        padding-top: 6px;
    }
    
    /* Botones grandes y fáciles de pulsar con el dedo */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 6px 0px;
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

# Cabecera
st.markdown(
    "<h2 style='text-align: center; font-size: 1.4rem; margin-bottom: 0px;'>Control de Puntos</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 0.85rem; margin-top: 0px; margin-bottom: 15px;'>Mes: {mes_actual}</p>",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos las filas de 2 en 2 asegurando el ancho del 50% por columna
for i in range(0, len(jugadoras), 2):
  col1, col2 = st.columns(2)

  with col1:
    jugadora_1 = jugadoras[i]
    st.markdown(
        f"<div class='nombre-jugadora'>{jugadora_1}</div>",
        unsafe_allow_html=True,
    )
    b_1, b_2, b_3 = st.columns([1.2, 1, 1])
    with b_1:
      st.markdown(
          f"<div class='puntos-texto'>{puntos_mes[jugadora_1]} pts</div>",
          unsafe_allow_html=True,
      )
    with b_2:
      if st.button("-", key=f"menos_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) - 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    with b_3:
      if st.button("+", key=f"mas_{jugadora_1}"):
        st.session_state.historial[mes_actual][jugadora_1] = (
            int(st.session_state.historial[mes_actual].get(jugadora_1, 0)) + 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    st.markdown(
        "<hr style='margin: 8px 0px; opacity: 0.15;'>", unsafe_allow_html=True
    )

  if i + 1 < len(jugadoras):
    with col2:
      jugadora_2 = jugadoras[i + 1]
      st.markdown(
          f"<div class='nombre-jugadora'>{jugadora_2}</div>",
          unsafe_allow_html=True,
      )
      c_1, c_2, c_3 = st.columns([1.2, 1, 1])
      with c_1:
        st.markdown(
            f"<div class='puntos-texto'>{puntos_mes[jugadora_2]} pts</div>",
            unsafe_allow_html=True,
        )
      with c_2:
        if st.button("-", key=f"menos_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) - 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
      with c_3:
        if st.button("+", key=f"mas_{jugadora_2}"):
          st.session_state.historial[mes_actual][jugadora_2] = (
              int(st.session_state.historial[mes_actual].get(jugadora_2, 0)) + 1
          )
          guardar_datos(st.session_state.historial)
          st.rerun()
      st.markdown(
          "<hr style='margin: 8px 0px; opacity: 0.15;'>", unsafe_allow_html=True
      )
