
import streamlit as st
import pandas as pd
from datetime import datetime

# Simulación de la estructura del DataFrame 'data' y variable 'dias'
dias = ["LU", "MA", "MI", "JU", "VI"]
data = pd.DataFrame({
    "": ["08:30 - 09:50", "10:00 - 11:20", "11:30 - 12:50", "13:00 - 14:20", "14:30 - 15:50", "16:00 - 17:20", "17:25 - 18:45"],
    "LU": ["", "", "", "", "", "", ""],
    "MA": ["", "", "", "", "", "", ""],
    "MI": ["", "", "", "", "", "", ""],
    "JU": ["", "", "", "", "", "", ""],
    "VI": ["", "", "", "", "", "", ""],
})

st.title("📅 Mi horario actual")
st.dataframe(data, hide_index=True, use_container_width=True)
