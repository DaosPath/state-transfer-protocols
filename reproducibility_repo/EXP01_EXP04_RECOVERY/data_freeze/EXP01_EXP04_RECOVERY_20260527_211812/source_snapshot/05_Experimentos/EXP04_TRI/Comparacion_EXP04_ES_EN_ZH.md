# Comparación EXP04 ES EN ZH

| language | natural | compressed | compressed_state | hybrid_min | hybrid_state | best_token | best_state | best_balance |
|---|---:|---:|---:|---:|---:|---|---|---|
| ES | 491.98 | 303.40 | 292.70 | 259.01 | 324.86 | hybrid_min | hybrid_state | compressed |
| EN | 354.10 | 243.42 | 243.64 | 215.24 | 276.81 | hybrid_min | natural | hybrid_state |
| ZH | 312.58 | 233.04 | 244.01 | 216.83 | 262.00 | hybrid_min | natural | compressed |

| language | cheapest_mode | best_quality_mode | best_state_mode | best_continuity_mode | best_handoff_mode | best_balance_mode | reading |
|---|---|---|---|---|---|---|---|
| ES | hybrid_min | compressed | hybrid_state | compressed | compressed | compressed | hybrid_min gana costo |
| EN | hybrid_min | natural | natural | natural | natural | hybrid_state | hybrid_min gana costo |
| ZH | hybrid_min | compressed | natural | compressed | compressed | compressed | hybrid_min gana costo |
