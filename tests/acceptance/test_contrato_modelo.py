"""Contrato del modelo fijado por el profesorado (criterios CM1-CM7 de AGENTS.md).

NO SE MODIFICA. Comprueba el modelo y sus salidas, sea cual sea la arquitectura del equipo.
"""
import numpy as np
import pandas as pd
import pytest
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import ElasticNet, ElasticNetCV, Lasso, LassoCV, LinearRegression, Ridge, RidgeCV
from sklearn.pipeline import Pipeline

from src.datos import PARTICIONES_CV, VALIDACION, limpiar_objetivo, separar
from src.validacion import mae

LINEALES = (LinearRegression, Ridge, RidgeCV, Lasso, LassoCV, ElasticNet, ElasticNetCV)


def _limpios(entrenamiento: pd.DataFrame) -> pd.DataFrame:
    return limpiar_objetivo(entrenamiento)


def _filas_validacion(entrenamiento: pd.DataFrame) -> pd.DataFrame:
    limpios = _limpios(entrenamiento)
    return limpios[limpios["particion"] == VALIDACION]


@pytest.mark.criterio("CM1")
def test_predice_filas_crudas(modelo, test_crudo):
    prediccion = np.asarray(modelo.predict(test_crudo), dtype=float)
    assert len(prediccion) == len(test_crudo)
    assert not np.isnan(prediccion).any(), "Hay predicciones vacías (NaN)"
    negativas = int((prediccion <= 0).sum())
    assert negativas == 0, f"{negativas} viviendas del test tienen un precio predicho de 0 o negativo"


@pytest.mark.criterio("CM2")
def test_formato_envio(envio, muestra_envio):
    assert list(envio.columns) == ["index", "precio"], f"Columnas del envío: {list(envio.columns)}"
    assert len(envio) == len(muestra_envio), "El envío no tiene una fila por vivienda del test"
    assert set(envio["index"]) == set(muestra_envio["index"]), "Los índices no coinciden con sampleSubmission.csv"
    assert envio["precio"].notna().all()


@pytest.mark.criterio("CM3")
def test_metricas_validacion(metricas, modelo, entrenamiento):
    validacion = _filas_validacion(entrenamiento)
    assert metricas["n_validacion"] == len(validacion), "Las métricas no se han calculado con la partición de validación"
    for quien in ("baseline", "modelo"):
        for nombre in ("mae", "rmse"):
            m = metricas[quien][nombre]
            inferior, superior = m["ic95"]
            assert inferior <= m["valor"] <= superior, f"{quien}.{nombre}: el valor no está dentro de su IC"
    X_val, y_val = separar(validacion)
    recalculado = mae(y_val, modelo.predict(X_val))
    assert recalculado == pytest.approx(metricas["modelo"]["mae"]["valor"], rel=1e-6), \
        "El MAE de metricas.json no es el del modelo guardado: volved a ejecutar src.entrenar"


@pytest.mark.criterio("CM4")
def test_reproducible(modelo, entrenamiento):
    from src.estrategias import crear_modelo_final
    limpios = _limpios(entrenamiento)
    X_ent, y_ent = separar(limpios[limpios["particion"].isin(PARTICIONES_CV)])
    X_val, _ = separar(_filas_validacion(entrenamiento))
    primera = crear_modelo_final().fit(X_ent, y_ent).predict(X_val)
    segunda = crear_modelo_final().fit(X_ent, y_ent).predict(X_val)
    assert np.array_equal(primera, segunda), "Entrenar dos veces no da las mismas predicciones"
    assert np.allclose(modelo.predict(X_val), primera), \
        "El modelo guardado no es el de MODELO_FINAL: volved a ejecutar src.entrenar"


def _partes(modelo):
    """Separa el preprocesado del estimador lineal, aceptando TransformedTargetRegressor fuera o dentro."""
    if isinstance(modelo, TransformedTargetRegressor):
        modelo = modelo.regressor_
    assert isinstance(modelo, Pipeline), "El modelo debe ser un Pipeline de scikit-learn"
    final = modelo[-1]
    if isinstance(final, TransformedTargetRegressor):
        final = final.regressor_
    return modelo[:-1], final


@pytest.mark.criterio("CM5")
def test_lineal_y_explicable(modelo, entrenamiento):
    preparacion, estimador = _partes(modelo)
    assert isinstance(estimador, LINEALES), f"El estimador final es {type(estimador).__name__}, no un modelo lineal"
    try:
        from src.explicar import explicar
    except ModuleNotFoundError:
        pytest.fail("Falta src/explicar.py con la función explicar(modelo, X) (AGENTS.md §3)", pytrace=False)
    X_val, _ = separar(_filas_validacion(entrenamiento).head(50))
    contribuciones = explicar(modelo, X_val)
    assert isinstance(contribuciones, pd.DataFrame) and "intercepto" in contribuciones.columns
    assert len(contribuciones) == len(X_val)
    esperado = estimador.predict(preparacion.transform(X_val))
    np.testing.assert_allclose(contribuciones.sum(axis=1).to_numpy(), esperado, rtol=1e-6, atol=1e-6,
                               err_msg="El intercepto más las contribuciones no da la predicción del modelo")


@pytest.mark.criterio("CM6")
def test_experimentos(experimentos):
    columnas = {"estrategia", "tipo", "descripcion", "mae_medio", "mae_sd"} | {f"mae_p{p}" for p in PARTICIONES_CV}
    faltan = columnas - set(experimentos.columns)
    assert not faltan, f"Faltan columnas en experimentos.csv: {sorted(faltan)}"
    assert experimentos["estrategia"].is_unique
    minimos = {"baseline": 1, "minimo": 1, "estrategia": 3, "caracteristica": 1}
    cuenta = experimentos["tipo"].value_counts()
    for tipo, n in minimos.items():
        assert cuenta.get(tipo, 0) >= n, f"Hacen falta al menos {n} fila(s) de tipo '{tipo}' y hay {cuenta.get(tipo, 0)}"
    particiones = experimentos[[f"mae_p{p}" for p in PARTICIONES_CV]]
    assert (particiones > 0).all().all()
    assert np.allclose(particiones.mean(axis=1), experimentos["mae_medio"]), "mae_medio no es la media de las particiones"


@pytest.mark.criterio("CM7")
def test_limpiar_objetivo_fila_a_fila(entrenamiento):
    limpios = limpiar_objetivo(entrenamiento)
    assert set(limpios.index) <= set(entrenamiento.index), "limpiar_objetivo no puede añadir filas"
    assert "particion" in limpios.columns, "limpiar_objetivo debe conservar la columna particion"
    for semilla in (1, 2):
        subconjunto = entrenamiento.sample(frac=0.3, random_state=semilla)
        esperado = limpios.loc[limpios.index.intersection(subconjunto.index)].sort_index()
        obtenido = limpiar_objetivo(subconjunto).sort_index()
        assert list(obtenido.index) == list(esperado.index), \
            "limpiar_objetivo no decide fila a fila: el resultado depende de qué otras filas hay"
        pd.testing.assert_frame_equal(obtenido, esperado, check_like=True)
