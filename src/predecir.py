"""Predice el conjunto de test con el modelo guardado y escribe el envío para Kaggle (R7).

    uv run python -m src.predecir
"""
from __future__ import annotations

import joblib
import pandas as pd

from src.datos import ENTREGABLES, MODELOS, cargar_test


def main() -> None:
    modelo = joblib.load(MODELOS / "modelo.joblib")
    test = cargar_test()
    envio = pd.DataFrame({"index": test.index, "precio": modelo.predict(test)})
    ENTREGABLES.mkdir(exist_ok=True)
    envio.to_csv(ENTREGABLES / "envio_kaggle.csv", index=False)
    print(f"Escrito {ENTREGABLES / 'envio_kaggle.csv'} ({len(envio)} filas)")


if __name__ == "__main__":
    main()
