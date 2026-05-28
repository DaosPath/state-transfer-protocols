# Resumen Ejecutivo EXP04_TRI

## Estado

- Piloto OK: True
- FULL ejecutado: sí
- Batch final decode ejecutado: True
- Filas generadas: 1350
- Llamadas HTTP: 2810
- Errores HTTP: 0

## Ganadores

| language | cheapest_mode | best_quality_mode | best_state_mode | best_continuity_mode | best_handoff_mode | best_balance_mode | reading |
|---|---|---|---|---|---|---|---|
| ES | hybrid_min | compressed | hybrid_state | compressed | compressed | compressed | hybrid_min gana costo |
| EN | hybrid_min | natural | natural | natural | natural | hybrid_state | hybrid_min gana costo |
| ZH | hybrid_min | compressed | natural | compressed | compressed | compressed | hybrid_min gana costo |

## Lectura principal

- ES: compressed=303.40; compressed_state=292.70; hybrid_min=259.01; hybrid_state=324.86.
- EN: compressed=243.42; compressed_state=243.64; hybrid_min=215.24; hybrid_state=276.81.
- ZH: compressed=233.04; compressed_state=244.01; hybrid_min=216.83; hybrid_state=262.00.

## Recomendación siguiente

Usar compressed para tareas simples y hybrid_state para handoff/memoria. Mantener hybrid_min como candidato de costo para EXP05, porque fue el modo más barato en ES/EN/ZH pero perdió estado y calidad frente a compressed/hybrid_state.

Datos antes que entusiasmo.
