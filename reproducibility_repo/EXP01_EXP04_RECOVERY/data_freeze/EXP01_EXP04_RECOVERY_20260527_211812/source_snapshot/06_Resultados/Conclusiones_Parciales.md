# Conclusiones Parciales

## Proposito

Registrar conclusiones parciales basadas solo en datos reales del proyecto.

## Estado

ACTUALIZADO_CON_EXP04_TRI_Y_EXP05_PARTE_1.

## Base empirica usada

- EXP01/EXP02 ES: referencia historica documentada en resultados.
- EXP01/EXP02 EN/ZH: corrida combinada multilingue con 30 filas por modo.
- EXP03 ES/EN/ZH: comparacion de natural, compressed y proto_v3.
- EXP04_TRI ES/EN/ZH: 1350 filas, 2810 llamadas HTTP, 0 errores HTTP, 0 parse errors, 7 fallos de formato.
- EXP05_PREMIUM_MULTIMODEL_TRILINGUAL Parte 1: 450 generaciones OK, 450 evaluaciones OK, 450 JSON validos, 0 fallbacks finales de evaluacion; generadores Grok, Gemini, Llama, Qwen y GLM; evaluador final Gemini Vertex.

## Conclusion parcial actual

La hipotesis fuerte no queda validada en forma general: un protolenguaje simbolico no supera de manera robusta a la compresion textual simple. La evidencia actual favorece una conclusion mas precisa:

> La comunicacion comprimida entre agentes puede reducir tokens de forma consistente, pero la mejor estrategia depende del objetivo: costo, calidad, continuidad, preservacion de estado o handoff.

EXP05 Parte 1 refuerza esa reformulacion y agrega una condicion nueva: la estrategia tambien depende del modelo generador y de su configuracion tecnica. `hybrid_state` aparece como mejor protocolo operativo comprimido en esta particion, mientras `compressed` conserva valor como baseline robusto. `hybrid_min` no debe presentarse como ganador general: en EXP04 era barato; en EXP05 Parte 1 vuelve a mostrar perdida de calidad relativa.

## Hallazgos principales

1. `compressed` es el modo mas estable como balance calidad/costo en ES y ZH.
2. `hybrid_min` es el modo mas barato en EXP04_TRI para ES, EN y ZH, pero no gana calidad ni estado.
3. `hybrid_state` mejora preservacion de estado en ES y EN, aunque aumenta costo frente a `compressed`.
4. EN conserva ventaja fuerte para `natural` en calidad, estado y continuidad.
5. ZH penaliza mas los formatos hibridos minimos: baja costo, pero tambien baja claridad, fidelidad y recuperabilidad.
6. Los protocolos proto_v1/proto_v2/proto_v3 no deben presentarse como ganadores generales; sirven mas como laboratorio de estructura que como solucion final de costo.
7. En EXP05 Parte 1, `hybrid_state` supera a `compressed` en preservacion de estado y continuidad operativa, manteniendo compactness alta.
8. En EXP05 Parte 1, `compressed` sigue siendo baseline fuerte y mas universal que `hybrid_min`.
9. Gemini como generador en EXP05 Parte 1 no es interpretable como derrota semantica del modelo: hay evidencia de truncamiento tecnico por presupuesto de razonamiento oculto.
10. ZH no se degrada en EXP05 Parte 1; la lectura multilingue queda abierta y merece repeticion balanceada.

## Datos clave EXP04_TRI

| Idioma | Modo mas barato | Mejor calidad | Mejor estado | Mejor continuidad | Mejor handoff | Mejor balance |
|---|---|---|---|---|---|---|
| ES | hybrid_min | compressed | hybrid_state | compressed | compressed | compressed |
| EN | hybrid_min | natural | natural | natural | natural | hybrid_state |
| ZH | hybrid_min | compressed | natural | compressed | compressed | compressed |

Tokens promedio:

| Idioma | natural | compressed | compressed_state | hybrid_min | hybrid_state |
|---|---:|---:|---:|---:|---:|
| ES | 491.98 | 303.40 | 292.70 | 259.01 | 324.86 |
| EN | 354.10 | 243.42 | 243.64 | 215.24 | 276.81 |
| ZH | 312.58 | 233.04 | 244.01 | 216.83 | 262.00 |

## Lectura comparativa EXP03 vs EXP04

EXP03 ya mostraba que `compressed` era dificil de superar:

| Idioma | EXP03 natural | EXP03 compressed | EXP03 proto_hybrid | Mejor token |
|---|---:|---:|---:|---|
| ES | 324.54 | 233.89 | 266.78 | compressed |
| EN | 228.06 | 188.98 | 199.81 | compressed_en |
| ZH | 195.54 | 194.86 | 211.36 | compressed_zh |

