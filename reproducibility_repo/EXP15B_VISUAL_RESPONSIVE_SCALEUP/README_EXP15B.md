# EXP15-B - Visual Responsive Scale-Up

EXP15-B amplifica EXP15 sin cambiar su pregunta central: mantenimiento largo de un repositorio/pagina cientifica por agentes con contratos de estado. La diferencia es que aqui el objetivo visual y movil se vuelve central.

## Pregunta

Que protocolo y que ruta de modelo mantienen mejor una pagina publica de investigacion durante diez rondas encadenadas, preservando claims, restricciones, dependencias y calidad visual/responsive?

## Diseno

- Escenarios: 10
- Rondas por escenario: 10
- Modos: `compressed`, `hybrid_state`
- Repeticiones: 2
- Modelos reales: 5
- Celdas reales esperadas: 2000

Formula:

```text
10 escenarios x 10 rondas x 2 modos x 2 reps x 5 modelos = 2000 celdas
```

Control local:

```text
10 escenarios x 10 rondas x 2 modos x 1 rep = 200 celdas dry-local
```

## Modelos

- `gemini_3_5_flash`
- `grok_4_20_non_reasoning`
- `grok_4_20_reasoning`
- `qwen3_next_80b_instruct`
- `glm_5`

## Metricas

Metricas operativas:

- `claim_drift_rate`
- `scope_drift_rate`
- `constraint_preservation`
- `dependency_preservation`
- `regression_rate`
- `recovery_after_previous_error`

Metricas visuales/responsive:

- `visual_quality_proxy`
- `visual_html_score`
- `visual_css_score`
- `visual_structure_score`
- `responsive_ok`
- conteos de secciones, headings, listas, cards/grids y media queries

Seguridad/release:

- `no_secret_leak`
- `no_local_paths`
- preservacion de DOI/GitHub cuando el escenario lo exige

## Comandos

Preflight:

```powershell
python .\run_exp15b_resumable.py --preflight
```

Control local:

```powershell
python .\run_exp15b_resumable.py --model-route dry_local_scaffold --reps 1
```

Rutas reales:

```powershell
python .\run_exp15b_resumable.py --model-route gemini_3_5_flash --reps 2
python .\run_exp15b_resumable.py --model-route grok_4_20_non_reasoning --reps 2
python .\run_exp15b_resumable.py --model-route grok_4_20_reasoning --reps 2
python .\run_exp15b_resumable.py --model-route qwen3_next_80b_instruct --reps 2
python .\run_exp15b_resumable.py --model-route glm_5 --reps 2
```

Secuencial completo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_exp15b_full_sequential.ps1
```

Status:

```powershell
python .\status_exp15b.py
```

Comparacion visual final:

```powershell
python .\compare_exp15b_pages_by_model.py
```

## Politica De Claims

No afirmar:

- que un modelo es universalmente mejor
- que `hybrid_state` gana globalmente
- que mantenimiento arbitrario de repos esta resuelto
- que responsive/mobile queda validado fuera de este sitio controlado
- que diferencias ZH/modelos chinos prueban tokenizacion como causa unica

Claim buscado:

```text
EXP15-B mide robustez operacional y visual bajo cadenas mas largas de mantenimiento de pagina/repo, comparando compressed e hybrid_state entre rutas de modelos distintas.
```
