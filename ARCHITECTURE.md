# ARCHITECTURE · Tasación de viviendas para Banc Avellaner

> **Cómo está construido.** Lo escribe el equipo. El agente puede proponer cambios, pero no aplicarlos sin aprobación.
> Las indicaciones entre `<!-- -->` son de la plantilla: borradlas cuando escribáis cada sección.

## 1. Flujo de datos y del modelo

Lo que ya viene en la plantilla (ejemplo resuelto):

```text
data/raw/*.csv ──► src/datos.py ──► src/estrategias.py ──┬─► src/experimentos.py ──► reports/experimentos.csv
                                     (ESTRATEGIAS,        │      (validación cruzada, particiones 1-5)
                                      MODELO_FINAL)       │
                                                          └─► src/entrenar.py ──► models/modelo.joblib
                                                                 (1-5 → validacion)  reports/metricas.json
                                                                                     reports/predicciones_validacion.csv
models/modelo.joblib + test_set.csv ──► src/predecir.py ──► entregables/envio_kaggle.csv
reports/ + models/ ──► src/app.py (cuadro de mando: solo lee, no entrena)
```

<!--
Completad el esquema con lo que añadirá el agente: ¿dónde vivirán vuestras transformaciones y características nuevas?
¿Dónde se calcula lo que muestra cada pantalla?
-->

## 2. Carpetas

| Carpeta | Qué contiene |
| --- | --- |
| `src/` | Todo el código del proyecto |
| `tests/acceptance/` | Tests del contrato del profesorado, del ejemplo resuelto y de vuestros criterios |
| `tests/unit/` | Tests unitarios (los puede escribir el agente) |
| `data/raw/` | CSV descargados. Solo lectura |
| `models/` | Modelo entrenado. No va a Git: se regenera con `src.entrenar` |
| `reports/` | Resultados de los experimentos y del modelo final |
| `entregables/` | Envío a Kaggle |
| `notebooks/` | Exploración. Importan de `src/`; nunca al revés |
| `scripts/` | Descarga de datos y comprobación de trazabilidad |

## 3. Módulos y responsabilidades

| Módulo | Hace | No hace |
| --- | --- | --- |
| `datos.py` | Carga los CSV, separa X e y y `limpiar_objetivo()` (fila a fila) | No transforma variables: eso va en el `Pipeline` |
| `baseline.py` | La tasación ingenua (R2) | |
| `validacion.py` | Validación cruzada e intervalos por bootstrap (R3, R4) | No sabe qué estrategias existen |
| `estrategias.py` | Define cada estrategia como un modelo sin entrenar y elige `MODELO_FINAL` | No entrena ni evalúa |
| `experimentos.py` | Evalúa todas las estrategias y escribe `experimentos.csv` | No toca `validacion` |
| `entrenar.py` | Entrena `MODELO_FINAL`, lo mide en `validacion` y lo guarda | |
| `predecir.py` | Predice el test con el modelo guardado | No entrena |
| `explicar.py` | _Por hacer (CM5)_ | |
| `app.py` | El cuadro de mando | No entrena ni recalcula experimentos |

<!--
Decidid qué módulos nuevos hacen falta (por ejemplo, preparacion.py para vuestras transformaciones
y características nuevas) y qué hace y qué NO hace cada uno. Los escribe el agente.
-->

## 4. Dependencias

<!--
Instaladas en pyproject.toml: pandas, numpy, scikit-learn, joblib, plotly, streamlit y pytest.
Las nuevas se añaden con `uv add` y se justifican aquí.
-->

| Librería | Para qué |
| --- | --- |
| | |

## 5. Qué está protegido

El agente no modifica `SPECS.md`, `DESIGN.md`, `data/raw/` ni este fichero sin aprobación del equipo. Los tests de `tests/acceptance/` los escribe el agente en sus tareas, una persona del equipo los valida y después nadie los cambia para que pasen. El equipo no escribe en `src/` ni en `tests/`.
