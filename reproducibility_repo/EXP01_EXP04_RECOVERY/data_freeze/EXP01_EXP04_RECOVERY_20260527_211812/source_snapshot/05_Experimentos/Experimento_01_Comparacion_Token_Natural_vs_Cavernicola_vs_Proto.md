# Experimento 01: Comparacion Token Natural vs Cavernicola vs Proto

## Proposito

Disenar una prueba controlada para comparar consumo de tokens y calidad entre tres modos de comunicacion.

## Objetivo

Comparar:

- Modo A: lenguaje natural completo.
- Modo B: lenguaje reducido tipo cavernicola.
- Modo C: protolenguaje simbolico.

## Hipotesis

El modo C reducira tokens frente al modo A y posiblemente frente al modo B, manteniendo suficiente calidad y traducibilidad en tareas estructuradas.

## Tarea base propuesta

Un agente debe resumir un documento breve, extraer riesgos, proponer un plan y generar una salida final para usuario.

## Modo A: lenguaje natural completo

```txt
Please analyze the document carefully. Identify the main goal, summarize the relevant context, list the key risks, propose a practical plan, and produce a clear final answer for a human user. Do not invent sources or results.
```

## Modo B: cavernicola

```txt
Analyze doc. Find goal, context, risks. Make plan. Final answer clear. No fake sources. No fake results.
```

## Modo C: protolenguaje

```txt
@TASK[DOC_ANALYZE_01]
GOAL{analyze_doc}
ACT{extract_goal,ctx,risks,plan}
LIMIT{no_fake_sources,no_fake_results}
OUT{clear_human_final}
```

## Metricas

- Tokens de entrada.
- Tokens de salida.
- Claridad.
- Errores.
- Perdida de informacion.
- Facilidad de traduccion.
- Calidad final.

## Registro

Estado:

```txt
PENDIENTE_DE_EJECUCION
```

## Riesgos o limitaciones

- La comparacion debe usar mismo modelo y mismo contenido.
- La salida de cada modo puede variar por aleatoriedad.
- El conteo debe declarar tokenizer.

## Proximos pasos

- Ejecutar con al menos 3 tareas distintas.
- Registrar resultados en tabla.
