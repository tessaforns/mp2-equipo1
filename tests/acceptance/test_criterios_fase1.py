"""Tests de aceptación de los criterios CA5-CA6 de SPECS.md."""
import numpy as np
import pandas as pd
import pytest
from scipy import sparse


@pytest.mark.criterio("CA5")
def test_informe_experimentos_compara_referencia_por_fold(experimentos):
    columnas = {
        "estrategia",
        "referencia",
        "mae_medio",
        "mae_sd",
        "mejora_media_euros",
        "particiones_mejora",
        "aceptada",
        *(f"mae_p{fold}" for fold in range(1, 6)),
    }
    assert columnas <= set(experimentos.columns), (
        f"Faltan columnas en experimentos.csv: {sorted(columnas - set(experimentos.columns))}"
    )
    assert experimentos["estrategia"].is_unique

    por_estrategia = experimentos.set_index("estrategia")
    assert pd.isna(por_estrategia.loc["baseline", "referencia"])
    assert pd.isna(por_estrategia.loc["modelo_minimo", "referencia"])

    for nombre, fila in por_estrategia.iterrows():
        errores = fila[[f"mae_p{fold}" for fold in range(1, 6)]].astype(float)
        assert fila["mae_medio"] == pytest.approx(errores.mean())
        assert fila["mae_sd"] == pytest.approx(errores.std(ddof=1))

        referencia = fila["referencia"]
        if pd.isna(referencia):
            continue

        assert referencia in por_estrategia.index, (
            f"{nombre} referencia una estrategia inexistente: {referencia}"
        )
        errores_referencia = por_estrategia.loc[
            referencia, [f"mae_p{fold}" for fold in range(1, 6)]
        ].astype(float)
        mejoras = errores_referencia.to_numpy() - errores.to_numpy()
        mejora_media = float(mejoras.mean())
        particiones_mejora = int((mejoras > 0).sum())
        aceptada = mejora_media >= 1_000 and particiones_mejora >= 4

        assert fila["mejora_media_euros"] == pytest.approx(mejora_media)
        assert fila["particiones_mejora"] == particiones_mejora
        assert bool(fila["aceptada"]) is aceptada


def _valores_preparados(modelo, datos: pd.DataFrame, columna: str) -> np.ndarray:
    preparacion = modelo.named_steps["preparacion"]
    nombres = list(preparacion.get_feature_names_out())
    indices = [
        indice
        for indice, nombre in enumerate(nombres)
        if nombre.rsplit("__", maxsplit=1)[-1] == columna
    ]
    assert len(indices) == 1, f"No se encontró una única columna preparada para {columna}"

    valores = preparacion.transform(datos)
    if sparse.issparse(valores):
        valores = valores.toarray()
    return np.asarray(valores)[:, indices[0]]


def _datos_superficies() -> tuple[pd.DataFrame, pd.Series]:
    datos = pd.DataFrame(
        {
            "superficie_construida": [100.0, 0.0, 300.0, 2_000.0],
            "superficie_util": [40.0, np.nan, 80.0, 120.0],
            "habitaciones": [1, 2, 3, 4],
            "banos": [1, 1, 2, 2],
            "distancia_centro_km": [1.0, 2.0, 3.0, 4.0],
            "poblacion_zona": [1_000, 2_000, 3_000, 4_000],
        }
    )
    objetivo = pd.Series([100_000.0, 150_000.0, 200_000.0, 250_000.0])
    return datos, objetivo


@pytest.mark.criterio("CA6")
def test_l1_imputa_ceros_con_mediana_y_conserva_extremos():
    from src.estrategias import buscar

    datos, objetivo = _datos_superficies()
    modelo = buscar("l1_superficie_corregida").crear()
    modelo.fit(datos, objetivo)

    np.testing.assert_allclose(
        _valores_preparados(modelo, datos, "superficie_construida"),
        [100.0, 300.0, 300.0, 2_000.0],
    )


@pytest.mark.criterio("CA6")
def test_l2_imputa_superficie_util_con_mediana():
    from src.estrategias import buscar

    datos, objetivo = _datos_superficies()
    modelo = buscar("l2_superficie_util").crear()
    modelo.fit(datos, objetivo)

    np.testing.assert_allclose(
        _valores_preparados(modelo, datos, "superficie_util"),
        [40.0, 80.0, 80.0, 120.0],
    )
