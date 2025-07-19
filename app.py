
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

cursos_data = [
    {
        "nombre": "Finanzas II",
        "seccion": 1,
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "paquete": "A",
        "catedra": ["LU 10:00-11:20", "LU 17:25-18:45", "JU 14:30-15:50", "VI 10:00-11:20"],
        "ayudantia": ["MA 11:30-12:50", "MI 11:30-12:50"]
    },
    {
        "nombre": "Finanzas II",
        "seccion": 2,
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "paquete": "B",
        "catedra": ["JU 14:30-15:50", "LU 17:25-18:45", "LU 10:00-11:20", "VI 10:00-11:20"],
        "ayudantia": ["MA 11:30-12:50", "MI 11:30-12:50"]
    },
    {
        "nombre": "Recursos Humanos",
        "seccion": 1,
        "profesor": "GOMEZ MARIA",
        "paquete": "C",
        "catedra": ["LU 08:30-09:50"],
        "ayudantia": []
    },
    {
        "nombre": "Fund. Económicos de la Org.",
        "seccion": 1,
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "D",
        "catedra": ["LU 08:30-09:50", "JU 08:30-09:50"],
        "ayudantia": []
    },
    {
        "nombre": "Fund. Económicos de la Org.",
        "seccion": 2,
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "E",
        "catedra": ["LU 10:00-11:20", "JU 10:00-11:20"],
        "ayudantia": []
    },
    {
        "nombre": "Taller Emprendimiento",
        "seccion": 1,
        "profesor": "RAMIREZ CLAUDIA",
        "paquete": "F",
        "catedra": ["LU 14:30-15:50"],
        "ayudantia": []
    },
    {
        "nombre": "Taller Emprendimiento",
        "seccion": 2,
        "profesor": "RAMIREZ CLAUDIA",
        "paquete": "G",
        "catedra": ["JU 14:30-15:50"],
        "ayudantia": []
    },
]

dias = ["LU", "MA", "MI", "JU", "VI"]
bloques = ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"]

def extraer_bloques(lista_bloques):
    resultado = []
    for entrada in lista_bloques:
        partes = entrada.split()
        if len(partes) != 2:
            continue
        dia, horas = partes
        try:
            index = bloques.index(horas.replace("-", " - "))
            resultado.append((dia, bloques[index]))
        except ValueError:
            pass
    return resultado

st.markdown("## 📚 Cursos disponibles:")

col1, col2 = st.columns([1, 3])

with col1:
    for curso in cursos_data:
        tarjeta = f"**{curso['nombre']}** Sección {curso['seccion']}"
        if st.button(tarjeta, key=f"{curso['nombre']}_{curso['seccion']}"):
            if curso not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(curso)
                st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

with col2:
    st.markdown("## 🗓️ Mi horario actual")
    horario_df = pd.DataFrame("", index=bloques, columns=dias)

    for curso in st.session_state.seleccionados:
        for dia, bloque in extraer_bloques(curso["catedra"]):
            horario_df.loc[bloque, dia] = curso["nombre"]
        for dia, bloque in extraer_bloques(curso["ayudantia"]):
            horario_df.loc[bloque, dia] = f"Ayudantía {curso['nombre']}"

    st.dataframe(horario_df, use_container_width=True, height=420)

    st.markdown("### 📋 Seleccionados:")
    for i, curso in enumerate(st.session_state.seleccionados, 1):
        st.markdown(f"""**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}  
*{curso['paquete']}*""")

