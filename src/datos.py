"""Carga de los datos, limpieza de la variable objetivo y rutas del proyecto (ejemplo resuelto: R1)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
MODELOS = RAIZ / "models"
INFORMES = RAIZ / "reports"
ENTREGABLES = RAIZ / "entregables"

OBJETIVO = "precio"
PARTICIONES_CV = ["1", "2", "3", "4", "5"]
VALIDACION = "validacion"
# Columnas que describen la operación, no la vivienda: no son variables del modelo
NO_VARIABLES = [OBJETIVO, "particion", "estado_operacion"]


def cargar_entrenamiento() -> pd.DataFrame:
    """Lee train_set.csv y le añade la columna `particion` de particiones.csv (R1).

    El índice es la columna `index` de los CSV. No se limpia nada: eso lo decide el equipo.
    """
    train = pd.read_csv(RAW / "train_set.csv")
    particiones = pd.read_csv(RAW / "particiones.csv", dtype={"particion": str})
    datos = train.merge(particiones, on="index", how="left", validate="one_to_one")
    return datos.set_index("index")


def cargar_test() -> pd.DataFrame:
    """Lee test_set.csv tal cual, con `index` como índice. No tiene `precio` (R1)."""
    return pd.read_csv(RAW / "test_set.csv", index_col="index")


def limpiar_objetivo(datos: pd.DataFrame) -> pd.DataFrame:
    """Filas del entrenamiento que se usan para entrenar y para evaluar (contrato CM7).

    Se aplica ANTES de separar las particiones, así que debe decidir FILA A FILA, con reglas
    fijas que no dependan de otras filas (nada de medianas, percentiles ni medias del conjunto).
    Puede quitar filas o corregir el precio de una fila; no puede añadir filas.

    La plantilla no toca nada: qué hacer con los precios dudosos lo decide el equipo en SPECS.md.
    """
    return datos


def separar(datos: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separa las variables (X) de la variable objetivo (y) (R1).

    Quita `precio`, `particion` y `estado_operacion`: describen la operación, no la vivienda,
    y no están en el test.
    """
    X = datos.drop(columns=NO_VARIABLES, errors="ignore")
    return X, datos[OBJETIVO]
