# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:13:37 2025

@author: alvaradocde
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:13:37 2025
@author: alvaradocde
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Fijar semilla para reproducibilidad
np.random.seed(0)
random.seed(0)

# Opciones para los campos
niveles = ["Licenciatura", "Maestría", "Doctorado"]
generos = ["Masculino", "Femenino", "Otro"]
idiomas_posibles = ["Inglés", "Francés", "Alemán", "Español"]

# Número de candidatos
n = 200

# Generar datos básicos
data = {
    "Nombre": [f"Candidato {i}" for i in range(1, n + 1)],
    "Edad": np.random.randint(25, 60, n),
    "Género": np.random.choice(generos, n),
    "Estudios": np.random.choice(niveles, n),
    "Salario": np.random.randint(12000, 35000, n),
    "Idiomas": [", ".join(np.random.choice(idiomas_posibles, size=np.random.randint(1, 4), replace=False)) for _ in range(n)],
    "Experiencia": np.random.choice(["Sí", "No"], n),
    "Entrevista": [
        (datetime.today() + timedelta(days=np.random.randint(1, 30))).strftime("%Y-%m-%d") +
        " " +
        f"{np.random.randint(9, 18):02d}:{np.random.choice([0, 15, 30, 45]):02d}"
        for _ in range(n)
    ],
    "CV_subido": np.random.choice(["Sí", "No"], n)
}

# Crear y guardar DataFrame
df = pd.DataFrame(data)
df.to_csv("candidatos.csv", index=False)

# Mostrar ejemplo
print(df.head())
