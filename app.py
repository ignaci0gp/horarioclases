
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("## 🧪 Cursos disponibles:")

# Datos de cursos (simulados)
cursos = [
    {
        "codigo": "ICO09412",
        "nombre": "Finanzas II",
        "seccion": "1",
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "paquete": "Finanzas II",
        "catedra": ["MA 11:30 - 12:50", "JU 11:30 - 12:50"],
        "ayudantia": ["VI 08:30 - 09:50"]
    },
    {
        "codigo": "ICO09413",
        "nombre": "Finanzas II",
        "seccion": "2",
        "profesor": "RANTUL FRANCISCO OSIEL",
        "paquete": "Finanzas II",
        "catedra": ["LU 13:00 - 14:20"],
        "ayudantia": ["MI 10:00 - 11:20"]
    },
    {
        "codigo": "RRHH123",
        "nombre": "Recursos Humanos",
        "seccion": "1",
        "profesor": "FERNANDEZ PAULINA",
        "paquete": "Recursos Humanos",
        "catedra": ["MA 10:00 - 11:20"],
        "ayudantia": ["VI 13:00 - 14:20"]
    }
]

# Sesión de estado
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []
if "horario" not in st.session_state:
    st.session_state.horario = {}

dias = ["LU", "MA", "MI", "JU", "VI"]
bloques = ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"]

def extraer_bloques(lista_horas):
    bloques_resultado = []
    for h in lista_horas:
        partes = h.split()
        if len(partes) == 3:
            dias_str, desde, _, hasta = partes[0], partes[1], '-', partes[2]
            for dia in dias_str.split():
                bloques_resultado.append((dia, f"{desde} - {hasta}"))
        else:
            dia, horas = partes
            bloques_resultado.append((dia, horas))
    return bloques_resultado

col1, col2 = st.columns([1, 3])

with col1:
    for curso in cursos:
        tarjeta = f"**{curso['nombre']}** Sección {curso['seccion']}"
        if st.button(tarjeta, key=curso['codigo']):
            if curso not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(curso)
                for dia, bloque in extraer_bloques(curso["catedra"] + curso["ayudantia"]):
                    st.session_state.horario[(dia, bloque)] = curso["nombre"]
                st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

with col2:
    st.markdown("## 📅 Mi horario actual")
    df_horario = pd.DataFrame("", index=dias, columns=bloques)
    for (dia, bloque), materia in st.session_state.horario.items():
        if dia in dias and bloque in bloques:
            df_horario.loc[dia, bloque] = materia
    st.dataframe(df_horario)

st.markdown("## 📝 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"**{i}. {curso['nombre']} — (Sec. {curso['seccion']}) — {curso['profesor']} — Paquete: {curso['paquete']}**")
