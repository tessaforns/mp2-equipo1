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
| P1 | `estado_operacion` | 620 filas (10 %) son anuncios retirados, que no se vendieron. El test solo tiene ventas | Su precio es lo que se pedía, no lo que se pagó | 1 · Limpieza |
| | | | | |

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

**Regla de decisión** (escrita antes de ejecutar nada): <!-- Cuándo aceptáis una estrategia. Por ejemplo: "si baja el MAE de su referencia en al menos 4 de las 5 particiones y en al menos N € de media". ¿Qué hacéis si no se cumple? -->

Cómo leemos los resultados: `src.experimentos` da el MAE de cada partición (`mae_p1` … `mae_p5`). Comparamos cada estrategia con su referencia partición a partición, porque hay particiones más difíciles que otras para todas las estrategias a la vez.

### Punto de partida (ejemplo resuelto)

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E0 | baseline | €/m² mediano de la zona × superficie construida | — | — | | — | La tasación que hay que batir |
| E1 | minimo | Regresión lineal con `superficie_construida`, `habitaciones`, `banos`, `distancia_centro_km` y `poblacion_zona`, sin transformar | — | _Vuestra hipótesis: ¿mejor o peor que E0? ¿Por qué?_ | | — | |

### Fase 1 · Limpieza

<!--
La limpieza del precio va en limpiar_objetivo() (AGENTS.md §3): decide fila a fila y se aplica antes de
separar las particiones. No es una estrategia, porque cambia las filas con las que se mide todo: cuando
la cambiéis, volved a ejecutar E0 y E1 y anotad sus cifras nuevas aquí.
El resto de la limpieza (por ejemplo, la superficie) sí son estrategias, dentro del Pipeline.
-->

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | estrategia | Modelo mínimo con la superficie corregida | E1 | Mejora: las superficies de 1.500 m² inflan la tasación | | | |
| | | | | | | | |

### Fase 2 · Transformaciones

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | estrategia | Añade la zona como categoría | L1 | Mejora mucho: en Pedralbes el m² vale el triple que en Nou Barris | | | |
| | | | | | | | |

### Fase 3 · Variables nuevas

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | caracteristica | Añade la relación baños / habitaciones | Última aceptada | _Vuestra hipótesis_ | | | |
| | | | | | | | |

### Fase 4 · Modelo

<!--
Las mismas variables que la última estrategia aceptada en la fase 3; solo cambia el estimador.
Una fila por valor de λ. Escribid antes cómo elegiréis λ y qué haréis si ningún Ridge mejora a la regresión lineal.
-->

| Id | Tipo | Qué cambia | Referencia | Hipótesis | MAE medio ± sd | Mejora media · particiones | Conclusión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | estrategia | Ridge con λ = 0,01 | Última aceptada | Igual que la regresión lineal: λ muy pequeño | | | |
| | | | | | | | |

## 5. Salidas

<!--
Las del contrato (AGENTS.md §3) y las que añadáis vosotros (por ejemplo, tablas extra para el cuadro de mando).
-->

| Fichero | Qué contiene | Lo escribe |
| --- | --- | --- |
| `reports/experimentos.csv` | Una fila por estrategia con su MAE por partición | `src.experimentos` |
| `models/modelo.joblib` | El modelo final entrenado con las particiones 1-5 | `src.entrenar` |
| `reports/metricas.json` | MAE y RMSE del baseline y del modelo en `validacion`, con IC 95 % | `src.entrenar` |
| `reports/predicciones_validacion.csv` | Precio real, predicción del modelo y del baseline de cada vivienda de `validacion` | `src.entrenar` |
| `entregables/envio_kaggle.csv` | Predicción de cada vivienda del test | `src.predecir` |

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

**Cómo decidimos**

<!-- La regla de decisión de §4 y las columnas que necesitáis en experimentos.csv para aplicarla (referencia, mejora media, particiones en las que mejora…). -->

**Fase 1 · Limpieza**

<!-- Qué hace limpiar_objetivo() con cada fila (qué quita, qué corrige) y cómo se corrigen los demás valores erróneos. -->

**Fase 2 · Transformaciones**

<!-- Para cada variable: cómo se convierte, cómo se rellenan sus vacíos y qué pasa con un valor que no aparece en el entrenamiento. -->

**Fase 3 · Variables nuevas**

<!-- La fórmula de cada variable nueva, con qué hacer si le falta un dato. -->

**Fase 4 · Modelo y explicación**

<!-- Qué valores de λ probáis, cómo elegís el modelo final y qué devuelve explicar() (CM5). -->

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

## 8. Fuera de alcance

- Modelos no lineales (árboles, *ensembles*, redes, k vecinos): llegan en las sesiones 14 y 15.
- Usar el test o sus precios públicos para entrenar o para elegir el modelo.

<!-- Añadid lo que no vais a hacer, para que nadie (ni el agente) lo haga. -->

## 9. Preguntas abiertas

<!-- Dudas pendientes de decidir. Cuando se decidan, pasan a "Decisiones". -->

## 10. Decisiones

<!--
Una línea por decisión: fecha · qué se decide · requisitos afectados · por qué, CON CIFRAS.
Ejemplo:
- 2026-12-01 · Aceptamos T1 (la zona como categoría) · R12 · Baja el MAE medio de N € a M € y mejora en 5 de 5 particiones.
-->
