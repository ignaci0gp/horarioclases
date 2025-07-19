
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📅 Mi horario actual")

DIAS = ["LU", "MA", "MI", "JU", "VI"]
BLOQUES = [
    "08:30 - 09:50",
    "10:00 - 11:20",
    "11:30 - 12:50",
    "13:00 - 14:20",
    "14:30 - 15:50",
    "16:00 - 17:20",
    "17:25 - 18:45",
]

HORAS_BLOQUE = {bloque: i for i, bloque in enumerate(BLOQUES)}
BLOQUE_HORA = {i: bloque for i, bloque in enumerate(BLOQUES)}

def dividir_bloque_largo(inicio, fin):
    fmt = "%H:%M"
    inicio_dt = datetime.strptime(inicio, fmt)
    fin_dt = datetime.strptime(fin, fmt)
    bloques = []
    while inicio_dt < fin_dt:
        bloque_fin = inicio_dt + timedelta(hours=1, minutes=20)
        bloques.append((inicio_dt.strftime(fmt), bloque_fin.strftime(fmt)))
        inicio_dt = bloque_fin + timedelta(minutes=10)
    return bloques

def extraer_bloques(cadena):
    partes = cadena.split()
    dias = [p for p in partes if p in DIAS]
    hora_inicio = partes[-3]
    hora_fin = partes[-1]
    rangos = dividir_bloque_largo(hora_inicio, hora_fin)
    resultado = []
    for dia in dias:
        for inicio, fin in rangos:
            bloque_str = f"{inicio} - {fin}"
            if bloque_str in HORAS_BLOQUE:
                resultado.append((dia, HORAS_BLOQUE[bloque_str]))
    return resultado

def inicializar_estado():
    if "seleccionados" not in st.session_state:
        st.session_state.seleccionados = []

def agregar_curso(curso):
    st.session_state.seleccionados.append(curso)

def eliminar_curso(index):
    if 0 <= index < len(st.session_state.seleccionados):
        st.session_state.seleccionados.pop(index)

# Datos de ejemplo organizados
cursos = [
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "1", "catedra": "MA JU 16:00 - 17:20", "ayudantia": "VI 16:00 - 17:20", "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "ICO09411_V01"},
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "2", "catedra": "MA JU 17:25 - 18:45", "ayudantia": "VI 16:00 - 17:20", "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "ICO09411_V02"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "1", "catedra": "MA JU 11:30 - 12:50", "ayudantia": "VI 08:30 - 09:50", "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "ICO09412_V01"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "2", "catedra": "MA JU 10:00 - 11:20", "ayudantia": "VI 08:30 - 09:50", "profesor": "RANTUL FRANCISCO OSIEL", "paquete": "ICO09412_V02"},
    {"codigo": "ICO09413", "nombre": "Recursos Humanos", "seccion": "1", "catedra": "LU MI 13:00 - 14:20", "ayudantia": "VI 13:00 - 14:20", "profesor": "TOLEDO MIGUEL APOLONIO", "paquete": "ICO09413_V01"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "1", "catedra": "MA 13:00 - 15:50", "ayudantia": "", "profesor": "FERNANDEZ ANDRES JOSE", "paquete": "ICO09414_V01"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "2", "catedra": "MA 13:00 - 15:50", "ayudantia": "", "profesor": "MUENA PAULINA", "paquete": "ICO09414_V02"},
]

inicializar_estado()

st.markdown("### 📚 Cursos disponibles:")
for curso in cursos:
    if st.button(f"{curso['nombre']} Sección {curso['seccion']}", key=curso["paquete"]):
        agregar_curso(curso)
        st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

# Crear horario base
horario = pd.DataFrame("", index=BLOQUES, columns=DIAS)

for curso in st.session_state.seleccionados:
    for bloque in extraer_bloques(curso["catedra"]):
        dia, num = bloque
        horario.loc[BLOQUE_HORA[num], dia] = curso["nombre"]
    if curso["ayudantia"]:
        for bloque in extraer_bloques(curso["ayudantia"]):
            dia, num = bloque
            horario.loc[BLOQUE_HORA[num], dia] = f"Ayudantía {curso['nombre']}"

st.markdown("### 🗓️ Mi horario actual")
st.dataframe(horario, use_container_width=True, height=400)

st.markdown("### 📋 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}  \n*{curso['paquete']}*")

    if st.button(f"❌ Eliminar {curso['nombre']} Sección {curso['seccion']}", key=f"eliminar_{i}"):
        eliminar_curso(i-1)
        st.rerun()
