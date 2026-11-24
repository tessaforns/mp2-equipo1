"""Cuadro de mando de validación del modelo (esqueleto de la plantilla).

    uv run streamlit run src/app.py

Solo lee lo que escriben src.experimentos y src.entrenar: no entrena nada.
El contenido de cada pantalla lo decide el equipo en DESIGN.md §4.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # para importar src/ desde Streamlit

import pandas as pd
import streamlit as st

from src.datos import INFORMES

st.set_page_config(page_title="Tasación · Banc Avellaner", layout="wide")


@st.cache_data
def leer_experimentos() -> pd.DataFrame | None:
    ruta = INFORMES / "experimentos.csv"
    return pd.read_csv(ruta) if ruta.exists() else None


@st.cache_data
def leer_metricas() -> dict | None:
    ruta = INFORMES / "metricas.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


@st.cache_data
def leer_predicciones() -> pd.DataFrame | None:
    ruta = INFORMES / "predicciones_validacion.csv"
    return pd.read_csv(ruta, index_col=0) if ruta.exists() else None


def falta(comando: str) -> None:
    st.info(f"Todavía no hay resultados. Ejecuta `{comando}`.")


def pantalla_experimentos() -> None:
    st.header("Experimentos")
    experimentos = leer_experimentos()
    if experimentos is None:
        return falta("uv run python -m src.experimentos")
    st.dataframe(experimentos, hide_index=True)
    st.caption("Pendiente: DESIGN.md §4 · Experimentos.")


def pantalla_rendimiento() -> None:
    st.header("Rendimiento")
    metricas = leer_metricas()
    if metricas is None:
        return falta("uv run python -m src.entrenar")
    st.json(metricas)
    st.caption("Pendiente: DESIGN.md §4 · Rendimiento.")


def pantalla_donde_falla() -> None:
    st.header("Dónde falla")
    predicciones = leer_predicciones()
    if predicciones is None:
        return falta("uv run python -m src.entrenar")
    st.dataframe(predicciones.head(20))
    st.caption("Pendiente: DESIGN.md §4 y §5 · Dónde falla y mapa de residuos.")


def pantalla_abrir_la_caja() -> None:
    st.header("Abrir la caja")
    st.caption("Pendiente: DESIGN.md §4 y §6 · Coeficientes y desglose de una vivienda (necesita src/explicar.py).")


paginas = [
    st.Page(pantalla_experimentos, title="Experimentos", url_path="experimentos"),
    st.Page(pantalla_rendimiento, title="Rendimiento", url_path="rendimiento"),
    st.Page(pantalla_donde_falla, title="Dónde falla", url_path="donde-falla"),
    st.Page(pantalla_abrir_la_caja, title="Abrir la caja", url_path="abrir-la-caja"),
]
st.navigation(paginas).run()
