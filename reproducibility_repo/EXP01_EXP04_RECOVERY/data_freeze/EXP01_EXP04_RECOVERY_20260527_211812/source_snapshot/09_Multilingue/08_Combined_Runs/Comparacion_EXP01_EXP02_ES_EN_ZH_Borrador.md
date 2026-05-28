# Comparacion EXP01 EXP02 ES EN ZH Borrador

## Referencias ES reales

| language | experiment | mode | avg_tokens | fidelity | source |
|---|---|---|---:|---:|---|
| ES | EXP01 | caveman | 263.97 | 4.97 | EXP01_ES real |
| ES | EXP01 | natural | 364.30 | 4.97 | EXP01_ES real |
| ES | EXP01 | proto_v1 | 377.13 | 4.87 | EXP01_ES real |
| ES | EXP01 | proto_v1_translated | 438.87 | 4.57 | EXP01_ES real |
| ES | EXP02 | caveman | 240.93 | 4.53 | EXP02_ES real |
| ES | EXP02 | natural | 354.63 | 4.93 | EXP02_ES real |
| ES | EXP02 | proto_v2 | 318.43 | 4.00 | EXP02_ES real |
| ES | EXP02 | proto_v2_translated | 332.70 | 4.30 | EXP02_ES real |

## Datos EN/ZH ejecutados

| language | experiment | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | compactness |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EN | EXP01 | compressed_en | 30 | 0 | 82.00 | 89.27 | 171.27 | 4.97 | 4.97 | 4.97 | 1.03 | 1.17 | 4.97 | 5.00 |
| EN | EXP01 | natural_en | 30 | 0 | 73.00 | 152.77 | 225.77 | 4.97 | 5.00 | 4.97 | 1.00 | 1.17 | 5.00 | 3.87 |
| EN | EXP01 | proto_v1_en | 30 | 0 | 135.00 | 216.27 | 351.27 | 5.00 | 5.00 | 5.00 | 1.00 | 1.00 | 5.00 | 4.27 |
| EN | EXP01 | proto_v1_translated_en | 30 | 0 | 275.27 | 113.57 | 388.83 | 4.93 | 4.97 | 4.93 | 1.03 | 1.13 | 4.93 | 4.10 |
| EN | EXP02 | compressed_en | 30 | 0 | 82.00 | 95.00 | 177.00 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 4.97 | 4.87 |
| EN | EXP02 | natural_en | 30 | 0 | 73.00 | 154.17 | 227.17 | 5.00 | 5.00 | 5.00 | 1.00 | 1.17 | 5.00 | 3.67 |
| EN | EXP02 | proto_v2_en | 30 | 0 | 144.00 | 152.20 | 296.20 | 4.90 | 4.93 | 4.93 | 1.10 | 1.10 | 4.93 | 4.60 |
| EN | EXP02 | proto_v2_translated_en | 30 | 0 | 211.20 | 116.20 | 327.40 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 5.00 | 4.33 |
| ZH | EXP01 | compressed_zh | 30 | 0 | 104.20 | 82.03 | 186.23 | 4.87 | 4.93 | 4.87 | 1.07 | 1.33 | 4.83 | 5.00 |
| ZH | EXP01 | natural_zh | 30 | 0 | 67.20 | 132.63 | 199.83 | 4.93 | 5.00 | 5.00 | 1.00 | 1.07 | 4.97 | 4.40 |
| ZH | EXP01 | proto_v1_core_zh | 30 | 0 | 149.20 | 222.43 | 371.63 | 5.00 | 5.00 | 5.00 | 1.00 | 1.07 | 5.00 | 4.37 |
| ZH | EXP01 | proto_v1_translated_zh | 30 | 0 | 275.43 | 152.63 | 428.07 | 4.90 | 4.97 | 4.93 | 1.03 | 1.20 | 4.93 | 4.37 |
| ZH | EXP02 | compressed_zh | 30 | 0 | 104.20 | 81.67 | 185.87 | 4.80 | 4.87 | 4.80 | 1.13 | 1.30 | 4.80 | 5.00 |
| ZH | EXP02 | natural_zh | 30 | 0 | 67.20 | 138.07 | 205.27 | 5.00 | 5.00 | 5.00 | 1.00 | 1.13 | 4.97 | 4.27 |
| ZH | EXP02 | proto_v2_core_zh | 30 | 0 | 153.20 | 226.00 | 379.20 | 4.90 | 5.00 | 5.00 | 1.00 | 1.10 | 5.00 | 4.07 |
| ZH | EXP02 | proto_v2_translated_zh | 30 | 0 | 279.00 | 173.83 | 452.83 | 4.93 | 5.00 | 5.00 | 1.00 | 1.17 | 4.93 | 4.07 |

## Nota metodologica

Los datos ES se leen como referencia historica ya documentada en el proyecto. Los datos EN/ZH son los de esta corrida. No mezclar sin considerar idioma, tokenizer y prompts traducidos.