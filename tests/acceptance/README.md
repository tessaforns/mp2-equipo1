# Tests de aceptación

- `test_contrato_modelo.py` es del profesorado (criterios CM1–CM7 de `AGENTS.md`). **No se modifica.**
- `test_ejemplo_resuelto.py` cubre el ejemplo resuelto (CA1–CA4 de `SPECS.md`). No lo borréis: sirve de modelo.
- El resto de ficheros los escribe el agente a partir de los criterios `CA…` de `SPECS.md` §7, en una tarea
  propia de `TASKS.md` al empezar cada fase, **antes** de implementar lo que comprueban. Una persona del equipo
  los valida (¿el ejemplo es el de `SPECS.md`?, ¿el resultado esperado está calculado a mano?) y lo anota en
  `Verificado por:` de esa tarea. Después, nadie los cambia para que pasen.
  Podéis organizarlos por fases, por ejemplo `test_limpieza.py`, `test_transformaciones.py`,
  `test_variables_nuevas.py` y `test_modelo.py`.

Cada test se marca con el criterio que verifica, para que `scripts/trazabilidad.py` lo encuentre:

```python
import pytest


@pytest.mark.criterio("CA5")
def test_sin_superficie_cero(entrenamiento):
    ...
```

Las *fixtures* de `tests/conftest.py` dan acceso a los datos y a los resultados:

| Fixture | Qué es |
| --- | --- |
| `entrenamiento` | Ventas de entrenamiento con la columna `particion` |
| `test_crudo` | Ventas del test, sin precio |
| `modelo` | El modelo guardado en `models/modelo.joblib` |
| `metricas` | `reports/metricas.json` |
| `experimentos` | `reports/experimentos.csv` |
| `envio` y `muestra_envio` | El envío a Kaggle y `sampleSubmission.csv` |

Tres tipos de test útiles en este proyecto:

- **Una transformación, con un ejemplo pequeño calculado a mano**, para saber el resultado exacto (como CA2 y CA4).
- **Un experimento, con `experimentos.csv`**: "E3 mejora a E1 en al menos 4 de las 5 particiones".
- **Una propiedad del modelo**: "ninguna vivienda del test se tasa por encima de 10 millones de euros".

Para probar la app sin navegador, `streamlit.testing.v1.AppTest`.
