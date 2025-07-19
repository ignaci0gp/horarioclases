
import streamlit as st

# Datos simulados de ejemplo
st.title("Horario de Clases")

# Simulación de cursos seleccionados
cursos = [
    {"nombre": "Finanzas II", "catedra": ["MA 11:30 - 12:50", "JU 11:30 - 12:50"]},
    {"nombre": "Recursos Humanos", "catedra": ["LU 13:00 - 14:20", "MI 13:00 - 14:20"]}
]

DIAS = ["LU", "MA", "MI", "JU", "VI"]
BLOQUES = {
    "08:30 - 09:50": 0,
    "10:00 - 11:20": 1,
    "11:30 - 12:50": 2,
    "13:00 - 14:20": 3,
    "14:30 - 15:50": 4,
    "16:00 - 17:20": 5,
    "17:25 - 18:45": 6
}

# Crear tabla vacía
horario = [["" for _ in DIAS] for _ in BLOQUES]

for curso in cursos:
    for b in curso["catedra"]:
        partes = b.split()
        if len(partes) != 4:
            st.error(f"Formato inválido en bloque: {b}")
            continue
        dia, hora_ini, _, hora_fin = partes
        bloque = f"{hora_ini} - {hora_fin}"
        if bloque in BLOQUES:
            fila = BLOQUES[bloque]
            col = DIAS.index(dia)
            horario[fila][col] = curso["nombre"]

# Mostrar horario
st.dataframe(horario)
