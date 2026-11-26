# SPECS · Tasación de viviendas para Banc Avellaner

> **Qué construimos.** Lo escribe el equipo; el agente lo lee pero no lo edita.
> Las indicaciones entre `<!-- -->` son de la plantilla: borradlas cuando escribáis cada sección.
> Lo marcado como **ejemplo resuelto** ya está implementado y testeado: no lo borréis, ampliadlo.

## 1. Objetivo

<!--
Una o dos frases: para quién es el modelo y qué decisión le ayuda a tomar.
Pista: Núria Casals no quiere "un modelo con buen R²". ¿Qué hará el banco con cada tasación?
-->

## 2. Usuarios y preguntas

<!--
- Usuario: quién usa el modelo y el cuadro de mando, cuándo y qué sabe.
- Preguntas: las del encargo, numeradas (P1, P2…) y concretadas. Cada pantalla del cuadro
  de mando responderá a una o más.
-->

## 3. Datos de entrada y problemas

<!--
Los problemas de calidad que encontréis con notebooks/exploracion.ipynb. Sed concretos: qué columna,
qué valor raro, cuántas filas (en entrenamiento y en test) y por qué importa para tasar.
Hito de la sesión 12: al menos seis problemas documentados.

La última columna dice en qué fase de §4 lo tratáis:
1 · Limpieza, 2 · Transformaciones, 3 · Variables nuevas o (ninguna), si decidís no usar la columna.
La fila P1 es un ejemplo: dejadla y seguid con P2, P3…
-->

Lo encontramos con `notebooks/exploracion.ipynb`. Entrenamiento: 6.237 filas. Test: 4.002.

| Id | Columna | Qué pasa (con cifras) | Por qué importa | Fase |
| --- | --- | --- | --- | --- |
| P1 | `estado_operacion` | En entrenamiento, 620 de 6.237 filas (9,9 %) son anuncios retirados; el test solo contiene ventas. | El precio de un anuncio retirado es el pedido, no el precio de una venta. | 1 · Limpieza |
| P2 | `districte`, `barri` | Ambas columnas faltan en las mismas 1.503 filas de entrenamiento (24,1 %) y 924 de test (23,1 %). Entre esas filas, `municipi` es Barcelona en 97 casos de entrenamiento y 63 de test; en el resto es otro municipio. | La zona sirve para distinguir niveles de precio. Que falte `barri` no significa siempre que la vivienda esté fuera de Barcelona. | 2 · Transformaciones |
| P3 | `superficie_util` | Faltan 2.046 de 6.237 valores en entrenamiento (32,8 %) y 1.305 de 4.002 en test (32,6 %). Los valores observados van de 20 a 348 m² en entrenamiento y de 22 a 414 m² en test. | Es una medida del tamaño de la vivienda y podría aportar información distinta de la superficie construida; su uso y tratamiento de vacíos deben probarse. | 2 · Transformaciones |
| P4 | `parking` | Faltan 626 de 6.237 valores en entrenamiento (10,0 %) y 398 de 4.002 en test (9,9 %). Los valores observados son `No`, `Sí`, `Opcional` e `Incluido`. | El parking puede relacionarse con el precio, pero un vacío no equivale necesariamente a `No`; `Opcional` e `Incluido` tampoco son la misma categoría observada. | 2 · Transformaciones |
| P5 | `estado` | Faltan 427 de 6.237 valores en entrenamiento (6,8 %) y 291 de 4.002 en test (7,3 %). Los valores observados son `a reformar`, `buen estado`, `reformado` y `obra nueva`. | El estado puede relacionarse con el precio; no se debe convertir una categoría nominal en una escala numérica sin justificar el orden y las distancias. | 2 · Transformaciones |
| P6 | `tipo` | No hay valores vacíos. Hay 11 escrituras literales; al ignorar mayúsculas y acentos quedan seis grupos: piso, ático, estudio, casa, dúplex y chalet. Ejemplos: `PISO`/`piso`/`Piso`, `Atico`/`Ático`, `Duplex`/`Dúplex`. | Si las variantes no se normalizan, una misma categoría puede representarse como categorías distintas. | 2 · Transformaciones |
| P7 | `superficie_construida` | Hay 21 ceros en entrenamiento y 9 en test. Hay 2 valores superiores a 1.000 m² en entrenamiento (máximo 1.590) y 6 en test (máximo 1.900). | Los ceros y los valores extremos pueden distorsionar el ajuste y las tasaciones; falta definir qué regla, si alguna, se probará para corregirlos. | 1 · Limpieza |

