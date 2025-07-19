
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📅 Planificador de Horarios Universitarios")

# Define días y bloques
dias = ["LU", "MA", "MI", "JU", "VI"]
bloques = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"
]

DIA_BLOQUES = {
    "08:30 - 09:50": 0,
    "10:00 - 11:20": 1,
    "11:30 - 12:50": 2,
    "13:00 - 14:20": 3,
    "14:30 - 15:50": 4,
    "16:00 - 17:20": 5,
    "17:25 - 18:45": 6,
}

DIAS_IDX = {dia: i for i, dia in enumerate(dias)}

# Utilidad para dividir bloques largos
def dividir_bloque_largo(inicio, fin):
    bloques = list(DIA_BLOQUES.keys())
    try:
        i = bloques.index(inicio)
        j = bloques.index(fin)
        return bloques[i : j + 1]
    except:
        return [f"{inicio} - {fin}"]

# Extrae bloques como pares (día, índice)
def extraer_bloques(texto):
    partes = texto.split()
    dias = [p for p in partes if p in dias]
    horas = " ".join([p for p in partes if p not in dias])
    hora_ini, _, hora_fin = horas.partition("-")
    hora_ini, hora_fin = hora_ini.strip(), hora_fin.strip()
    tramos = dividir_bloque_largo(hora_ini, hora_fin)
    return [[dia, DIA_BLOQUES[bloque]] for dia in dias for bloque in tramos]

# Cursos cargados manualmente
cursos_disponibles = [
    {
        "codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "1",
        "catedra": "MA JU 11:30 - 12:50", "ayudantia": "VI 08:30 - 09:50",
        "profesor": "Yañez", "paquete": "ICO09412_V01"
    },
    {
        "codigo": "ICO09411", "nombre": "Fund. Económicos", "seccion": "2",
        "catedra": "MA JU 17:25 - 18:45", "ayudantia": "VI 16:00 - 17:20",
        "profesor": "Muñoz", "paquete": "ICO09411_V02"
    },
    {
        "codigo": "ICO09413", "nombre": "Recursos Humanos", "seccion": "1",
        "catedra": "LU MI 13:00 - 14:20", "ayudantia": "VI 13:00 - 14:20",
        "profesor": "Toledo", "paquete": "ICO09413_V01"
    },
]

# Inicializa session
if "seleccionados" not in st.session_state:
    st.session_state["seleccionados"] = []

# Layout dividido
col1, col2 = st.columns([1, 3])

# Tarjetas de cursos
with col1:
    st.markdown("### Cursos Disponibles")
    for i, curso in enumerate(cursos_disponibles):
        nombre_curso = f"{curso['nombre']} - Sección {curso['seccion']}"
        if st.button(nombre_curso):
            st.session_state.seleccionados.append(curso)

# Horario actual
grid = [["" for _ in dias] for _ in bloques]
for curso in st.session_state.seleccionados:
    for bloque in extraer_bloques(curso["catedra"]) + extraer_bloques(curso["ayudantia"]):
        dia, idx = bloque
        if 0 <= idx < len(bloques):
            grid[idx][DIAS_IDX[dia]] = f"{curso['nombre']}"

df = pd.DataFrame(grid, index=bloques, columns=dias)

with col2:
    st.markdown("### Horario")
    st.dataframe(df, use_container_width=True)

# Lista de cursos seleccionados
st.markdown("### Cursos Seleccionados")
for i, curso in enumerate(st.session_state["seleccionados"], 1):
    st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}")
