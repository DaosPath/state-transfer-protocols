# Análisis de traducciones EXP03 ZH

La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.

| language | proto_mode | proto_tokens | translated_tokens | architectural_total | clarity_proto | clarity_translated | fidelity_proto | fidelity_translated | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| ZH | proto_v3_min_core_zh | 302.57 | 207.10 | 509.67 | 4.34 | 4.27 | 4.47 | 4.30 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_state_core_zh | 262.10 | 228.54 | 490.64 | 4.61 | 4.48 | 4.58 | 4.40 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_hybrid_zh | 211.36 | 200.13 | 411.49 | 4.69 | 4.56 | 4.59 | 4.48 | extra_call;destroys_saving_vs_compressed |
| ZH | proto_v3_zh_native | 262.70 | 171.06 | 433.76 | 3.88 | 4.38 | 4.20 | 4.31 | extra_call;destroys_saving_vs_compressed |
