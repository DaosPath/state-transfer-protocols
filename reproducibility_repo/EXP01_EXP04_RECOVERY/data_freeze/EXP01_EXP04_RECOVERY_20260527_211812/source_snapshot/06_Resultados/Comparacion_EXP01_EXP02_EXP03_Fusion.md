# Comparacion EXP01 vs EXP02 vs EXP03 Fusion

## Evolucion de tokens

| Modo | EXP01 tokens | EXP02 tokens | EXP03 tokens | Cambio vs EXP02 | Fidelidad EXP03 | Lectura |
|---|---:|---:|---:|---:|---:|---|
| natural | 364.30 | 354.63 | 324.54 | -30.09 | 4.84 | bajo tokens y mantuvo calidad alta |
| caveman | 263.97 | 240.93 | 233.89 | -7.04 | 4.14 | siguio siendo el modo base mas barato |
| proto_v1 | 377.13 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia pesada |
| proto_v2 | NO_CALCULABLE | 318.43 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia intermedia |
| proto_v3_min | NO_CALCULABLE | NO_CALCULABLE | 370.87 | NO_CALCULABLE | 3.69 | peor que proto_v2 en tokens y calidad |
| proto_v3_state | NO_CALCULABLE | NO_CALCULABLE | 377.23 | NO_CALCULABLE | 3.79 | no justifico el costo de estado |
| proto_v3_hybrid | NO_CALCULABLE | NO_CALCULABLE | 266.78 | NO_CALCULABLE | 4.46 | mejor variante proto; cerca de caveman |
| proto_v1_translated | 438.87 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia traducida pesada |
| proto_v2_translated | NO_CALCULABLE | 332.70 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia traducida |
| proto_v3_min_translated | NO_CALCULABLE | NO_CALCULABLE | 224.83 | NO_CALCULABLE | 2.63 | llamada traducida barata pero baja calidad; no incluye costo proto previo |
| proto_v3_state_translated | NO_CALCULABLE | NO_CALCULABLE | 253.03 | NO_CALCULABLE | 3.10 | baja calidad; no incluye costo proto previo |
| proto_v3_hybrid_translated | NO_CALCULABLE | NO_CALCULABLE | 248.91 | NO_CALCULABLE | 3.72 | mejora claridad frente a min/state, pero baja fidelidad frente al proto fuente |

## Evolucion de fidelidad

- natural EXP03: 4.84.
- caveman EXP03: 4.14.
- proto_v3_min EXP03: 3.69.
- proto_v3_state EXP03: 3.79.
- proto_v3_hybrid EXP03: 4.46.

## Evolucion de utilidad

- caveman EXP02 utilidad: 4.60.
- proto_v2 utilidad: 3.53.
- proto_v3_min utilidad: 3.19.
- proto_v3_state utilidad: 3.17.
- proto_v3_hybrid utilidad: 4.47.

## Evolucion de ambiguedad

- proto_v2 ambiguedad: 2.37.
- proto_v3_min: 2.21.
- proto_v3_state: 2.47.
- proto_v3_hybrid: 1.52.

## Evolucion de perdida de informacion

- proto_v2 perdida de informacion: 2.27.
- proto_v3_min: 2.19.
- proto_v3_state: 2.30.
- proto_v3_hybrid: 1.60.

## Evolucion de traducibilidad

- proto_v3_min: 3.42.
- proto_v3_state: 3.37.
- proto_v3_hybrid: 4.80.

## Que cambio en cada version

- Proto v1: estructura clara pero pesada.
- Proto v2: etiquetas cortas, pero campos aun demasiado obligatorios.
- Proto v3 min/state: campos opcionales, pero compresion demasiado criptica.
- Proto v3 hybrid: mezcla caveman + marcadores; mejor equilibrio experimental.

## Lectura experimental

El simbolismo puro no mejoro la eficiencia. La mezcla hibrida si produjo una mejora real frente a Proto v2, aunque caveman siguio siendo el baseline base mas barato.

## Recomendacion

C. Hybrid_Min
