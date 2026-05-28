# Conclusiones Experimento 03 Fusion

## Base de datos

- Filas: 720
- Errores: 0
- Llamadas HTTP: 1474

## Conclusiones basadas en datos

## Hipotesis que sobrevivieron

- Proto v3 hybrid sobrevivio parcialmente: mejoro frente a Proto v2 y quedo cerca de caveman, aunque no cumplio el criterio fuerte.

## Hipotesis que cayeron

- Proto v3 min no redujo tokens frente a Proto v2.
- Proto v3 min no se acerco lo suficiente a caveman en tokens.
- Proto v3 state no mejoro manejo_estado frente a caveman.
- Proto v3 hybrid no cumplio el criterio fuerte de equilibrio.
- La traduccion por salida no queda justificada: agrega una llamada adicional y en esta tanda bajo fidelidad y utilidad.

## Lectura

- Modo base mas barato: caveman.
- Fila derivada mas barata: proto_v3_min_translated, pero no debe leerse como costo total porque requiere generar primero proto_v3_min.
- Mejor fidelidad: natural.
- Mejor manejo de estado: natural.
- Mejor variante proto no traducida: proto_v3_hybrid.

## Recomendacion EXP04

C. Hybrid_Min
