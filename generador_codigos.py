import datetime
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
    div.stMarkdown {
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Archivo de persistencia de datos
JSON_FILE = "historial_puntos.json"

# Obtener el mes actual en formato 'YYYY-MM'
mes_actual = datetime.datetime.now().strftime("%Y-%m")


# Cargar datos iniciales
def cargar_datos():
  if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      # Asegurar compatibilidad si el JSON es antiguo o por meses
      if "2026-09" in data or any("-" in k for k in data.keys()):
        return data
      else:
        # Estructura antigua a mensual por defecto
        return {
            mes_actual: {
                jugadora: puntos for jugadora, puntos in data.items()
            }
        }
  else:
    # 16 jugadoras por defecto para el mes actual
    jugadoras_def = {f"Jugadora {i+1}": 0 for i in range(16)}
    return {mes_actual: jugadoras_def}


# Guardar datos
def guardar_datos(datos):
  with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=4)


# Inicializar estado
if "historial" not in st.session_state:
  st.session_state.historial = cargar_datos()

# Asegurar que el mes actual existe en el estado
if mes_actual not in st.session_state.historial:
  # Copiar nombres con 0 puntos del mes anterior o iniciar vacíos
  primer_jugadora = {f"Jugadora {i+1}": 0 for i in range(16)}
  st.session_state.historial[mes_actual] = primer_jugadora

st.title("🏆 Control de Puntos")
st.subheader(f"Mes: {mes_actual}")

# Organizar en 2 columnas para aprovechar la pantalla del móvil
puntos_mes = st.session_state.historial[mes_actual]
jugadoras = list(puntos_mes.keys())
cols = st.columns(2)

for i, jugadora in enumerate(jugadoras):
  col_actual = cols[i % 2]
  with col_actual:
    st.markdown(f"**{jugadora}**")
    st.info(f"Puntos: {puntos_mes[jugadora]}")

    # Botones de restar y sumar en subcolumnas compactas
    c1, c2 = st.columns(2)
    with c1:
      if st.button("-", key=f"menos_{jugadora}"):
        st.session_state.historial[mes_actual][jugadora] -= 1
        guardar_datos(st.session_state.historial)
        st.rerun()
    with c2:
      if st.button("+", key=f"mas_{jugadora}"):
        st.session_state.historial[mes_actual][jugadora] += 1
        guardar_datos(st.session_state.historial)
        st.rerun()

    st.markdown("---")
