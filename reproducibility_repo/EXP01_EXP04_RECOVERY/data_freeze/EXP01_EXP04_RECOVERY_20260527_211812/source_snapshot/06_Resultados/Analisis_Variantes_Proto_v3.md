# Analisis de variantes Proto v3

## proto_v3_min

- Tokens promedio: 370.87.
- Fidelidad: 3.69.
- Claridad: 2.69.
- Utilidad: 3.19.
- Ambiguedad: 2.21.
- Perdida de informacion: 2.19.
- Formato valido: 100.00%.

Lectura: cumplio formato, pero fue demasiado criptico y caro. No mejoro frente a Proto v2 ni se acerco a caveman.

## proto_v3_state

- Tokens promedio: 377.23.
- Manejo estado: 3.47.
- Fidelidad: 3.79.
- Claridad: 2.64.
- Utilidad: 3.17.
- Formato valido: 97.78%.

Lectura: agrego campos de estado, pero no supero a caveman en manejo de estado. La estructura extra no produjo valor suficiente.

## proto_v3_hybrid

- Tokens promedio: 266.78.
- Fidelidad: 4.46.
- Claridad: 4.43.
- Utilidad: 4.47.
- Ambiguedad: 1.52.
- Perdida de informacion: 1.60.
- Formato valido: 100.00%.

Lectura: fue la mejor variante proto. No vencio a caveman en tokens, pero quedo cerca y mejoro claramente frente a Proto v2 en costo y calidad.

## Comparacion entre variantes

- Modo base mas barato: caveman.
- Fila derivada mas barata: proto_v3_min_translated, pero no comparable como costo total porque exige una llamada proto previa.
- Mejor manejo de estado global: natural.
- Mejor claridad entre proto: proto_v3_hybrid.
- Mejor equilibrio entre proto: proto_v3_hybrid.

## Donde gana cada una

- proto_v3_min gana solo en formato compacto, no en tokens totales ni calidad.
- proto_v3_state gana en validez formal casi perfecta, pero no en estado.
- proto_v3_hybrid gana como direccion de diseno: menos formal, mas legible y con compacidad alta.

## Donde falla cada una

- proto_v3_min pierde demasiada claridad y utilidad.
- proto_v3_state agrega campos sin mejorar el manejo de estado.
- proto_v3_hybrid sigue usando 14.06% mas tokens que caveman.
- Las variantes traducidas no deben leerse como ahorro arquitectonico porque suman una llamada adicional.

## Reglas que deberian cambiar

- Abandonar proto_v3_min como candidato principal.
- Reducir state a un modo especializado solo para tareas con memoria real.
- Convertir hybrid en la rama principal de EXP04.
- Evaluar traduccion por lote, no traduccion por salida.

## Candidata para EXP04

C. Hybrid_Min
