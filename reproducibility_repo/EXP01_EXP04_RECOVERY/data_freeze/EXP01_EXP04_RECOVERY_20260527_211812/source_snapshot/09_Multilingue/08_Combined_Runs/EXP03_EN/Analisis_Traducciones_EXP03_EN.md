# Análisis de traducciones EXP03 EN

La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.

| language | proto_mode | proto_tokens | translated_tokens | architectural_total | clarity_proto | clarity_translated | fidelity_proto | fidelity_translated | reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| EN | proto_v3_min_core_en | 273.91 | 200.90 | 474.81 | 3.70 | 3.77 | 4.29 | 3.69 | extra_call;destroys_saving_vs_compressed |
| EN | proto_v3_state_core_en | 293.19 | 276.61 | 569.80 | 4.81 | 4.79 | 4.88 | 4.72 | extra_call;destroys_saving_vs_compressed |
| EN | proto_v3_hybrid_en | 199.81 | 229.77 | 429.58 | 4.93 | 4.79 | 4.89 | 4.67 | extra_call;destroys_saving_vs_compressed |
