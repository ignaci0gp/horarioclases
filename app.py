
import streamlit as st

# Diccionario de bloques
DIA_BLOQUES = {
    "08:30 - 09:50": 0,
    "10:00 - 11:20": 1,
    "11:30 - 12:50": 2,
    "13:00 - 14:20": 3,
    "14:30 - 15:50": 4,
    "16:00 - 17:20": 5,
    "17:25 - 18:45": 6,
    "18:50 - 20:10": 7
}

# Días de la semana
DIAS = ["LU", "MA", "MI", "JU", "VI", "SA"]

# Función para dividir bloques largos
from datetime import datetime, timedelta
def dividir_bloque_largo(inicio, fin):
    bloques = []
    fmt = "%H:%M"
    inicio_dt = datetime.strptime(inicio, fmt)
    fin_dt = datetime.strptime(fin, fmt)
    actual = inicio_dt
    while actual < fin_dt:
        siguiente = actual + timedelta(minutes=80)
        if siguiente > fin_dt:
            break
        bloque = f"{actual.strftime(fmt)} - {siguiente.strftime(fmt)}"
        bloques.append(bloque)
        actual = siguiente + timedelta(minutes=10)
    return bloques

# Función corregida para extraer bloques desde el string de horario
def extraer_bloques(horario_str):
    bloques = []
    partes = horario_str.split()
    if len(partes) >= 3:
        dias = partes[:-2]
        tramo = " ".join(partes[-2:])
        hora_inicio, _, hora_fin = tramo.partition(" - ")
        rangos = dividir_bloque_largo(hora_inicio, hora_fin)
        for dia in dias:
            for r in rangos:
                if r in DIA_BLOQUES:
                    bloques.append((dia, DIA_BLOQUES[r]))
    return bloques

# Simulación de curso con horario largo
st.title("Test División de Bloques Largos")
curso_test = {
    "nombre": "Taller Emprendimiento",
    "catedra": "MA 13:00 - 15:50"
}

bloques = extraer_bloques(curso_test["catedra"])
st.write("Bloques extraídos:", bloques)