## 4. Estrategias y experimentos

<!--
Trabajáis en CUATRO FASES, en este orden. Lo que aceptáis en una fase es el punto de partida
de la siguiente.

  1. Limpieza: qué filas y qué valores son errores (el precio, la superficie…).
  2. Transformaciones: pasar las variables a una forma que el modelo entienda
     (logaritmos, categorías, textos convertidos en números).
  3. Variables nuevas: crear variables que no están en los datos tal cual (al menos una).
  4. Modelo: cambiar la regresión lineal por Ridge y AJUSTAR λ (alpha en scikit-learn),
     probando varios valores (al menos cuatro, por ejemplo de 0,01 a 100).

Cada fila se escribe ANTES DE EJECUTARLA: qué cambia respecto a su referencia (una sola cosa)
y qué esperáis que pase (la hipótesis). Después, con experimentos.csv, rellenáis el resultado y la conclusión
(aceptada o descartada, según vuestra regla de decisión).

- Referencia: la estrategia con la que se compara. Normalmente, la última aceptada.
- MAE medio ± sd: de experimentos.csv.
- Mejora media · particiones: cuánto baja el MAE frente a la referencia, de media, y en cuántas de
  las 5 particiones mejora. Por ejemplo, "2.150 € · 5 de 5". Pedid al agente que lo añada a
  experimentos.csv (escribidlo como requisito en §6, "Cómo decidimos").
- Tipo: "estrategia" o "caracteristica" (las de la fase 3). CM6 pide al menos 3 de la primera y 1 de la segunda.

La primera fila de cada fase es un ejemplo para arrancar: podéis quedárosla, cambiarla o borrarla.
-->

**Regla de decisión** (escrita antes de ejecutar nada): una estrategia se acepta si reduce el MAE medio al menos 1.000 € respecto a su referencia y mejora el MAE en al menos 4 de las 5 particiones. La mejora por partición es `mae_referencia - mae_estrategia`; una mejora positiva cuenta como una partición mejorada. Si no cumple ambas condiciones, se descarta.

Cómo leemos los resultados: `src.experimentos` da el MAE de cada partición (`mae_p1` … `mae_p5`). Comparamos cada estrategia con su referencia partición a partición, porque hay particiones más difíciles que otras para todas las estrategias a la vez.

### Punto de partida (ejemplo resuelto)

| Id | Tipo     | Qué cambia                                                                                                                                 | Referencia | Hipótesis                                                 | MAE medio ± sd | Mejora media · particiones | Conclusión                    |
| -- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------- | --------------- | --------------------------- | ------------------------------ |
| E0 | baseline | €/m² mediano de la zona × superficie construida                                                                                          | —         | —                                                         |                 | —                          | La tasación que hay que batir |
| E1 | minimo   | Regresión lineal con `superficie_construida`, `habitaciones`, `banos`, `distancia_centro_km` y `poblacion_zona`, sin transformar | —         | _Vuestra hipótesis: ¿mejor o peor que E0? ¿Por qué?_ | `126,535`     | —                          |                                |

### Fase 1 · Limpieza

<!--
La limpieza del precio va en limpiar_objetivo() (AGENTS.md §3): decide fila a fila y se aplica antes de
separar las particiones. No es una estrategia, porque cambia las filas con las que se mide todo: cuando
la cambiéis, volved a ejecutar E0 y E1 y anotad sus cifras nuevas aquí.
El resto de la limpieza (por ejemplo, la superficie) sí son estrategias, dentro del Pipeline.
-->

