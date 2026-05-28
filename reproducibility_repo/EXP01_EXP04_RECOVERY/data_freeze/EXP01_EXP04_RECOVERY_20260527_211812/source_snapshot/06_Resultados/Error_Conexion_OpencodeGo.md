# Error Conexion Opencode Go

## Proposito

Registrar incidencias historicas de conexion ocurridas antes de la ejecucion final exitosa del Experimento 01.

## Estado actual

SUPERADO_EN_EJECUCION_FINAL.

La corrida final del experimento logro:

- `/models`: correcto.
- chat simple: correcto.
- piloto ampliado: correcto.
- experimento completo: 120 filas.
- errores HTTP finales: 0.

## Incidencias previas

Durante intentos anteriores hubo:

- bloqueo de red/proxy en entorno sandbox;
- `502 Bad gateway` temporal;
- salidas vacias por `thinking` activado en DeepSeek V4 con `max_tokens` bajo.

## Correccion aplicada

El script final envia:

```json
{"thinking": {"type": "disabled"}}
```

para modelos `deepseek-v4-*`. Esto evita que el presupuesto de salida se consuma en `reasoning_content` y deje `content` vacio.

## Seguridad

No se registra API key en este archivo.

## Proximo paso

Usar `Experimento_01_Resultados.md` y `experimento_01_runs.jsonl` como fuente de la corrida final.
