# Errores y Anomalías EXP04 TRI

- Filas: 1350
- Errores: 0
- Parse errors: 0
- Missing tokens: 0
- Fallos de formato: 7

- format:hybrid_min_too_many_fields: 2
- format:empty_field: 2
- format:compressed_too_field_dominant: 1
- format:compressed_state_too_many_fields: 1
- format:hybrid_state_zh_too_long: 1

### Ejemplos
- EN T001 hybrid_min_en: notes=['hybrid_min_too_many_fields']
- ZH T003 hybrid_state_zh: notes=['empty_field']
- EN T006 hybrid_min_en: notes=['hybrid_min_too_many_fields']
- ES T008 compressed_es: notes=['compressed_too_field_dominant']
- EN T008 compressed_state_en: notes=['compressed_state_too_many_fields']
- EN T008 hybrid_state_en: notes=['empty_field']
- ZH T030 hybrid_state_zh: notes=['hybrid_state_zh_too_long']
