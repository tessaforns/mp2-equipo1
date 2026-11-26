# TASKS · Tasación de viviendas para Banc Avellaner

> **La lista de tareas, en pasos pequeños.** El agente propone el desglose a partir de SPECS.md; el equipo lo aprueba.
> El agente marca `[x]` y añade la línea `Agente:` cuando los tests pasan. Una persona del equipo completa `Verificado por:`.

<!--
Formato de cada tarea (una tarea = algo que se implementa y verifica en una sola conversación):

- [ ] 1. Qué se hace, en una línea (R…, CA…)

Cuando el agente la termina:

- [x] 1. Qué se hace, en una línea (R…, CA…)
  - Agente: qué hizo y cómo lo comprobó (tests, fila de experimentos.csv).
  - Verificado por: nombre · cómo lo comprobó (diff leído, cifra recalculada a mano, pantalla revisada).
  - Fallos del agente: lo que hizo mal o fuera de SPECS y cómo lo detectasteis (si no hubo, "ninguno").

Pistas:
- Pedid el desglose de una fase cada vez, cuando su parte de SPECS.md esté escrita.
- La primera tarea de cada fase son los tests de sus criterios (CA…). Se revisan antes de implementar nada.
- En los experimentos, una tarea = una fila de SPECS.md §4.
-->

## Ejemplo resuelto

- [x] 0. Carga de datos, baseline, validación cruzada, modelo mínimo, entrenamiento y envío (R1-R7, CA1-CA4)
  - Agente: viene en la plantilla. `uv run pytest`: CA1-CA4, CM2, CM3, CM4 y CM7 en verde; CM1, CM5 y CM6 fallan.
  - Verificado por: profesorado · baseline recalculado a mano en CA2.

> **Flujo de aceptación.** Los tests CA5-CA6 de la fase 1 están redactados y validados. Los criterios de fases posteriores aún deben añadirse a `SPECS.md`; T6 también necesita una decisión sobre la métrica de distancia antes de implementarse.

## Fase 1 · Limpieza (sesión 12)

- [x] 1. Preparar tests de aceptación de las decisiones experimentales y limpieza de superficies (R8-R9, CA5-CA6)
  - Agente: redactó los tests CA5-CA6; `uv run pytest --collect-only -q tests/acceptance/test_criterios_fase1.py` recogió los 3 tests y `uv run python scripts/trazabilidad.py` reconoció todos los criterios. Las comprobaciones de comportamiento quedan para cuando se implementen R8-R9.
  - Verificado por: @tessaforns · validó los ejemplos y resultados esperados de CA5-CA6.
- [ ] 2. Implementar L1: sustituir ceros de `superficie_construida` por la mediana del fold de entrenamiento (R9, CA6)
- [ ] 3. Implementar L2: añadir `superficie_util` con imputación aprendida en cada fold (R9, CA6)

## Fase 2 · Transformaciones (sesión 12)

- [ ] 4. Preparar tests de aceptación para categorías e inferencia geográfica (R10-R11, CA7-CA12)
- [ ] 5. Implementar T1: añadir la zona como categoría (R10, CA7)
- [ ] 6. Implementar T2: añadir parking tratando vacíos como `No` (R10, CA8)
- [ ] 7. Implementar T3: añadir parking conservando vacíos como `Sin dato` (R10, CA9)
- [ ] 8. Implementar T4: añadir estado y conservar vacíos como `Sin dato` (R10, CA10)
- [ ] 9. Implementar T5: normalizar y codificar `tipo` (R10, CA11)
- [ ] 10. Implementar T6: imputar barrio ausente con código postal y centroide (R11, CA12)

## Fase 3 · Variables nuevas (entre sesiones)

- [ ] 11. Preparar tests de aceptación para las variables derivadas y sus casos límite (R12, CA13-CA14)
- [ ] 12. Implementar N1: relación baños / habitaciones y su imputación (R12, CA13)
- [ ] 13. Implementar N2: relación superficie útil / habitaciones y sus imputaciones (R12, CA14)

## Fase 4 · Modelo y explicación (sesión 13)

- [ ] 14. Preparar tests de aceptación para la selección Ridge sin usar `validacion` (R13, CA15)
- [ ] 15. Evaluar M1: Ridge con `alpha = 0,001` frente a la regresión lineal (R13, CA15)
- [ ] 16. Evaluar M2: Ridge con `alpha = 0,01` frente a la regresión lineal (R13, CA15)
- [ ] 17. Evaluar M3: Ridge con `alpha = 0,1` frente a la regresión lineal (R13, CA15)
- [ ] 18. Evaluar M4: Ridge con `alpha = 1` frente a la regresión lineal (R13, CA15)
- [ ] 19. Fijar `MODELO_FINAL` con el `alpha` seleccionado y generar modelo, métricas y envío (R6-R7, R13, CM1-CM5)

## Cuadro de mando (entre sesiones y sesión 13)
