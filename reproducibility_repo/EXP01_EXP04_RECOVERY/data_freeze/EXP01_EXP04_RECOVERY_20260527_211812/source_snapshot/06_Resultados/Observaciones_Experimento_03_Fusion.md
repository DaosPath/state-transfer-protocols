# Observaciones Experimento 03 Fusion

## Patrones

- Modo base mas barato: caveman.
- Fila derivada mas barata: proto_v3_min_translated, pero no comparable como costo total porque requiere una llamada proto previa.
- Mejor calidad por fidelidad: natural.
- Mejor manejo de estado: natural.
- Mejor variante proto: proto_v3_hybrid.
- Las traducciones por salida no deben interpretarse como ahorro total: son llamadas adicionales.

## Ejemplos buenos

- proto_v3_min T001: `p=consumo_excesivo_tokens/agentes_verbosos;s=respuestas_estructuradas+limite_tokens_por_agente;r=perdida_contexto|rigidez;n=monitorear>ajustar_limites`
- proto_v3_state T001: `g=reducir_tokens;c=sistema_multiagente_explicaciones_largas;s=limitar_output_agentes_con_plantillas_compactas;r=pierde_coherencia_si_muy_breve;n=test_con_limite_50_palabras;conf=me`
- proto_v3_hybrid T001: `p: multi-agent token waste from verbose explanations  
s: enforce structured output templates + shared context buffer  
r: reduced flexibility, agent coordination overhead  
n: tes`

## Ejemplos malos

- proto_v3_state T019: `g=contexto_entre_agentes;p=límite_tokens;c=5_agentes;m=proto_v3_state; s=resumir_estado_clave_por_agente; a=transmitir_solo_k+m; r=pérdida_detalle; v=verificar_integridad_post_paso` notas=['field_count_gt_8']
- proto_v3_state T028: `g=comparar_arq_traduccion;p=latencia_vs_costo;c=traduccion_inmediata_vs_lote;k=inmediata=menor_latencia_mayor_costo;lote=menor_costo_mayor_riesgo_acumulacion;s=inmediata_para_tiemp` notas=['field_count_gt_8']

## Dudas

- El evaluador automatico puede premiar claridad humana sobre compresion operativa.
- La traduccion por salida puede inflar costo frente a traduccion por lote.
- La utilidad de estado debe revisarse manualmente en tareas T011-T020.
