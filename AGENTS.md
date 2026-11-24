# AGENTS.md

Instrucciones para el agente de IA que trabaja en este repositorio. **Léelas al empezar cada conversación y síguelas siempre.**

El proyecto: un modelo que tasa viviendas de Barcelona y su área metropolitana para Banc Avellaner (un banco inventado) y un cuadro de mando para entenderlo. Los barrios y las direcciones son reales; las viviendas y las ventas (2023-2025) son simuladas.

## 1. Antes de empezar

Lee estos ficheros, en este orden:

1. `SPECS.md`: **qué** construimos. Está organizado en cuatro fases: limpieza, transformaciones, variables nuevas y modelo.
2. `DESIGN.md`: cómo se ve el cuadro de mando.
3. `ARCHITECTURE.md`: dónde va cada cosa en el código.
4. `TASKS.md`: qué toca ahora. Haz la primera tarea sin marcar, salvo que te pidan otra.
5. `DATOS.md`: qué significa cada columna.

Si falta algo para hacer la tarea, **no lo supongas**: pregunta.

## 2. Comandos

| Para | Comando |
| --- | --- |
| Instalar el entorno | `uv sync` |
| Descargar los datos | `uv run python scripts/descargar_datos.py` |
| Comparar las estrategias | `uv run python -m src.experimentos` |
| Entrenar el modelo final | `uv run python -m src.entrenar` |
| Hacer el envío a Kaggle | `uv run python -m src.predecir` |
| Ejecutar los tests | `uv run pytest` |
| Ver si cada criterio tiene su test | `uv run python scripts/trazabilidad.py` |
| Abrir el cuadro de mando | `uv run streamlit run src/app.py` |

## 3. Reglas del profesorado (no se cambian)

**Funciones y ficheros que deben existir** (los usan los tests del profesorado):

| Dónde | Qué |
| --- | --- |
| `src/datos.py` | `cargar_entrenamiento()`, `cargar_test()`, `separar(datos)` y `limpiar_objetivo(datos)` |
| `src/estrategias.py` | La lista `ESTRATEGIAS`, la constante `MODELO_FINAL` y la función `crear_modelo_final()` |
| `src/explicar.py` | `explicar(modelo, X)`, que devuelve una tabla (ver CM5) |
| `src.experimentos` | Escribe `reports/experimentos.csv` |
| `src.entrenar` | Escribe `models/modelo.joblib`, `reports/metricas.json` y `reports/predicciones_validacion.csv` |
| `src.predecir` | Escribe `entregables/envio_kaggle.csv` |

**Cómo es el modelo:**

- Es un `Pipeline` de scikit-learn con **toda la preparación dentro**: `modelo.predict()` recibe las filas tal como vienen en `test_set.csv`.
- El último paso es lineal: `LinearRegression`, `Ridge`, `Lasso` o `ElasticNet`. Para predecir el logaritmo del precio se usa `TransformedTargetRegressor`.
- `limpiar_objetivo()` se aplica primero. Después se entrena con las particiones 1-5 y se mide **una sola vez** en `validacion`. Nunca se usa `validacion` para comparar estrategias ni para elegir λ.
- `limpiar_objetivo()` decide cada fila mirando **solo esa fila** (por ejemplo, quitarla si es un anuncio retirado). No puede usar medias, medianas ni nada calculado con otras filas.
- Solo se usan variables que el banco conoce **antes de la venta**.
- El test solo se usa para hacer el envío.

**Tests del profesorado** (`tests/acceptance/test_contrato_modelo.py`):

| Test | Qué comprueba |
| --- | --- |
| CM1 | El modelo tasa todas las viviendas del test sin errores, sin vacíos y con precios positivos |
| CM2 | `envio_kaggle.csv` tiene las columnas `index` y `precio` y una fila por vivienda del test |
| CM3 | `metricas.json` tiene el MAE y el RMSE del baseline y del modelo en `validacion`, cada uno con su intervalo de confianza del 95 % |
| CM4 | Entrenar el modelo final dos veces da las mismas tasaciones |
| CM5 | El último paso es lineal y `explicar()` devuelve una columna `intercepto` y una por cada columna del modelo; sumadas, dan la predicción (en logaritmo, si se predice el logaritmo) |
| CM6 | `experimentos.csv` tiene al menos 1 `baseline`, 1 `minimo`, 3 `estrategia` y 1 `caracteristica`, con el MAE de cada partición, la media y la desviación |
| CM7 | `limpiar_objetivo()` decide fila a fila: limpiar una parte de los datos da lo mismo que limpiarlo todo y quedarse con esa parte |

## 4. Cómo trabajas

