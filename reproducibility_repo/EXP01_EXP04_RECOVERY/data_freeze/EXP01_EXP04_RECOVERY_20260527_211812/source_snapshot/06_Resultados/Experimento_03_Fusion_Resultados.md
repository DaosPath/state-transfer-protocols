# Experimento 03 Fusion: Proto v3 minimalista, state e hybrid

## Objetivo

Ejecutar una comparacion ampliada entre lenguaje natural, caveman y tres variantes de Proto v3, incluyendo traducciones finales humanas de cada variante proto.

## Hipotesis

Proto v3 minimalista puede reducir tokens frente a Proto v2 y recuperar calidad semantica al eliminar estructura obligatoria. Proto v3 state puede aportar valor en memoria/estado. Proto v3 hybrid puede equilibrar ahorro, claridad y traducibilidad.

## Motivo del rediseño

EXP01 mostro que Proto v1 era demasiado pesado. EXP02 mostro que reducir etiquetas no bastaba si los campos seguian siendo obligatorios. EXP03 prueba campos opcionales y formatos mas cercanos a caveman.

## Cambios frente a Proto v2

- Campos opcionales.
- Una linea cuando sea posible.
- No plantilla fija de 8 campos.
- Tres variantes: min, state e hybrid.
- Validadores locales de formato.

## Configuracion

