# Error Experimento 03 Fusion

## Estado

SUPERADO_EN_CORRIDA_FINAL.

## Proposito

Conservar registro de un fallo inicial de piloto sin confundirlo con el resultado final de EXP03.

## Contenido principal

Antes de la corrida final, el piloto fallo por una regla local de validacion demasiado estricta. El validador marcaba como etiquetas de Proto v1/v2 salidas validas de `proto_v3_state` y `proto_v3_hybrid`.

No fue un error de API, autenticacion, modelo ni datos del experimento. Se corrigio el validador y luego el piloto final paso correctamente.

Resultado final posterior:

- Perfil ejecutado: FULL.
- Filas finales: 720.
- Llamadas HTTP: 1474.
- Errores por fila: 0.
- Evaluaciones JSON invalidas: 0.
- Tokens presentes: si.

## Riesgos o limitaciones

Este archivo no debe usarse como resumen de resultados. Para resultados reales usar:

- `Experimento_03_Fusion_Resultados.md`.
- `experimento_03_fusion_runs.jsonl`.

## Proximos pasos

Mantener el archivo como nota historica de depuracion. Si se vuelve a ejecutar EXP03, revisar primero los validadores locales para evitar falsos positivos.
