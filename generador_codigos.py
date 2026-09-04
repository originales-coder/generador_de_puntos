import json
import os
import streamlit as st

# Configuración de la página optimizada para móvil
st.set_page_config(
    page_title="Control de Puntos", page_icon="🏆", layout="centered"
)

# Estilos CSS personalizados para móvil (botones granates y diseño compacto)
st.markdown(
    """
    <style>
    /* Estilo general y colores granates */
    .stButton > button {
        background-color: #800020;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 6px 12px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #5a0017;
        color: white;
    }
    /* Reducir márgenes de las tarjetas de jugadoras */
    div.stMarkdown {
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Archivo de persistencia de datos
JSON_FILE = "historial_puntos.json"


# Cargar datos iniciales
def cargar_datos():
  if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    # 16 jugadoras por defecto si no existe el archivo
    return {f"Jugadora {i+1}": 0 for i in range(16)}


# Guardar datos
def guardar_datos(datos):
  with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=4)


# Inicializar estado
if "puntos" not in st.session_state:
  st.session_state.puntos = cargar_datos()

st.title("🏆 Control de Puntos")

# Organizar en 2 columnas para aprovechar la pantalla del móvil
jugadoras = list(st.session_state.puntos.keys())
cols = st.columns(2)

for i, jugadora in enumerate(jugadoras):
  col_actual = cols[i % 2]
  with col_actual:
    st.markdown(
        f"**{jugadora}**"
    )  # Nombre de la jugadora centrado o compacto
    st.info(f"Puntos: {st.session_state.puntos[jugadora]}")

    # Botones de restar y sumar en subcolumnas compactas
    c1, c2 = st.columns(2)
    with c1:
      if st.button("-", key=f"menos_{jugadora}"):
        st.session_state.puntos[jugadora] -= 1
        guardar_datos(st.session_state.puntos)
        st.rerun()
    with c2:
      if st.button("+", key=f"mas_{jugadora}"):
        st.session_state.puntos[jugadora] += 1
        guardar_datos(st.session_state.puntos)
        st.rerun()

    st.markdown("---")
