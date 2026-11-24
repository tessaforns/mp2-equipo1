"""Tasación ingenua con la que se compara cualquier modelo (ejemplo resuelto: R2)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin


def zona(X: pd.DataFrame) -> pd.Series:
    """El barrio en Barcelona; el municipio fuera de Barcelona o si falta el barrio (R2)."""
    return X["barri"].fillna(X["municipi"])


class BaselineMetroCuadrado(RegressorMixin, BaseEstimator):
    """Tasación de un tasador con prisa: €/m² mediano de la zona × superficie construida (R2).

    - Zona sin ventas en el entrenamiento → €/m² mediano global.
    - Vivienda sin superficie (vacía o 0) → precio mediano de su zona (o global).
    """

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "BaselineMetroCuadrado":
        y = pd.Series(np.asarray(y, dtype=float), index=X.index)
        superficie = X["superficie_construida"].where(X["superficie_construida"] > 0)
        euros_m2 = (y / superficie).dropna()
        z = zona(X)
        self.m2_zona_ = euros_m2.groupby(z.loc[euros_m2.index]).median()
        self.m2_global_ = float(euros_m2.median())
        self.precio_zona_ = y.groupby(z).median()
        self.precio_global_ = float(y.median())
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        z = zona(X)
        superficie = X["superficie_construida"].where(X["superficie_construida"] > 0)
        por_m2 = z.map(self.m2_zona_).fillna(self.m2_global_) * superficie
        sin_superficie = z.map(self.precio_zona_).fillna(self.precio_global_)
        return por_m2.fillna(sin_superficie).to_numpy(dtype=float)
