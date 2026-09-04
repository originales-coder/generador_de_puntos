import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="wide"
)

# Estilos CSS avanzados para eliminar espacios muertos por completo
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 0.4rem;
        padding-bottom: 2rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;
        max-width: 100% !important;
    }
    
    /* Contenedor principal en 2 columnas reales de CSS sin huecos raros */
    .contenedor-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px 12px;
    }
    
    /* Cada fila de jugadora con distribución compacta */
    .fila-jugadora {
        display: flex;
        align-items: center;
        background-color: #fafafa;
        border-radius: 6px;
        padding: 4px 8px;
        justify-content: space-between;
    }
    
    .info-jugadora {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-grow: 1;
        overflow: hidden;
    }
    
    .nombre-jugadora {
        font-size: 0.95rem;
        font-weight: bold;
        color: #222;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .puntos-jugadora {
        font-size: 0.95rem;
        font-weight: bold;
        color: #555;
        white-space: nowrap;
    }
    
    /* Grupo de botones juntos y compactos */
    .grupo-botones {
        display: flex;
        gap: 4px;
        align-items: center;
    }
    
    /* Botones cuadrados y táctiles */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 2px 8px;
        font-size: 16px;
        font-weight: bold;
        min-height: 32px;
        min-width: 32px;
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

# Título y mes limpios
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 12px;'>
        <h2 style='margin: 0; font-size: 1.3rem; display: inline-block;'>Control de Puntos</h2>
        <span style='color: gray; font-size: 0.9rem; margin-left: 8px;'>({mes_actual})</span>
    </div>
""",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos usando una estructura de rejilla limpia en HTML/CSS
st.markdown("<div class='contenedor-grid'>", unsafe_allow_html=True)

for jugadora in jugadoras:
  puntos = puntos_mes[jugadora]

  # Abrimos la tarjeta de la jugadora
  st.markdown(
      f"""
        <div class='fila-jugadora'>
            <div class='info-jugadora'>
                <span class='nombre-jugadora'>{jugadora}</span>
                <span class='puntos-jugadora'>{puntos} pts</span>
            </div>
    """,
      unsafe_allow_html=True,
  )

  # Botones interactivos de Streamlit colocados de forma nativa
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

st.markdown("</div>", unsafe_allow_html=True)
