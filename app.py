
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Datos de ejemplo (puedes reemplazar esto con carga desde archivo)
cursos = [
    {
        "codigo": "ICO09412",
        "nombre": "Finanzas II",
        "seccion": "1",
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "catedra": "MA JU 11:30 - 12:50",
        "ayudantia": "VI 08:30 - 09:50",
        "paquete": "Paquete A"
    },
    {
        "codigo": "ICO09412",
        "nombre": "Finanzas II",
        "seccion": "2",
        "profesor": "RANTUL FRANCISCO OSIEL",
        "catedra": "LU MI 08:30 - 09:50",
        "ayudantia": "",
        "paquete": "Paquete A"
    },
    {
        "codigo": "ICO09320",
        "nombre": "Recursos Humanos",
        "seccion": "1",
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "catedra": "VI 11:30 - 12:50",
        "ayudantia": "",
        "paquete": "Paquete B"
    },
]

tramos = [
    "08:30 - 09:50",
    "10:00 - 11:20",
    "11:30 - 12:50",
    "13:00 - 14:20",
    "14:30 - 15:50",
    "16:00 - 17:20",
    "17:25 - 18:45"
]
dias = ["LU", "MA", "MI", "JU", "VI"]

# Inicializar sesión
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

def extraer_bloques(texto):
    bloques = []
    if not texto:
        return bloques
    partes = texto.split()
    i = 0
    while i < len(partes):
        if partes[i] in dias:
            try:
                if partes[i+1] in dias:
                    horas = partes[i+2]
                    bloques.append((partes[i], horas))
                    bloques.append((partes[i+1], horas))
                    i += 3
                else:
                    horas = partes[i+1]
                    bloques.append((partes[i], horas))
                    i += 2
            except IndexError:
                break
        else:
            i += 1
    return bloques

def agregar_al_horario(curso):
    bloques = extraer_bloques(curso["catedra"]) + extraer_bloques(curso["ayudantia"])
    for dia, tramo in bloques:
        horario.at[tramo, dia] = curso["nombre"]
    st.session_state.seleccionados.append(curso)

# Construir horario base
horario = pd.DataFrame("", index=tramos, columns=dias)

st.markdown("### 📚 Cursos disponibles:")

cols = st.columns(3)
for i, curso in enumerate(cursos):
    with cols[i % 3]:
        if st.button(f"**{curso['nombre']}** Sección {curso['seccion']}", key=f"{curso['codigo']}-{curso['seccion']}"):
            agregar_al_horario(curso)
            st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

st.markdown("### 🗓️ Mi horario actual")
st.dataframe(horario, height=400)

st.markdown("### 📋 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}  
*{curso['paquete']}*")
