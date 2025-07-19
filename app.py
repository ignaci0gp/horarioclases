
import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .tarjetas {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 250px;
            padding-right: 20px;
        }
        .contenedor {
            display: flex;
            gap: 40px;
        }
        .tarjeta {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background-color: white;
            cursor: pointer;
        }
        .tarjeta.agregado {
            border: 1px solid #2ecc71;
            background-color: #eafaf1;
        }
        .tarjeta.error {
            border: 1px solid #e74c3c;
            background-color: #fdecea;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 Cursos disponibles y 🗓️ Mi horario actual")

cursos = [
    {"nombre": "Fund. Económicos de la Org.", "seccion": "1", "bloques": [["LU", 2], ["JU", 2]], "ayudantia": [["VI", 4]], "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "ICO09411_V01"},
    {"nombre": "Fund. Económicos de la Org.", "seccion": "2", "bloques": [["LU", 2], ["JU", 2]], "ayudantia": [["VI", 4]], "profesor": "MUÑOZ JUAN ANDRÉS", "paquete": "ICO09411_V02"},
    {"nombre": "Finanzas II", "seccion": "1", "bloques": [["MA", 2], ["JU", 2]], "ayudantia": [["VI", 1]], "profesor": "YAÑEZ GUILLERMO JOSE", "paquete": "ICO09412_V01"},
    {"nombre": "Finanzas II", "seccion": "2", "bloques": [["MA", 2], ["JU", 2]], "ayudantia": [["VI", 1]], "profesor": "RANTUL FRANCISCO OSIEL", "paquete": "ICO09412_V02"},
    {"nombre": "Recursos Humanos", "seccion": "1", "bloques": [["LU", 3], ["MI", 3]], "ayudantia": [["VI", 3]], "profesor": "TOLEDO MIGUEL APOLONIO", "paquete": "ICO09413_V01"},
    {"nombre": "Taller Emprendimiento", "seccion": "1", "bloques": [["MA", 3], ["MA", 4]], "ayudantia": [], "profesor": "FERNANDEZ ANDRES JOSE", "paquete": "ICO09414_V01"},
    {"nombre": "Taller Emprendimiento", "seccion": "2", "bloques": [["MA", 3], ["MA", 4]], "ayudantia": [], "profesor": "MUENA PAULINA", "paquete": "ICO09414_V02"},
]

dias = ["LU", "MA", "MI", "JU", "VI"]
bloques_horarios = ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"]

horario = {dia: [""] * len(bloques_horarios) for dia in dias}
seleccionados = []

with st.container():
    st.markdown('<div class="contenedor">', unsafe_allow_html=True)
    st.markdown('<div class="tarjetas">', unsafe_allow_html=True)

    for i, curso in enumerate(cursos, start=1):
        clave = f"{curso['nombre']} Sección {curso['seccion']}"
        clase_css = "tarjeta"
        if clave in seleccionados:
            clase_css += " agregado"
        elif any(
            horario[dia][bloque - 1] != ""
            for dia, bloque in curso["bloques"] + curso["ayudantia"]
        ):
            clase_css += " error"

        if st.button(clave, key=clave):
            if clave not in seleccionados:
                if not any(horario[dia][bloque - 1] != "" for dia, bloque in curso["bloques"] + curso["ayudantia"]):
                    for dia, bloque in curso["bloques"]:
                        horario[dia][bloque - 1] = curso["nombre"]
                    for dia, bloque in curso["ayudantia"]:
                        horario[dia][bloque - 1] = f"Ayudantía {curso['nombre']}"
                    seleccionados.append(clave)
                    st.success(f"{clave} agregado al horario.")
                else:
                    st.error(f"{clave} tiene tope con otro curso.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Mostrar el horario
    st.markdown("### 📅 Mi horario actual")
    data = []
    for i, rango in enumerate(bloques_horarios):
        fila = [rango]
        for dia in dias:
            fila.append(horario[dia][i])
        data.append(fila)

    st.dataframe(data, columns=[""] + dias, hide_index=True, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
