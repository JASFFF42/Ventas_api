from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse  #permite que la respuesta tenga formato que no sea json
from io import BytesIO
import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Optional
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

app = FastAPI()

app = FastAPI()

RUTA_CSV = Path(__file__).parent / "ventas_sinteticas.csv"
df = pd.read_csv(RUTA_CSV)
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

@app.get("/")
def saludo():
    return{"mensaje": "Hola a mi API de ventas pandas"}

columnas_cuantitativas = ["precio_unitario","cantidad","descuento","total"]

@app.get("/metrica/{columna}")
def calcular_metrica(columna):
    if columna not in columnas_cuantitativas:
        raise HTTPException(detail ="esa columa no es cuantitativa",status_code=404)
    datos = df[columna]
    media = datos.mean()
    mediana = datos.median()
    minimo = datos.min()
    maximo = datos.max()
    desvest = datos.std()
    return{
        "media":media,
        "mediana":mediana,
        "minimo":minimo,
        "maximo":maximo,
        "desvest":desvest,
        "saludos":"saludos cordiales"
    }

@app.post("/correlacion")
def calcular_correlacion(columna_x, columna_y):
    if columna_x  not in columnas_cuantitativas and columna_y not in columnas_cuantitativas:
        raise HTTPException(detail="No se pueden ni contar db",status_code=404)

    columna_x = df[columna_x] 
    columna_y = df[columna_y]
    corr1 = columna_x.corr(columna_y)


    return{corr1}
        



@app.get("/ventas_x_region")
def ventas(regiones: Optional[str] = None):
    if regiones:
        lista_regiones=regiones.split(",")
        data = df.groupby("region")["total"].sum().loc[lista_regiones]
        return data
    else:
        data = df.groupby("region")["total"].sum()
        return data. to_dict()








@app.get("/graficas/precios")
def grafica_precios(bins,columna_x):
    if columna_x in columnas_cuantitativas:
        fig, ax = plt.subplots()
        ax.hist(df["precio_unitario"].dropna(), int(bins))
        ax.set_title("Distribución de precios unitarios")
        ax.set_xlabel("Precio unitario")
        ax.set_ylabel("Frecuencia")

        imagen = BytesIO()
        fig.savefig(imagen, format="png", bbox_inches="tight")
        plt.close(fig)
        imagen.seek(0)

        return StreamingResponse(imagen, media_type="image/png")
    else:
        raise HTTPException(status_code=403, detail="No se pueden las cualitativas")



