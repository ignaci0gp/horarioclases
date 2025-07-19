
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

DIA_BLOQUES = {
    "08:30 - 09:50": 0,
    "10:00 - 11:20": 1,
    "11:30 - 12:50": 2,
    "13:00 - 14:20": 3,
    "14:30 - 15:50": 4,
    "16:00 - 17:20": 5,
    "17:25 - 18:45": 6,
}

DIAS = ["LU", "MA", "MI", "JU", "VI"]

def generar_tabla_horaria():
    data = [["" for _ in range(len(DIAS))] for _ in range(len(DIA_BLOQUES))]
    return pd.DataFrame(data, columns=DIAS, index=DIA_BLOQUES.keys())

def extraer_bloques(horario_str, tipo, nombre):
    bloques = []
    if horario_str.strip().upper() == "NO HAY":
        return bloques
    partes = horario_str.split()
    dias = []
    hora_inicio = None
    for parte in partes:
        if parte in DIA_BLOQUES:
            continue
        if parte in DIAS:
            dias.append(parte)
        elif "-" in parte:
            hora_inicio = " ".join(partes[-3:])
            break
    for dia in dias:
        bloques.append((dia, hora_inicio, tipo, nombre))
    return bloques

def nombre_ayudantia(nombre):
    return f"Ayudantía {nombre}"

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

st.markdown("## 📚 Cursos disponibles:")

cursos = [
    {
        "codigo": "ICO09412",
        "nombre": "Finanzas II",
        "seccion": "1",
        "catedra": "MA JU 11:30 - 12:50",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "paquete": "ICO09412_V01"
    },
    {
        "codigo": "ICO09412",
        "nombre": "Finanzas II",
        "seccion": "2",
        "catedra": "MA JU 10:00 - 11:20",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "RANTUL FRANCISCO OSIEL",
        "paquete": "ICO09412_V02"
    },
    {
        "codigo": "ICO09411",
        "nombre": "Fund. Económicos de la Org.",
        "seccion": "1",
        "catedra": "MA JU 16:00 - 17:20",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "ICO09411_V01"
    },
    {
        "codigo": "ICO09411",
        "nombre": "Fund. Económicos de la Org.",
        "seccion": "2",
        "catedra": "MA JU 17:25 - 18:45",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "ICO09411_V02"
    },
    {
        "codigo": "ICO09413",
        "nombre": "Recursos Humanos",
        "seccion": "1",
        "catedra": "LU MI 13:00 - 14:20",
        "ayudantia": "VI 13:00 - 14:20",
        "profesor": "TOLEDO MIGUEL APOLONIO",
        "paquete": "ICO09413_V01"
    },
    {
        "codigo": "ICO09414",
        "nombre": "Taller Emprendimiento",
        "seccion": "1",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "No hay",
        "profesor": "FERNANDEZ ANDRES JOSE",
        "paquete": "ICO09414_V01"
    },
    {
        "codigo": "ICO09414",
        "nombre": "Taller Emprendimiento",
        "seccion": "2",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "No hay",
        "profesor": "MUENA PAULINA",
        "paquete": "ICO09414_V02"
    }
]

col1, col2 = st.columns([1, 3])

with col1:
    for i, curso in enumerate(cursos):
        key = f"{curso['codigo']}_{curso['seccion']}"
        if st.button(f"{curso['nombre']} Sección {curso['seccion']}", key=key):
            if curso not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(curso)
                st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

with col2:
    tabla = generar_tabla_horaria()
    for curso in st.session_state.seleccionados:
        for dia, hora, tipo, nombre in extraer_bloques(curso["catedra"], "catedra", curso["nombre"]):
            bloque = DIA_BLOQUES[hora]
            tabla.at[hora, dia] = curso["nombre"]
        for dia, hora, tipo, nombre in extraer_bloques(curso["ayudantia"], "ayudantia", curso["nombre"]):
            bloque = DIA_BLOQUES[hora]
            tabla.at[hora, dia] = nombre_ayudantia(nombre)

    st.markdown("## 🗓️ Mi horario actual")
    st.dataframe(tabla, use_container_width=True)

st.markdown("## 📝 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}  \n*{curso['paquete']}*")

