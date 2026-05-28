# Resultados EXP03 ZH

## Configuración

- Experimento: `EXP03_ZH`
- Perfil: `EXP03_ZH_FULL_SEPARATE`
- Endpoint: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo generador: `deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: 0.2
- Repeticiones: 3
- Filas esperadas: 900
- Filas generadas: 900
- Llamadas HTTP: 1842
- Errores HTTP contabilizados: 0
- Parse errors: 0
- Missing tokens: 0
- Fallos de formato: 125
- Soft stop: False
- Backup JSONL previo: no_aplica

## Conexión

```json
{
  "timestamp": "2026-05-13T20:20:58.495396+00:00",
  "language": "ZH",
  "models_ok": true,
  "models_count": 15,
  "chat_ok": true,
  "chat_response": "OK_EXP03_LANGUAGE_TEST",
  "chat_model": "deepseek-v4-flash",
  "chat_latency_ms": 1635,
  "usage": {
    "input_tokens": 14,
    "output_tokens": 7,
    "total_tokens": 21,
    "token_count_method": null
  },
  "error": null
}
```

## Piloto

```json
{
  "language": "ZH",
  "rows": 20,
  "expected_rows": 20,
  "errors": 0,
  "parse_errors": 0,
  "missing_tokens": 0,
  "format_invalid": 3,
  "format_invalid_base": 0,
  "zh_caricature": 0,
  "stopped": false,
  "ok": true
}
```

## Tabla global

| language | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | completeness | utility | ambiguity | info_loss | translation_ease | state_preservation | compactness |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ZH | natural_zh | 90 | 0 | 79.10 | 116.44 | 195.54 | 4.93 | 4.97 | 4.71 | 4.91 | 1.04 | 1.10 | 4.99 | 4.91 | 4.18 |
| ZH | compressed_zh | 90 | 0 | 126.10 | 68.76 | 194.86 | 4.86 | 4.89 | 4.53 | 4.84 | 1.11 | 1.20 | 4.94 | 4.83 | 4.98 |
| ZH | proto_v3_min_core_zh | 90 | 0 | 242.10 | 60.47 | 302.57 | 4.47 | 4.34 | 4.20 | 4.48 | 1.61 | 1.59 | 4.57 | 4.53 | 4.98 |
| ZH | proto_v3_state_core_zh | 90 | 0 | 189.10 | 73.00 | 262.10 | 4.58 | 4.61 | 4.24 | 4.57 | 1.39 | 1.46 | 4.79 | 4.63 | 5.00 |
| ZH | proto_v3_hybrid_zh | 90 | 0 | 153.10 | 58.26 | 211.36 | 4.59 | 4.69 | 3.94 | 4.58 | 1.32 | 1.49 | 4.82 | 4.56 | 5.00 |
| ZH | proto_v3_zh_native | 90 | 0 | 219.10 | 43.60 | 262.70 | 4.20 | 3.88 | 3.58 | 4.04 | 1.99 | 2.04 | 4.20 | 4.10 | 5.00 |
| ZH | proto_v3_min_translated_zh | 90 | 0 | 141.47 | 65.63 | 207.10 | 4.30 | 4.27 | 3.64 | 4.17 | 1.71 | 1.84 | 4.79 | 4.13 | 4.98 |
| ZH | proto_v3_state_translated_zh | 90 | 0 | 154.00 | 74.54 | 228.54 | 4.40 | 4.48 | 3.90 | 4.41 | 1.50 | 1.63 | 4.79 | 4.34 | 4.92 |
| ZH | proto_v3_hybrid_translated_zh | 90 | 0 | 139.26 | 60.88 | 200.13 | 4.48 | 4.56 | 3.78 | 4.46 | 1.43 | 1.61 | 4.86 | 4.43 | 4.99 |
| ZH | proto_v3_zh_native_translated | 90 | 0 | 124.60 | 46.46 | 171.06 | 4.31 | 4.38 | 3.50 | 4.22 | 1.62 | 1.84 | 4.83 | 4.22 | 4.97 |

## Tabla por grupo de tarea

| language | task_group | best_tokens | best_quality | best_state | best_balance | observation |
|---|---|---|---|---|---|---|
| ZH | base_comparable | natural_zh | natural_zh | natural_zh | compressed_zh | calculo_solo_modos_base |
| ZH | memory_state | compressed_zh | natural_zh | natural_zh | compressed_zh | calculo_solo_modos_base |
| ZH | medium_complexity | compressed_zh | natural_zh | natural_zh | compressed_zh | calculo_solo_modos_base |

## Variantes proto

| language | proto_variant | avg_total_tokens | avg_output_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ZH | proto_v3_min_core_zh | 302.57 | 60.47 | 4.47 | 4.34 | 4.48 | 1.61 | 1.59 | 4.53 | not_stronger_than_compressed |
| ZH | proto_v3_state_core_zh | 262.10 | 73.00 | 4.58 | 4.61 | 4.57 | 1.39 | 1.46 | 4.63 | not_stronger_than_compressed |
| ZH | proto_v3_hybrid_zh | 211.36 | 58.26 | 4.59 | 4.69 | 4.58 | 1.32 | 1.49 | 4.56 | promising |
| ZH | proto_v3_zh_native | 262.70 | 43.60 | 4.20 | 3.88 | 4.04 | 1.99 | 2.04 | 4.10 | not_stronger_than_compressed |

## Traducciones

La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.

| language | proto_mode | proto_tokens | translated_tokens | architectural_total | clarity_proto | clarity_translated | fidelity_proto | fidelity_translated | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| ZH | proto_v3_min_core_zh | 302.57 | 207.10 | 509.67 | 4.34 | 4.27 | 4.47 | 4.30 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_state_core_zh | 262.10 | 228.54 | 490.64 | 4.61 | 4.48 | 4.58 | 4.40 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_hybrid_zh | 211.36 | 200.13 | 411.49 | 4.69 | 4.56 | 4.59 | 4.48 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_zh_native | 262.70 | 171.06 | 433.76 | 3.88 | 4.38 | 4.20 | 4.31 | extra_call;destroys_saving_vs_compressed |

## Ganadores

- Modo base más barato: `compressed_zh`
- Mejor calidad base: `natural_zh`
- Mejor manejo de estado base: `natural_zh`
- Mejor variante proto base: `proto_v3_hybrid_zh`

## Lectura

- `compressed_zh` reduce tokens frente a `natural_zh`.
- `proto_v3_min_core_zh` no supera el criterio fuerte contra `compressed_zh`.
- `proto_v3_state_core_zh` no supera el criterio fuerte contra `compressed_zh`.
- `proto_v3_hybrid_zh` no supera el criterio fuerte contra `compressed_zh`.
- `proto_v3_zh_native` mejora tokens frente al core mínimo chino.

## Errores y anomalías

- format:translation_still_looks_like_proto: 69
- format:too_many_fields_for_min: 44
- format:missing_state_field: 5
- format:too_many_fields_for_state: 4
- format:hybrid_zh_missing_markers: 2
- format:compressed_zh_too_long: 1

### Ejemplos
- T001 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T002 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T002 proto_v3_state_core_zh: format_notes=['too_many_fields_for_state']
- T002 proto_v3_state_translated_zh: format_notes=['translation_still_looks_like_proto']
- T003 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T003 proto_v3_state_core_zh: format_notes=['too_many_fields_for_state']
- T003 proto_v3_min_translated_zh: format_notes=['translation_still_looks_like_proto']
- T003 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T003 proto_v3_min_translated_zh: format_notes=['translation_still_looks_like_proto']
- T004 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T004 proto_v3_min_core_zh: format_notes=['too_many_fields_for_min']
- T004 proto_v3_min_translated_zh: format_notes=['translation_still_looks_like_proto']
