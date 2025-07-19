
import streamlit as st

# Datos de ejemplo (pueden ser reemplazados por tu propia lógica)
cursos = [
    {"nombre": "Finanzas II", "seccion": "1", "profesor": "Yañez", "horario": "MA JU 11:30 - 12:50"},
    {"nombre": "Fund. Económicos", "seccion": "2", "profesor": "Muñoz", "horario": "MA JU 17:25 - 18:45"},
    {"nombre": "Recursos Humanos", "seccion": "1", "profesor": "Toledo", "horario": "LU MI 13:00 - 14:20"},
]

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

st.title("📆 Planificador de Horarios Universitarios")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## Cursos Disponibles")
    for idx, curso in enumerate(cursos):
        if st.button(f"{curso['nombre']} - Sección {curso['seccion']}", key=idx):
            if curso not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(curso)

with col2:
    st.markdown("## Horario")
    st.dataframe(
        [[""] * 6 for _ in range(10)], 
        hide_index=True, 
        use_container_width=True
    )
    st.markdown("## Cursos Seleccionados")
    for i, curso in enumerate(st.session_state.seleccionados, 1):
        st.markdown(f"**{i}. {curso['nombre']} - Sección {curso['seccion']}** — {curso['profesor']}")
