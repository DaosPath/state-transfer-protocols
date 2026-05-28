# Resultados EXP04_TRI

## Configuración

- Experimento: `EXP04_TRI`
- Nombre corto: `EXP04_TRI_Hybrid_Min_vs_Compressed_State`
- Modelo generador: `deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: 0.2
- Repeticiones: 3
- Filas esperadas FULL: 1350
- Filas generadas FULL: 1350
- Llamadas HTTP: 2810
- Errores HTTP contabilizados: 0
- Parse errors: 0
- Missing tokens: 0
- Fallos de formato: 7
- Soft stop: False
- Backup JSONL previo: no_aplica
- Batch final decode ejecutado: True

## Conexión

```json
{
  "timestamp": "2026-05-14T01:19:39.483416+00:00",
  "models_ok": true,
  "chat_ok": true,
  "models_count": 15,
  "error": null,
  "chat_model": "deepseek-v4-flash",
  "chat_latency_ms": 2054,
  "chat_response": "OK_EXP04_TRI_TEST",
  "usage": {
    "input_tokens": 15,
    "output_tokens": 7,
    "total_tokens": 22
  }
}
```

## Piloto

```json
{
  "rows": 45,
  "errors": 0,
  "parse_errors": 0,
  "missing_tokens": 0,
  "format_invalid": 0,
  "deprecated_term": 0,
  "ok": true
}
```

## Tabla global

| language | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | operational_continuity | context_recoverability | handoff_quality | compactness |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ES | natural | 90 | 0 | 166.13 | 325.84 | 491.98 | 4.83 | 4.89 | 4.83 | 1.14 | 1.17 | 4.71 | 4.82 | 4.73 | 4.82 | 3.98 |
| ES | compressed | 90 | 0 | 216.13 | 87.27 | 303.40 | 4.99 | 4.99 | 4.97 | 1.03 | 1.16 | 4.76 | 4.97 | 4.76 | 4.94 | 5.00 |
| ES | compressed_state | 90 | 0 | 214.13 | 78.57 | 292.70 | 4.67 | 4.64 | 4.61 | 1.34 | 1.48 | 4.57 | 4.61 | 4.28 | 4.56 | 4.97 |
| ES | hybrid_min | 90 | 0 | 197.13 | 61.88 | 259.01 | 4.81 | 4.66 | 4.79 | 1.32 | 1.47 | 4.44 | 4.79 | 4.19 | 4.73 | 4.98 |
| ES | hybrid_state | 90 | 0 | 192.13 | 132.72 | 324.86 | 4.86 | 4.90 | 4.87 | 1.14 | 1.16 | 4.86 | 4.86 | 4.69 | 4.86 | 4.92 |
| EN | natural | 90 | 0 | 145.53 | 208.57 | 354.10 | 4.96 | 4.99 | 4.97 | 1.02 | 1.04 | 4.91 | 4.96 | 4.94 | 4.98 | 4.12 |
| EN | compressed | 90 | 0 | 176.53 | 66.89 | 243.42 | 4.90 | 4.94 | 4.86 | 1.08 | 1.30 | 4.58 | 4.83 | 4.58 | 4.82 | 4.98 |
| EN | compressed_state | 90 | 0 | 178.53 | 65.11 | 243.64 | 4.64 | 4.66 | 4.56 | 1.38 | 1.51 | 4.48 | 4.54 | 4.23 | 4.51 | 4.89 |
| EN | hybrid_min | 90 | 0 | 169.53 | 45.71 | 215.24 | 4.79 | 4.60 | 4.72 | 1.34 | 1.42 | 4.48 | 4.72 | 4.21 | 4.64 | 4.98 |
| EN | hybrid_state | 90 | 0 | 169.53 | 107.28 | 276.81 | 4.93 | 4.98 | 4.90 | 1.12 | 1.23 | 4.91 | 4.90 | 4.74 | 4.92 | 4.97 |
| ZH | natural | 90 | 0 | 144.10 | 168.48 | 312.58 | 4.83 | 4.89 | 4.82 | 1.14 | 1.17 | 4.76 | 4.83 | 4.78 | 4.83 | 4.50 |
| ZH | compressed | 90 | 0 | 171.10 | 61.94 | 233.04 | 4.97 | 4.97 | 4.93 | 1.06 | 1.17 | 4.71 | 4.93 | 4.71 | 4.91 | 5.00 |
| ZH | compressed_state | 90 | 0 | 181.10 | 62.91 | 244.01 | 4.60 | 4.31 | 4.59 | 1.70 | 1.71 | 4.33 | 4.58 | 4.08 | 4.50 | 4.93 |
| ZH | hybrid_min | 90 | 0 | 166.10 | 50.73 | 216.83 | 4.46 | 4.17 | 4.40 | 1.68 | 1.87 | 4.10 | 4.36 | 3.81 | 4.34 | 4.92 |
| ZH | hybrid_state | 90 | 0 | 175.10 | 86.90 | 262.00 | 4.82 | 4.83 | 4.81 | 1.18 | 1.37 | 4.76 | 4.82 | 4.62 | 4.79 | 4.97 |

## Ganadores por idioma

| language | cheapest_mode | best_quality_mode | best_state_mode | best_continuity_mode | best_handoff_mode | best_balance_mode | reading |
|---|---|---|---|---|---|---|---|
| ES | hybrid_min | compressed | hybrid_state | compressed | compressed | compressed | hybrid_min gana costo |
| EN | hybrid_min | natural | natural | natural | natural | hybrid_state | hybrid_min gana costo |
| ZH | hybrid_min | compressed | natural | compressed | compressed | compressed | hybrid_min gana costo |

## Ganadores por grupo de tarea

| language | task_group | cheapest_mode | best_state_mode | best_continuity_mode | best_balance_mode | observation |
|---|---|---|---|---|---|---|
| ES | base_comparable | hybrid_min | natural | natural | compressed | grupo_EXP04 |
| ES | memory_state | hybrid_min | hybrid_state | compressed | compressed | grupo_EXP04 |
| ES | multiagent_continuation | hybrid_min | hybrid_state | compressed | compressed | grupo_EXP04 |
| EN | base_comparable | hybrid_min | natural | natural | compressed | grupo_EXP04 |
| EN | memory_state | hybrid_min | natural | hybrid_state | hybrid_state | grupo_EXP04 |
| EN | multiagent_continuation | hybrid_min | hybrid_state | natural | compressed | grupo_EXP04 |
| ZH | base_comparable | hybrid_min | natural | natural | compressed | grupo_EXP04 |
| ZH | memory_state | hybrid_min | compressed | compressed | compressed | grupo_EXP04 |
| ZH | multiagent_continuation | hybrid_min | natural | natural | compressed | grupo_EXP04 |

## Comparación con EXP03

| language | exp03_compressed | exp04_compressed | exp03_hybrid | exp04_hybrid_min | exp04_compressed_state | token_change_hybrid | reading |
|---|---:|---:|---:|---:|---:|---:|---|
| ES | 233.89 | 303.40 | 266.78 | 259.01 | 292.70 | -7.77 | hybrid_min_baja_vs_EXP03 |
| EN | 188.98 | 243.42 | 199.81 | 215.24 | 243.64 | 15.43 | hybrid_min_no_baja_vs_EXP03 |
| ZH | 194.86 | 233.04 | 211.36 | 216.83 | 244.01 | 5.47 | hybrid_min_no_baja_vs_EXP03 |

## Criterio de éxito

| language | mode | tokens_vs_compressed | state_delta_vs_compressed | continuity_delta_vs_compressed | success_level | reading |
|---|---|---:|---:|---:|---|---|
| ES | compressed | 0.00% | 0.00 | 0.00 | weak | criterio_EXP04 |
| ES | compressed_state | -3.53% | -0.19 | -0.36 | weak | criterio_EXP04 |
| ES | hybrid_min | -14.63% | -0.31 | -0.18 | weak | criterio_EXP04 |
| ES | hybrid_state | 7.07% | 0.10 | -0.11 | weak | criterio_EXP04 |
| EN | compressed | 0.00% | 0.00 | 0.00 | weak | criterio_EXP04 |
| EN | compressed_state | 0.09% | -0.10 | -0.29 | weak | criterio_EXP04 |
| EN | hybrid_min | -11.58% | -0.10 | -0.11 | weak | criterio_EXP04 |
| EN | hybrid_state | 13.72% | 0.33 | 0.07 | weak | criterio_EXP04 |
| ZH | compressed | 0.00% | 0.00 | 0.00 | weak | criterio_EXP04 |
| ZH | compressed_state | 4.71% | -0.38 | -0.36 | weak | criterio_EXP04 |
| ZH | hybrid_min | -6.96% | -0.61 | -0.58 | weak | criterio_EXP04 |
| ZH | hybrid_state | 12.42% | 0.04 | -0.11 | weak | criterio_EXP04 |

## Input/output tokens

| language | mode | avg_input_tokens | avg_output_tokens | input_share | output_share | reading |
|---|---|---:|---:|---:|---:|---|
| ES | natural | 166.13 | 325.84 | 33.77% | 66.23% | output_domina |
| ES | compressed | 216.13 | 87.27 | 71.24% | 28.76% | input_domina |
| ES | compressed_state | 214.13 | 78.57 | 73.16% | 26.84% | input_domina |
| ES | hybrid_min | 197.13 | 61.88 | 76.11% | 23.89% | input_domina |
| ES | hybrid_state | 192.13 | 132.72 | 59.14% | 40.86% | input_domina |
| EN | natural | 145.53 | 208.57 | 41.10% | 58.90% | output_domina |
| EN | compressed | 176.53 | 66.89 | 72.52% | 27.48% | input_domina |
| EN | compressed_state | 178.53 | 65.11 | 73.28% | 26.72% | input_domina |
| EN | hybrid_min | 169.53 | 45.71 | 78.76% | 21.24% | input_domina |
| EN | hybrid_state | 169.53 | 107.28 | 61.25% | 38.75% | input_domina |
| ZH | natural | 144.10 | 168.48 | 46.10% | 53.90% | balanceado |
| ZH | compressed | 171.10 | 61.94 | 73.42% | 26.58% | input_domina |
| ZH | compressed_state | 181.10 | 62.91 | 74.22% | 25.78% | input_domina |
| ZH | hybrid_min | 166.10 | 50.73 | 76.60% | 23.40% | input_domina |
| ZH | hybrid_state | 175.10 | 86.90 | 66.83% | 33.17% | input_domina |

## Tabla por idioma

| language | natural | compressed | compressed_state | hybrid_min | hybrid_state | best_token | best_state | best_balance |
|---|---:|---:|---:|---:|---:|---|---|---|
| ES | 491.98 | 303.40 | 292.70 | 259.01 | 324.86 | hybrid_min | hybrid_state | compressed |
| EN | 354.10 | 243.42 | 243.64 | 215.24 | 276.81 | hybrid_min | natural | hybrid_state |
| ZH | 312.58 | 233.04 | 244.01 | 216.83 | 262.00 | hybrid_min | natural | compressed |

## Errores y anomalías

- format:hybrid_min_too_many_fields: 2
- format:empty_field: 2
- format:compressed_too_field_dominant: 1
- format:compressed_state_too_many_fields: 1
- format:hybrid_state_zh_too_long: 1

### Ejemplos
- EN T001 hybrid_min_en: notes=['hybrid_min_too_many_fields']
- ZH T003 hybrid_state_zh: notes=['empty_field']
- EN T006 hybrid_min_en: notes=['hybrid_min_too_many_fields']
- ES T008 compressed_es: notes=['compressed_too_field_dominant']
- EN T008 compressed_state_en: notes=['compressed_state_too_many_fields']
- EN T008 hybrid_state_en: notes=['empty_field']
- ZH T030 hybrid_state_zh: notes=['hybrid_state_zh_too_long']
