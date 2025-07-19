
import streamlit as st
import pandas as pd

# ---------------------- Datos base ----------------------
bloques = [
    "08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50",
    "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"
]
dias = ["LU", "MA", "MI", "JU", "VI"]

cursos = [
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "1",
     "catedra": ["MA JU 16:00 - 17:20"], "ayudantia": ["VI 16:00 - 17:20"], "profesor": "MUÑOZ JUAN ANDRÉS"},
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "2",
     "catedra": ["MA JU 17:25 - 18:45"], "ayudantia": ["VI 16:00 - 17:20"], "profesor": "MUÑOZ JUAN ANDRÉS"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "1",
     "catedra": ["MA JU 11:30 - 12:50"], "ayudantia": ["VI 08:30 - 09:50"], "profesor": "YAÑEZ GUILLERMO JOSE"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "2",
     "catedra": ["MA JU 10:00 - 11:20"], "ayudantia": ["VI 08:30 - 09:50"], "profesor": "RANTUL FRANCISCO OSIEL"},
    {"codigo": "ICO09413", "nombre": "Recursos Humanos", "seccion": "1",
     "catedra": ["LU MI 13:00 - 14:20"], "ayudantia": ["VI 13:00 - 14:20"], "profesor": "TOLEDO MIGUEL APOLONIO"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "1",
     "catedra": ["MA 13:00 - 15:50"], "ayudantia": [], "profesor": "FERNANDEZ ANDRES JOSE"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "2",
     "catedra": ["MA 13:00 - 15:50"], "ayudantia": [], "profesor": "MUENA PAULINA"}
]

# ---------------------- Funciones ----------------------
def crear_horario_vacio():
    return {bloque: {dia: "" for dia in dias} for bloque in bloques}

def extraer_bloques(horas):
    resultado = []
    for h in horas:
        partes = h.strip().split()
        if len(partes) >= 3:
            tramo = " ".join(partes[-2:])
            dias_str = partes[:-2]
            for d in dias_str:
                if d in dias and tramo in bloques:
                    resultado.append((tramo, d))
    return resultado

def hay_tope(horario, bloques_nuevos):
    for bloque, dia in bloques_nuevos:
        if horario[bloque][dia] != "":
            return True
    return False

def agregar_curso(horario, curso):
    bloques_total = extraer_bloques(curso["catedra"] + curso["ayudantia"])
    for bloque, dia in bloques_total:
        horario[bloque][dia] = f"{curso['nombre']} ({curso['seccion']})"
    return horario

# ---------------------- App ----------------------
st.set_page_config(layout="wide")
st.title("📚 Horario Interactivo - Segundo Semestre 2025")

if "horario" not in st.session_state:
    st.session_state.horario = crear_horario_vacio()
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []
if "detalle" not in st.session_state:
    st.session_state.detalle = []

st.subheader("🧩 Selecciona tus cursos:")
cols = st.columns(3)

for i, curso in enumerate(cursos):
    col = cols[i % 3]
   tarjeta = f\"\"\"
**{curso['nombre']}**
Sección {curso['seccion']}
\"\"\"
    key = f"btn_{i}"
    if col.button(tarjeta, key=key):
        nombre = f"{curso['nombre']} - Sección {curso['seccion']}"
        if nombre in st.session_state.seleccionados:
            st.warning(f"{nombre} ya fue agregado.")
        elif hay_tope(st.session_state.horario, extraer_bloques(curso["catedra"] + curso["ayudantia"])):
            st.error(f"⛔ {nombre} tiene tope de horario.")
        else:
            st.session_state.horario = agregar_curso(st.session_state.horario, curso)
            st.session_state.seleccionados.append(nombre)
            st.session_state.detalle.append(curso)
            st.success(f"✅ {nombre} agregado al horario.")

# Mostrar horario
st.subheader("📅 Mi horario actual")
df = pd.DataFrame(st.session_state.horario).T[dias]
st.dataframe(df.style.set_properties(**{"text-align": "center"}), height=360)

# Mostrar lista de cursos seleccionados
if st.session_state.detalle:
    st.subheader("📋 Cursos seleccionados:")
    for i, curso in enumerate(st.session_state.detalle, 1):
        st.markdown(f"""
**{i}. {curso['nombre']} - Sección {curso['seccion']}**  
Profesor: {curso['profesor']}  
Cátedra: {' | '.join(curso['catedra'])}  
Ayudantía: {' | '.join(curso['ayudantia']) if curso['ayudantia'] else 'No tiene'}  
---
""")
