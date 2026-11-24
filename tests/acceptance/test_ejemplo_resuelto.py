"""Tests del ejemplo resuelto (criterios CA1-CA4 de SPECS.md).

Son el modelo de los tests que el agente escribirá para vuestros criterios: un test con los datos
reales (CA1) y tres con ejemplos pequeños calculados a mano (CA2-CA4), donde se sabe el resultado exacto.
"""
import numpy as np
import pandas as pd
import pytest

from src.baseline import BaselineMetroCuadrado
from src.datos import PARTICIONES_CV, VALIDACION
from src.validacion import intervalo_bootstrap, mae, validacion_cruzada


@pytest.mark.criterio("CA1")
def test_carga_y_particiones(entrenamiento):
    assert len(entrenamiento) == 6237
    assert set(entrenamiento["particion"]) == set(PARTICIONES_CV) | {VALIDACION}
    proporcion = (entrenamiento["particion"] == VALIDACION).mean()
    assert 0.18 < proporcion < 0.22, f"La validación tiene el {proporcion:.0%} de las filas"
    particiones_por_inmueble = entrenamiento.groupby("ref_catastral")["particion"].nunique()
    assert (particiones_por_inmueble == 1).all(), "Un mismo inmueble aparece en dos particiones"


@pytest.mark.criterio("CA2")
def test_baseline_a_mano():
    X = pd.DataFrame({"barri": ["A", "A", None], "municipi": ["Barcelona", "Barcelona", "Badalona"],
                      "superficie_construida": [100.0, 50.0, 80.0]})
    y = pd.Series([300_000.0, 200_000.0, 160_000.0])
    baseline = BaselineMetroCuadrado().fit(X, y)
    # €/m²: A = mediana(3.000, 4.000) = 3.500 · Badalona = 2.000 · global = mediana(3.000, 4.000, 2.000) = 3.000
    nuevas = pd.DataFrame({"barri": ["A", None, "C", "A"], "municipi": ["Barcelona", "Badalona", "Barcelona", "Barcelona"],
                           "superficie_construida": [60.0, 0.0, 100.0, np.nan]})
    # A, 60 m² → 210.000 · Badalona sin superficie → precio mediano de Badalona = 160.000
    # C no tiene ventas → 3.000 × 100 = 300.000 · A sin superficie → precio mediano de A = 250.000
    np.testing.assert_allclose(baseline.predict(nuevas), [210_000, 160_000, 300_000, 250_000])


def _datos_pequenos(precio_validacion: float) -> pd.DataFrame:
    filas = []
    for p in PARTICIONES_CV:
        filas += [{"habitaciones": 1, "precio": 100.0, "particion": p}, {"habitaciones": 2, "precio": 200.0, "particion": p}]
    filas += [{"habitaciones": 1, "precio": precio_validacion, "particion": VALIDACION}]
    return pd.DataFrame(filas)


@pytest.mark.criterio("CA3")
def test_validacion_cruzada_no_mira_validacion():
    from sklearn.linear_model import LinearRegression
    normal = validacion_cruzada(LinearRegression(), _datos_pequenos(100.0))
    absurdo = validacion_cruzada(LinearRegression(), _datos_pequenos(1e9))
    assert len(normal) == 5
    assert normal == absurdo, "Cambiar el precio de la validación ha cambiado el error de la validación cruzada"
    np.testing.assert_allclose(normal, 0, atol=1e-6)  # precio = 100 · habitaciones: el ajuste es perfecto


@pytest.mark.criterio("CA4")
def test_intervalo_bootstrap():
    real, pred = np.array([100.0, 200, 300, 400]), np.array([110.0, 190, 330, 400])
    resultado = intervalo_bootstrap(real, pred, mae)
    assert resultado["valor"] == pytest.approx(12.5)  # (10 + 10 + 30 + 0) / 4
    inferior, superior = resultado["ic95"]
    assert 0 <= inferior <= 12.5 <= superior <= 30
    assert intervalo_bootstrap(real, pred, mae) == resultado, "Con la misma semilla debe dar lo mismo"