| Id | Tipo     | Qué cambia                                                                               | Referencia | Hipótesis                                               | MAE medio ± sd | Mejora media · particiones | Conclusión |
| -- | -------- | ----------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------- | --------------- | --------------------------- | ----------- |
| L1 | estrategia | En `superficie_construida`, sustituye los ceros por la mediana aprendida en el fold de entrenamiento; deja los demás valores, incluidos los extremos, sin cambios. | E1 | Corregir los ceros podría reducir su influencia en las tasaciones. | | | |
| L2 | estrategia | Añade `superficie_util` como variable e imputa sus vacíos con la mediana aprendida solo con las filas de entrenamiento de cada fold. | E1 | La superficie útil podría aportar información sobre el precio. | | | |

### Fase 2 · Transformaciones

Para las categorías se propone probar One-Hot Encoding; no se asignarán códigos numéricos ordinales sin una justificación.

| Id | Tipo            | Qué cambia                                                                                                                                                                                                                                          | Referencia | Hipótesis                                                         | MAE medio ± sd | Mejora media · particiones | Conclusión |
| -- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------ | --------------- | --------------------------- | ----------- |
| T1 | estrategia | Añade la zona definida en R2 como categoría, usando el municipio cuando falte `barri`. | L2 | La zona puede recoger diferencias de precio geográficas. | | | |
| T2 | estrategia | Añade `parking`; en esta variante, los vacíos se tratan como `No` y las demás categorías se mantienen distintas. | T1 | La variable podría aportar información, pero esta variante prueba la hipótesis de que un vacío equivale a `No`. | | | |
| T3 | estrategia | Igual que T2, pero los vacíos de `parking` se conservan como una categoría separada `Sin dato`. | T2 | Distinguir un dato desconocido de `No` podría evitar una imputación incorrecta. | | | |
| T4 | estrategia | Añade `estado` como categoría y conserva los vacíos como `Sin dato`. | T3 | El estado de conservación podría aportar información sobre el precio. | | | |
| T5 | estrategia | Añade `tipo` como categoría, normalizando mayúsculas y acentos antes de codificarla. | T4 | El tipo de vivienda podría aportar información sobre el precio. | | | |
| T6 | estrategia | Para `municipi == Barcelona` y `barri` ausente, imputa primero el barrio más frecuente del mismo código postal usando solo el fold de entrenamiento. Si hay empate o no existe ese código postal, usa el centroide de barrio más cercano calculado con ese fold. Si no se puede inferir un único barrio, usa `municipi` (`Barcelona`). | T1 | La inferencia geográfica podría recuperar información de barrio sin usar validación ni test para aprender los mapeos. | | | |

### Fase 3 · Variables nuevas

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | caracteristica | Añade `banos / habitaciones`; cuando `habitaciones == 0`, deja la relación ausente y la imputa con la mediana de la relación aprendida en el fold de entrenamiento. | Última aceptada | La relación entre baños y habitaciones podría aportar información adicional. | | | |
| N2 | caracteristica | Imputa primero `superficie_util` con la mediana aprendida en el fold de entrenamiento y añade `superficie_util / habitaciones`; cuando `habitaciones == 0`, deja la relación ausente y la imputa con la mediana de la relación aprendida en ese fold. | Última aceptada | La superficie útil relativa al número de habitaciones podría aportar información adicional. | | | |

### Fase 4 · Modelo

<!--
Las mismas variables que la última estrategia aceptada en la fase 3; solo cambia el estimador.
Una fila por valor de λ. Escribid antes cómo elegiréis λ y qué haréis si ningún Ridge mejora a la regresión lineal.
-->

