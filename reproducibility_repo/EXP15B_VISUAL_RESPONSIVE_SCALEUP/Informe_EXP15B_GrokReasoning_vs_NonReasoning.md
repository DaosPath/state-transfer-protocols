# Informe EXP15-B - Grok Reasoning vs Non-Reasoning

Freeze: `EXP15B_GROK_REASONING_FREEZE_20260530_061027`

## Resultado

- Grok non-reasoning: 43/400 (10.8%)
- Grok reasoning: 98/400 (24.5%)
- Delta absoluto: 13.8%
- Multiplicador relativo: 2.279x

## Lectura segura
Reasoning mejora la compatibilidad con el contrato JSON/tool-interface de EXP15-B, pero no elimina el failure mode. Este resultado no prueba superioridad general de reasoning: prueba una diferencia bajo este contrato long-horizon controlado.

## Siguiente paso
EXP16 debe comparar contrato estricto contra contrato adaptativo y medir first-pass, repair y recuperacion por familia de modelo.
