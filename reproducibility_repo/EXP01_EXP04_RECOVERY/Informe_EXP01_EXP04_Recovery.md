# Informe EXP01-EXP04 Recovery

## Estado

Se encontraron datos ejecutados para EXP01, EXP02, EXP03 y EXP04. No fue necesario regenerar nada.

Los originales quedan intactos. Se creó un paquete separado de recuperación con:

- snapshot congelado de fuentes
- hashes SHA256
- `clean_latest_ok`
- errores terminales separados
- manifiesto reproducible
- sweep de secretos

## Ubicación

Base:

`Investigaciones/Protolenguaje_AgentesIA/05_Experimentos/EXP01_EXP04_RECOVERY`

Freeze:

`data_freeze/EXP01_EXP04_RECOVERY_20260527_211812`

Clean:

`clean_latest_ok/EXP01_EXP04_ALL.clean_latest_ok.jsonl`

Manifest:

`data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/manifest.json`

## Datos recuperados

| Fuente | Filas raw | Celdas únicas | OK clean | Errores terminales |
|---|---:|---:|---:|---:|
| `06_Resultados/experimento_01_runs.jsonl` | 120 | 120 | 120 | 0 |
| `06_Resultados/experimento_02_runs.jsonl` | 120 | 120 | 120 | 0 |
| `06_Resultados/experimento_03_fusion_runs.jsonl` | 720 | 720 | 720 | 0 |
| `09_Multilingue/08_Combined_Runs/exp01_exp02_en_zh_runs.jsonl` | 480 | 480 | 480 | 0 |
| `09_Multilingue/08_Combined_Runs/EXP03_EN/exp03_en_runs.jsonl` | 720 | 720 | 720 | 0 |
| `09_Multilingue/08_Combined_Runs/EXP03_ZH/exp03_zh_runs.jsonl` | 900 | 900 | 900 | 0 |
| `05_Experimentos/EXP04_TRI/exp04_tri_runs.jsonl` | 1350 | 1350 | 1350 | 0 |
| `05_Experimentos/EXP04_TRI/exp04b_batch_decode_results.jsonl` | 9 | 9 | 9 | 0 |

Total clean latest OK: **4419 filas**.

## Cobertura

Por idioma:

| Idioma | Filas OK |
|---|---:|
| ES | 1413 |
| EN | 1413 |
| ZH | 1593 |

Por modelo:

| Modelo generador | Filas OK |
|---|---:|
| `deepseek-v4-flash` | 4419 |

Modelo evaluador dominante:

| Modelo evaluador | Uso |
|---|---:|
| `deepseek-v4-pro` | todas las filas con evaluación LLM |

## Política de limpieza

La clave de celda usada fue:

`experiment/language/task_id/mode/run/generator_model`

Política:

- `last row wins`
- filas con `error` o `evaluation_parse_error` quedan fuera de `clean_latest_ok`
- errores terminales se guardan en archivo separado
- no se borran logs ni evidencia histórica

Resultado: no había duplicados efectivos ni errores terminales en los JSONL principales recuperados.

## Lectura metodológica

EXP01-EXP03 son la fase temprana:

- EXP01: natural vs caveman/proto inicial.
- EXP02: proto_v2 frente a caveman/natural.
- EXP03: familia proto_v3, incluyendo variantes `min`, `state` e `hybrid`.

EXP04 consolida la transición:

- trilingüe ES/EN/ZH
- modos ya cercanos a la nomenclatura posterior: `compressed`, `compressed_state`, `hybrid_min`, `hybrid_state`
- 1350 filas principales más 9 filas de batch final decode

Para el paper, EXP01-EXP04 pueden presentarse como camino histórico y diseño iterativo, no como evidencia causal principal. La evidencia fuerte debe seguir apoyándose en EXP05-EXP10.

## Seguridad

Sweep de secretos: **0 hits**.

Patrones revisados:

- claves OpenAI estilo `sk-`
- claves Google estilo `AIza`
- bearer tokens
- prefijo sensible de Azure conocido

## Archivos producidos

- `README_EXP01_EXP04_RECOVERY.md`
- `analysis/EXP01_EXP04_summary_counts.csv`
- `clean_latest_ok/EXP01_EXP04_ALL.clean_latest_ok.jsonl`
- `clean_latest_ok/EXP01_EXP04_ALL.terminal_errors.jsonl`
- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/manifest.json`
- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/SHA256SUMS.txt`
- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/source_snapshot/`
