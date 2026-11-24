# DESIGN · Cuadro de mando de validación del modelo

> **Cómo se ve y cómo se comporta.** Lo escribe el equipo; el agente lo lee pero no lo edita.
> Las indicaciones entre `<!-- -->` son de la plantilla: borradlas cuando escribáis cada sección.

## 1. Para quién

<!--
Núria Casals, directora de riesgos, y quizá un auditor. ¿Qué saben de estadística? ¿Cuánto tiempo
le dedicarán? Todo lo que viene después depende de esta respuesta.
-->

## 2. Formatos

<!-- Cómo se escribe cada cifra en pantalla. Pensad en un lector español no técnico. -->

| Qué | Formato | Ejemplo |
| --- | --- | --- |
| Precios y errores en euros | | |
| Errores en porcentaje | | |
| Intervalos de confianza | | |
| Coeficientes | | |
| Sin dato | | |

## 3. Estilo de los gráficos

<!--
Plotly Express con plantilla simple_white. Colores del curso: azul #2a78d6 (principal),
naranja #eb6834 (contraste), gris #898781 (neutro). ¿Qué color es siempre "modelo" y cuál "baseline"?
Pista: un buen título dice la conclusión, no el tema ("El modelo falla más en las casas caras",
no "Error por rango de precio").
-->

## 4. Pantallas

<!--
Mínimo, las cuatro del enunciado. Para cada una: qué pregunta responde (SPECS §2) y qué hay
de arriba abajo. La plantilla ya trae el esqueleto en src/app.py con estas cuatro pantallas.
-->

| Pantalla | Pregunta | Contenido, de arriba abajo |
| --- | --- | --- |
| Experimentos | | |
| Rendimiento | | |
| Dónde falla | | |
| Abrir la caja | | |

## 5. El mapa de residuos

<!-- Qué representa cada punto, el color (¿tasación por encima o por debajo?), el tamaño, qué se ve al pasar el ratón. -->

## 6. Abrir la caja

<!--
- Coeficientes: ¿cómo los hacéis comparables entre sí? ¿Mostráis todos o los N más grandes?
- Desglose de una vivienda: ¿cómo se elige la vivienda? ¿Cómo se lee una contribución si el precio
  está en logaritmo (un factor multiplicativo, ×1,12, en lugar de +X €)?
- ¿Dónde y cómo avisáis de que un coeficiente no es un efecto causal?
-->

## 7. Filtros e interacción

<!-- Qué filtros hay, sus valores por defecto y a qué afectan. -->

## 8. Casos límite

<!-- Qué ve el usuario si falta reports/ o models/, si un filtro no deja viviendas, etc. Nunca un error. -->
