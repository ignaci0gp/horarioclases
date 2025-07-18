
import streamlit as st

# Datos de los cursos
cursos = [
    {
        "nombre": "Fundamentos Económicos de la Organización",
        "codigo": "ICO09411",
        "seccion": "1",
        "catedra": ["MA 16:00 - 17:20", "JU 16:00 - 17:20"],
        "ayudantia": ["VI 16:00 - 17:20"],
        "profesor": "MUÑOZ JUAN ANDRÉS"
    },
    {
        "nombre": "Fundamentos Económicos de la Organización",
        "codigo": "ICO09411",
        "seccion": "2",
        "catedra": ["MA 17:25 - 18:45", "JU 17:25 - 18:45"],
        "ayudantia": ["VI 16:00 - 17:20"],
        "profesor": "MUÑOZ JUAN ANDRÉS"
    },
    {
        "nombre": "Finanzas II",
        "codigo": "ICO09412",
        "seccion": "1",
        "catedra": ["MA 11:30 - 12:50", "JU 11:30 - 12:50"],
        "ayudantia": ["VI 08:30 - 09:50"],
        "profesor": "YAÑEZ GUILLERMO JOSE"
    },
    {
        "nombre": "Finanzas II",
        "codigo": "ICO09412",
        "seccion": "2",
        "catedra": ["MA 10:00 - 11:20", "JU 10:00 - 11:20"],
        "ayudantia": ["VI 08:30 - 09:50"],
        "profesor": "RANTUL FRANCISCO OSIEL"
    },
    {
        "nombre": "Recursos Humanos",
        "codigo": "ICO09413",
        "seccion": "1",
        "catedra": ["LU 13:00 - 14:20", "MI 13:00 - 14:20"],
        "ayudantia": ["VI 13:00 - 14:20"],
        "profesor": "TOLEDO MIGUEL APOLONIO"
    },
    {
        "nombre": "Taller Emprendimiento",
        "codigo": "ICO09414",
        "seccion": "1",
        "catedra": ["MA 13:00 - 15:50"],
        "ayudantia": [],
        "profesor": "FERNANDEZ ANDRES JOSE"
    },
    {
        "nombre": "Taller Emprendimiento",
        "codigo": "ICO09414",
        "seccion": "2",
        "catedra": ["MA 13:00 - 15:50"],
        "ayudantia": [],
        "profesor": "MUENA PAULINA"
    }
]

st.title("🗓️ Horario Interactivo - Segundo Semestre 2025")
st.write("Selecciona un curso para ver los horarios y detalles. Aún no se valida topes en esta versión inicial.")

# Mostrar cursos disponibles
opciones = [f"{c['nombre']} - Sección {c['seccion']}" for c in cursos]
seleccion = st.selectbox("📚 Elige un curso:", opciones)

# Mostrar información del curso seleccionado
for c in cursos:
    if seleccion == f"{c['nombre']} - Sección {c['seccion']}":
        st.subheader(f"{c['nombre']} (Sección {c['seccion']})")
        st.write(f"**Código:** {c['codigo']}")
        st.write(f"**Profesor:** {c['profesor']}")
        st.write(f"**Cátedra:** {' | '.join(c['catedra'])}")
        st.write(f"**Ayudantía:** {' | '.join(c['ayudantia']) if c['ayudantia'] else 'No tiene'}")
        break
