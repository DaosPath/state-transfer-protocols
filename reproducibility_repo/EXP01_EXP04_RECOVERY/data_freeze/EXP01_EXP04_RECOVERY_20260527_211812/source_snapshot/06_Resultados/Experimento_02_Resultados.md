# Experimento 02: Proto v2 vs Caveman

## Objetivo

Probar si Proto v2, con etiquetas minimas y menor sobrecarga estructural, reduce tokens frente a Proto v1 y puede acercarse o superar al modo caveman.

## Hipotesis

Un protolenguaje simbolico v2, con etiquetas minimas y diccionario compacto, puede acercarse o superar al modo caveman en consumo de tokens sin perder demasiada fidelidad semantica.

## Cambios respecto al Experimento 01

- Proto v1 no se ejecuto de nuevo; se usa como referencia historica.
- Proto v2 reemplaza etiquetas largas por `T/G/C/P/S/R/V/N`.
- Caveman usa formato `P/S/R/N`.
- DeepSeek V4 se ejecuto con `thinking: disabled`.

## Configuracion

- Endpoint usado: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo generador: `deepseek-v4-flash`
- Modelo generador fallback: `opencode-go/deepseek-v4-flash`
- Modelo evaluador: `deepseek-v4-pro`
- Modelo evaluador fallback: `deepseek-v4-flash`
- Tareas: 10
- Repeticiones: 3
- Temperatura: 0.2
- Max llamadas: 300
- Llamadas HTTP intentadas: 249
- Llamadas HTTP exitosas: 249
- Errores HTTP: 0
- Fecha: 2026-05-12T22:36:58.997478+00:00

## Piloto

```json
{
  "timestamp": "2026-05-12T22:16:13.519159+00:00",
  "task_id": "T001",
  "ok": true,
  "thinking_disabled_applied": true,
  "checks": [
    {
      "mode": "natural",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "latency_ms": 4504,
      "http_status": 200,
      "tokens_present": true,
      "token_count_method": null,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "comentario": "La respuesta aborda completamente la tarea, con solución concreta, riesgos y próximos pasos bien definidos, sin ambigüedad ni pérdida de información relevante."
      }
    },
    {
      "mode": "caveman",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "latency_ms": 3206,
      "http_status": 200,
      "tokens_present": true,
      "token_count_method": null,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "comentario": "La respuesta captura fielmente el problema, propone soluciones concretas, enumera riesgos y próximos pasos, todo con alta claridad y sin ambigüedad. La estructura es directa y fácil de traducir."
      }
    },
    {
      "mode": "proto_v2",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "latency_ms": 2988,
      "http_status": 200,
      "tokens_present": true,
      "token_count_method": null,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 4,
        "completitud": 4,
        "utilidad": 5,
        "ambiguedad": 2,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "comentario": "La respuesta captura fielmente el problema y propone una solución concreta, riesgos y próximos pasos. La estructura es clara aunque las abreviaturas (T, G, C, P, S, R, V, N) pueden ser ligeramente ambiguas sin contexto. La completitud es alta pero podría detallar más los riesgos. No hay pérdida de información relevante y es fácil de traducir a otros formatos."
      }
    },
    {
      "mode": "proto_v2_translated",
      "generation_ok": true,
      "model": "deepseek-v4-flash",
      "latency_ms": 2666,
      "http_status": 200,
      "tokens_present": true,
      "token_count_method": null,
      "evaluation_ok": true,
      "evaluator_model": "deepseek-v4-pro",
      "error": null,
      "evaluation_error": null,
      "evaluation": {
        "fidelidad_semantica": 5,
        "claridad": 5,
        "completitud": 5,
        "utilidad": 5,
        "ambiguedad": 1,
        "perdida_informacion": 1,
        "facilidad_traduccion": 5,
        "comentario": "La respuesta cubre todos los elementos solicitados (solución, riesgos, próximos pasos) de forma concisa y fiel al problema original."
      }
    }
  ]
}
```

## Tabla de resultados EXP02

| Modo | Filas | Errores | Tokens promedio | Ahorro vs natural | Ahorro vs caveman | Fidelidad | Claridad | Completitud | Ambiguedad | Perdida info | Utilidad | Latencia ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| natural | 30 | 0 | 354.63 | 0.00% | -47.19% | 4.93 | 5.00 | 4.57 | 1.03 | 1.03 | 4.93 | 4638 |
| caveman | 30 | 0 | 240.93 | 32.06% | 0.00% | 4.53 | 4.70 | 4.00 | 1.40 | 1.43 | 4.60 | 3052 |
| proto_v2 | 30 | 0 | 318.43 | 10.21% | -32.17% | 4.00 | 3.10 | 3.03 | 2.37 | 2.27 | 3.53 | 2777 |
| proto_v2_translated | 30 | 0 | 332.70 | 6.18% | -38.09% | 4.30 | 4.50 | 3.43 | 1.60 | 1.80 | 4.17 | 2570 |

## Comparacion con EXP01

| Comparacion | EXP01 tokens | EXP02 tokens | Cambio tokens | EXP01 fidelidad | EXP02 fidelidad | Lectura |
|---|---:|---:|---:|---:|---:|---|
| natural EXP02 vs natural EXP01 | 364.30 | 354.63 | -9.67 | 4.97 | 4.93 | menos tokens |
| caveman EXP02 vs caveman EXP01 | 263.97 | 240.93 | -23.04 | 4.97 | 4.53 | menos tokens |
| proto_v2 vs proto_v1 EXP01 | 377.13 | 318.43 | -58.70 | 4.87 | 4.00 | menos tokens |
| proto_v2_translated vs proto_v1_translated EXP01 | 438.87 | 332.70 | -106.17 | 4.57 | 4.30 | menos tokens |
| proto_v2 vs caveman EXP02 | 240.93 | 318.43 | 77.50 | 4.53 | 4.00 | mas tokens |
| proto_v2_translated vs caveman EXP02 | 240.93 | 332.70 | 91.77 | 4.53 | 4.30 | mas tokens |

## Analisis

- Modo mas barato EXP02: `caveman`.
- Proto v2 prometedor segun criterios: `False`.
- Proto v2 traducido aceptable segun criterios: `False`.
- Proto v2 debe evaluarse no solo por tokens, sino tambien por fidelidad, utilidad, ambiguedad y perdida de informacion.

## Errores

- No se registraron errores por fila.

## Conclusion parcial

Esta tanda exploratoria no demuestra la tesis por si sola. Si Proto v2 reduce tokens frente a Proto v1, eso indica que la sobrecarga estructural era parte del problema. Si caveman sigue ganando, el protocolo necesita una v3 aun mas compacta o una tarea donde la estructura aporte mas valor que costo. Si Proto v2 traducido sigue siendo caro, la arquitectura debe reservar traduccion solo para salidas finales realmente necesarias.

## Recomendacion para Experimento 03

- Probar Proto v3 sin todas las etiquetas obligatorias.
- Medir variantes `key:value` en una sola linea.
- Comparar tareas con mayor necesidad de estado y memoria.
- Agregar evaluacion humana de una muestra.
- Probar si un traductor final puede procesar lotes de Proto en una sola llamada.
