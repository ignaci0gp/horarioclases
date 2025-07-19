import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# Constantes
DIAS = ["LU", "MA", "MI", "JU", "VI"]
BLOQUES_HORARIOS = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"
]
DIA_BLOQUES = {h: i for i, h in enumerate(BLOQUES_HORARIOS)}

# Función para dividir rangos largos en tramos de 1h20m
def dividir_bloque_largo(inicio, fin):
    fmt = "%H:%M"
    inicio_dt = datetime.strptime(inicio, fmt)
    fin_dt = datetime.strptime(fin, fmt)
    bloques = []
    actual = inicio_dt
    while actual + timedelta(minutes=80) <= fin_dt:
        bloque_inicio = actual.strftime(fmt)
        bloque_fin = (actual + timedelta(minutes=80)).strftime(fmt)
        bloques.append(f"{bloque_inicio} - {bloque_fin}")
        actual += timedelta(minutes=90)
    return bloques

# Extrae los bloques horarios desde un string tipo "MA JU 11:30 - 12:50"
def extraer_bloques(cadena):
    if cadena.strip().lower() == "no hay":
        return []
    partes = cadena.split()
    dias = [p for p in partes if p in DIAS]
    hora_inicio, _, hora_fin = partes[-3:]
    bloques = dividir_bloque_largo(hora_inicio, hora_fin)
    return [[dia, DIA_BLOQUES[b]] for dia in dias for b in bloques]

# Cargar cursos
with open("cursos.json", "r", encoding="utf-8") as f:
    cursos = json.load(f)

st.set_page_config(layout="wide")
st.markdown("# 📅 Planificador de Horarios Universitarios")

# Sesión
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📚 Cursos Disponibles")
    for i, curso in enumerate(cursos):
        nombre = f"{curso['nombre']} - {curso['seccion']}"
        if any(c["paquete"] == curso["paquete"] for c in st.session_state.seleccionados):
            st.button(nombre, key=f"{i}_disabled", disabled=True)
        elif st.button(nombre, key=i):
            st.session_state.seleccionados.append(curso)

with col2:
    st.subheader("🗓️ Horario")
    data = [["" for _ in DIAS] for _ in BLOQUES_HORARIOS]
    df = pd.DataFrame(data, columns=DIAS, index=BLOQUES_HORARIOS)

    for curso in st.session_state.seleccionados:
        bloques_catedra = extraer_bloques(curso["catedra"])
        bloques_ayudantia = extraer_bloques(curso["ayudantia"])
        for dia, bloque in bloques_catedra:
            df.at[BLOQUES_HORARIOS[bloque], dia] = curso["nombre"]
        for dia, bloque in bloques_ayudantia:
            df.at[BLOQUES_HORARIOS[bloque], dia] = f"Ayudantía {curso['nombre']}"

    st.dataframe(df, use_container_width=True)

st.markdown("## 🧾 Cursos Seleccionados")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - {curso['seccion']}** — {curso['profesor']} — *{curso['paquete']}*")
