
import streamlit as st

# Datos de ejemplo (resumido solo para la demostración de bloques)
cursos = [
    {
        "codigo": "ICO09414",
        "nombre": "TALLER EMPRENDIMIENTO",
        "seccion": "Sección 1",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "",
        "profesor": "FERNANDEZ ANDRES JOSE",
        "paquete": "ICO09414_V01"
    },
]

DIA_BLOQUES = {
    "08:30 - 09:50": 0,
    "10:00 - 11:20": 1,
    "11:30 - 12:50": 2,
    "13:00 - 14:20": 3,
    "14:30 - 15:50": 4,
    "16:00 - 17:20": 5,
    "17:25 - 18:45": 6,
    "18:50 - 20:10": 7,
    "20:15 - 21:35": 8
}
DIAS = ["LU", "MA", "MI", "JU", "VI"]

def extraer_bloques(horario_str):
    bloques = []
    partes = horario_str.strip().split()
    dias = [p for p in partes if p in DIAS]
    horas = " ".join(p for p in partes if p not in DIAS)
    if horas == "13:00 - 15:50":
        rangos = ["13:00 - 14:20", "14:30 - 15:50"]
    else:
        rangos = [horas]
    for dia in dias:
        for r in rangos:
            bloques.append((dia, r))
    return bloques

st.title("🔍 Test Horario con Bloques Largos")
curso_test = cursos[0]
st.write("Curso de prueba:", curso_test["nombre"])
bloques = extraer_bloques(curso_test["catedra"])
st.write("Bloques extraídos:", bloques)
