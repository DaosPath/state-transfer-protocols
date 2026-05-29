# Informe EXP13 - Real Multi-Agent Scientific Repo Benchmark

## Resumen

EXP13 evalua si los protocolos `compressed` y `hybrid_state` pueden sostener mantenimiento de un repositorio/pagina cientifica bajo asignacion multiagente controlada.

El experimento usa escenarios donde el modelo debe actuar como equipo coordinado:

- Writer agent
- Reviewer agent
- Reproducibility agent
- Security/claims agent
- Merge/repair agent

La tarea no es solo escribir texto. Debe editar artefactos reales (`index.html`, `styles.css`) preservando claims, dependencias, enlaces, restricciones de seguridad, responsive layout y alcance de archivos.

## Diseno Experimental

- Escenarios: 16
- Modos: `compressed`, `hybrid_state`
- Modelos: `gemini_3_5_flash`, `azure_gpt_5_4_high`
- Repeticiones: 2
- Celdas reales esperadas: 128
- Scaffold local: 32 celdas de control

## Resultado Principal

| Grupo | Exitos | Fallos | Total |
|---|---:|---:|---:|
| Modelos reales | 126 | 2 | 128 |
| Scaffold local | 32 | 0 | 32 |
| Total latest cells | 158 | 2 | 160 |

EXP13 no quedo saturado perfecto. Eso es metodologicamente util: aparecen fallos reales de contrato en condiciones multiagente.

## Resultado Por Modo

| Modo | Exitos | Fallos | Total |
|---|---:|---:|---:|
| compressed | 64 | 0 | 64 |
| hybrid_state | 62 | 2 | 64 |

Lectura: `compressed` fue mas robusto como protocolo operacional general. `hybrid_state` mantuvo buen rendimiento, pero concentro los dos fallos finales. Esto evita vender un claim falso de superioridad global.

## Resultado Por Modelo

| Modelo | Exitos | Fallos | Total |
|---|---:|---:|---:|
| Gemini 3.5 Flash | 63 | 1 | 64 |
| Azure GPT-5.4 High | 63 | 1 | 64 |

Ambos modelos terminaron con una falla persistente. La simetria es interesante: el problema no parece solo de un proveedor.

## Reparaciones

| Modelo | Modo | Celdas reparadas |
|---|---|---:|
| Gemini 3.5 Flash | compressed | 16 |
| Gemini 3.5 Flash | hybrid_state | 11 |
| Azure GPT-5.4 High | compressed | 0 |
| Azure GPT-5.4 High | hybrid_state | 0 |

Gemini requirio mas reparacion automatica de contrato/validacion. Azure produjo menos salidas reparables, pero tuvo un caso persistente de `no_changes`.

## Fallos Finales

| Escenario | Tipo | Modo | Rep | Modelo | Error |
|---|---|---|---:|---|---|
| S009 | outreach | hybrid_state | 2 | gemini_3_5_flash | `no_json_object` |
| S011 | roles | hybrid_state | 1 | azure_gpt_5_4_high | `no_changes` |

Interpretacion:

- `no_json_object`: fallo de contrato de salida. El modelo no devolvio objeto JSON utilizable.
- `no_changes`: fallo de accion. El modelo no produjo ediciones aplicables.

Ambos fallos son relevantes para agentes reales: preservar estado no basta si el contrato tool/JSON se rompe.

## Metricas Objetivas Del Validator

EXP13 valida automaticamente:

- `merge_safety`
- `constraint_preservation`
- `dependency_preservation`
- `claim_drift_rate`
- `scope_drift_rate`
- `regression_rate`
- `repair_success`
- `no_secret_leak`
- `no_local_paths`
- `responsive_ok`
- `html_integrity_score`

Los validadores revisan terminos requeridos, secciones, links, claims prohibidos, archivos inesperados, secretos, rutas locales, integridad HTML y responsive CSS.

## Hallazgos

1. `compressed` fue el protocolo mas estable en este benchmark: 64/64.
2. `hybrid_state` sigue siendo util, pero en EXP13 aumento el riesgo de fallo de contrato en tareas multiagente largas.
3. Las metricas objetivas capturan problemas que un juez LLM podria suavizar: archivos inesperados, claims prohibidos, rutas locales, HTML roto y falta de cambios.
4. Gemini 3.5 Flash completo casi todo, pero necesito reparaciones frecuentes.
5. Azure GPT-5.4 High fue mas directo cuando funciono, pero una celda quedo sin cambios aun tras reintento.

## Incidentes Operativos

- El proceso Azure inicialmente requirio limpiar variables proxy (`HTTP_PROXY`, `HTTPS_PROXY`) para llamadas reales.
- Los fallos historicos se preservan en `exp13_runs.jsonl`.
- El analisis principal debe usar ultimo estado por `cell_id`.

## Claim Recomendado

Claim fuerte:

> EXP13 shows that state-transfer protocols can drive controlled multi-agent maintenance of scientific repository artifacts with objective validators, reaching 126/128 successful real-model cells.

Claim limitado:

> In this benchmark, `compressed` was more operationally robust than `hybrid_state`, while `hybrid_state` exposed contract fragility under longer role-conditioned tasks.

No afirmar:

- que `hybrid_state` gana globalmente
- que EXP13 prueba colaboracion multiagente universal
- que los modelos quedan rankeados de forma general

## Archivos

- `task_bank_exp13_scientific_repo.jsonl`
- `prompts_exp13_modes.json`
- `model_registry_exp13.json`
- `run_exp13_resumable.py`
- `validators/validate_scientific_repo.py`
- `exp13_runs.jsonl`
- `exp13_cost_ledger.jsonl`
- `exp13_latest_cells_clean.jsonl`
- `exp13_failures_latest.jsonl`
- `workspace_runs/`
- `SHA256SUMS_EXP13.txt`
