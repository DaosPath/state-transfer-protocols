# Experimento 01: Comparación de lenguaje natural, cavernícola y protolenguaje

## Objetivo

Comparar tres formas de comunicacion para agentes IA: lenguaje natural completo, lenguaje reducido tipo cavernicola y protolenguaje simbolico. La variante `proto_translated` mide el costo adicional de convertir el protolenguaje a espanol humano.

## Configuracion

- Endpoint usado: `https://opencode.ai/zen/go/v1/chat/completions`
- Endpoint de modelos: `https://opencode.ai/zen/go/v1/models`
- Modelo generador principal: `deepseek-v4-flash`
- Modelo generador fallback: `opencode-go/deepseek-v4-flash`
- Modelo evaluador principal: `deepseek-v4-pro`
- Modelo evaluador fallback: `deepseek-v4-flash`
- DeepSeek V4 thinking: `disabled`
- Numero de tareas: 10
- Repeticiones por modo: 3
- Temperatura: 0.2
- Fecha de ejecucion: 2026-05-12T22:01:34.393498+00:00
- Filas de resultados: 120
- Filas exitosas sin error registrado: 120
- Filas con error registrado: 0
- Llamadas HTTP intentadas por script: 250
- Llamadas HTTP exitosas por script: 250
- Llamadas HTTP con error por script: 0
- Reintentos por rate limit: 0
- Prueba de conexion: models_ok=True, chat_ok=True
- Piloto: {"timestamp": "2026-05-12T21:40:29.223451+00:00", "task_id": "T001", "ok": true, "checks": [{"mode": "natural", "generation_ok": true, "model": "deepseek-v4-flash", "latency_ms": 4359, "http_status": 200, "evaluation_ok": true, "evaluator_model": "deepseek-v4-pro", "error": null, "evaluation_error": null, "evaluation": {"fidelidad_semantica": 5, "claridad": 5, "completitud": 5, "utilidad": 5, "ambiguedad": 1, "perdida_informacion": 1, "facilidad_traduccion": 5, "comentario": "La respuesta aborda completamente la tarea, identifica el problema, propone una solución concreta, enumera riesgos y detalla próximos pasos. Es clara, útil y sin ambigüedades."}}, {"mode": "caveman", "generation_ok": true, "model": "deepseek-v4-flash", "latency_ms": 3509, "http_status": 200, "evaluation_ok": true, "evaluator_model": "deepseek-v4-pro", "error": null, "evaluation_error": null, "evaluation": {"fidelidad_semantica": 5, "claridad": 5, "completitud": 4, "utilidad": 5, "ambiguedad": 1, "perdida_informacion": 1, "facilidad_traduccion": 5, "comentario": "La respuesta captura fielmente el problema, propone una solución concreta, enumera riesgos y pasos siguientes de forma clara y concisa, aunque podría detallar un poco más la compresión de contexto compartido."}}, {"mode": "proto", "generation_ok": true, "model": "deepseek-v4-flash", "latency_ms": 3492, "http_status": 200, "evaluation_ok": true, "evaluator_model": "deepseek-v4-pro", "error": null, "evaluation_error": null, "evaluation": {"fidelidad_semantica": 5, "claridad": 5, "completitud": 5, "utilidad": 5, "ambiguedad": 1, "perdida_informacion": 1, "facilidad_traduccion": 5, "comentario": "La respuesta captura fielmente el problema, propone solución, riesgos y próximos pasos de forma concisa y estructurada, sin ambigüedad ni pérdida de información relevante."}}, {"mode": "proto_translated", "generation_ok": true, "model": "deepseek-v4-flash", "latency_ms": 2843, "http_status": 200, "evaluation_ok": true, "evaluator_model": "deepseek-v4-pro", "error": null, "evaluation_error": null, "evaluation": {"fidelidad_semantica": 4, "claridad": 4, "completitud": 4, "utilidad": 4, "ambiguedad": 2, "perdida_informacion": 2, "facilidad_traduccion": 5, "comentario": "La respuesta captura bien la esencia del problema y propone soluciones alineadas, aunque omite detalles como ejemplos concretos de formato o métricas de riesgo."}}]}

No se incluye API key.

## Metodologia

Se generaron respuestas para 10 tareas en tres modos: `natural`, `caveman` y `proto`, con 3 repeticiones por modo. Cada salida `proto` se tradujo adicionalmente a `proto_translated`. Luego se envio cada salida final al evaluador automatico, que devolvio puntajes JSON de 1 a 5. Los resultados se guardaron incrementalmente en `experimento_01_runs.jsonl`.

Para modelos `deepseek-v4-*` se envio `thinking: disabled`, porque con pensamiento activado y limites bajos la API podia consumir tokens en `reasoning_content` y devolver `content` vacio.

Si la API devolvio `usage`, se registraron `prompt_tokens`, `completion_tokens` y `total_tokens`. Si no hubo `usage`, los tokens quedaron como `null` y se marco `token_count_method: missing_from_api`.

## Tabla de resultados

| Modo | Tokens promedio | Ahorro vs natural | Fidelidad | Claridad | Completitud | Ambigüedad | Pérdida info | Utilidad | Conclusión |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| natural | 364.30 | 0.00% | 4.97 | 5.00 | 4.73 | 1.00 | 1.00 | 5.00 | Baseline claro |
| caveman | 263.97 | 27.54% | 4.97 | 4.97 | 4.27 | 1.03 | 1.10 | 4.97 | Reduce forma; mantiene lectura directa |
| proto | 377.13 | -3.52% | 4.87 | 4.90 | 4.43 | 1.17 | 1.27 | 4.87 | Compacto; requiere traduccion para usuario |
| proto_translated | 438.87 | -20.47% | 4.57 | 4.80 | 4.33 | 1.33 | 1.37 | 4.70 | Mide costo de salida humana final |

## Observaciones

- Menor consumo promedio observado: `caveman`.
- Mayor claridad promedio evaluada: `natural`.
- Mayor fidelidad semantica promedio evaluada: `natural`.

## Errores detectados

- No se registraron errores por fila.

## Conclusion parcial

Esta tanda exploratoria indica patrones iniciales, no una demostracion definitiva. Los resultados deben interpretarse como primera evidencia controlada. Para sostener la hipotesis hacen falta mas tareas, mas dominios, mas modelos y revision humana de una muestra.

## Proximos pasos

- Aumentar tareas.
- Aumentar repeticiones.
- Probar otros modelos.
- Comparar con mas dominios.
- Medir tokens exactos si faltaron.
- Mejorar reglas del protolenguaje.
- Agregar evaluacion humana.