| Id | Tipo       | Qué cambia         | Referencia       | Hipótesis                                      | MAE medio ± sd | Mejora media · particiones | Conclusión |
| -- | ---------- | ------------------- | ---------------- | ----------------------------------------------- | --------------- | --------------------------- | ----------- |
| M1 | estrategia | Ridge con `alpha = 0,001` | Regresión lineal de la última estrategia aceptada | Regularización muy pequeña. | | | |
| M2 | estrategia | Ridge con `alpha = 0,01` | Regresión lineal de la última estrategia aceptada | Regularización pequeña. | | | |
| M3 | estrategia | Ridge con `alpha = 0,1` | Regresión lineal de la última estrategia aceptada | Regularización moderada. | | | |
| M4 | estrategia | Ridge con `alpha = 1` | Regresión lineal de la última estrategia aceptada | Regularización mayor que en M1–M3. | | | |

Se elige el `alpha` con menor MAE medio en las cinco particiones 1–5, aunque no mejore a la regresión lineal; si hay empate, se elige el `alpha` menor. No se estandarizan las variables numéricas antes de Ridge. No se usa `validacion` para elegir el `alpha`.

## 5. Salidas

<!--
Las del contrato (AGENTS.md §3) y las que añadáis vosotros (por ejemplo, tablas extra para el cuadro de mando).
-->

| Fichero                                 | Qué contiene                                                                         | Lo escribe           |
| --------------------------------------- | ------------------------------------------------------------------------------------- | -------------------- |
| `reports/experimentos.csv`            | Una fila por estrategia con su MAE por partición                                     | `src.experimentos` |
| `models/modelo.joblib`                | El modelo final entrenado con las particiones 1-5                                     | `src.entrenar`     |
| `reports/metricas.json`               | MAE y RMSE del baseline y del modelo en `validacion`, con IC 95 %                   | `src.entrenar`     |
| `reports/predicciones_validacion.csv` | Precio real, predicción del modelo y del baseline de cada vivienda de `validacion` | `src.entrenar`     |
| `entregables/envio_kaggle.csv`        | Predicción de cada vivienda del test                                                 | `src.predecir`     |

## 6. Requisitos

<!--
Reglas numeradas, cada una verificable y sin ambigüedad. Cada problema de §3 y cada estrategia
de §4 debería acabar en un requisito que diga exactamente qué se hace.
Continuad la numeración del ejemplo resuelto (R8, R9…) y escribid los de cada fase antes de empezarla.
-->

**Ejemplo resuelto: datos y validación**

