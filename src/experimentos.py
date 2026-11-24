"""Evalúa todas las estrategias con validación cruzada y escribe reports/experimentos.csv (R5).

    uv run python -m src.experimentos
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.datos import INFORMES, PARTICIONES_CV, cargar_entrenamiento, limpiar_objetivo
from src.estrategias import ESTRATEGIAS, TIPOS
from src.validacion import validacion_cruzada


def evaluar_estrategias(datos: pd.DataFrame) -> pd.DataFrame:
    """Una fila por estrategia: MAE de cada partición, media y desviación típica (R5)."""
    filas = []
    for estrategia in ESTRATEGIAS:
        if estrategia.tipo not in TIPOS:
            raise ValueError(f"{estrategia.nombre}: tipo {estrategia.tipo!r} no es uno de {TIPOS}")
        errores = validacion_cruzada(estrategia.crear(), datos)
        fila = {"estrategia": estrategia.nombre, "tipo": estrategia.tipo,
                "descripcion": estrategia.descripcion}
        fila |= {f"mae_p{p}": e for p, e in zip(PARTICIONES_CV, errores)}
        fila |= {"mae_medio": float(np.mean(errores)), "mae_sd": float(np.std(errores, ddof=1))}
        filas.append(fila)
        print(f"{estrategia.nombre:30s} MAE medio {fila['mae_medio']:>12,.0f} €  ± {fila['mae_sd']:>9,.0f}")
    return pd.DataFrame(filas)


def main() -> None:
    resultados = evaluar_estrategias(limpiar_objetivo(cargar_entrenamiento()))
    INFORMES.mkdir(exist_ok=True)
    resultados.to_csv(INFORMES / "experimentos.csv", index=False)
    print(f"Escrito {INFORMES / 'experimentos.csv'}")


if __name__ == "__main__":
    main()
