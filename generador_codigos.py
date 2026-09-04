import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="wide"
)

# Estilos CSS para maximizar el ancho, eliminar márgenes y hacer todo grande
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Eliminar los márgenes laterales gigantes de Streamlit para ganar espacio real */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        padding-left: 0.3rem;
        padding-right: 0.3rem;
        max-width: 100% !important;
    }
    
    /* Forzar que las dos columnas principales ocupen el 50% exacto cada una */
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0px 2px !important;
    }
    
    /* Tarjeta horizontal compacta pero con letra grande */
    .fila-horizontal {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #fafafa;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 6px 8px;
        margin-bottom: 6px;
    }
    
    /* Botones grandes y fáciles de pulsar */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 2px 0px;
        font-size: 16px;
        font-weight: bold;
        min-height: 36px;
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

# Título y mes limpios y en una línea
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h2 style='margin: 0; font-size: 1.3rem; display: inline-block;'>Control de Puntos</h2>
        <span style='color: gray; font-size: 0.9rem; margin-left: 8px;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos las 16 jugadoras en dos columnas aprovechando todo el ancho
for i in range(0, len(jugadoras), 2):
  col1, col2 = st.columns(2)

  # Columna Izquierda
  with col1:
    jugadora_1 = jugadoras[i]
    st.markdown(
        f"<div class='fila-horizontal'>", unsafe_allow_html=True
    )

    nc1, nc2, nc3, nc4 = st.columns([2.2, 1.1, 1, 1])
    with nc1:
      st.markdown(
          f"<div style='font-size: 0.9rem; font-weight: bold; color: #222; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding-top: 6px;'>{jugadora_1}</div>",
          unsafe_allow_html=True,
      )
    with nc2:
      st.markdown(
          f"<div style='font-size: 0.95rem; font-weight: bold; color: #444; text-align: center; padding-top: 6px;'>{puntos_mes[jugadora_1]} pts</div>",
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

    st.markdown("</div>", unsafe_allow_html=True)

  # Columna Derecha
  if i + 1 < len(jugadoras):
    with col2:
      jugadora_2 = jugadoras[i + 1]
      st.markdown(
          f"<div class='fila-horizontal'>", unsafe_allow_html=True
      )

      dc1, dc2, dc3, dc4 = st.columns([2.2, 1.1, 1, 1])
      with dc1:
        st.markdown(
            f"<div style='font-size: 0.9rem; font-weight: bold; color: #222; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding-top: 6px;'>{jugadora_2}</div>",
            unsafe_allow_html=True,
        )
      with dc2:
        st.markdown(
            f"<div style='font-size: 0.95rem; font-weight: bold; color: #444; text-align: center; padding-top: 6px;'>{puntos_mes[jugadora_2]} pts</div>",
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

      st.markdown("</div>", unsafe_allow_html=True)
