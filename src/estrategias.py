"""Estrategias que se comparan con validación cruzada (R5).

Cada estrategia es una forma de preparar los datos y ajustar el modelo, descrita en
SPECS.md §4 antes de añadirla aquí. `uv run python -m src.experimentos` las evalúa todas.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.baseline import BaselineMetroCuadrado

TIPOS = ("baseline", "minimo", "estrategia", "caracteristica")


@dataclass(frozen=True)
class Estrategia:
    nombre: str          # identificador corto, sin espacios: aparece en experimentos.csv
    tipo: str            # uno de TIPOS
    descripcion: str     # qué hace, en una frase
    crear: Callable[[], BaseEstimator]  # devuelve el modelo SIN entrenar


VARIABLES_MINIMO = ["superficie_construida", "habitaciones", "banos", "distancia_centro_km", "poblacion_zona"]


def modelo_minimo() -> Pipeline:
    """Regresión lineal con las variables numéricas que no tienen nulos, sin transformar (R5)."""
    seleccion = ColumnTransformer([("numericas", "passthrough", VARIABLES_MINIMO)])
    return Pipeline([("preparacion", seleccion), ("regresion", LinearRegression())])


def l1_superficie_corregida() -> Pipeline:
    """Sustituye los ceros de superficie construida por la mediana del fold de entrenamiento (R9)."""
    resto_variables = [variable for variable in VARIABLES_MINIMO if variable != "superficie_construida"]
    preparacion = ColumnTransformer(
        [
            (
                "superficie",
                SimpleImputer(missing_values=0, strategy="median"),
                ["superficie_construida"],
            ),
            ("resto", "passthrough", resto_variables),
        ]
    )
    return Pipeline([("preparacion", preparacion), ("regresion", LinearRegression())])


ESTRATEGIAS: list[Estrategia] = [
    Estrategia("baseline", "baseline",
               "€/m² mediano de la zona × superficie construida", BaselineMetroCuadrado),
    Estrategia("modelo_minimo", "minimo",
               "Regresión lineal con las 5 variables numéricas sin nulos, sin transformar", modelo_minimo),
    Estrategia(
        "l1_superficie_corregida",
        "estrategia",
        "Modelo mínimo con los ceros de superficie construida imputados por la mediana del fold",
        l1_superficie_corregida,
    ),
]

# La estrategia que se entrena como modelo final (uv run python -m src.entrenar).
MODELO_FINAL = "modelo_minimo"


def buscar(nombre: str) -> Estrategia:
    """Devuelve la estrategia con ese nombre."""
    for estrategia in ESTRATEGIAS:
        if estrategia.nombre == nombre:
            return estrategia
    raise KeyError(f"No hay ninguna estrategia llamada {nombre!r} en ESTRATEGIAS")


def crear_modelo_final() -> BaseEstimator:
    """El modelo de MODELO_FINAL, sin entrenar."""
    return buscar(MODELO_FINAL).crear()
