"""Fixtures compartidas: datos, modelo guardado y resultados (contrato de AGENTS.md §3)."""
import json
from pathlib import Path

import joblib
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent


def _exige(ruta: Path, comando: str) -> Path:
    if not ruta.exists():
        pytest.fail(f"No existe {ruta.relative_to(RAIZ)}. Ejecuta antes `{comando}`.", pytrace=False)
    return ruta


@pytest.fixture(scope="session")
def entrenamiento() -> pd.DataFrame:
    from src.datos import cargar_entrenamiento
    _exige(RAIZ / "data" / "raw" / "train_set.csv", "uv run python scripts/descargar_datos.py")
    return cargar_entrenamiento()


@pytest.fixture(scope="session")
def test_crudo() -> pd.DataFrame:
    from src.datos import cargar_test
    _exige(RAIZ / "data" / "raw" / "test_set.csv", "uv run python scripts/descargar_datos.py")
    return cargar_test()


@pytest.fixture(scope="session")
def modelo():
    return joblib.load(_exige(RAIZ / "models" / "modelo.joblib", "uv run python -m src.entrenar"))


@pytest.fixture(scope="session")
def metricas() -> dict:
    ruta = _exige(RAIZ / "reports" / "metricas.json", "uv run python -m src.entrenar")
    return json.loads(ruta.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def experimentos() -> pd.DataFrame:
    return pd.read_csv(_exige(RAIZ / "reports" / "experimentos.csv", "uv run python -m src.experimentos"))


@pytest.fixture(scope="session")
def envio() -> pd.DataFrame:
    return pd.read_csv(_exige(RAIZ / "entregables" / "envio_kaggle.csv", "uv run python -m src.predecir"))


@pytest.fixture(scope="session")
def muestra_envio() -> pd.DataFrame:
    return pd.read_csv(_exige(RAIZ / "data" / "raw" / "sampleSubmission.csv",
                              "uv run python scripts/descargar_datos.py"))
