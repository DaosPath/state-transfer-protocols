# Resultados EXP01 EXP02 EN ZH

## Configuracion

- Perfil: `FULL_COMBINED_EXP01_EXP02_EN_ZH`
- Endpoint: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo generador: `deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: 0.2
- Repeticiones: 3
- Filas: 480
- Llamadas HTTP: 994
- Errores HTTP contabilizados por cliente: 0
- Parse errors: 0
- Missing tokens: 0
- Backup JSONL previo: no_aplica
- Soft stop: False

## Conexion

```json
{
  "timestamp": "2026-05-13T02:17:31.174489+00:00",
  "models_ok": true,
  "models_count": 15,
  "chat_ok": true,
  "chat_response": "OK_MULTILINGUAL_TEST",
  "error": null,
  "chat_model": "deepseek-v4-flash",
  "chat_latency_ms": 1519
}
```

## Piloto

```json
{
  "rows": 16,
  "errors": 0,
  "parse_errors": 0,
  "missing_tokens": 0,
  "format_invalid": 1,
  "zh_caricature": 0,
  "ok": true
}
```

## Tabla global

| language | experiment | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | compactness |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EN | EXP01 | compressed_en | 30 | 0 | 82.00 | 89.27 | 171.27 | 4.97 | 4.97 | 4.97 | 1.03 | 1.17 | 4.97 | 5.00 |
| EN | EXP01 | natural_en | 30 | 0 | 73.00 | 152.77 | 225.77 | 4.97 | 5.00 | 4.97 | 1.00 | 1.17 | 5.00 | 3.87 |
| EN | EXP01 | proto_v1_en | 30 | 0 | 135.00 | 216.27 | 351.27 | 5.00 | 5.00 | 5.00 | 1.00 | 1.00 | 5.00 | 4.27 |
| EN | EXP01 | proto_v1_translated_en | 30 | 0 | 275.27 | 113.57 | 388.83 | 4.93 | 4.97 | 4.93 | 1.03 | 1.13 | 4.93 | 4.10 |
| EN | EXP02 | compressed_en | 30 | 0 | 82.00 | 95.00 | 177.00 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 4.97 | 4.87 |
| EN | EXP02 | natural_en | 30 | 0 | 73.00 | 154.17 | 227.17 | 5.00 | 5.00 | 5.00 | 1.00 | 1.17 | 5.00 | 3.67 |
| EN | EXP02 | proto_v2_en | 30 | 0 | 144.00 | 152.20 | 296.20 | 4.90 | 4.93 | 4.93 | 1.10 | 1.10 | 4.93 | 4.60 |
| EN | EXP02 | proto_v2_translated_en | 30 | 0 | 211.20 | 116.20 | 327.40 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 5.00 | 4.33 |
| ZH | EXP01 | compressed_zh | 30 | 0 | 104.20 | 82.03 | 186.23 | 4.87 | 4.93 | 4.87 | 1.07 | 1.33 | 4.83 | 5.00 |
| ZH | EXP01 | natural_zh | 30 | 0 | 67.20 | 132.63 | 199.83 | 4.93 | 5.00 | 5.00 | 1.00 | 1.07 | 4.97 | 4.40 |
| ZH | EXP01 | proto_v1_core_zh | 30 | 0 | 149.20 | 222.43 | 371.63 | 5.00 | 5.00 | 5.00 | 1.00 | 1.07 | 5.00 | 4.37 |
| ZH | EXP01 | proto_v1_translated_zh | 30 | 0 | 275.43 | 152.63 | 428.07 | 4.90 | 4.97 | 4.93 | 1.03 | 1.20 | 4.93 | 4.37 |
| ZH | EXP02 | compressed_zh | 30 | 0 | 104.20 | 81.67 | 185.87 | 4.80 | 4.87 | 4.80 | 1.13 | 1.30 | 4.80 | 5.00 |
| ZH | EXP02 | natural_zh | 30 | 0 | 67.20 | 138.07 | 205.27 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 4.97 | 4.27 |
| ZH | EXP02 | proto_v2_core_zh | 30 | 0 | 153.20 | 226.00 | 379.20 | 4.90 | 5.00 | 5.00 | 1.00 | 1.10 | 5.00 | 4.07 |
| ZH | EXP02 | proto_v2_translated_zh | 30 | 0 | 279.00 | 173.83 | 452.83 | 4.93 | 5.00 | 5.00 | 1.00 | 1.17 | 4.93 | 4.07 |

## Ganadores por bloque

| language | experiment | cheapest_mode | best_quality_mode | best_state_mode | best_balance_mode | reading |
|---|---|---|---|---|---|---|
| EN | EXP01 | compressed_en | proto_v1_en | natural_en | compressed_en | compressed_wins_tokens |
| EN | EXP02 | compressed_en | natural_en | natural_en | compressed_en | compressed_wins_tokens |
| ZH | EXP01 | compressed_zh | proto_v1_core_zh | proto_v1_core_zh | compressed_zh | compressed_wins_tokens |
| ZH | EXP02 | compressed_zh | natural_zh | proto_v2_core_zh | compressed_zh | compressed_wins_tokens |

## Compressed vs natural

| language | experiment | natural_tokens | compressed_tokens | saving | quality_delta | reading |
|---|---|---:|---:|---:|---:|---|
| EN | EXP01 | 225.77 | 171.27 | 24.14% | 0.00 | compressed_cheaper |
| EN | EXP02 | 227.17 | 177.00 | 22.08% | 0.00 | compressed_cheaper |
| ZH | EXP01 | 199.83 | 186.23 | 6.81% | -0.07 | compressed_cheaper |
| ZH | EXP02 | 205.27 | 185.87 | 9.45% | -0.20 | compressed_cheaper |

## Proto v1 vs Proto v2

| language | metric | proto_v1 | proto_v2 | change | reading |
|---|---|---:|---:|---:|---|
| EN | avg_total_tokens | 351.27 | 296.20 | -55.07 | improved |
| EN | avg_input_tokens | 135.00 | 144.00 | 9.00 | worse_or_equal |
| EN | avg_output_tokens | 216.27 | 152.20 | -64.07 | improved |
| EN | semantic_fidelity | 5.00 | 4.90 | -0.10 | worse_or_equal |
| EN | utility | 5.00 | 4.93 | -0.07 | worse_or_equal |
| EN | ambiguity | 1.00 | 1.10 | 0.10 | worse_or_equal |
| EN | information_loss | 1.00 | 1.10 | 0.10 | worse_or_equal |
| EN | state_preservation | 5.00 | 4.93 | -0.07 | worse_or_equal |
| ZH | avg_total_tokens | 371.63 | 379.20 | 7.57 | worse_or_equal |
| ZH | avg_input_tokens | 149.20 | 153.20 | 4.00 | worse_or_equal |
| ZH | avg_output_tokens | 222.43 | 226.00 | 3.57 | worse_or_equal |
| ZH | semantic_fidelity | 5.00 | 4.90 | -0.10 | worse_or_equal |
| ZH | utility | 5.00 | 5.00 | 0.00 | worse_or_equal |
| ZH | ambiguity | 1.00 | 1.00 | 0.00 | worse_or_equal |
| ZH | information_loss | 1.07 | 1.10 | 0.03 | worse_or_equal |
| ZH | state_preservation | 5.00 | 5.00 | 0.00 | worse_or_equal |

## Traducciones

Nota: `translated_tokens` mide la llamada traducida sola. El costo arquitectonico real es `proto_tokens + translated_tokens`.

| language | experiment | proto_mode | proto_tokens | translated_tokens | total_architectural_cost | fidelity_proto | fidelity_translated | reading |
|---|---|---|---:|---:|---:|---:|---:|---|
| EN | EXP01 | proto_v1_en | 351.27 | 388.83 | 740.10 | 5.00 | 4.93 | translation_extra_call_quality_down |
| EN | EXP02 | proto_v2_en | 296.20 | 327.40 | 623.60 | 4.90 | 5.00 | translation_extra_call |
| ZH | EXP01 | proto_v1_core_zh | 371.63 | 428.07 | 799.70 | 5.00 | 4.90 | translation_extra_call_quality_down |
| ZH | EXP02 | proto_v2_core_zh | 379.20 | 452.83 | 832.03 | 4.90 | 4.93 | translation_extra_call |

## Anomalias

- format:missing_proto_v1_tags:CHK{: 7
- format:compressed_en_looks_like_proto: 1

### Ejemplos
- EN EXP01 T001 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T001 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T003 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T007 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T007 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T007 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP01 T009 proto_v1_en: format_notes=['missing_proto_v1_tags:CHK{']
- EN EXP02 T007 compressed_en: format_notes=['compressed_en_looks_like_proto']