- Endpoint: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo generador: `deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: 0.2
- Repeticiones: 3
- Perfil: FULL
- Llamadas HTTP: 1474
- Errores HTTP: 0
- Soft stop activado: False
- Backup JSONL previo: no_aplica
- Conexion: {"timestamp": "2026-05-12T23:37:49.801760+00:00", "models_ok": true, "models_count": 15, "chat_ok": true, "error": null, "chat_model": "deepseek-v4-flash", "chat_latency_ms": 1370, "chat_response": "OK_EXP03_TEST"}

## Perfil de ejecucion usado

FULL.

## Piloto

```json
{
  "timestamp": "2026-05-12T23:37:51.173216+00:00",
  "ok": true,
  "attempt": 1,
  "checks": [
    {
      "task_id": "T001",
      "mode": "natural",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": null,
      "format_notes": [
        "not_applicable"
      ],
      "error": null,
      "word_count": 133,
      "field_count": 0,
      "fields_used": [],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta aborda completamente el problema, propone una solución concreta, identifica riesgos relevantes y enumera próximos pasos accionables, todo de forma clara y sin ambigüedades."
      }
    },
    {
      "task_id": "T001",
      "mode": "caveman",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": null,
      "format_notes": [
        "not_applicable"
      ],
      "error": null,
      "word_count": 71,
      "field_count": 0,
      "fields_used": [],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 4,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta captura fielmente el problema, propone soluciones concretas, riesgos y próximos pasos de forma extremadamente concisa y sin ambigüedades, alineada con el modo caveman solicitado."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_min",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 6,
      "field_count": 4,
      "fields_used": [
        "n",
        "p",
        "r",
        "s"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 4,
        "completitud": 4,
        "utilidad": 4,
        "ambiguedad": 2,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 3,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia del problema y propone una solución concreta, riesgos y próximos pasos en formato extremadamente compacto. La claridad y completitud son altas para el formato, aunque la extrema compresión introduce cierta ambigüedad y pérdida de detalle. El manejo de estado está implícito pero no detallado."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_state",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 8,
      "field_count": 8,
      "fields_used": [
        "c",
        "conf",
        "g",
        "lim",
        "n",
        "p",
        "r",
        "s"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 4,
        "claridad": 2,
        "completitud": 3,
        "utilidad": 3,
        "ambiguedad": 3,
        "perdida_informacion": 2,
        "facilidad_traduccion": 4,
        "manejo_estado": 2,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia (problema, solución, riesgos, próximos pasos) de forma muy compacta, pero la claridad y completitud se ven afectadas por el formato abreviado, lo que introduce ambigüedad en algunos campos."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_hybrid",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 39,
      "field_count": 4,
      "fields_used": [
        "n",
        "p",
        "r",
        "s"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 4,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 4,
        "compacidad": 5,
        "comentario": "La respuesta captura fielmente el problema, propone una solución concreta, identifica riesgos clave y sugiere próximos pasos medibles. Es concisa y directa, aunque podría detallar un poco más los riesgos o el diseño de la prueba."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_min_translated",
      "base_mode": "proto_v3_min",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 3,
        "claridad": 2,
        "completitud": 2,
        "utilidad": 2,
        "ambiguedad": 3,
        "perdida_informacion": 3,
        "facilidad_traduccion": 4,
        "manejo_estado": 1,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia del problema pero omite detalles clave solicitados: no desarrolla la solución, no enumera riesgos concretos ni propone próximos pasos. Es excesivamente compacta y carece de estructura."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_state_translated",
      "base_mode": "proto_v3_state",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 4,
        "claridad": 4,
        "completitud": 3,
        "utilidad": 4,
        "ambiguedad": 2,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 3,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia del problema y propone una solución concreta, aunque omite detalles como tipos de riesgos adicionales o métricas de evaluación más específicas."
      }
    },
    {
      "task_id": "T001",
      "mode": "proto_v3_hybrid_translated",
      "base_mode": "proto_v3_hybrid",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 4,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta captura fielmente el problema, propone una solución concreta, menciona riesgos y sugiere una métrica de validación. Es clara, compacta y fácil de traducir. Pierde mínima información respecto a la tarea original (no detalla próximos pasos como una hoja de ruta, pero los implica)."
      }
    },
    {
      "task_id": "T011",
      "mode": "natural",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": null,
      "format_notes": [
        "not_applicable"
      ],
      "error": null,
      "word_count": 82,
      "field_count": 0,
      "fields_used": [],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 4,
        "comentario": "La respuesta cubre todos los elementos solicitados (agente objetivo, contexto, error, riesgo, próxima acción) de forma clara y sin ambigüedades. Es ligeramente extensa para un resumen de estado, pero mantiene alta utilidad y fidelidad."
      }
    },
    {
      "task_id": "T011",
      "mode": "caveman",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": null,
      "format_notes": [
        "not_applicable"
      ],
      "error": null,
      "word_count": 65,
      "field_count": 0,
      "fields_used": [],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta captura exactamente los elementos solicitados (objetivo, contexto, error, riesgo, próxima acción) de forma concisa y estructurada, sin ambigüedad ni pérdida de información."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_min",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 7,
      "field_count": 5,
      "fields_used": [
        "c",
        "e",
        "n",
        "p",
        "r"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 4,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta captura con precisión los elementos solicitados (agente, contexto, error, riesgo, acción) en un formato compacto y fácil de traducir. Solo se omite el detalle explícito del 'objetivo', pero se infiere en la acción 'validar>transferir'."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_state",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 7,
      "field_count": 7,
      "fields_used": [
        "a",
        "c",
        "g",
        "m",
        "n",
        "p",
        "r"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 4,
        "claridad": 4,
        "completitud": 4,
        "utilidad": 4,
        "ambiguedad": 2,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 5,
        "compacidad": 5,
        "comentario": "La respuesta captura bien los elementos clave (objetivo, contexto, error, riesgo, acción) en formato compacto. Sin embargo, 'c=espera_siguiente_agente' es ligeramente ambiguo (¿espera activa o pasiva?) y 'm=tarea_finalizada_sin_errores' omite el matiz de 'error detectado' como campo, aunque lo cubre implícitamente. En general, es eficiente y traducible."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_hybrid",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "format_valid": true,
      "format_notes": [],
      "error": null,
      "word_count": 26,
      "field_count": 4,
      "fields_used": [
        "n",
        "p",
        "r",
        "s"
      ],
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 4,
        "claridad": 5,
        "completitud": 3,
        "utilidad": 4,
        "ambiguedad": 2,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 3,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia de la tarea original de forma muy compacta y clara, pero omite detalles como la estructura concreta del handoff o ejemplos de los campos, lo que reduce ligeramente la completitud y el manejo de estado."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_min_translated",
      "base_mode": "proto_v3_min",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 2,
        "claridad": 3,
        "completitud": 2,
        "utilidad": 2,
        "ambiguedad": 3,
        "perdida_informacion": 4,
        "facilidad_traduccion": 4,
        "manejo_estado": 2,
        "compacidad": 4,
        "comentario": "La respuesta omite el contexto, el error detectado y el agente objetivo explícitos de la tarea original. Sustituye los campos requeridos por etiquetas genéricas (Problema, Objetivo, Solución) que no reflejan fielmente la estructura solicitada. Aunque es compacta y traducible, la pérdida de información es alta y la utilidad para la transición de estado es baja."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_state_translated",
      "base_mode": "proto_v3_state",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 3,
        "claridad": 4,
        "completitud": 2,
        "utilidad": 3,
        "ambiguedad": 2,
        "perdida_informacion": 3,
        "facilidad_traduccion": 4,
        "manejo_estado": 2,
        "compacidad": 4,
        "comentario": "La respuesta captura la idea general pero omite detalles clave de la tarea original como 'contexto', 'error detectado' y 'riesgo' específicos, reemplazándolos con contenido genérico. No se transfiere el estado real del agente anterior."
      }
    },
    {
      "task_id": "T011",
      "mode": "proto_v3_hybrid_translated",
      "base_mode": "proto_v3_hybrid",
      "generation_ok": true,
      "tokens_present": true,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "model": "deepseek-v4-flash",
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 4,
        "claridad": 5,
        "completitud": 3,
        "utilidad": 4,
        "ambiguedad": 2,
        "perdida_informacion": 2,
        "facilidad_traduccion": 5,
        "manejo_estado": 3,
        "compacidad": 5,
        "comentario": "La respuesta captura la esencia del traspaso y añade riesgos y un paso siguiente, pero omite detallar explícitamente los campos 'objetivo, contexto, error detectado' como contenido real, lo que reduce completitud y manejo de estado."
      }
    }
  ]
}
```

## Metodologia

Se ejecutaron modos base `natural`, `caveman`, `proto_v3_min`, `proto_v3_state` y `proto_v3_hybrid`. Para cada salida proto se genero una traduccion humana breve. Todas las salidas fueron evaluadas por modelo evaluador con JSON estructurado. Los resultados se guardaron incrementalmente en `experimento_03_fusion_runs.jsonl`.

## Tabla de resultados global

| Modo | Filas | Errores | Tokens promedio | Ahorro vs natural | Ahorro vs caveman | Ahorro vs proto_v2 | Fidelidad | Claridad | Completitud | Ambigüedad | Pérdida info | Utilidad | Traducibilidad | Manejo estado | Compacidad | Latencia ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| natural | 90 | 0 | 324.54 | 0.00% | -38.76% | -1.92% | 4.84 | 4.94 | 4.61 | 1.09 | 1.13 | 4.86 | 4.97 | 4.81 | 4.36 | 4198 |
| caveman | 90 | 0 | 233.89 | 27.93% | 0.00% | 26.55% | 4.14 | 4.37 | 3.54 | 1.67 | 1.81 | 4.17 | 4.70 | 3.67 | 4.80 | 2753 |
| proto_v3_min | 90 | 0 | 370.87 | -14.27% | -58.57% | -16.47% | 3.69 | 2.69 | 3.06 | 2.21 | 2.19 | 3.19 | 3.42 | 2.91 | 4.72 | 2261 |
| proto_v3_state | 90 | 0 | 377.23 | -16.23% | -61.29% | -18.47% | 3.79 | 2.64 | 3.07 | 2.47 | 2.30 | 3.17 | 3.37 | 3.47 | 4.91 | 2581 |
| proto_v3_hybrid | 90 | 0 | 266.78 | 17.80% | -14.06% | 16.22% | 4.46 | 4.43 | 3.74 | 1.52 | 1.60 | 4.47 | 4.80 | 3.90 | 4.98 | 2469 |
| proto_v3_min_translated | 90 | 0 | 224.83 | 30.72% | 3.87% | 29.39% | 2.63 | 2.81 | 1.92 | 2.53 | 2.63 | 2.20 | 3.60 | 1.70 | 3.92 | 2155 |
| proto_v3_state_translated | 90 | 0 | 253.03 | 22.03% | -8.19% | 20.54% | 3.10 | 3.18 | 2.27 | 2.30 | 2.43 | 2.69 | 3.88 | 2.49 | 4.18 | 2280 |
| proto_v3_hybrid_translated | 90 | 0 | 248.91 | 23.30% | -6.42% | 21.83% | 3.72 | 4.00 | 2.92 | 2.09 | 2.21 | 3.58 | 4.44 | 2.69 | 4.54 | 2251 |

## Validez de formato Proto v3

| Modo | Formato válido % | Palabras prom. | Campos prom. | Campos frecuentes | Notas |
|---|---:|---:|---:|---|---|
| proto_v3_min | 100.00% | 6.46 | 4.52 | p:87, s:84, r:78, n:77, g:21, v:20, m:19, c:11 | sin_notas |
| proto_v3_state | 97.78% | 7.72 | 6.33 | c:90, g:90, n:85, s:66, m:58, v:49, r:43, k:34 | field_count_gt_8:2 |
| proto_v3_hybrid | 100.00% | 35.27 | 4.07 | n:90, p:90, s:90, r:87, calidad:3, error:3, tokens:3 | sin_notas |

## Analisis por grupos de tarea

| Grupo | Mejor por tokens | Mejor por calidad | Mejor por estado | Observacion |
|---|---|---|---|---|
| base_comparable | caveman | natural | natural | proto_v3_hybrid fue la mejor variante proto |
| memory_state | caveman | natural | natural | proto_v3_state no supero a caveman en estado |
| medium_complexity | caveman | natural | natural | hybrid mantuvo mejor equilibrio proto |

## Analisis de traducciones

Nota: `Tokens traducido` mide solo la llamada de traduccion. El costo arquitectonico real de traducir por salida es `tokens proto + tokens traducido`.

| Modo proto | Tokens proto | Tokens traducido | Costo extra | Claridad proto | Claridad traducido | Fidelidad proto | Fidelidad traducido | Lectura |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| proto_v3_min | 370.87 | 224.83 | 224.83 | 2.69 | 2.81 | 3.69 | 2.63 | extra_call;total=595.70 |
| proto_v3_state | 377.23 | 253.03 | 253.03 | 2.64 | 3.18 | 3.79 | 3.10 | extra_call;total=630.26 |
| proto_v3_hybrid | 266.78 | 248.91 | 248.91 | 4.43 | 4.00 | 4.46 | 3.72 | extra_call;total=515.69 |

## Comparacion con EXP01

EXP01 sirve como referencia de Proto v1 y caveman inicial. Ver tabla historica completa en `Comparacion_EXP01_EXP02_EXP03_Fusion.md`.

## Comparacion con EXP02

| Modo | EXP01 tokens | EXP02 tokens | EXP03 tokens | Cambio vs EXP02 | Fidelidad EXP03 | Lectura |
|---|---:|---:|---:|---:|---:|---|
| natural | 364.30 | 354.63 | 324.54 | -30.09 | 4.84 | menos que EXP02 |
| caveman | 263.97 | 240.93 | 233.89 | -7.04 | 4.14 | menos que EXP02 |
| proto_v1 | 377.13 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia |
| proto_v2 | NO_CALCULABLE | 318.43 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia |
| proto_v3_min | NO_CALCULABLE | NO_CALCULABLE | 370.87 | NO_CALCULABLE | 3.69 | referencia |
| proto_v3_state | NO_CALCULABLE | NO_CALCULABLE | 377.23 | NO_CALCULABLE | 3.79 | referencia |
| proto_v3_hybrid | NO_CALCULABLE | NO_CALCULABLE | 266.78 | NO_CALCULABLE | 4.46 | referencia |
| proto_v1_translated | 438.87 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia |
| proto_v2_translated | NO_CALCULABLE | 332.70 | NO_CALCULABLE | NO_CALCULABLE | NO_CALCULABLE | referencia |
| proto_v3_min_translated | NO_CALCULABLE | NO_CALCULABLE | 224.83 | NO_CALCULABLE | 2.63 | referencia |
| proto_v3_state_translated | NO_CALCULABLE | NO_CALCULABLE | 253.03 | NO_CALCULABLE | 3.10 | referencia |
| proto_v3_hybrid_translated | NO_CALCULABLE | NO_CALCULABLE | 248.91 | NO_CALCULABLE | 3.72 | referencia |

## Que hipotesis sobrevivio

- Proto v3 hybrid sobrevivio parcialmente: mejoro frente a Proto v2 y quedo cerca de caveman, aunque no cumplio el criterio fuerte.

## Que hipotesis cayo

- Proto v3 min no redujo tokens frente a Proto v2.
- Proto v3 min no se acerco lo suficiente a caveman en tokens.
- Proto v3 state no mejoro manejo_estado frente a caveman.
- Proto v3 hybrid no cumplio el criterio fuerte de equilibrio.
- La traduccion por salida no queda justificada: agrega una llamada adicional y en esta tanda redujo fidelidad y utilidad.

## Errores

- No se registraron errores por fila.

## Limitaciones

- Evaluacion automatica, no humana.
- Un solo generador principal.
- El costo de traduccion por salida puede no representar traduccion por lote.
- Las tareas siguen siendo sinteticas.

## Conclusion parcial

Datos antes que entusiasmo: caveman siguio siendo el modo base mas barato. Proto v3 min y state no justificaron su costo. Proto v3 hybrid fue la mejor variante proto: no vencio a caveman, pero mejoro claramente frente a Proto v2 en tokens, fidelidad, utilidad, ambiguedad y perdida de informacion.

## Recomendacion para EXP04

C. Hybrid_Min