**Todo el código de `src/` y de `tests/` lo escribes tú.** El equipo no edita esos ficheros: escribe los `.md`, explora en `notebooks/` y verifica lo que haces. Si algo del código está mal, el equipo corrige la especificación y te pide el cambio.

1. **Una tarea cada vez.** Antes de escribir código, di qué vas a hacer, qué requisitos (`R…`) y criterios (`CA…`) cubre y qué ficheros vas a tocar.
2. **Haz solo lo que pide la tarea**, siguiendo `ARCHITECTURE.md` y `DESIGN.md`.
3. **Comprueba:**
   - Ejecuta los tests de la tarea.
   - Si has añadido una estrategia, ejecuta `uv run python -m src.experimentos` y **copia en tu respuesta** su fila de `experimentos.csv` y la de su referencia. No decidas tú si se acepta: lo decide el equipo con la regla de `SPECS.md`.
   - Si has cambiado el modelo final, ejecuta `src.entrenar` y `src.predecir`.
4. **Actualiza `TASKS.md`:** marca la tarea con `[x]` si pasan sus tests y añade una línea `Agente:` con qué hiciste y cómo lo comprobaste. La línea `Verificado por:` la escribe una persona.
5. **Para** y espera a que te pidan la siguiente tarea.

**Tests de aceptación.** En las tareas de tests, escribes en `tests/acceptance/` los tests de los criterios `CA…` de `SPECS.md`, con los ejemplos tal como están escritos. Los marcas con `@pytest.mark.criterio("CA…")`. Una persona del equipo los valida (¿el ejemplo es el de `SPECS.md`?, ¿el resultado esperado está calculado a mano?) y lo anota en `Verificado por:` antes de que implementes la tarea siguiente. Después ya no los cambias.

## 5. Lo que nunca haces

- Nunca modificas `SPECS.md` ni `DESIGN.md`, ni `ARCHITECTURE.md` sin que el equipo lo apruebe. Si ves un error o una contradicción, dilo y para.
- Nunca cambias un test para que pase. Si falla, el problema está en el código, salvo que el equipo diga otra cosa.
- Nunca decides cómo se prepara el modelo (qué variables, qué vacíos, qué λ) si no está en `SPECS.md`. Propón opciones y para.
- Nunca usas las filas de `validacion` para comparar estrategias ni para elegir λ, y nunca usas el test salvo en `src/predecir.py`.
- Nunca calculas nada con todos los datos antes de separar las particiones (medianas, medias por barrio, escalas): va dentro del `Pipeline`.
- Nunca inventas columnas ni datos, y nunca modificas `data/raw/`.
- Nunca escribes cifras fijas en el código para que cuadre un test.
- Nunca añades librerías sin decirlo (se añaden con `uv add`).
- Nunca te sales de la tarea. Si ves otro problema, avisa, pero no lo arregles.

## 6. Estilo de código

- Python con pandas y scikit-learn. Funciones pequeñas, con *type hints*.
- Nombres en castellano y en `snake_case`. Las columnas de los datos conservan su nombre (`municipi`, `barri`, `any_construccio`…).
- Lo que transforma los datos va en funciones usadas con `FunctionTransformer` o en transformadores de scikit-learn, para que esté dentro del `Pipeline`.
- El *docstring* de cada función dice qué requisito cumple, por ejemplo `"""Corrige la superficie construida (R10)."""`.

## 7. Lo que debes saber de los datos

- `train_set.csv`: 6.237 filas con precio. `test_set.csv`: 4.002 sin precio. `particiones.csv` dice en qué partición está cada fila (`1` a `5` o `validacion`).
- Todas las filas de un mismo inmueble (`ref_catastral`) están en la misma partición.
- `separar()` quita `precio`, `estado_operacion` y `particion` de las variables.
- Los datos tienen errores y vacíos. Qué se hace con cada uno está en `SPECS.md`. Si ves algo raro que `SPECS.md` no trata, avisa.

## 8. Notas técnicas

- `src/app.py` añade la raíz del proyecto a `sys.path` para poder importar de `src/`.
- El cuadro de mando **no entrena**: lee `reports/` y `models/`.
- Los nombres de las columnas del modelo se obtienen con `get_feature_names_out()`.
- Si al predecir el logaritmo sale alguna tasación absurda (millones de euros en un piso), avisa.

## 9. Una tarea está terminada cuando

- Hace lo que dicen `SPECS.md`, `DESIGN.md` y `ARCHITECTURE.md`.
- Pasan sus tests.
- `TASKS.md` tiene la línea `Agente:`.
- No se ha tocado nada fuera de la tarea.
