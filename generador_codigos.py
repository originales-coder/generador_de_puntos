import datetime
import json
import os
import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="centered"
)

# Estilos CSS muy potentes para forzar 2 columnas reales en móvil y ocultar elementos sobrantes
st.markdown(
    """
    <style>
    /* Ocultar barra superior molesta de Streamlit para ganar espacio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* Contenedor principal de la rejilla de 2 columnas */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr; /* 2 columnas exactas */
        gap: 8px;
        margin-bottom: 10px;
    }
    
    /* Tarjeta individual para cada jugadora */
    .jugadora-box {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 6px 8px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .nombre-jugadora {
        font-size: 0.9rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .fila-controles {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 4px;
    }
    
    .puntos-texto {
        font-size: 0.85rem;
        font-weight: bold;
        color: #555;
    }
    
    /* Botones granates compactos */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 2px 6px;
        font-size: 14px;
        font-weight: bold;
        min-height: 28px;
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

# Cabecera compacta
st.markdown(
    "<h2 style='text-align: center; font-size: 1.2rem; margin-bottom: 0px;'>Control de Puntos</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 0.75rem; margin-top: 0px; margin-bottom: 10px;'>Mes: {mes_actual}</p>",
    unsafe_allow_html=True,
)

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Renderizamos usando filas de 2 elementos para asegurar la cuadrícula visual
for i in range(0, len(jugadoras), 2):
  col1, col2 = st.columns(2)

  # Jugadora izquierda
  with col1:
    jugadora_1 = jugadoras[i]
    st.markdown(
        f"<div class='nombre-jugadora'>{jugadora_1}</div>",
        unsafe_allow_html=True,
    )
    b_1, b_2, b_3 = st.columns([1.2, 1, 1])
    with b_1:
      st.markdown(
          f"<div style='font-size: 0.85rem; padding-top: 4px;'><b>{puntos_mes[jugadora_1]}</b> pts</div>",
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
        "<hr style='margin: 4px 0px; opacity: 0.1;'>", unsafe_allow_html=True
    )

  # Jugadora derecha (si existe)
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
            f"<div style='font-size: 0.85rem; padding-top: 4px;'><b>{puntos_mes[jugadora_2]}</b> pts</div>",
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
          "<hr style='margin: 4px 0px; opacity: 0.1;'>", unsafe_allow_html=True
      )
