import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🗓️ Generador de Horario Interactivo - Semestre VII")

# Datos de cursos (última versión funcional)
cursos = [
    {
        "codigo": "ICO09411",
        "nombre": "Fundamentos Económicos de la Organización",
        "creditos": 6,
        "seccion": "1",
        "catedra": "MA JU 16:00 - 17:20",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "ICO09411_V01"
    },
    {
        "codigo": "ICO09411",
        "nombre": "Fundamentos Económicos de la Organización",
        "creditos": 6,
        "seccion": "2",
        "catedra": "MA JU 17:25 - 18:45",
        "ayudantia": "VI 16:00 - 17:20",
        "profesor": "MUÑOZ JUAN ANDRÉS",
        "paquete": "ICO09411_V02"
    },
    {
        "codigo": "ICO09412",
        "nombre": "FINANZAS II",
        "creditos": 6,
        "seccion": "1",
        "catedra": "MA JU 11:30 - 12:50",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "YAÑEZ GUILLERMO JOSE",
        "paquete": "ICO09412_V01"
    },
    {
        "codigo": "ICO09412",
        "nombre": "FINANZAS II",
        "creditos": 6,
        "seccion": "2",
        "catedra": "MA JU 10:00 - 11:20",
        "ayudantia": "VI 08:30 - 09:50",
        "profesor": "RANTUL FRANCISCO OSIEL",
        "paquete": "ICO09412_V02"
    },
    {
        "codigo": "ICO09413",
        "nombre": "RECURSOS HUMANOS",
        "creditos": 6,
        "seccion": "1",
        "catedra": "LU MI 13:00 - 14:20",
        "ayudantia": "VI 13:00 - 14:20",
        "profesor": "TOLEDO MIGUEL APOLONIO",
        "paquete": "ICO09413_V01"
    },
    {
        "codigo": "ICO09414",
        "nombre": "TALLER EMPRENDIMIENTO",
        "creditos": 6,
        "seccion": "1",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "",
        "profesor": "FERNANDEZ ANDRES JOSE",
        "paquete": "ICO09414_V01"
    },
    {
        "codigo": "ICO09414",
        "nombre": "TALLER EMPRENDIMIENTO",
        "creditos": 6,
        "seccion": "2",
        "catedra": "MA 13:00 - 15:50",
        "ayudantia": "",
        "profesor": "MUENA PAULINA",
        "paquete": "ICO09414_V02"
    },
]

with open("/mnt/data/app_funcional.py", "w", encoding="utf-8") as f:
    f.write(app_code)
