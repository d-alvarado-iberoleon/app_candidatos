# -*- coding: utf-8 -*-

from supabase import create_client, Client
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import unicodedata
import re

def sanear_nombre(nombre):
    # Normalizar a NFD (descomponer acentos)
    nombre = unicodedata.normalize('NFD', nombre)
    # Remover caracteres no ASCII
    nombre = nombre.encode('ascii', 'ignore').decode('utf-8')
    # Reemplazar espacios y caracteres no alfanuméricos por guiones 
    nombre = re.sub(r'[^a-zA-Z0-9]', '-', nombre)
    # Convertir a minúsculas
    return nombre.lower()

# Conexión a Supabase

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


# para crear la tabla:
# create table candidatos (
#   id bigint primary key generated always as identity,
#   nombre text not null,
#   edad integer not null,
#   salario numeric,
#   genero text,
#   estudios text,
#   idiomas text,
#   experiencia text,
#   entrevista text,
#   cv_subido boolean default false,
#   cv_url text,
#   fecha_registro timestamp with time zone default now()
# );


st.title("Registro de candidatos")

st.write("Por favor, rellene los siguientes campos:")

with st.form("formulario_candidato"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre completo")
        edad = st.slider("Edad", min_value=18, max_value=99, value=30)
        genero = st.radio("Género", ["Masculino", "Femenino", "Otro"])

    with col2:
        nivel_estudios = st.selectbox("Último nivel de estudios", ["Licenciatura", "Maestría", "Doctorado"])
        idiomas = st.multiselect("Idiomas que domina", ["Inglés", "Francés", "Alemán", "Español"])
        salario = st.number_input("Salario mensual actual (MXN)", min_value=0.0, step=500.0)
        experiencia = st.checkbox("¿Tiene experiencia previa en el área?")

    with st.expander("Sugerir fecha y hora de entrevista"):
        fecha_entrevista = st.date_input("Fecha de entrevista")
        hora_entrevista = st.time_input("Hora de entrevista")

    cv = st.file_uploader("Subir CV (PDF)", type=["pdf"])
    enviar = st.form_submit_button("Registrar candidato")

if enviar:
    if nombre:
        # Preparar datos
        idiomas_str = ", ".join(idiomas)
        entrevista_str = f"{fecha_entrevista} {hora_entrevista}"

        # Cargar CV si está presente
        url_cv = None
        if cv is not None:
            nombre_saneado = sanear_nombre(nombre)
            nombre_archivo = f"{nombre_saneado}_{int(time.time())}.pdf"
            #nombre_archivo = f"{nombre.lower().replace(' ', '-')}_{int(time.time())}.pdf"
            
            ruta = f"{nombre_archivo}"
            
            contenido = cv.read()  # Leer contenido en bytes
            try:
                #res_upload = supabase.storage.from_("cv-candidatos").upload(ruta, contenido)
                
                #url_cv = supabase.storage.from_("cv-candidatos").get_public_url(ruta)
                bucket = supabase.storage.from_("cv-candidatos")
                bucket.upload(nombre_archivo, contenido, {"content-type": "application/pdf"})
                url_cv = bucket.get_public_url(nombre_archivo)
                st.success("CV subido exitosamente.")
            except Exception as e:
                st.warning(f"No se pudo subir el CV. {e}")

        # Guardar en la base
        datos = {
            "nombre": nombre,
            "edad": edad,
            "salario": salario,
            "genero": genero,
            "estudios": nivel_estudios,
            "idiomas": idiomas_str,
            "experiencia": "Sí" if experiencia else "No",
            "entrevista": entrevista_str,
            "cv_subido": True if url_cv else False,
        }

        if url_cv:
            datos["cv_url"] = url_cv

        supabase.table("candidatos").insert(datos).execute()
        st.success("Candidato registrado exitosamente.")
    else:
        st.warning("El nombre es obligatorio.")
