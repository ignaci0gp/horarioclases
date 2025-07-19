
import streamlit as st
from datetime import datetime, timedelta

# Diccionario de bloques estándar
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

# Días válidos
DIAS = ["LU", "MA", "MI", "JU", "VI", "SA"]

# Función para dividir bloques largos
def dividir_bloque_largo(inicio, fin):
    bloques = []
    fmt = "%H:%M"
    try:
        inicio_dt = datetime.strptime(inicio, fmt)
        fin_dt = datetime.strptime(fin, fmt)
    except ValueError:
        return []
    actual = inicio_dt
    while actual < fin_dt:
        siguiente = actual + timedelta(minutes=80)
        if siguiente > fin_dt:
            break
        bloque = f"{actual.strftime(fmt)} - {siguiente.strftime(fmt)}"
        bloques.append(bloque)
        actual = siguiente + timedelta(minutes=10)
    return bloques

# Función para extraer bloques desde string de horario
def extraer_bloques(horario_str):
    bloques = []
    partes = horario_str.strip().split()
    if len(partes) >= 3:
        dias = [p for p in partes if p in DIAS]
        tramo = " ".join([p for p in partes if ":" in p or "-" in p])
        try:
            hora_inicio, hora_fin = [x.strip() for x in tramo.split("-")]
            rangos = dividir_bloque_largo(hora_inicio, hora_fin)
            for dia in dias:
                for r in rangos:
                    if r in DIA_BLOQUES:
                        bloques.append((dia, DIA_BLOQUES[r]))
        except ValueError:
            pass
    return bloques

# App de prueba
st.title("🔎 Verificación de bloques correctos")
curso_test = {
    "nombre": "Taller Emprendimiento",
    "catedra": "MA 13:00 - 15:50"
}
st.write("Entrada original:", curso_test["catedra"])
bloques = extraer_bloques(curso_test["catedra"])
st.write("Bloques extraídos:", bloques)
