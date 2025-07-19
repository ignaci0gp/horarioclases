
import streamlit as st
from datetime import datetime

# Diccionarios de utilidad
DIAS = ["LU", "MA", "MI", "JU", "VI"]
DIA_COLUMNAS = {"LU": 0, "MA": 1, "MI": 2, "JU": 3, "VI": 4}
BLOQUES = ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20",
           "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"]
HORARIO = [[None for _ in range(5)] for _ in range(len(BLOQUES))]

# Cursos predefinidos
CURSOS = [
    {
        "nombre": "Fund. Económicos de la Org.",
        "seccion": "1",
        "catedra": "MA JU 16:00 - 17:20",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "Muñoz",
        "paquete": "ICO09411_V01"
    },
    {
        "nombre": "Fund. Económicos de la Org.",
        "seccion": "2",
        "catedra": "MA JU 17:25 - 18:45",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "Muñoz",
        "paquete": "ICO09411_V02"
    },
    {
        "nombre": "Finanzas II",
        "seccion": "1",
        "catedra": "MA JU 11:30 - 12:50",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "Yañez",
        "paquete": "ICO09412_V01"
    },
    {
        "nombre": "Finanzas II",
        "seccion": "2",
        "catedra": "MA JU 10:00 - 11:20",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "Rantul",
        "paquete": "ICO09412_V02"
    },
    {
        "nombre": "Recursos Humanos",
        "seccion": "1",
        "catedra": "LU MI 13:00 - 14:20",
        "ayudantia": "VI 13:00 - 14:20",
        "profesor": "Toledo",
        "paquete": "ICO09413_V01"
    },
    {
        "nombre": "Taller Emprendimiento",
        "seccion": "1",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "No hay",
        "profesor": "Fernandez",
        "paquete": "ICO09414_V01"
    },
    {
        "nombre": "Taller Emprendimiento",
        "seccion": "2",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "No hay",
        "profesor": "Muena",
        "paquete": "ICO09414_V02"
    },
]

# Streamlit layout
st.set_page_config(layout="wide")
st.title("📅 Planificador de Horarios Universitarios")

col1, col2 = st.columns([1, 3])
with col1:
    st.header("Cursos Disponibles")
    for idx, curso in enumerate(CURSOS):
        if st.button(f"{curso['nombre']} - Sección {curso['seccion']}", key=idx):
            st.session_state.selected = st.session_state.get("selected", [])
            ya_existe = any(c["nombre"] == curso["nombre"] for c in st.session_state.selected)
            if not ya_existe:
                st.session_state.selected.append(curso)
            else:
                st.warning("Ya agregaste otra sección de este curso.")

with col2:
    st.header("Horario")
    data = [["" for _ in range(5)] for _ in range(len(BLOQUES))]
    if "selected" in st.session_state:
        for curso in st.session_state.selected:
            bloques = [curso["catedra"], curso["ayudantia"]]
            for b in bloques:
                if b == "No hay": continue
                dias, hora_ini, _, hora_fin = b.split()
                for dia in dias.split():
                    if dia not in DIA_COLUMNAS: continue
                    col = DIA_COLUMNAS[dia]
                    try:
                        fila = BLOQUES.index(f"{hora_ini} - {hora_fin}")
                        data[fila][col] = curso["nombre"]
                    except:
                        pass
    st.dataframe(data, column_order=DIAS, use_container_width=True, hide_index=True)

st.markdown("### Cursos Seleccionados")
if "selected" in st.session_state:
    for i, curso in enumerate(st.session_state.selected, 1):
        st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}")
