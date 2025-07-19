
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

DIAS = ["LU", "MA", "MI", "JU", "VI"]
BLOQUES = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20",
    "17:25 - 18:45", "18:50 - 20:10", "20:15 - 21:35"
]

def dividir_bloque_largo(inicio, fin):
    bloques = []
    try:
        fmt = "%H:%M"
        inicio_dt = datetime.strptime(inicio, fmt)
        fin_dt = datetime.strptime(fin, fmt)
        duracion = timedelta(hours=1, minutes=20)
        while inicio_dt + duracion <= fin_dt:
            bloque_fin = inicio_dt + duracion
            bloque_str = f"{inicio_dt.strftime(fmt)} - {bloque_fin.strftime(fmt)}"
            bloques.append(bloque_str)
            inicio_dt = bloque_fin + timedelta(minutes=10)
    except Exception as e:
        st.error(f"Error procesando bloque largo: {e}")
    return bloques if bloques else [f"{inicio} - {fin}"]

def extraer_bloques(texto):
    bloques = []
    partes = texto.split()
    dias = [p for p in partes if p in DIAS]
    try:
        hora_inicio = partes[-3]
        hora_fin = partes[-1]
        rangos = dividir_bloque_largo(hora_inicio, hora_fin)
        for dia in dias:
            for r in rangos:
                bloques.append(f"{dia} {r}")
    except:
        pass
    return bloques

# Datos de ejemplo
curso_test = {
    "nombre": "Fundamentos Económicos",
    "seccion": "1",
    "profesor": "Juan Muñoz",
    "paquete": "ICO09411_V01",
    "catedra": "MA JU 10:00 - 11:20",
    "ayudantia": "VI 16:00 - 17:20"
}

# Verificación visual
st.title("🔎 Verificación de bloques correctos")

st.subheader("Bloques Cátedra:")
bloques = extraer_bloques(curso_test["catedra"])
st.write(bloques)

st.subheader("Bloques Ayudantía:")
bloques_ay = extraer_bloques(curso_test["ayudantia"])
st.write(bloques_ay)
