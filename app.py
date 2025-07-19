
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📅 Planificador de Horarios Universitarios")

# Constantes
DIAS = ["LU", "MA", "MI", "JU", "VI"]
BLOQUES = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"
]
DIA_IDX = {"LU": 0, "MA": 1, "MI": 2, "JU": 3, "VI": 4}
BLOQUE_IDX = {bloque: i for i, bloque in enumerate(BLOQUES)}

# Datos de cursos
cursos_disponibles = [
    {
        "nombre": "Fund. Económicos",
        "seccion": "1",
        "catedra": "MA JU 16:00 - 17:20",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "Muñoz",
        "paquete": "ICO09411_V01"
    },
    {
        "nombre": "Fund. Económicos",
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
        "nombre": "Recursos Humanos",
        "seccion": "1",
        "catedra": "LU MI 13:00 - 14:20",
        "ayudantia": "VI 13:00 - 14:20",
        "profesor": "Toledo",
        "paquete": "ICO09413_V01"
    }
]

# Estado de sesión
if "cursos_seleccionados" not in st.session_state:
    st.session_state.cursos_seleccionados = []

# Utilidades
def obtener_bloques(horario_str):
    if horario_str.strip().lower() == "no hay":
        return []
    partes = horario_str.split()
    dias = partes[:-3]
    hora_inicio = partes[-3]
    hora_fin = partes[-1]
    bloques = []

    def bloque_index(hora):
        for i, rango in enumerate(BLOQUES):
            inicio, fin = rango.split(" - ")
            if inicio == hora:
                return i
        return -1

    idx_ini = bloque_index(hora_inicio)
    idx_fin = bloque_index(hora_fin)
    if idx_ini == -1 or idx_fin == -1:
        return []
    for dia in dias:
        for idx in range(idx_ini, idx_fin + 1):
            bloques.append((dia, BLOQUES[idx]))
    return bloques

# Layout
col1, col2 = st.columns([1, 4])
with col1:
    st.subheader("Cursos Disponibles")
    for i, curso in enumerate(cursos_disponibles):
        label = f"{curso['nombre']} - Sección {curso['seccion']}"
        if st.button(label, key=f"btn_{i}"):
            st.session_state.cursos_seleccionados.append(curso)

with col2:
    st.subheader("Horario")

    tabla = [["" for _ in range(5)] for _ in BLOQUES]
    for curso in st.session_state.cursos_seleccionados:
        for bloque in obtener_bloques(curso["catedra"]) + obtener_bloques(curso["ayudantia"]):
            dia, hora = bloque
            if dia in DIA_IDX and hora in BLOQUE_IDX:
                i = BLOQUE_IDX[hora]
                j = DIA_IDX[dia]
                if tabla[i][j] == "":
                    tabla[i][j] = curso["nombre"]
                else:
                    tabla[i][j] += f" / {curso['nombre']}"

    df = pd.DataFrame(tabla, index=BLOQUES, columns=DIAS)
    st.dataframe(df, use_container_width=True)

# Cursos seleccionados
st.subheader("Cursos Seleccionados")
for i, curso in enumerate(st.session_state.cursos_seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}")
