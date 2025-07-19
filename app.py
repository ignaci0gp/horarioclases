
import streamlit as st

st.set_page_config(layout="wide")
st.title("📅 Mi horario actual")

# Días y bloques
dias = ["LU", "MA", "MI", "JU", "VI"]
bloques = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"
]

# Estado inicial
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []
if "horario" not in st.session_state:
    st.session_state.horario = {}

# Datos de los cursos
cursos = [
    {
        "codigo": "ECO101", "nombre": "Fund. Económicos de la Org.",
        "seccion": 1, "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "A",
        "catedra": ["LU 08:30 - 09:50", "JU 17:25 - 18:45"], "ayudantia": []
    },
    {
        "codigo": "ECO101", "nombre": "Fund. Económicos de la Org.",
        "seccion": 2, "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "B",
        "catedra": ["VI 10:00 - 11:20", "JU 13:00 - 14:20"], "ayudantia": []
    },
    {
        "codigo": "FIN201", "nombre": "Finanzas II",
        "seccion": 1, "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "A",
        "catedra": ["LU 10:00 - 11:20", "JU 17:25 - 18:45"],
        "ayudantia": ["MA 11:30 - 12:50", "MI 11:30 - 12:50"]
    },
    {
        "codigo": "FIN201", "nombre": "Finanzas II",
        "seccion": 2, "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "B",
        "catedra": ["VI 08:30 - 09:50", "JU 17:25 - 18:45"],
        "ayudantia": ["MA 11:30 - 12:50", "MI 11:30 - 12:50"]
    },
    {
        "codigo": "RRHH101", "nombre": "Recursos Humanos",
        "seccion": 1, "profesor": "GOMEZ MARIA", "paquete": "C",
        "catedra": ["LU 08:30 - 09:50"], "ayudantia": []
    },
    {
        "codigo": "TALL301", "nombre": "Taller Emprendimiento",
        "seccion": 1, "profesor": "ROJAS MARCELO", "paquete": "A",
        "catedra": ["MI 10:00 - 11:20"], "ayudantia": []
    },
    {
        "codigo": "TALL301", "nombre": "Taller Emprendimiento",
        "seccion": 2, "profesor": "ROJAS MARCELO", "paquete": "B",
        "catedra": ["JU 08:30 - 09:50"], "ayudantia": []
    }
]

# Mostrar cursos como tarjetas
st.markdown("### 🎨 Cursos disponibles:")
cols = st.columns(4)
for i, curso in enumerate(cursos):
    with cols[i % 4]:
        seleccionado = any(
            c["codigo"] == curso["codigo"] and c["seccion"] == curso["seccion"]
            for c in st.session_state.seleccionados
        )
        style = "border: 2px solid red; border-radius: 10px; padding: 10px; margin: 5px;" if seleccionado else "border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 5px;"
        if st.button(f"{curso['nombre']} Sección {curso['seccion']}", key=f"boton_{i}"):
            if not seleccionado:
                st.session_state.seleccionados.append(curso)
                st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")
        st.markdown(f"<div style='{style}'>{curso['nombre']}<br><small>Sección {curso['seccion']}</small></div>", unsafe_allow_html=True)

# Tabla de horario
st.markdown("### 🗓️ Mi horario actual")
import pandas as pd

tabla = pd.DataFrame("", index=bloques, columns=dias)
for curso in st.session_state.seleccionados:
    for bloque in curso["catedra"]:
        dia, horas = bloque.split()
        if dia in dias and horas in bloques:
            tabla.at[horas, dia] = curso["nombre"]
    for bloque in curso["ayudantia"]:
        dia, horas = bloque.split()
        if dia in dias and horas in bloques:
            tabla.at[horas, dia] = f"Ayudantía {curso['nombre']}"

st.dataframe(tabla, use_container_width=True)

# Listado de cursos seleccionados
st.markdown("### 📋 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}  
*Paquete {curso['paquete']}*")
