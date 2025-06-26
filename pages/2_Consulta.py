import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Conexión a Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Consulta de candidatos registrados")

# Consultar datos desde Supabase
respuesta = supabase.table("candidatos").select("*").order("fecha_registro", desc=True).execute()

if respuesta.data:
    df = pd.DataFrame(respuesta.data)

    # Convertir fechas si existen
    if "fecha_registro" in df.columns:
        df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])

    # Mostrar tabla
    st.dataframe(df)

    # Botón para descarga
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv, file_name="candidatos.csv", mime="text/csv")
else:
    st.info("Aún no hay candidatos registrados.")