- R1. `cargar_entrenamiento()` devuelve las 6.237 filas de `train_set.csv` con la columna `particion` de `particiones.csv`; `cargar_test()` devuelve las 4.002 del test. No se limpia nada al cargar. `limpiar_objetivo()` todavía no quita ninguna fila.
- R2. Baseline: la tasación de una vivienda es el €/m² mediano de las operaciones de entrenamiento de su zona (el barrio en Barcelona; el municipio fuera de Barcelona o si falta el barrio) × su `superficie_construida`. Si la zona no tiene operaciones, el €/m² mediano global; si la vivienda no tiene superficie (vacía o 0), el precio mediano de su zona.
- R3. Validación cruzada: cada estrategia se entrena cinco veces, cada vez con cuatro de las particiones 1-5, y se mide el MAE en la que queda fuera. Las filas de `validacion` no se usan.
- R4. El error en `validacion` se da con un intervalo de confianza del 95 % por bootstrap percentil de las filas (2.000 remuestras, semilla 2026).
- R5. Modelo mínimo: regresión lineal con `superficie_construida`, `habitaciones`, `banos`, `distancia_centro_km` y `poblacion_zona`, sin transformar. Es la referencia de las estrategias.
- R6. El modelo final se entrena con las particiones 1-5 y se mide una vez en `validacion`, junto al baseline entrenado con las mismas filas.
- R7. El envío a Kaggle son las predicciones del modelo guardado para las 4.002 viviendas del test.
- R8. `reports/experimentos.csv` incluye para cada estrategia su referencia (el valor de `estrategia` de la fila de referencia), el MAE de cada fold, la media y la desviación estándar muestral (`ddof=1`), la mejora media en euros (`mae_referencia - mae_estrategia`), el número de folds en que mejora y un booleano `aceptada`. La referencia queda vacía para `baseline` y `modelo_minimo`. Se acepta una estrategia solo si la mejora media es de al menos 1.000 € y mejora en al menos 4 de los 5 folds.
- R9. En L1 (`l1_superficie_corregida`), los ceros de `superficie_construida` se tratan como ausentes y se sustituyen por la mediana de los valores no nulos y no cero aprendida solo con las filas del fold de entrenamiento; los demás valores, incluidos los extremos, no se modifican. En L2 (`l2_superficie_util`), los vacíos de `superficie_util` se imputan con la mediana aprendida solo con las filas del fold de entrenamiento.
- R10. En las estrategias T1–T5, las categorías se codifican con One-Hot Encoding. T1 usa el municipio cuando falta el barrio. T2 trata un parking vacío como `No`; T3 lo conserva como `Sin dato`. T4 conserva un `estado` vacío como `Sin dato`. T5 normaliza mayúsculas y acentos de `tipo` antes de codificarlo.
- R11. T6 solo infiere un barrio cuando `municipi == Barcelona` y `barri` está vacío: primero usa el barrio más frecuente para el mismo código postal, calculado con el fold de entrenamiento; si hay empate o no hay correspondencia, usa el centroide de barrio más cercano calculado con ese fold. El centroide es la media de latitud y longitud de las filas del fold con ese barrio y coordenadas válidas. Si no puede inferir un único barrio (por falta de coordenadas o empate de distancia), usa `Barcelona` como zona. Ningún mapeo se calcula con validación o test.
- R12. N1 calcula `banos / habitaciones`. Si `habitaciones == 0`, deja la relación vacía y la imputa con la mediana de la relación calculada en el fold de entrenamiento. N2 imputa primero `superficie_util` con la mediana de esa variable en el fold de entrenamiento y después calcula `superficie_util / habitaciones`; si `habitaciones == 0`, imputa la relación vacía con su mediana calculada en ese fold.
- R13. Se prueban Ridge con `alpha` 0,001, 0,01, 0,1 y 1, usando en cada caso las mismas variables que la última estrategia aceptada de fase 3 y sin estandarizar las variables numéricas. Se elige el `alpha` con menor MAE medio en los folds 1–5, aunque no mejore a la regresión lineal; si hay empate, se elige el menor `alpha`. `validacion` no se usa para seleccionarlo.

**Cómo decidimos**

`experimentos.csv` incluye `referencia`, `mae_p1` … `mae_p5`, `mae_medio`, `mae_sd`, `mejora_media_euros` y `particiones_mejora`. `mejora_media_euros` es la media de `mae_referencia - mae_estrategia` en los cinco folds; `particiones_mejora` cuenta los folds en que esa diferencia es positiva. Se acepta una estrategia solo si `mejora_media_euros >= 1000` y `particiones_mejora >= 4`.

**Fase 1 · Limpieza**

L1 y L2 se describen en R9. La limpieza del objetivo sigue siendo fila a fila, según R1 y las reglas de `limpiar_objetivo()` que se definan antes de esa tarea.

**Fase 2 · Transformaciones**

Las codificaciones categóricas, sus categorías para vacíos y la inferencia de barrio están especificadas en R10–R11.

**Fase 3 · Variables nuevas**

Las fórmulas y los casos de cero o datos ausentes de N1 y N2 están especificados en R12.

**Fase 4 · Modelo y explicación**

Los valores de `alpha`, la selección y la ausencia de estandarización están especificados en R13. La explicación del modelo sigue pendiente de CM5.

**Cuadro de mando**

<!-- Las pantallas de DESIGN.md y qué hace la app si falta algún fichero. -->

## 7. Criterios de aceptación

<!--
Cada criterio (CA5, CA6…) dice qué requisito verifica y cómo se comprueba con una cifra o un hecho
concreto. Cada uno tendrá al menos un test en tests/acceptance/ marcado con
@pytest.mark.criterio("CA…"). scripts/trazabilidad.py lee los CA de esta sección.

Escribid los criterios de cada fase antes de empezarla: el agente escribe sus tests en una tarea propia,
vosotros los revisáis y solo después implementa la fase.

