# Datos · Viviendas de Barcelona y su área metropolitana

**Qué es real y qué es simulado.** Los barrios, sus límites y sus indicadores (viviendas, población, superficie media, años de construcción, valor catastral y renta) son reales: Open Data BCN y CartoBCN, Ajuntament de Barcelona, CC-BY 4.0. El nivel de precios de cada municipio del área metropolitana se basa en precios de oferta publicados. **Cada vivienda, cada venta y cada precio son simulados**: las cifras no describen ventas reales, aunque se parecen al mercado de 2023-2025.

**Direcciones.** Las direcciones y sus códigos postales son reales (Institut Cartogràfic i Geològic de Catalunya, «Adreces simplificat», CC BY 4.0). A cada finca simulada se le ha dado la dirección real más cercana a sus coordenadas. Que una dirección aparezca aquí **no** significa que en ese edificio se haya vendido nada.

Se descargan con `uv run python scripts/descargar_datos.py`.

## Ficheros

| Fichero | Filas | Una fila es |
| --- | --- | --- |
| `train_set.csv` | 6.237 | Una operación con su precio: una venta o un anuncio retirado |
| `test_set.csv` | 4.002 | Una venta, sin precio. Es lo que se predice para Kaggle |
| `sampleSubmission.csv` | 4.002 | Ejemplo del formato de envío a Kaggle (`index`, `precio`); el precio no significa nada |
| `particiones.csv` | 6.237 | La partición de cada fila del entrenamiento: `1` a `5` (validación cruzada) o `validacion` |

La columna `index` identifica cada fila y une `train_set.csv` con `particiones.csv`, y `test_set.csv` con el envío.

## Columnas

| Columna | Qué es |
| --- | --- |
| `fecha_venta` | Fecha de la operación, en formato día/mes/año |
| `municipi` | Municipio: Barcelona u otro del área metropolitana |
| `districte`, `barri` | Distrito y barrio, solo en Barcelona |
| `direccion` | Calle y número de la finca, como aparece en el anuncio |
| `codigo_postal` | Código postal de la finca |
| `latitud`, `longitud` | Coordenadas de la finca |
| `distancia_centro_km` | Distancia a la plaza de Catalunya, en km |
| `ref_catastral` | Referencia catastral del inmueble (simulada): identifica la vivienda |
| `tipo` | Piso, ático, dúplex, estudio o casa |
| `superficie_construida` | Superficie construida según el catastro, en m² |
| `superficie_util` | Superficie útil según el anuncio, en m² |
| `habitaciones` | Dormitorios (un estudio tiene 0) |
| `banos` | Baños |
| `planta` | Planta, como aparece en el anuncio |
| `ascensor` | Si la finca tiene ascensor |
| `terraza_m2` | Superficie de terraza en m²; 0 si no tiene |
| `parking` | Plaza de aparcamiento |
| `any_construccio` | Año de construcción de la finca |
| `estado` | A reformar, buen estado, reformado u obra nueva |
| `certificado_energetico` | Calificación energética, de A a G |
| `agencia` | Agencia que gestionó la operación (código) o `Particular` |
| `poblacion_zona` | Habitantes del barrio (en Barcelona) o del municipio |
| `dias_en_venta` | Días entre la publicación del anuncio y el cierre de la operación |
| `estado_operacion` | Solo en el entrenamiento: `vendida` o `retirada` (el anuncio se retiró sin vender) |
| `precio` | Solo en el entrenamiento: precio de la operación, en euros. **Variable objetivo** |

Esta tabla describe lo que *debería* haber en cada columna. Lo que hay de verdad, con sus nulos, sus ceros y sus valores raros, lo descubrís vosotros.
