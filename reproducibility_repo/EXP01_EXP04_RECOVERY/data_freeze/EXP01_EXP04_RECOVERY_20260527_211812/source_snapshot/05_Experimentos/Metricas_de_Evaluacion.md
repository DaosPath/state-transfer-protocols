# Metricas de Evaluacion

## Proposito

Definir metricas para comparar modos de comunicacion.

## Metricas principales

| Metrica | Definicion | Medicion inicial |
|---|---|---|
| Ahorro de tokens | Reduccion frente a baseline natural | `(tokens_A - tokens_modo) / tokens_A` |
| Fidelidad semantica | Conserva significado esencial | Rubrica 1-5 |
| Claridad final | Salida humana entendible | Rubrica 1-5 |
| Tasa de error | Errores por tarea | Conteo y tipo |
| Estabilidad entre pasos | Conserva simbolos y significado | Rubrica 1-5 |
| Recuperabilidad humana | Humano puede auditar mensaje | Rubrica 1-5 |
| Traducibilidad | Proto puede pasar a lenguaje humano | Rubrica 1-5 |
| Perdida de informacion | Datos criticos omitidos | Conteo |

## Errores a clasificar

- Omision de objetivo.
- Omision de restriccion.
- Fuente inventada.
- Resultado inventado.
- Simbolo no definido.
- Traduccion infiel.
- Ambiguedad no marcada.
- Deriva de etiqueta.

## Umbrales iniciales propuestos

Estos umbrales son criterios de trabajo, no resultados:

- Ahorro minimo interesante: 20%.
- Fidelidad aceptable: 4/5.
- Claridad final aceptable: 4/5.
- Error critico permitido: 0.

## Riesgos o limitaciones

- Los umbrales deben ajustarse segun tarea.
- Un promedio alto puede ocultar errores criticos.

## Proximos pasos

- Crear hoja de evaluacion por experimento.