EXP04 confirma el patron: las variantes hibridas son utiles, pero el protocolo minimo no desplaza a `compressed` como mejor equilibrio. Su valor principal es economico.

## Lectura EXP05 Parte 1

Resultados por modo en escala 1-5, donde `ambiguity` e `information_loss` son negativas:

| Modo | n | Fidelity | Utility | State | Continuity | Compactness | Ambiguity | Info Loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| natural | 120 | 4.050 | 4.017 | 4.000 | 4.017 | 4.150 | 1.633 | 1.933 |
| compressed | 110 | 3.927 | 3.964 | 3.918 | 4.036 | 4.591 | 1.791 | 2.145 |
| hybrid_min | 110 | 3.564 | 3.591 | 3.555 | 3.609 | 4.518 | 2.291 | 2.491 |
| hybrid_state | 110 | 3.955 | 4.018 | 4.091 | 4.082 | 4.645 | 1.882 | 2.018 |

Lectura prudente:

- `hybrid_state` es el mejor candidato operativo comprimido de Parte 1: conserva estado y continuidad mejor que `compressed`, sin perder compactness.
- `compressed` no queda descartado; funciona como baseline robusto y menos formal.
- `hybrid_min` no valida la hipotesis de que menor estructura basta; su compactness viene con perdida de fidelidad, utilidad, continuidad y mayor ambiguedad.
- `natural` sigue fuerte en fidelidad y baja ambiguedad, pero no ofrece la eficiencia estructural de los modos comprimidos.
- La Parte 1 no autoriza conclusion final por no cubrir toda la matriz y por la anomalia de Gemini generador.

Resultados por generador:

| Generador | n | Fidelity | Utility | State | Continuity | Compactness | Ambiguity | Info Loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| grok_4_20_non_reasoning | 90 | 4.767 | 4.711 | 4.789 | 4.789 | 4.944 | 1.156 | 1.167 |
| qwen3_next_80b_instruct | 90 | 4.656 | 4.722 | 4.689 | 4.744 | 4.922 | 1.122 | 1.322 |
| glm_5 | 90 | 4.600 | 4.644 | 4.589 | 4.656 | 4.944 | 1.133 | 1.433 |
| llama_4_maverick | 90 | 4.156 | 4.300 | 4.256 | 4.389 | 4.778 | 1.533 | 1.900 |
| gemini_3_1_pro_preview | 90 | 1.211 | 1.122 | 1.144 | 1.111 | 2.756 | 4.522 | 4.889 |

El bloque Gemini generador debe marcarse como condicion tecnica contaminada. Sus salidas tuvieron promedio visible de 16.6 tokens frente a 62.9-84.4 en otros generadores, compatible con truncamiento por razonamiento oculto y presupuesto de salida insuficiente.

## Reformulacion de tesis

La tesis debe abandonar la idea de un "protolenguaje ganador" unico. Formulacion mas defendible:

> Los agentes de IA no necesitan comunicarse siempre en lenguaje natural completo. Pueden operar con registros comprimidos, pero el registro optimo no es universal: depende de la tarea, idioma, tokenizer, necesidad de estado y tolerancia a perdida semantica.

Tras EXP05 Parte 1, agregar: depende tambien del modelo generador, del evaluador y de la configuracion de presupuesto visible/razonamiento.

## Limitaciones

- Evaluacion automatica.
- Un solo pipeline principal para EXP04_TRI.
- Muestra aun pequena por modo/idioma cuando se separa por grupo de tarea.
- No hay validacion humana independiente de recuperabilidad.
- No se ha probado robustez multi-modelo.
- La robustez multimodelo empezo a probarse en EXP05, pero solo con una particion; falta matriz completa y auditoria de juez.
- Gemini generador en EXP05 Parte 1 esta contaminado por truncamiento tecnico probable.
- Comparacion multilingue afectada por tokenizacion, traduccion y localizacion cultural del protocolo.

## Proximos pasos

- Completar EXP05 y separar analisis por parte, modelo, idioma, modo y tarea.
- Repetir condicion Gemini generador con mayor `max_tokens` o menor razonamiento visible/oculto si la API lo permite.
- Mantener dos rutas: `compressed` para tareas simples y `hybrid_state` para memoria/handoff.
- Agregar evaluacion humana ciega sobre recuperabilidad y perdida semantica.
- Repetir EXP04_TRI con otro modelo y mismo banco de tareas.
- Medir costo de decodificacion: tokens ahorrados por el emisor vs esfuerzo del receptor.
- Tratar ZH nativo como rama propia, no como simple traduccion de ES/EN.
