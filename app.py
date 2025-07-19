
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Datos de ejemplo (reemplazar con tus datos reales)
cursos = [
    {"codigo": "FIN200", "nombre": "Finanzas II", "seccion": "1", "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "Paquete A", "catedra": ["LU 17:25 - 18:45", "JU 17:25 - 18:45"], "ayudantia": ["MA 11:30 - 12:50"]},
    {"codigo": "FIN200", "nombre": "Finanzas II", "seccion": "2", "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "Paquete B", "catedra": ["LU 10:00 - 11:20", "VI 10:00 - 11:20"], "ayudantia": ["MI 11:30 - 12:50"]},
    {"codigo": "RRHH100", "nombre": "Recursos Humanos", "seccion": "1", "profesor": "GOMEZ MARIA", "paquete": "Paquete C", "catedra": ["LU 08:30 - 09:50"], "ayudantia": []}
]

dias_semana = ["LU", "MA", "MI", "JU", "VI"]
bloques = ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"]

def extraer_bloques(lista):
    resultado = []
    for entrada in lista:
        partes = entrada.split()
        if len(partes) >= 3:
            dia = partes[0]
            tramo = " ".join(partes[1:])
            resultado.append((dia, tramo))
    return resultado

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

st.markdown("## 🧮 Cursos disponibles:")
cols = st.columns(3)
for i, curso in enumerate(cursos):
    with cols[i % 3]:
        tarjeta = f"**{curso['nombre']}** Sección {curso['seccion']}"
        if st.button(tarjeta, key=f"{curso['codigo']}-{curso['seccion']}"):
            if curso not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(curso)
                st.success(f"{curso['nombre']} - Sección {curso['seccion']} agregado al horario.")

st.markdown("## 🗓️ Mi horario actual")
horario_df = pd.DataFrame("", index=bloques, columns=dias_semana)

for curso in st.session_state.seleccionados:
    bloques_catedra = extraer_bloques(curso["catedra"])
    bloques_ayudantia = extraer_bloques(curso["ayudantia"])

    for dia, tramo in bloques_catedra:
        if dia in dias_semana and tramo in horario_df.index:
            horario_df.loc[tramo, dia] = curso["nombre"]

    for dia, tramo in bloques_ayudantia:
        if dia in dias_semana and tramo in horario_df.index:
            horario_df.loc[tramo, dia] = f"Ayudantía {curso['nombre']}"

st.dataframe(horario_df, use_container_width=True, height=360)

st.markdown("### 📋 Seleccionados:")
for i, curso in enumerate(st.session_state.seleccionados, 1):
    st.markdown(f"""**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}
*{curso['paquete']}*""")