Tres tipos útiles:
- Con un ejemplo pequeño calculado a mano: "CA5 (R9). Con cinco filas inventadas (una vendida normal,
  una retirada…), limpiar_objetivo deja estas tres: …"
- Con los datos reales: "CA6 (R10). Tras corregir la superficie, ninguna vivienda tiene 0 m²."
- Sobre los experimentos: "CA9 (R8). experimentos.csv tiene una fila para cada estrategia de §4."

Lo que no se pueda testear (p. ej. si un gráfico se entiende) indicad cómo se verifica.
-->

**Ejemplo resuelto** (tests en `tests/acceptance/test_ejemplo_resuelto.py`)

- CA1 (R1). Hay 6.237 filas de entrenamiento; cada una está en `1`-`5` o en `validacion`, que tiene entre el 18 % y el 22 % de las filas, y ningún inmueble (`ref_catastral`) aparece en dos particiones.
- CA2 (R2). Con tres ventas de ejemplo (barrio A: 100 m² por 300.000 € y 50 m² por 200.000 €; Badalona: 80 m² por 160.000 €), el baseline tasa un piso de 60 m² en A en 210.000 €, uno de Badalona sin superficie en 160.000 €, uno de 100 m² en un barrio sin ventas en 300.000 € (€/m² global) y uno de A sin superficie en 250.000 €.
- CA3 (R3). La validación cruzada devuelve cinco errores, y cambiar el precio de las filas de `validacion` no los cambia.
- CA4 (R4). Con precios reales 100, 200, 300 y 400 y predicciones 110, 190, 330 y 400, el MAE es 12,5, su intervalo lo contiene y repetir el cálculo da el mismo intervalo.

**Vuestros criterios**

- CA5 (R8). `experimentos.csv` contiene las columnas `estrategia`, `referencia`, `mae_p1` … `mae_p5`, `mae_medio`, `mae_sd`, `mejora_media_euros`, `particiones_mejora` y `aceptada`. Con cada fila que tenga referencia, las mejoras por fold son `mae_p<fold>(referencia) - mae_p<fold>(estrategia)`; `mejora_media_euros` es la media de esas cinco diferencias, `particiones_mejora` cuenta las diferencias positivas y `aceptada` es verdadero exactamente cuando la mejora media es al menos 1.000 € y mejora en 4 o 5 folds. Las referencias nombran una estrategia existente; `baseline` y `modelo_minimo` tienen la referencia vacía.
- CA6 (R9). Con las cuatro filas de entrenamiento de `test_superficies`, L1 transforma `superficie_construida` `[100, 0, 300, 2000]` en `[100, 300, 300, 2000]`: la mediana de los valores no cero es 300 y el extremo 2.000 no cambia. L2 transforma `superficie_util` `[40, NaN, 80, 120]` en `[40, 80, 80, 120]`: la mediana de entrenamiento es 80. Las medianas se ajustan solo al entrenar cada pipeline.

## 8. Fuera de alcance

- Modelos no lineales (árboles, *ensembles*, redes, k vecinos): llegan en las sesiones 14 y 15.
- Usar el test o sus precios públicos para entrenar o para elegir el modelo.

<!-- Añadid lo que no vais a hacer, para que nadie (ni el agente) lo haga. -->

## 9. Preguntas abiertas

<!-- Dudas pendientes de decidir. Cuando se decidan, pasan a "Decisiones". -->

- ¿Qué distancia se usa para decidir cuál centroide de barrio es el más cercano en T6? El documento ya fija cómo calcular los centroides, pero aún no la métrica de distancia.
- Completar y validar los criterios CA5 en adelante para R8–R13 antes de implementar las fases; la sección «Vuestros criterios» sigue vacía.

## 10. Decisiones

<!--
Una línea por decisión: fecha · qué se decide · requisitos afectados · por qué, CON CIFRAS.
Ejemplo:
- 2026-12-01 · Aceptamos T1 (la zona como categoría) · R12 · Baja el MAE medio de N € a M € y mejora en 5 de 5 particiones.
-->
