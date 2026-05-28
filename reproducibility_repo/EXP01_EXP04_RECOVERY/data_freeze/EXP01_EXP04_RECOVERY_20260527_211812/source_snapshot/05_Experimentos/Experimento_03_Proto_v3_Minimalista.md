# Experimento 03: Proto v3 minimalista vs Caveman

## Objetivo

Comparar Proto v3 contra caveman y lenguaje natural para medir si una notacion minima puede ahorrar tokens sin perder demasiada calidad.

## Hipotesis

Proto v3 puede acercarse al consumo de tokens de caveman y podria superarlo en tareas con estado, memoria o seguimiento de riesgos.

## Modos a comparar

- `natural`
- `caveman`
- `proto_v3_min`
- `proto_v3_state`
- `proto_v3_hybrid`
- `proto_v3_translated` opcional

## Prompts de modo

### natural

```txt
Responde en español claro y completo. Explica el problema, solución, riesgos y siguiente paso. Mantén buena claridad humana.
```

### caveman

```txt
Responde ultra corto. Sin adornos. Frases simples. Mantén problema, solución, riesgos y siguiente paso. No expliques de más.

Formato:
Problema:
Solución:
Riesgo:
Siguiente:
```

### proto_v3_min

```txt
Responde usando Proto v3 mínimo. Una sola línea si puedes. Usa solo claves necesarias.

Diccionario:
p=problema
s=solución
r=riesgo
n=siguiente paso
g=objetivo
c=contexto
v=verificar
e=error
m=memoria
o=salida
conf=confianza

Ejemplo:
p=tokens_high; s=min_internal_code; r=ambig+loss; n=test_v3
```

### proto_v3_state

```txt
Responde usando Proto v3 con estado. Usa pocas claves. Preserva memoria, riesgo y siguiente acción.

Ejemplo:
g=reduce_tokens; c=multiagent; m=exp2_caveman_wins; s=v3_min; r=ambiguity; n=run_state_tasks
```

### proto_v3_hybrid

```txt
Responde con mezcla de lenguaje simple y claves compactas. Debe ser más legible que proto puro, pero más corto que lenguaje natural.

Ejemplo:
p: token waste high
s: min internal code
r: ambiguity, drift
n: test v3
```

### proto_v3_translated

```txt
Primero genera una salida Proto v3 mínima.
Luego tradúcela a español humano breve.
Mide si la traducción final aumenta demasiado el costo.

Formato:
PROTO:
...

HUMANO:
...
```

## Variables

- tokens de entrada;
- tokens de salida;
- tokens totales;
- fidelidad semantica;
- claridad;
- completitud;
- utilidad;
- ambiguedad;
- perdida de informacion;
- facilidad de traduccion;
- latencia;
- errores.

## Criterios de exito

Proto v3 sera prometedor si cumple al menos una de estas condiciones:

1. Usa menos tokens que caveman con calidad similar.
2. Usa tokens cercanos a caveman, pero mejora fidelidad o manejo de estado.
3. Usa mas tokens que caveman, pero reduce errores en tareas complejas.
4. Mejora claramente frente a Proto v2.

## Criterios de fracaso

Proto v3 fracasa si:

1. Usa muchos mas tokens que caveman.
2. Pierde demasiada claridad.
3. Aumenta ambiguedad.
4. Requiere traduccion constante.
5. La estructura pesa mas que el contenido.

## Tareas sugeridas

Usar tareas mas exigentes que en experimentos anteriores:

1. Resumir una decision y conservar riesgos.
2. Coordinar dos agentes con memoria compartida.
3. Reportar un error y proponer correccion.
4. Comprimir una instruccion larga.
5. Traducir una salida simbolica a lenguaje humano.
6. Mantener estado entre pasos.
7. Comparar alternativas.
8. Crear plan con restricciones.
9. Evaluar resultado previo.
10. Preparar siguiente accion.

## Recomendacion de interpretacion

No evaluar Proto v3 solo por tokens. Evaluar tambien:

- conserva significado;
- puede traducirse;
- reduce ambiguedad respecto a caveman;
- sirve mejor para memoria;
- sirve mejor para coordinacion multiagente;
- tiene menor costo que Proto v2;
- la estructura aporta algo o solo consume tokens.

## Resultado esperado

No asumir que Proto v3 ganara. El objetivo es descubrir si la estructura minima aporta valor real o si caveman sigue siendo superior.

## Estado

EJECUTADO.

## Resultado real EXP03 Fusion

La version ampliada se ejecuto con perfil FULL:

- 30 tareas.
- 3 repeticiones.
- 8 modos por tarea/repeticion.
- 720 filas JSONL.
- 1474 llamadas HTTP.
- 0 errores por fila.
- Modelo generador: `deepseek-v4-flash`.
- Modelo evaluador: `deepseek-v4-pro`.

Lectura principal:

- Caveman siguio siendo el modo base mas barato: 233.89 tokens promedio.
- Proto v3 min no mejoro frente a Proto v2: 370.87 tokens promedio y baja claridad.
- Proto v3 state no justifico su costo por manejo de estado.
- Proto v3 hybrid fue la mejor variante proto: 266.78 tokens, fidelidad 4.46, utilidad 4.47, formato valido 100%.
- Las traducciones por salida no deben leerse como ahorro total porque agregan una llamada adicional.

Resultado completo: `06_Resultados/Experimento_03_Fusion_Resultados.md`.

## Proximos pasos

- Preparar EXP04 como `Hybrid_Min`.
- Mantener caveman como baseline fuerte.
- Evaluar traduccion por lote solo si hay necesidad real de interfaz humana final.
