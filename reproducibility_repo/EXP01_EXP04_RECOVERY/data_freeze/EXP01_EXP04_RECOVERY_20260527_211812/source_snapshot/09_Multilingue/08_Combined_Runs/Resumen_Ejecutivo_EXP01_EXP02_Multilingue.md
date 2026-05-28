# Resumen Ejecutivo EXP01 EXP02 Multilingue

## Estado

- FULL ejecutado: si
- Filas generadas: 480
- Llamadas HTTP: 994

## Ganadores

| language | experiment | cheapest_mode | best_quality_mode | best_state_mode | best_balance_mode | reading |
|---|---|---|---|---|---|---|
| EN | EXP01 | compressed_en | proto_v1_en | natural_en | compressed_en | compressed_wins_tokens |
| EN | EXP02 | compressed_en | natural_en | natural_en | compressed_en | compressed_wins_tokens |
| ZH | EXP01 | compressed_zh | proto_v1_core_zh | proto_v1_core_zh | compressed_zh | compressed_wins_tokens |
| ZH | EXP02 | compressed_zh | natural_zh | proto_v2_core_zh | compressed_zh | compressed_wins_tokens |

## Lectura principal

- EN EXP01: mas barato `compressed_en`, mejor calidad `proto_v1_en`, mejor estado `natural_en`.
- EN EXP02: mas barato `compressed_en`, mejor calidad `natural_en`, mejor estado `natural_en`.
- ZH EXP01: mas barato `compressed_zh`, mejor calidad `proto_v1_core_zh`, mejor estado `proto_v1_core_zh`.
- ZH EXP02: mas barato `compressed_zh`, mejor calidad `natural_zh`, mejor estado `proto_v2_core_zh`.

## Riesgos metodologicos

- Evaluador automatico puede favorecer idioma o estilo.
- Traduccion de tareas puede alterar dificultad.
- Tokenizer puede afectar EN/ZH de forma distinta.
- Separar input_tokens y output_tokens antes de concluir.

## Recomendacion

Ejecutar EXP03_EN/ZH solo si no hay fallo grave de formato o evaluacion en EXP01/EXP02.