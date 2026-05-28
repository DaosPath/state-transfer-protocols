# Resultados EXP03 EN

## Configuración

- Experimento: `EXP03_EN`
- Perfil: `EXP03_EN_FULL_SEPARATE`
- Endpoint: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo generador: `deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: 0.2
- Repeticiones: 3
- Filas esperadas: 720
- Filas generadas: 720
- Llamadas HTTP: 1474
- Errores HTTP contabilizados: 0
- Parse errors: 0
- Missing tokens: 0
- Fallos de formato: 70
- Soft stop: False
- Backup JSONL previo: no_aplica

## Conexión

```json
{
  "timestamp": "2026-05-13T17:54:16.670648+00:00",
  "language": "EN",
  "models_ok": true,
  "models_count": 15,
  "chat_ok": true,
  "chat_response": "OK_EXP03_LANGUAGE_TEST",
  "chat_model": "deepseek-v4-flash",
  "chat_latency_ms": 2234,
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
  "language": "EN",
  "rows": 16,
  "expected_rows": 16,
  "errors": 0,
  "parse_errors": 0,
  "missing_tokens": 0,
  "format_invalid": 1,
  "format_invalid_base": 0,
  "zh_caricature": 0,
  "stopped": false,
  "ok": true
}
```

## Tabla global

| language | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | completeness | utility | ambiguity | info_loss | translation_ease | state_preservation | compactness |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EN | natural_en | 90 | 0 | 85.10 | 142.96 | 228.06 | 4.87 | 4.96 | 4.73 | 4.90 | 1.04 | 1.10 | 4.98 | 4.92 | 3.56 |
| EN | compressed_en | 90 | 0 | 102.10 | 86.88 | 188.98 | 4.88 | 4.92 | 4.44 | 4.88 | 1.09 | 1.14 | 4.93 | 4.87 | 4.91 |
| EN | proto_v3_min_core_en | 90 | 0 | 228.10 | 45.81 | 273.91 | 4.29 | 3.70 | 3.60 | 4.24 | 1.86 | 1.86 | 4.28 | 4.27 | 5.00 |
| EN | proto_v3_state_core_en | 90 | 0 | 200.10 | 93.09 | 293.19 | 4.88 | 4.81 | 4.56 | 4.92 | 1.12 | 1.10 | 4.92 | 4.92 | 4.98 |
| EN | proto_v3_hybrid_en | 90 | 0 | 129.10 | 70.71 | 199.81 | 4.89 | 4.93 | 4.38 | 4.91 | 1.08 | 1.14 | 4.98 | 4.90 | 4.99 |
| EN | proto_v3_min_translated_en | 90 | 0 | 131.81 | 69.09 | 200.90 | 3.69 | 3.77 | 2.63 | 3.31 | 2.20 | 2.63 | 4.34 | 3.04 | 4.81 |
| EN | proto_v3_state_translated_en | 90 | 0 | 179.09 | 97.52 | 276.61 | 4.72 | 4.79 | 4.09 | 4.72 | 1.19 | 1.30 | 4.89 | 4.46 | 4.76 |
| EN | proto_v3_hybrid_translated_en | 90 | 0 | 156.71 | 73.06 | 229.77 | 4.67 | 4.79 | 4.01 | 4.66 | 1.26 | 1.41 | 4.91 | 4.52 | 4.89 |

## Tabla por grupo de tarea

| language | task_group | best_tokens | best_quality | best_state | best_balance | observation |
|---|---|---|---|---|---|---|
| EN | base_comparable | proto_v3_hybrid_en | natural_en | natural_en | compressed_en | calculo_solo_modos_base |
| EN | memory_state | compressed_en | proto_v3_state_core_en | proto_v3_state_core_en | compressed_en | calculo_solo_modos_base |
| EN | medium_complexity | compressed_en | compressed_en | compressed_en | compressed_en | calculo_solo_modos_base |

## Variantes proto

| language | proto_variant | avg_total_tokens | avg_output_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| EN | proto_v3_min_core_en | 273.91 | 45.81 | 4.29 | 3.70 | 4.24 | 1.86 | 1.86 | 4.27 | not_stronger_than_compressed |
| EN | proto_v3_state_core_en | 293.19 | 93.09 | 4.88 | 4.81 | 4.92 | 1.12 | 1.10 | 4.92 | not_stronger_than_compressed |
| EN | proto_v3_hybrid_en | 199.81 | 70.71 | 4.89 | 4.93 | 4.91 | 1.08 | 1.14 | 4.90 | promising |

## Traducciones

La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.

| language | proto_mode | proto_tokens | translated_tokens | architectural_total | clarity_proto | clarity_translated | fidelity_proto | fidelity_translated | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| EN | proto_v3_min_core_en | 273.91 | 200.90 | 474.81 | 3.70 | 3.77 | 4.29 | 3.69 | extra_call;destroys_saving_vs_compressed |
| EN | proto_v3_state_core_en | 293.19 | 276.61 | 569.80 | 4.81 | 4.79 | 4.88 | 4.72 | extra_call;destroys_saving_vs_compressed |
| EN | proto_v3_hybrid_en | 199.81 | 229.77 | 429.58 | 4.93 | 4.79 | 4.89 | 4.67 | extra_call;destroys_saving_vs_compressed |

## Ganadores

- Modo base más barato: `compressed_en`
- Mejor calidad base: `proto_v3_hybrid_en`
- Mejor manejo de estado base: `natural_en`
- Mejor variante proto base: `proto_v3_hybrid_en`

## Lectura

- `compressed_en` reduce tokens frente a `natural_en`.
- `proto_v3_min_core_en` no supera el criterio fuerte contra `compressed_en`.
- `proto_v3_state_core_en` no supera el criterio fuerte contra `compressed_en`.
- `proto_v3_hybrid_en` no supera el criterio fuerte contra `compressed_en`.

## Errores y anomalías

- format:too_many_fields_for_state: 30
- format:translation_still_looks_like_proto: 27
- format:too_many_fields_for_min: 10
- format:compressed_en_looks_like_proto: 3

### Ejemplos
- T001 proto_v3_state_translated_en: format_notes=['translation_still_looks_like_proto']
- T001 proto_v3_state_translated_en: format_notes=['translation_still_looks_like_proto']
- T001 proto_v3_min_translated_en: format_notes=['translation_still_looks_like_proto']
- T001 proto_v3_state_translated_en: format_notes=['translation_still_looks_like_proto']
- T002 proto_v3_state_core_en: format_notes=['too_many_fields_for_state']
- T003 proto_v3_state_core_en: format_notes=['too_many_fields_for_state']
- T003 proto_v3_min_translated_en: format_notes=['translation_still_looks_like_proto']
- T003 proto_v3_state_translated_en: format_notes=['translation_still_looks_like_proto']
- T003 proto_v3_state_core_en: format_notes=['too_many_fields_for_state']
- T003 proto_v3_state_core_en: format_notes=['too_many_fields_for_state']
- T004 proto_v3_hybrid_translated_en: format_notes=['translation_still_looks_like_proto']
- T005 proto_v3_state_core_en: format_notes=['too_many_fields_for_state']
