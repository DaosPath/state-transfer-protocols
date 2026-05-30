# EXP15 - Cross-Cultural Long-Horizon Repo Maintenance

EXP15 es el experimento principal posterior a EXP14. Mantiene el mismo nucleo de mantenimiento de repositorio a cinco rondas, pero agrega comparacion cross-cultural/model-route con dos modelos chinos.

## Pregunta

Que protocolo mantiene mejor estado operativo, restricciones, claims y dependencias cuando agentes de distintas familias editan el mismo repositorio cientifico durante cadenas largas?

## Modelos

Rutas principales:

- `gemini_3_5_flash`
- `azure_gpt_5_4_high`
- `qwen3_next_80b_instruct`
- `glm_5`

Modelos chinos agregados:

- Qwen3-Next-80B Instruct: `qwen/qwen3-next-80b-a3b-instruct-maas`
- GLM-5: `zai-org/glm-5-maas`

## Diseno

- Escenarios: 10
- Rondas por escenario: 5
- Modos: `compressed`, `hybrid_state`
- Repeticiones: 2
- Modelos reales: 4
- Celdas reales esperadas: 800

Formula:

```text
10 escenarios x 5 rondas x 2 modos x 2 reps x 4 modelos = 800 celdas
```

Control local:

```text
10 escenarios x 5 rondas x 2 modos x 1 rep = 100 celdas dry-local
```

## Metricas

Validador determinista:

- `claim_drift_rate`
- `scope_drift_rate`
- `constraint_preservation`
- `dependency_preservation`
- `visual_quality_proxy`
- `visual_html_score`
- `visual_css_score`
- `visual_structure_score`
- `regression_rate`
- `html_integrity_score`
- `responsive_ok`
- `no_secret_leak`
- `no_local_paths`

Lectura por cadena:

- exito por celda
- cadena completa sin fallos
- errores por ronda
- reparaciones `ok_repaired`
- diferencia `compressed` vs `hybrid_state`
- diferencia modelos chinos vs rutas Gemini/Azure
- comparacion visual de paginas finales por modelo

## Comandos

Preflight:

```powershell
python .\run_exp15_resumable.py --preflight
```

Control local:

```powershell
python .\run_exp15_resumable.py --model-route dry_local_scaffold --reps 1
```

Rutas reales:

```powershell
python .\run_exp15_resumable.py --model-route gemini_3_5_flash --reps 2
python .\run_exp15_resumable.py --model-route azure_gpt_5_4_high --reps 2
python .\run_exp15_resumable.py --model-route qwen3_next_80b_instruct --reps 2
python .\run_exp15_resumable.py --model-route glm_5 --reps 2
```

Status:

```powershell
python .\status_exp15.py
```

## Politica De Claims

No afirmar:

- que modelos chinos son universalmente mejores
- que modelos occidentales son universalmente mejores
- que tokenizacion explica todo
- que `hybrid_state` gana globalmente
- que mantenimiento arbitrario de repos esta resuelto

Claim buscado:

```text
EXP15 mide robustez operacional y degradacion acumulada entre rutas de modelos cultural/arquitectonicamente distintas bajo el mismo contrato de herramientas.
```
