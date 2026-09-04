import datetime
import json
import os
import streamlit as st

# Configuración ampliada para aprovechar mejor la pantalla del S23
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="wide"
)

# Estilos CSS avanzados para ajustar márgenes y densidad en móvil
st.markdown(
    """
    <style>
    /* Forzar diseño más compacto y aprovechar ancho en móviles */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    /* Estilo de los botones granates adaptados a táctil */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 4px 8px;
        font-size: 15px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #5a0017;
        color: white;
    }
    /* Reducir separación de las cajas informativas de puntos */
    div[data-testid="stInfo"] {
        padding: 6px;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    h3, h2, h1 {
        text-align: center;
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

st.title("🏆 Puntos")
st.caption(f"Mes: {mes_actual}")

puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())

# Dividimos en 2 columnas para ver varias jugadoras a la vez cómodamente
cols = st.columns(2)

for i, jugadora in enumerate(jugadoras):
  col_actual = cols[i % 2]
  with col_actual:
    st.markdown(f"**{jugadora}**")
    st.info(f"Pts: **{puntos_mes[jugadora]}**")

    # Botones compactos de restar y sumar
    c1, c2 = st.columns(2)
    with c1:
      if st.button("-", key=f"menos_{jugadora}"):
        st.session_state.historial[mes_actual][jugadora] = (
            int(st.session_state.historial[mes_actual].get(jugadora, 0)) - 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()
    with c2:
      if st.button("+", key=f"mas_{jugadora}"):
        st.session_state.historial[mes_actual][jugadora] = (
            int(st.session_state.historial[mes_actual].get(jugadora, 0)) + 1
        )
        guardar_datos(st.session_state.historial)
        st.rerun()

    st.write("")  # Pequeño espacio separador entre filas
