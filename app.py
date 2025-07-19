
import streamlit as st
import pandas as pd

# ---------------------- Datos base ----------------------
bloques = [
    "08:30 - 09:50",
    "10:00 - 11:20",
    "11:30 - 12:50",
    "13:00 - 14:20",
    "14:30 - 15:50",
    "16:00 - 17:20",
    "17:25 - 18:45"
]
dias = ["LU", "MA", "MI", "JU", "VI"]

# Base de cursos
cursos = [
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "1",
     "catedra": ["MA 16:00 - 17:20", "JU 16:00 - 17:20"],
     "ayudantia": ["VI 16:00 - 17:20"], "profesor": "MUÑOZ JUAN ANDRÉS"},
    {"codigo": "ICO09411", "nombre": "Fund. Económicos de la Org.", "seccion": "2",
     "catedra": ["MA 17:25 - 18:45", "JU 17:25 - 18:45"],
     "ayudantia": ["VI 16:00 - 17:20"], "profesor": "MUÑOZ JUAN ANDRÉS"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "1",
     "catedra": ["MA 11:30 - 12:50", "JU 11:30 - 12:50"],
     "ayudantia": ["VI 08:30 - 09:50"], "profesor": "YAÑEZ GUILLERMO JOSE"},
    {"codigo": "ICO09412", "nombre": "Finanzas II", "seccion": "2",
     "catedra": ["MA 10:00 - 11:20", "JU 10:00 - 11:20"],
     "ayudantia": ["VI 08:30 - 09:50"], "profesor": "RANTUL FRANCISCO OSIEL"},
    {"codigo": "ICO09413", "nombre": "Recursos Humanos", "seccion": "1",
     "catedra": ["LU 13:00 - 14:20", "MI 13:00 - 14:20"],
     "ayudantia": ["VI 13:00 - 14:20"], "profesor": "TOLEDO MIGUEL APOLONIO"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "1",
     "catedra": ["MA 13:00 - 15:50"], "ayudantia": [], "profesor": "FERNANDEZ ANDRES JOSE"},
    {"codigo": "ICO09414", "nombre": "Taller Emprendimiento", "seccion": "2",
     "catedra": ["MA 13:00 - 15:50"], "ayudantia": [], "profesor": "MUENA PAULINA"}
]

# ---------------------- Funciones ----------------------
def crear_horario_vacio():
    return {dia: {bloque: "" for bloque in bloques} for dia in dias}

def extraer_bloques(horas):
    resultado = []
    for h in horas:
        dia, tramo = h.split()
        if tramo in bloques:
            resultado.append((dia, tramo))
    return resultado

def hay_tope(horario, bloques_nuevos):
    for dia, bloque in bloques_nuevos:
        if horario[dia][bloque] != "":
            return True
    return False

def agregar_curso(horario, curso):
    bloques_catedra = extraer_bloques(curso["catedra"])
    bloques_ayud = extraer_bloques(curso["ayudantia"])
    for dia, bloque in bloques_catedra + bloques_ayud:
        horario[dia][bloque] = f"{curso['nombre']} ({curso['seccion']})"
    return horario

# ---------------------- App ----------------------
st.title("📚 Horario Interactivo - Segundo Semestre 2025")

if "horario" not in st.session_state:
    st.session_state.horario = crear_horario_vacio()
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

opciones = [f"{c['nombre']} - Sección {c['seccion']}" for c in cursos]
curso_str = st.selectbox("Selecciona un curso:", opciones)
curso = next(c for c in cursos if f"{c['nombre']} - Sección {c['seccion']}" == curso_str)

st.markdown(f"""
**Código:** {curso['codigo']}  
**Profesor:** {curso['profesor']}  
**Cátedra:** {' | '.join(curso['catedra'])}  
**Ayudantía:** {' | '.join(curso['ayudantia']) if curso['ayudantia'] else 'No tiene'}
""")

if st.button("➕ Agregar curso al horario"):
    bloques_nuevos = extraer_bloques(curso["catedra"] + curso["ayudantia"])
    if hay_tope(st.session_state.horario, bloques_nuevos):
        st.error("⛔ Este curso tiene tope de horario con otro ya agregado.")
    elif curso_str in st.session_state.seleccionados:
        st.warning("⚠️ Este curso ya fue agregado.")
    else:
        st.session_state.horario = agregar_curso(st.session_state.horario, curso)
        st.session_state.seleccionados.append(curso_str)
        st.success("✅ Curso agregado al horario.")

st.subheader("📅 Mi horario actual")
df = pd.DataFrame(st.session_state.horario).T[bloques]
st.dataframe(df.style.set_properties(**{"text-align": "center"}), height=360)

if st.session_state.seleccionados:
    quitar = st.selectbox("❌ Quitar curso:", st.session_state.seleccionados)
    if st.button("Eliminar curso del horario"):
        curso_quitar = next(c for c in cursos if f"{c['nombre']} - Sección {c['seccion']}" == quitar)
        for dia, bloque in extraer_bloques(curso_quitar["catedra"] + curso_quitar["ayudantia"]):
            st.session_state.horario[dia][bloque] = ""
        st.session_state.seleccionados.remove(quitar)
        st.success("Curso eliminado del horario.")


