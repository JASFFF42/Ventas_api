from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

app = FastAPI()

RUTA_CSV = Path(__file__).parent / "ventas_sinteticas.csv"
df = pd.read_csv(RUTA_CSV)
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")


@app.get("/calculos/estadisticas")
def saludo():
    return {"mensaje":"Hola desde mi api"}

columnas_categoricas=["categoria","region","canal","vendedor"]

@app.get("/calculos/estadisticas")
def calcular(columna):
    if columna not in columnas_categoricas:
        raise HTTPException(status_code=404,detail="esa columna no es cuantitativas, ndm")
    datos = df[columna]
    media= datos.mean()
    mediana = datos.median()
    minimo= datos.min()
    maximo = datos.max()
    desvvest= datos.std()
    moda = datos.mode()

    return {
        "media": media,
        "mediana": mediana,
        "mínimo": minimo,
        "máximo": maximo,
        "desvvest": desvvest,
        "moda": moda
    }


