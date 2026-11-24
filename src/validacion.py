"""Cómo se mide el error: validación cruzada e intervalos por bootstrap (ejemplo resuelto: R3 y R4)."""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from src.datos import PARTICIONES_CV, separar

Metrica = Callable[[np.ndarray, np.ndarray], float]


def validacion_cruzada(modelo: BaseEstimator, datos: pd.DataFrame) -> list[float]:
    """MAE de cada partición 1-5, entrenando con las otras cuatro (R3).

    Solo usa las filas de las particiones 1-5: las de `validacion` no se miran nunca.
    El modelo se clona en cada partición, así que todo lo que aprende (medianas, escalas,
    categorías…) se calcula solo con las filas de entrenamiento de esa partición.
    """
    cv = datos[datos["particion"].isin(PARTICIONES_CV)]
    errores = []
    for particion in PARTICIONES_CV:
        X_ent, y_ent = separar(cv[cv["particion"] != particion])
        X_eval, y_eval = separar(cv[cv["particion"] == particion])
        ajustado = clone(modelo).fit(X_ent, y_ent)
        errores.append(float(mean_absolute_error(y_eval, ajustado.predict(X_eval))))
    return errores


def mae(y_real: np.ndarray, y_pred: np.ndarray) -> float:
    return float(mean_absolute_error(y_real, y_pred))


def rmse(y_real: np.ndarray, y_pred: np.ndarray) -> float:
    return float(root_mean_squared_error(y_real, y_pred))


def intervalo_bootstrap(y_real: np.ndarray, y_pred: np.ndarray, metrica: Metrica,
                        n: int = 2000, nivel: float = 0.95, semilla: int = 2026) -> dict:
    """Valor de la métrica e intervalo de confianza percentil por bootstrap de las filas (R4)."""
    y_real, y_pred = np.asarray(y_real, dtype=float), np.asarray(y_pred, dtype=float)
    rng = np.random.default_rng(semilla)
    muestras = rng.integers(0, len(y_real), size=(n, len(y_real)))
    valores = np.array([metrica(y_real[i], y_pred[i]) for i in muestras])
    alfa = (1 - nivel) / 2
    return {
        "valor": metrica(y_real, y_pred),
        "ic95": [float(np.quantile(valores, alfa)), float(np.quantile(valores, 1 - alfa))],
    }
