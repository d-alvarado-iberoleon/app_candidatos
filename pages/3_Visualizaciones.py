# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:48:33 2025

@author: alvaradocde
"""

# -*- coding: utf-8 -*-
"""
Visualizador de salarios por nivel de estudios
Adaptado para datos en Supabase
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from supabase import create_client, Client

# Conexión a Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Visualizador de salarios por nivel de estudios")

# Obtener datos desde Supabase
res = supabase.table("candidatos").select("*").execute()

if res.data:
    df = pd.DataFrame(res.data)

    niveles = ["Licenciatura", "Maestría", "Doctorado"]
    niveles_seleccionados = st.multiselect("Selecciona los niveles de estudios:", 
                                           niveles, default=niveles)

    df_filtrado = df[df["estudios"].isin(niveles_seleccionados)]

    if df_filtrado.empty:
        st.warning("No hay registros para los niveles seleccionados.")
    else:
        st.write("📊 Opción 1: Visualización con Seaborn")

        fig, ax = plt.subplots()
        sns.set(style="darkgrid", palette="muted")
        sns.boxplot(data=df_filtrado, x='estudios', y='salario', ax=ax, hue='estudios')

        ax.set_title("Distribución de salarios por nivel de estudios")
        ax.set_ylabel("Salario (MXN)")
        ax.set_xlabel("Nivel de estudios")

        st.pyplot(fig)

        st.write("📈 Opción 2: Visualización interactiva con Plotly")

        fig2 = px.box(
            df_filtrado, 
            x="estudios", 
            y="salario", 
            color="estudios",
            title="Distribución de salarios por nivel de estudios",
            points='all',
            labels={"salario": "Salario ($)"},
            category_orders={'estudios': niveles}
        )

        fig2.update_traces(hoveron='points', selector=dict(type='box'))
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Aún no hay candidatos registrados.")
