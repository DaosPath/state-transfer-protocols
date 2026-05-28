# Prompts de Prueba

## Proposito

Guardar prompts iniciales para comparar los tres modos.

## Prompt comun de evaluacion

```txt
Evalua la salida segun fidelidad semantica, claridad, errores, perdida de informacion y traducibilidad. Usa escala 1-5. No inventes resultados.
```

## Modo A: lenguaje natural completo

```txt
You are an AI agent working with another AI agent. Please analyze the following task in detail, preserve all important constraints, identify risks, create a structured plan, and produce a clear final output for a human reader. Do not invent sources, data, or experimental results.
```

## Modo B: cavernicola

```txt
Agent task. Analyze. Keep constraints. Find risks. Make plan. Final human output clear. No fake sources/data/results.
```

## Modo C: protolenguaje

```txt
@TASK[TEST_MODE_C]
GOAL{analyze_task}
ACT{keep_constraints,detect_risks,make_plan}
LIMIT{no_fake_sources,no_fake_data,no_fake_results}
OUT{clear_human_final}
```

## Prompt de traduccion proto -> humano

```txt
Traduce el siguiente protolenguaje a lenguaje humano claro. No agregues informacion no presente. Marca incertidumbre si aparece CHK? o C baja.
```

## Prompt de compresion humano -> proto

```txt
Convierte el texto a protolenguaje. Preserva objetivo, contexto, restricciones, decisiones, riesgos, fuentes, datos numericos y salida esperada. Usa solo simbolos registrados.
```

## Riesgos o limitaciones

- Los prompts deben mantenerse equivalentes en contenido.
- El modo C puede necesitar ejemplos previos para modelos menos acostumbrados.

## Proximos pasos

- Ejecutar estos prompts con una tarea comun.
- Guardar conteos de tokens.
