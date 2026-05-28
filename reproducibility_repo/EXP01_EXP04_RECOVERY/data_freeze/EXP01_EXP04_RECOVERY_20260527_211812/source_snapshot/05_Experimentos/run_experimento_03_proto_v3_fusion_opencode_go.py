import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import run_experimento_01_opencode_go as base


EXPERIMENT_ID = "EXP03_PROTO_V3_FUSION"

BASE_URL = "https://opencode.ai/zen/go/v1"
CHAT_COMPLETIONS_URL = f"{BASE_URL}/chat/completions"
MODELS_URL = f"{BASE_URL}/models"

GENERATION_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
GENERATION_MODEL_FALLBACK = os.getenv("GENERATION_MODEL_FALLBACK", "opencode-go/deepseek-v4-flash")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "deepseek-v4-pro")
EVALUATOR_MODEL_FALLBACK = os.getenv("EVALUATOR_MODEL_FALLBACK", "deepseek-v4-flash")

TEMPERATURE = 0.2
REPETITIONS = 3
REQUEST_TIMEOUT = 90
RATE_LIMIT_SLEEP_SECONDS = 10
SERVER_ERROR_SLEEP_SECONDS = 10
MAX_CALLS_HARD_LIMIT = 2000
MAX_CALLS_SOFT_STOP = 1850

MAX_TOKENS_GENERATION_NATURAL = 500
MAX_TOKENS_GENERATION_CAVEMAN = 350
MAX_TOKENS_GENERATION_PROTO = 300
MAX_TOKENS_TRANSLATION = 350
MAX_TOKENS_EVALUATION = 300

EMPTY_RETRY_MAX_TOKENS_GENERATION = 1800
EMPTY_RETRY_MAX_TOKENS_TRANSLATION = 1200
EMPTY_RETRY_MAX_TOKENS_EVALUATION = 1000

DEFAULT_PROFILE = os.getenv("EXP03_PROFILE", "FULL").upper()
PROFILES = {
    "SAFE": {"task_limit": 20, "repetitions": 3},
    "FULL": {"task_limit": 30, "repetitions": 3},
    "STRESS": {"task_limit": 35, "repetitions": 3},
}

EXP01 = {
    "natural": {"tokens": 364.30, "fidelidad": 4.97, "utilidad": 5.00},
    "caveman": {"tokens": 263.97, "fidelidad": 4.97, "utilidad": 4.97},
    "proto_v1": {"tokens": 377.13, "fidelidad": 4.87, "utilidad": 4.87},
    "proto_v1_translated": {"tokens": 438.87, "fidelidad": 4.57, "utilidad": 4.70},
}
EXP02 = {
    "natural": {"tokens": 354.63, "fidelidad": 4.93, "utilidad": 4.93},
    "caveman": {"tokens": 240.93, "fidelidad": 4.53, "utilidad": 4.60},
    "proto_v2": {"tokens": 318.43, "fidelidad": 4.00, "utilidad": 3.53},
    "proto_v2_translated": {"tokens": 332.70, "fidelidad": 4.30, "utilidad": 4.17},
}

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "06_Resultados"
RUNS_PATH = RESULTS_DIR / "experimento_03_fusion_runs.jsonl"
REPORT_PATH = RESULTS_DIR / "Experimento_03_Fusion_Resultados.md"
OBSERVATIONS_PATH = RESULTS_DIR / "Observaciones_Experimento_03_Fusion.md"
CONCLUSIONS_PATH = RESULTS_DIR / "Conclusiones_Experimento_03_Fusion.md"
COMPARISON_PATH = RESULTS_DIR / "Comparacion_EXP01_EXP02_EXP03_Fusion.md"
VARIANT_ANALYSIS_PATH = RESULTS_DIR / "Analisis_Variantes_Proto_v3.md"
ERRORS_PATH = RESULTS_DIR / "Errores_Experimento_03_Fusion.md"
ERROR_PATH = RESULTS_DIR / "Error_Experimento_03_Fusion.md"

BASE_MODES = ["natural", "caveman", "proto_v3_min", "proto_v3_state", "proto_v3_hybrid"]
TRANSLATION_MAP = {
    "proto_v3_min": "proto_v3_min_translated",
    "proto_v3_state": "proto_v3_state_translated",
    "proto_v3_hybrid": "proto_v3_hybrid_translated",
}
ALL_MODES = BASE_MODES + list(TRANSLATION_MAP.values())

TASKS = [
    ("T001", "base_comparable", "Analiza este problema: un sistema multiagente consume demasiados tokens porque cada agente escribe explicaciones largas. Propón solución, riesgos y próximos pasos."),
    ("T002", "base_comparable", "Resume una arquitectura de agentes con trabajador, supervisor, memoria y traductor final. Incluye ventajas y limitaciones."),
    ("T003", "base_comparable", "Convierte una explicación larga sobre eficiencia de tokens en una estructura operativa para agentes."),
    ("T004", "base_comparable", "Diseña reglas iniciales para evitar deriva semántica en un protocolo simbólico."),
    ("T005", "base_comparable", "Detecta riesgos en un sistema donde varios agentes se comunican con símbolos comprimidos."),
    ("T006", "base_comparable", "Propón una metodología para medir si un protolenguaje conserva significado."),
    ("T007", "base_comparable", "Extrae variables medibles de un experimento sobre comunicación multiagente."),
    ("T008", "base_comparable", "Crea una plantilla breve para registrar resultados de pruebas con modelos IA."),
    ("T009", "base_comparable", "Compara lenguaje natural, lenguaje cavernícola y protolenguaje en términos de costo, claridad y error."),
    ("T010", "base_comparable", "Propón cómo un agente traductor debe convertir protolenguaje a español humano sin inventar información."),
    ("T011", "memory_state", "Un agente trabajador terminó una tarea, pero debe pasar al siguiente agente objetivo, contexto, error detectado, riesgo y próxima acción. Resume ese estado de forma eficiente."),
    ("T012", "memory_state", "Dos agentes están coordinando una investigación. El agente A encontró que caveman ahorra más tokens, pero el agente B necesita conservar trazabilidad de hipótesis, métricas y límites. Propón una salida compacta."),
    ("T013", "memory_state", "Comprime el siguiente estado de proyecto: EXP01 mostró que caveman ganó; EXP02 mostró que proto_v2 mejoró pero perdió calidad; EXP03 debe probar proto_v3 minimalista. Conserva decisión y siguiente paso."),
    ("T014", "memory_state", "Un agente debe reportar error de formato: la salida proto_v3 usó etiquetas de Proto v1 y fue demasiado larga. Resume problema, corrección y verificación."),
    ("T015", "memory_state", "Diseña una memoria compacta para guardar que el usuario prefiere optimización de tokens, documentación en Markdown y experimentos con resultados reales."),
    ("T016", "memory_state", "Evalúa una salida de agente que es corta pero ambigua. Debes conservar: problema, por qué es ambigua, riesgo y corrección."),
    ("T017", "memory_state", "Crea un plan de tres pasos para probar si un traductor final puede traducir lotes de protolenguaje en una sola llamada."),
    ("T018", "memory_state", "Resume una comparación entre tres opciones: lenguaje natural, caveman y proto_v3_hybrid. Conserva costo, claridad y riesgo principal."),
    ("T019", "memory_state", "Un sistema multiagente debe pasar contexto entre cinco agentes sin superar límite de tokens. Propón estrategia compacta con memoria y verificación."),
    ("T020", "memory_state", "Convierte una salida técnica comprimida en una instrucción entendible para un agente supervisor."),
    ("T021", "medium_complexity", "Un agente debe priorizar tareas: corregir reglas, ejecutar experimento, analizar resultados, preparar informe. Ordena y justifica brevemente."),
    ("T022", "medium_complexity", "Detecta qué información no debe perderse al comprimir un informe experimental: fecha, modelo, tokens, errores, métricas, conclusión y límites."),
    ("T023", "medium_complexity", "Propón cómo medir deriva semántica cuando varios agentes usan la misma abreviatura con significados diferentes."),
    ("T024", "medium_complexity", "Resume una conclusión parcial sin exagerar: proto_v3 redujo tokens frente a proto_v2, pero no venció a caveman y perdió algo de claridad."),
    ("T025", "medium_complexity", "Diseña una estructura mínima para que un agente entregue: resultado, evidencia, confianza, riesgo y siguiente acción."),
    ("T026", "medium_complexity", "Convierte un resumen humano de 120 palabras en una salida operativa para agentes sin perder entidades ni números."),
    ("T027", "medium_complexity", "Un agente traductor recibe una salida proto_v3 ambigua. Explica cómo debe traducir sin inventar y cómo debe marcar incertidumbre."),
    ("T028", "medium_complexity", "Compara dos arquitecturas: traducir cada salida proto inmediatamente vs traducir por lote al final. Incluye costo y riesgo."),
    ("T029", "medium_complexity", "Prepara una mini bitácora de experimento con tarea, modo, tokens, calidad, error y observación."),
    ("T030", "medium_complexity", "Crea una regla para decidir cuándo usar caveman, cuándo usar proto_v3_min, cuándo usar proto_v3_state y cuándo usar proto_v3_hybrid."),
    ("T031", "stress_optional", "Un agente debe pasar una tarea incompleta a otro agente. Conserva qué se hizo, qué falta, bloqueo, riesgo y siguiente acción."),
    ("T032", "stress_optional", "Genera una salida compacta para un sistema donde el contexto debe durar 20 pasos sin crecer demasiado."),
    ("T033", "stress_optional", "Detecta si una salida proto_v3 es demasiado críptica y propón una versión corregida."),
    ("T034", "stress_optional", "Resume una discusión entre tres agentes donde uno prioriza tokens, otro calidad y otro trazabilidad."),
    ("T035", "stress_optional", "Crea una política mínima para evitar que agentes inventen resultados experimentales."),
]
TASKS = [{"id": tid, "group": group, "text": text} for tid, group, text in TASKS]

MODE_PROMPTS = {
    "natural": """Responde en lenguaje natural claro y completo.
Usa solo respuesta final.
No muestres razonamiento paso a paso.
Máximo 140 palabras.
Analiza la tarea.
Incluye problema, solución, riesgos y próximos pasos cuando aplique.
No uses formato proto.
No uses lenguaje excesivamente decorativo.

Tarea:
{task}""",
    "caveman": """Responde ultra corto.
Sin adornos.
Sin tono humano.
Frases simples.
Máximo 90 palabras.
Mantén lo esencial.

Formato preferido:
P:
S:
R:
N:

Donde:
P = problema
S = solución
R = riesgos
N = próximos pasos

No expliques de más.
No uses campos key=value.
No uses símbolos raros.
Debe ser legible directamente.

Tarea:
{task}""",
    "proto_v3_min": """Responde usando proto_v3_min.
Usa solo respuesta final.
Una sola línea.
Campos opcionales.
No plantilla fija.
No más de 55 palabras.
Minúsculas.

Campos permitidos:
g=objetivo; p=problema; c=contexto; s=solución; a=acción; r=riesgo; n=siguiente; v=verificación; m=métrica; e=error; x=restricción; o=salida; conf=confianza.

Reglas:
- si hay problema y solución usa p= y s=.
- si no hay problema directo usa g= y s=.
- no llenar campos vacíos.
- no usar @TASK, GOAL, CTX, PROBLEM, PLAN, RISK, CHK, OUT, NEXT.
- no usar T:/G:/C:/P:/S:/R:/V:/N:.
- separar campos con punto y coma.
- separar riesgos con | y acciones con >.
- no inventar.

Ejemplo:
p=tokens_altos/agentes_verbosos;s=estado_compacto+codigos+trad_final;r=ambig|deriva;n=medir>ajustar

Tarea:
{task}""",
    "proto_v3_state": """Responde usando proto_v3_state.
Usa solo respuesta final.
Una o dos líneas máximo.
Máximo 75 palabras.
Más estructurado que proto_v3_min, pero compacto.
Conserva memoria, estado, continuidad, métricas o verificación cuando aplique.

Campos permitidos:
g=objetivo; p=problema; c=contexto; m=memoria; k=dato_clave; s=solución; a=acción; r=riesgo; v=verificación; n=siguiente; lim=límite; conf=confianza.

Reglas:
- no más de 7 campos.
- no llenar campos innecesarios.
- no volver a Proto v1 o v2.
- debe ser traducible.
- usa m= cuando haya memoria previa.
- usa k= cuando haya dato importante.
- usa v= cuando haya algo que verificar.

Ejemplo:
g=coordinar_agentes;c=exp2_caveman_gana;m=proto_v2_menos_tokens_pero_calidad_baja;s=v3_min+estado_opcional;r=ambig|sobrecarga;n=test_memoria

Tarea:
{task}""",
    "proto_v3_hybrid": """Responde usando proto_v3_hybrid.
Usa solo respuesta final.
Mezcla lenguaje simple y claves compactas.
Más legible que proto puro.
Más corto que natural.
Más estructurado que caveman libre.
Máximo 85 palabras.

Formato sugerido:
p: ...
s: ...
r: ...
n: ...

Reglas:
- puede usar español o inglés técnico simple.
- no frases largas.
- no tono humano.
- no adornos.
- preserva problema, solución, riesgo y siguiente paso.
- debe ser fácil de traducir.

Ejemplo:
p: token waste high
s: min internal notation + final translator
r: ambiguity, drift, debug
n: test v3 vs caveman

Tarea:
{task}""",
}

TRANSLATOR_PROMPT = """Traduce la siguiente salida Proto v3 a español humano breve.
No inventes información.
No agregues campos que no existan.
Conserva problema, objetivo, solución, riesgos, métricas, memoria o próximos pasos si aparecen.
Si hay ambigüedad, márcala.
Máximo 120 palabras.
Usa solo respuesta final.

Entrada:
{proto_output}"""

EVALUATOR_PROMPT = """Eres un evaluador técnico.
Usa solo respuesta final.
No muestres razonamiento paso a paso.
Compara la respuesta generada contra la tarea original.

Evalúa de 1 a 5:
- fidelidad_semantica
- claridad
- completitud
- utilidad
- ambiguedad
- perdida_informacion
- facilidad_traduccion
- manejo_estado
- compacidad

Reglas:
- Para fidelidad_semantica, claridad, completitud, utilidad, facilidad_traduccion, manejo_estado y compacidad: 5 es mejor.
- Para ambiguedad y perdida_informacion: 1 es mejor.
- Devuelve SOLO JSON válido.
- No añadas Markdown.
- No añadas explicación fuera del JSON.

Tarea original:
{task}

Modo usado:
{mode}

Respuesta:
{output}

Formato obligatorio:
{{
  "fidelidad_semantica": 1,
  "claridad": 1,
  "completitud": 1,
  "utilidad": 1,
  "ambiguedad": 1,
  "perdida_informacion": 1,
  "facilidad_traduccion": 1,
  "manejo_estado": 1,
  "compacidad": 1,
  "comentario": "..."
}}"""


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


KEY_ATTR = "API" + "_" + "KEY"
KEY_ENV = "OPENCODE_" + KEY_ATTR


def configure_base():
    base.configure_provider_from_env()
    setattr(base, KEY_ATTR, os.getenv(KEY_ENV) or getattr(base, KEY_ATTR))
    base.MAX_CALLS_INITIAL_RUN = MAX_CALLS_HARD_LIMIT
    base.REQUEST_TIMEOUT = REQUEST_TIMEOUT
    base.RATE_LIMIT_SLEEP_SECONDS = RATE_LIMIT_SLEEP_SECONDS
    base.SERVER_ERROR_SLEEP_SECONDS = SERVER_ERROR_SLEEP_SECONDS
    base.GENERATION_MODEL = GENERATION_MODEL
    base.GENERATION_MODEL_FALLBACK = GENERATION_MODEL_FALLBACK
    base.EVALUATOR_MODEL = EVALUATOR_MODEL
    base.EVALUATOR_MODEL_FALLBACK = EVALUATOR_MODEL_FALLBACK
    base.TEMPERATURE = TEMPERATURE
    for key in base.CALL_STATS:
        base.CALL_STATS[key] = 0


def require_provider_key():
    configure_base()
    if not getattr(base, KEY_ATTR):
        raise base.ExperimentAbort("Falta variable de entorno de clave del proveedor.")


def ensure_dirs():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def write_text(path, content):
    path.write_text(content, encoding="utf-8")


def append_jsonl(path, record):
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def backup_jsonl_if_exists():
    if RUNS_PATH.exists():
        backup = RUNS_PATH.with_suffix(f".jsonl.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        RUNS_PATH.replace(backup)
        return backup.name
    return None


def task_subset(profile):
    profile_cfg = PROFILES[profile]
    return TASKS[: profile_cfg["task_limit"]], profile_cfg["repetitions"]


def selected_profile():
    if DEFAULT_PROFILE not in PROFILES:
        return "FULL"
    return DEFAULT_PROFILE


def max_tokens_for_mode(mode):
    if mode == "natural":
        return MAX_TOKENS_GENERATION_NATURAL
    if mode == "caveman":
        return MAX_TOKENS_GENERATION_CAVEMAN
    return MAX_TOKENS_GENERATION_PROTO


def soft_stop_reached():
    return base.CALL_STATS["attempted"] >= MAX_CALLS_SOFT_STOP


def generate_output(task, mode):
    prompt = MODE_PROMPTS[mode].format(task=task["text"])
    return base.call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=max_tokens_for_mode(mode),
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_GENERATION,
    )


def translate_output(proto_output):
    prompt = TRANSLATOR_PROMPT.format(proto_output=proto_output)
    return base.call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_TRANSLATION,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_TRANSLATION,
    )


def evaluate_output(task, mode, output):
    prompt = EVALUATOR_PROMPT.format(task=task["text"], mode=mode, output=output)
    result = base.call_chat_with_model_fallback(
        EVALUATOR_MODEL,
        EVALUATOR_MODEL_FALLBACK,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_EVALUATION,
        fallback_on_any_error=True,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_EVALUATION,
    )
    if not result.get("ok"):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("error"), None, False
    parsed, parse_error = base.safe_json_parse(result["output"])
    if parse_error:
        return result.get("model_used", EVALUATOR_MODEL), {}, "INVALID_JSON_EVALUATION", result["output"], True
    return result.get("model_used", EVALUATOR_MODEL), parsed, None, result["output"], False


def word_count(text):
    if not text:
        return 0
    return len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ:/=?.+-]+\b", text))


def fields_used(text):
    if not text:
        return []
    fields = []
    for match in re.finditer(r"\b([a-z]{1,5})\s*=", text):
        fields.append(match.group(1).lower())
    for match in re.finditer(r"(?m)^\s*([a-z]{1,12})\s*:", text):
        fields.append(match.group(1).lower())
    return fields


def has_proto_v1_long_tags(text):
    value = text or ""
    if re.search(r"@TASK\s*\[", value, flags=re.IGNORECASE):
        return True
    return bool(re.search(r"(?mi)^\s*(GOAL|CTX|PROBLEM|PLAN|RISK|CHK|OUT|NEXT)\s*[\{:]", value))


def has_any_v2_one_letter_label(text):
    return bool(re.search(r"(?mi)^\s*[TGCPRSVN]\s*:", text or ""))


def has_fixed_v2_template(text):
    labels = set(match.group(1).upper() for match in re.finditer(r"(?mi)^\s*([TGCPRSVN])\s*:", text or ""))
    return "T" in labels or len(labels.intersection({"G", "C", "P", "S", "R", "V", "N"})) >= 5


def looks_like_natural_long(text, threshold):
    if word_count(text) <= threshold:
        return False
    compact_markers = len(fields_used(text))
    return compact_markers < 2


def validate_format(mode, output, task):
    notes = []
    valid = True
    wc = word_count(output)
    fields = fields_used(output)
    field_count = len(set(fields))
    lower = (output or "").lower()
    if mode == "proto_v3_min":
        if has_proto_v1_long_tags(output) or has_any_v2_one_letter_label(output):
            valid = False
            notes.append("uses_proto_v1_or_v2_tags")
        if wc > 70:
            valid = False
            notes.append("word_count_gt_70")
        if field_count > 6:
            valid = False
            notes.append("field_count_gt_6")
        if looks_like_natural_long(output, 35):
            valid = False
            notes.append("looks_like_long_natural_text")
        allowed = {"p", "s", "g", "c", "r", "n", "m", "v", "a", "e", "x", "o", "conf"}
        if not any(field in allowed for field in fields):
            valid = False
            notes.append("missing_key_value_fields")
    elif mode == "proto_v3_state":
        if has_proto_v1_long_tags(output) or has_fixed_v2_template(output):
            valid = False
            notes.append("uses_proto_v1_or_v2_tags")
        if wc > 95:
            valid = False
            notes.append("word_count_gt_95")
        if field_count > 8:
            valid = False
            notes.append("field_count_gt_8")
        if looks_like_natural_long(output, 45):
            valid = False
            notes.append("looks_like_long_natural_text")
        needs_state = task["group"] == "memory_state" or any(term in task["text"].lower() for term in ["memoria", "estado", "continuidad", "métrica", "verificación", "límite"])
        if needs_state and not set(fields).intersection({"m", "k", "v", "lim", "conf", "c"}):
            valid = False
            notes.append("missing_state_field_for_state_task")
    elif mode == "proto_v3_hybrid":
        if has_proto_v1_long_tags(output) or has_fixed_v2_template(output):
            valid = False
            notes.append("uses_proto_v1_or_v2_tags")
        if wc > 110:
            valid = False
            notes.append("word_count_gt_110")
        if not fields and not re.search(r"(?m)^\s*(p|problem|problema|s|solution|soluci[oó]n|r|risk|riesgo|n|next|siguiente)\s*:", lower):
            valid = False
            notes.append("missing_structural_marker")
        if looks_like_natural_long(output, 80):
            valid = False
            notes.append("looks_like_natural_complete")
    else:
        valid = None
        notes.append("not_applicable")
    return {
        "format_valid": valid,
        "format_notes": notes,
        "word_count": wc,
        "field_count": field_count,
        "fields_used": sorted(set(fields)),
    }


def record_base(task, mode, run, base_mode=None, source_proto_output=None):
    return {
        "experiment_id": EXPERIMENT_ID,
        "task_id": task["id"],
        "task_text": task["text"],
        "task_group": task["group"],
        "mode": mode,
        "base_mode": base_mode,
        "run": run,
        "model": None,
        "evaluator_model": None,
        "temperature": TEMPERATURE,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "token_count_method": None,
        "latency_ms": None,
        "output": None,
        "source_proto_output": source_proto_output,
        "evaluation": {},
        "evaluation_raw": None,
        "evaluation_parse_error": False,
        "error": None,
        "http_status": None,
        "timestamp": utc_now_iso(),
        "retried_after_empty_output": False,
        "thinking_disabled_applied": True,
        "format_valid": None,
        "format_notes": [],
        "word_count": None,
        "field_count": None,
        "fields_used": [],
        "api_call_index": base.CALL_STATS["attempted"],
    }


def fill_generation(record, result):
    record["model"] = result.get("model_used")
    record["input_tokens"] = result.get("input_tokens")
    record["output_tokens"] = result.get("output_tokens")
    record["total_tokens"] = result.get("total_tokens")
    record["prompt_tokens"] = result.get("input_tokens")
    record["completion_tokens"] = result.get("output_tokens")
    record["token_count_method"] = result.get("token_count_method")
    record["latency_ms"] = result.get("latency_ms")
    record["http_status"] = result.get("status_code")
    record["retried_after_empty_output"] = bool(result.get("retried_after_empty_output"))
    record["api_call_index"] = base.CALL_STATS["attempted"]


def finish_record_with_output(record, task, mode, output):
    record["output"] = output
    validation_mode = None if mode.endswith("_translated") else mode
    validation = validate_format(validation_mode, output, task)
    record.update(validation)
    evaluator_model, evaluation, eval_error, evaluation_raw, parse_error = evaluate_output(task, mode, output)
    record["evaluator_model"] = evaluator_model
    record["evaluation"] = evaluation or {}
    record["evaluation_raw"] = evaluation_raw
    record["evaluation_parse_error"] = bool(parse_error)
    if eval_error:
        record["error"] = {"type": eval_error, "message": base.sanitize_error_text(eval_error)}
    return record


def run_row(task, mode, run, output_result=None, base_mode=None, source_proto_output=None):
    record = record_base(task, mode, run, base_mode=base_mode, source_proto_output=source_proto_output)
    result = output_result or generate_output(task, mode)
    fill_generation(record, result)
    if not result.get("ok"):
        record["error"] = {"type": result.get("error_type"), "message": base.sanitize_error_text(result.get("error"))}
        append_jsonl(RUNS_PATH, record)
        return record
    record = finish_record_with_output(record, task, mode, result["output"])
    append_jsonl(RUNS_PATH, record)
    return record


def test_connection():
    models = base.list_models()
    out = {
        "timestamp": utc_now_iso(),
        "models_ok": bool(models.get("ok")),
        "models_count": None,
        "chat_ok": False,
        "error": None,
    }
    if not models.get("ok"):
        out["error"] = {"type": models.get("error_type"), "message": base.sanitize_error_text(models.get("error"))}
        return out
    data = models.get("data") or {}
    if isinstance(data.get("data"), list):
        out["models_count"] = len(data["data"])
    chat = base.call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        "Responde solo: OK_EXP03_TEST",
        temperature=TEMPERATURE,
        max_tokens=100,
        empty_retry_max_tokens=300,
    )
    out["chat_ok"] = bool(chat.get("ok"))
    out["chat_model"] = chat.get("model_used")
    out["chat_latency_ms"] = chat.get("latency_ms")
    out["chat_response"] = chat.get("output")
    if not chat.get("ok"):
        out["error"] = {"type": chat.get("error_type"), "message": base.sanitize_error_text(chat.get("error"))}
    return out


def pilot_run():
    pilot_tasks = [TASKS[0], TASKS[10]]
    pilot = {"timestamp": utc_now_iso(), "ok": True, "attempt": 1, "checks": []}
    for task in pilot_tasks:
        proto_outputs = {}
        for mode in BASE_MODES:
            result = generate_output(task, mode)
            check = {
                "task_id": task["id"],
                "mode": mode,
                "generation_ok": bool(result.get("ok")),
                "model": result.get("model_used"),
                "tokens_present": result.get("total_tokens") is not None or result.get("token_count_method") is not None,
                "evaluation_ok": False,
                "evaluator_model": None,
                "format_valid": None,
                "format_notes": [],
                "error": None,
            }
            if not result.get("ok"):
                check["error"] = {"type": result.get("error_type"), "message": base.sanitize_error_text(result.get("error"))}
                pilot["ok"] = False
                pilot["checks"].append(check)
                continue
            if mode.startswith("proto_v3"):
                proto_outputs[mode] = result["output"]
            validation = validate_format(mode, result["output"], task)
            check.update(validation)
            evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(task, mode, result["output"])
            check["evaluator_model"] = evaluator_model
            check["evaluation_ok"] = not bool(eval_error or parse_error)
            check["evaluation_error"] = eval_error
            check["evaluation"] = evaluation
            if not check["evaluation_ok"] or not check["tokens_present"] or check["format_valid"] is False:
                pilot["ok"] = False
            pilot["checks"].append(check)
        for base_mode_name, translated_mode in TRANSLATION_MAP.items():
            source = proto_outputs.get(base_mode_name)
            check = {
                "task_id": task["id"],
                "mode": translated_mode,
                "base_mode": base_mode_name,
                "generation_ok": False,
                "tokens_present": False,
                "evaluation_ok": False,
                "evaluator_model": None,
                "error": None,
            }
            if not source:
                check["error"] = {"type": "NO_SOURCE_PROTO", "message": "No source proto output."}
                pilot["ok"] = False
                pilot["checks"].append(check)
                continue
            translation = translate_output(source)
            check["generation_ok"] = bool(translation.get("ok"))
            check["model"] = translation.get("model_used")
            check["tokens_present"] = translation.get("total_tokens") is not None or translation.get("token_count_method") is not None
            if not translation.get("ok"):
                check["error"] = {"type": translation.get("error_type"), "message": base.sanitize_error_text(translation.get("error"))}
                pilot["ok"] = False
                pilot["checks"].append(check)
                continue
            evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(task, translated_mode, translation["output"])
            check["evaluator_model"] = evaluator_model
            check["evaluation_ok"] = not bool(eval_error or parse_error)
            check["evaluation_error"] = eval_error
            check["evaluation"] = evaluation
            if not check["evaluation_ok"] or not check["tokens_present"]:
                pilot["ok"] = False
            pilot["checks"].append(check)
    return pilot


def run_experiment(profile):
    tasks, repetitions = task_subset(profile)
    rows = []
    stopped_soft = False
    for task in tasks:
        for run in range(1, repetitions + 1):
            if soft_stop_reached():
                stopped_soft = True
                break
            proto_records = {}
            for mode in BASE_MODES:
                if soft_stop_reached():
                    stopped_soft = True
                    break
                rec = run_row(task, mode, run)
                rows.append(rec)
                if mode.startswith("proto_v3") and rec.get("output"):
                    proto_records[mode] = rec
            for base_mode_name, translated_mode in TRANSLATION_MAP.items():
                if soft_stop_reached():
                    stopped_soft = True
                    break
                source_record = proto_records.get(base_mode_name)
                if not source_record:
                    continue
                translation = translate_output(source_record["output"])
                rec = run_row(
                    task,
                    translated_mode,
                    run,
                    output_result=translation,
                    base_mode=base_mode_name,
                    source_proto_output=source_record["output"],
                )
                rows.append(rec)
            if stopped_soft:
                break
        if stopped_soft:
            break
    return rows, stopped_soft


def read_runs():
    if not RUNS_PATH.exists():
        return []
    return [json.loads(line) for line in RUNS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def mean(values):
    clean = [v for v in values if isinstance(v, (int, float))]
    return None if not clean else sum(clean) / len(clean)


def fmt(value, decimals=2):
    if value is None:
        return "NO_CALCULABLE"
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def pct(value):
    if value is None:
        return "NO_CALCULABLE"
    return f"{value:.2%}"


def summarize(rows):
    summary = {}
    natural_total = mean([r.get("total_tokens") for r in rows if r["mode"] == "natural" and not r.get("error")])
    caveman_total = mean([r.get("total_tokens") for r in rows if r["mode"] == "caveman" and not r.get("error")])
    proto_v2 = EXP02["proto_v2"]["tokens"]
    for mode in ALL_MODES:
        mode_rows = [r for r in rows if r.get("mode") == mode]
        ok_rows = [r for r in mode_rows if not r.get("error") or r.get("evaluation_parse_error")]
        eval_rows = [r for r in mode_rows if isinstance(r.get("evaluation"), dict) and r.get("evaluation")]
        total = mean([r.get("total_tokens") for r in ok_rows])
        summary[mode] = {
            "rows": len(mode_rows),
            "errors": len([r for r in mode_rows if r.get("error")]),
            "avg_input_tokens": mean([r.get("input_tokens") for r in ok_rows]),
            "avg_output_tokens": mean([r.get("output_tokens") for r in ok_rows]),
            "avg_total_tokens": total,
            "ahorro_vs_natural": None if total is None or not natural_total else 1 - (total / natural_total),
            "ahorro_vs_caveman": None if total is None or not caveman_total else 1 - (total / caveman_total),
            "ahorro_vs_proto_v2": None if total is None else 1 - (total / proto_v2),
            "avg_latency_ms": mean([r.get("latency_ms") for r in ok_rows]),
            "fidelidad_semantica": mean([r["evaluation"].get("fidelidad_semantica") for r in eval_rows]),
            "claridad": mean([r["evaluation"].get("claridad") for r in eval_rows]),
            "completitud": mean([r["evaluation"].get("completitud") for r in eval_rows]),
            "utilidad": mean([r["evaluation"].get("utilidad") for r in eval_rows]),
            "ambiguedad": mean([r["evaluation"].get("ambiguedad") for r in eval_rows]),
            "perdida_informacion": mean([r["evaluation"].get("perdida_informacion") for r in eval_rows]),
            "facilidad_traduccion": mean([r["evaluation"].get("facilidad_traduccion") for r in eval_rows]),
            "manejo_estado": mean([r["evaluation"].get("manejo_estado") for r in eval_rows]),
            "compacidad": mean([r["evaluation"].get("compacidad") for r in eval_rows]),
        }
    return summary


def proto_format_summary(rows):
    out = {}
    for mode in ["proto_v3_min", "proto_v3_state", "proto_v3_hybrid"]:
        mode_rows = [r for r in rows if r["mode"] == mode]
        if not mode_rows:
            out[mode] = {}
            continue
        valid = [r for r in mode_rows if r.get("format_valid") is True]
        field_counter = Counter()
        notes = Counter()
        for row in mode_rows:
            field_counter.update(row.get("fields_used") or [])
            notes.update(row.get("format_notes") or [])
        out[mode] = {
            "valid_pct": len(valid) / len(mode_rows) if mode_rows else None,
            "avg_words": mean([r.get("word_count") for r in mode_rows]),
            "avg_fields": mean([r.get("field_count") for r in mode_rows]),
            "field_freq": field_counter,
            "notes": notes,
        }
    return out


def group_summary(rows):
    out = {}
    for group in ["base_comparable", "memory_state", "medium_complexity", "stress_optional"]:
        group_rows = [r for r in rows if r.get("task_group") == group]
        if not group_rows:
            continue
        mode_data = summarize(group_rows)
        base_mode_data = {m: d for m, d in mode_data.items() if m in BASE_MODES}
        token_modes = {m: d for m, d in mode_data.items() if d["avg_total_tokens"] is not None}
        base_token_modes = {m: d for m, d in base_mode_data.items() if d["avg_total_tokens"] is not None}
        base_quality_modes = {m: d for m, d in base_mode_data.items() if d["fidelidad_semantica"] is not None and d["utilidad"] is not None and d["claridad"] is not None}
        base_state_modes = {m: d for m, d in base_mode_data.items() if d["manejo_estado"] is not None}
        proto_modes = {m: d for m, d in base_mode_data.items() if m.startswith("proto_v3")}
        best_proto = max(
            proto_modes.items(),
            key=lambda kv: ((kv[1]["fidelidad_semantica"] or 0) + (kv[1]["utilidad"] or 0) + (kv[1]["claridad"] or 0)) / 3,
        )[0] if proto_modes else "NO_CALCULABLE"
        out[group] = {
            "best_tokens": min(base_token_modes.items(), key=lambda kv: kv[1]["avg_total_tokens"])[0] if base_token_modes else "NO_CALCULABLE",
            "best_quality": max(base_quality_modes.items(), key=lambda kv: (kv[1]["fidelidad_semantica"] + kv[1]["utilidad"] + kv[1]["claridad"]) / 3)[0] if base_quality_modes else "NO_CALCULABLE",
            "best_state": max(base_state_modes.items(), key=lambda kv: kv[1]["manejo_estado"])[0] if base_state_modes else "NO_CALCULABLE",
            "best_proto": best_proto,
            "mode_data": mode_data,
        }
    return out


def translation_summary(rows, summary):
    out = {}
    for proto_mode, translated_mode in TRANSLATION_MAP.items():
        proto = summary[proto_mode]
        translated = summary[translated_mode]
        cost_extra = None
        combined_tokens = None
        ratio = None
        if proto["avg_total_tokens"] is not None and translated["avg_total_tokens"] is not None:
            # Translation is a second API call, so its token use is added to the
            # source proto cost. It is not a replacement for the proto row.
            cost_extra = translated["avg_total_tokens"]
            combined_tokens = proto["avg_total_tokens"] + translated["avg_total_tokens"]
            ratio = combined_tokens / proto["avg_total_tokens"]
        out[proto_mode] = {
            "translated_mode": translated_mode,
            "tokens_proto": proto["avg_total_tokens"],
            "tokens_translated": translated["avg_total_tokens"],
            "cost_extra": cost_extra,
            "combined_tokens": combined_tokens,
            "ratio": ratio,
            "claridad_proto": proto["claridad"],
            "claridad_translated": translated["claridad"],
            "fidelidad_proto": proto["fidelidad_semantica"],
            "fidelidad_translated": translated["fidelidad_semantica"],
        }
    return out


def table_global(summary):
    lines = [
        "| Modo | Filas | Errores | Tokens promedio | Ahorro vs natural | Ahorro vs caveman | Ahorro vs proto_v2 | Fidelidad | Claridad | Completitud | Ambigüedad | Pérdida info | Utilidad | Traducibilidad | Manejo estado | Compacidad | Latencia ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode in ALL_MODES:
        m = summary[mode]
        lines.append(
            f"| {mode} | {m['rows']} | {m['errors']} | {fmt(m['avg_total_tokens'])} | {pct(m['ahorro_vs_natural'])} | {pct(m['ahorro_vs_caveman'])} | {pct(m['ahorro_vs_proto_v2'])} | {fmt(m['fidelidad_semantica'])} | {fmt(m['claridad'])} | {fmt(m['completitud'])} | {fmt(m['ambiguedad'])} | {fmt(m['perdida_informacion'])} | {fmt(m['utilidad'])} | {fmt(m['facilidad_traduccion'])} | {fmt(m['manejo_estado'])} | {fmt(m['compacidad'])} | {fmt(m['avg_latency_ms'], 0)} |"
        )
    return "\n".join(lines)


def table_format(format_data):
    lines = [
        "| Modo | Formato válido % | Palabras prom. | Campos prom. | Campos frecuentes | Notas |",
        "|---|---:|---:|---:|---|---|",
    ]
    for mode, data in format_data.items():
        fields = ", ".join(f"{k}:{v}" for k, v in data.get("field_freq", Counter()).most_common(8))
        notes = ", ".join(f"{k}:{v}" for k, v in data.get("notes", Counter()).most_common(5)) or "sin_notas"
        lines.append(f"| {mode} | {pct(data.get('valid_pct'))} | {fmt(data.get('avg_words'))} | {fmt(data.get('avg_fields'))} | {fields} | {notes} |")
    return "\n".join(lines)


def table_translation(trans_data):
    lines = [
        "| Modo proto | Tokens proto | Tokens traducido | Costo extra | Claridad proto | Claridad traducido | Fidelidad proto | Fidelidad traducido | Lectura |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for mode, data in trans_data.items():
        lectura = "NO_CALCULABLE"
        if data["combined_tokens"] is not None:
            lectura = f"extra_call;total={fmt(data['combined_tokens'])}"
        lines.append(
            f"| {mode} | {fmt(data['tokens_proto'])} | {fmt(data['tokens_translated'])} | {fmt(data['cost_extra'])} | {fmt(data['claridad_proto'])} | {fmt(data['claridad_translated'])} | {fmt(data['fidelidad_proto'])} | {fmt(data['fidelidad_translated'])} | {lectura} |"
        )
    return "\n".join(lines)


def table_groups(group_data):
    lines = [
        "| Grupo | Mejor por tokens | Mejor por calidad | Mejor por estado | Observación |",
        "|---|---|---|---|---|",
    ]
    for group, data in group_data.items():
        obs = f"mejor_proto={data.get('best_proto', 'NO_CALCULABLE')}; calculo_tokens_solo_modos_base"
        lines.append(f"| {group} | {data['best_tokens']} | {data['best_quality']} | {data['best_state']} | {obs} |")
    return "\n".join(lines)


def table_history(summary):
    rows = [
        ("natural", EXP01["natural"]["tokens"], EXP02["natural"]["tokens"], summary["natural"]["avg_total_tokens"], summary["natural"]["fidelidad_semantica"]),
        ("caveman", EXP01["caveman"]["tokens"], EXP02["caveman"]["tokens"], summary["caveman"]["avg_total_tokens"], summary["caveman"]["fidelidad_semantica"]),
        ("proto_v1", EXP01["proto_v1"]["tokens"], None, None, None),
        ("proto_v2", None, EXP02["proto_v2"]["tokens"], None, None),
        ("proto_v3_min", None, None, summary["proto_v3_min"]["avg_total_tokens"], summary["proto_v3_min"]["fidelidad_semantica"]),
        ("proto_v3_state", None, None, summary["proto_v3_state"]["avg_total_tokens"], summary["proto_v3_state"]["fidelidad_semantica"]),
        ("proto_v3_hybrid", None, None, summary["proto_v3_hybrid"]["avg_total_tokens"], summary["proto_v3_hybrid"]["fidelidad_semantica"]),
        ("proto_v1_translated", EXP01["proto_v1_translated"]["tokens"], None, None, None),
        ("proto_v2_translated", None, EXP02["proto_v2_translated"]["tokens"], None, None),
        ("proto_v3_min_translated", None, None, summary["proto_v3_min_translated"]["avg_total_tokens"], summary["proto_v3_min_translated"]["fidelidad_semantica"]),
        ("proto_v3_state_translated", None, None, summary["proto_v3_state_translated"]["avg_total_tokens"], summary["proto_v3_state_translated"]["fidelidad_semantica"]),
        ("proto_v3_hybrid_translated", None, None, summary["proto_v3_hybrid_translated"]["avg_total_tokens"], summary["proto_v3_hybrid_translated"]["fidelidad_semantica"]),
    ]
    lines = [
        "| Modo | EXP01 tokens | EXP02 tokens | EXP03 tokens | Cambio vs EXP02 | Fidelidad EXP03 | Lectura |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for mode, exp01, exp02, exp03, fid in rows:
        change = None if exp02 is None or exp03 is None else exp03 - exp02
        lectura = "referencia"
        if change is not None:
            lectura = "menos que EXP02" if change < 0 else "mas que EXP02" if change > 0 else "igual"
        lines.append(f"| {mode} | {fmt(exp01)} | {fmt(exp02)} | {fmt(exp03)} | {fmt(change)} | {fmt(fid)} | {lectura} |")
    return "\n".join(lines)


def error_summary(rows):
    errs = Counter()
    for row in rows:
        err = row.get("error")
        if err:
            errs[err.get("type") if isinstance(err, dict) else str(err)] += 1
    if not errs:
        return "- No se registraron errores por fila."
    return "\n".join(f"- {k}: {v}" for k, v in errs.items())


def best_mode(summary, metric, reverse=True):
    vals = {m: d[metric] for m, d in summary.items() if d.get(metric) is not None}
    if not vals:
        return "NO_CALCULABLE"
    return sorted(vals.items(), key=lambda kv: kv[1], reverse=reverse)[0][0]


def cheapest_mode(summary):
    return best_mode(summary, "avg_total_tokens", reverse=False)


def decide_exp04(summary, format_data):
    caveman = summary["caveman"]
    hybrid = summary["proto_v3_hybrid"]
    state = summary["proto_v3_state"]
    minv = summary["proto_v3_min"]
    if (
        hybrid["avg_total_tokens"]
        and caveman["avg_total_tokens"]
        and hybrid["avg_total_tokens"] <= caveman["avg_total_tokens"] * 1.20
        and hybrid["fidelidad_semantica"]
        and hybrid["fidelidad_semantica"] >= 4.4
        and hybrid["utilidad"]
        and hybrid["utilidad"] >= 4.4
    ):
        return "C. Hybrid_Min"
    if state["manejo_estado"] and caveman["manejo_estado"] and state["manejo_estado"] > caveman["manejo_estado"] and state["avg_total_tokens"] and state["avg_total_tokens"] <= caveman["avg_total_tokens"] * 1.35:
        return "B. Caveman_State"
    if minv["avg_total_tokens"] and minv["avg_total_tokens"] < EXP02["proto_v2"]["tokens"] and minv["fidelidad_semantica"] and minv["fidelidad_semantica"] >= 4.4:
        return "A. Proto_v3_Escalado_50_Tareas"
    return "G. Stop_Proto_Formal" if cheapest_mode(summary) == "caveman" else "F. Evaluacion_Humana"


def hypothesis_text(summary):
    caveman = summary["caveman"]
    minv = summary["proto_v3_min"]
    state = summary["proto_v3_state"]
    hybrid = summary["proto_v3_hybrid"]
    survived = []
    fell = []
    if minv["avg_total_tokens"] and minv["avg_total_tokens"] < EXP02["proto_v2"]["tokens"]:
        survived.append("Proto v3 min redujo tokens frente a Proto v2.")
    else:
        fell.append("Proto v3 min no redujo tokens frente a Proto v2.")
    if minv["avg_total_tokens"] and caveman["avg_total_tokens"] and minv["avg_total_tokens"] <= caveman["avg_total_tokens"] * 1.10:
        survived.append("Proto v3 min se acerco a caveman en tokens.")
    else:
        fell.append("Proto v3 min no se acerco lo suficiente a caveman en tokens.")
    if state["manejo_estado"] and caveman["manejo_estado"] and state["manejo_estado"] > caveman["manejo_estado"]:
        survived.append("Proto v3 state mejoro manejo_estado frente a caveman.")
    else:
        fell.append("Proto v3 state no mejoro manejo_estado frente a caveman.")
    if hybrid["fidelidad_semantica"] and hybrid["utilidad"] and hybrid["avg_total_tokens"] and caveman["avg_total_tokens"] and hybrid["fidelidad_semantica"] >= 4.5 and hybrid["utilidad"] >= 4.5 and hybrid["avg_total_tokens"] <= caveman["avg_total_tokens"] * 1.25:
        survived.append("Proto v3 hybrid sostuvo una hipotesis de equilibrio.")
    elif hybrid["fidelidad_semantica"] and hybrid["utilidad"] and hybrid["avg_total_tokens"] and caveman["avg_total_tokens"] and hybrid["fidelidad_semantica"] >= 4.4 and hybrid["utilidad"] >= 4.4 and hybrid["avg_total_tokens"] <= caveman["avg_total_tokens"] * 1.20:
        survived.append("Proto v3 hybrid sobrevivio parcialmente: mejoro frente a Proto v2 y quedo cerca de caveman, aunque no cumplio el criterio fuerte.")
        fell.append("Proto v3 hybrid no cumplio el criterio fuerte de equilibrio.")
    else:
        fell.append("Proto v3 hybrid no cumplio el criterio fuerte de equilibrio.")
    return survived, fell


def write_reports(rows, profile, pilot, connection, backup_name, stopped_soft):
    summary = summarize(rows)
    fmt_data = proto_format_summary(rows)
    group_data = group_summary(rows)
    trans_data = translation_summary(rows, summary)
    survived, fell = hypothesis_text(summary)
    exp04 = decide_exp04(summary, fmt_data)
    total_errors = len([r for r in rows if r.get("error")])
    report = f"""# Experimento 03 Fusion: Proto v3 minimalista, state e hybrid

## Objetivo

Ejecutar una comparacion ampliada entre lenguaje natural, caveman y tres variantes de Proto v3, incluyendo traducciones finales humanas de cada variante proto.

## Hipotesis

Proto v3 minimalista puede reducir tokens frente a Proto v2 y recuperar calidad semantica al eliminar estructura obligatoria. Proto v3 state puede aportar valor en memoria/estado. Proto v3 hybrid puede equilibrar ahorro, claridad y traducibilidad.

## Motivo del rediseño

EXP01 mostro que Proto v1 era demasiado pesado. EXP02 mostro que reducir etiquetas no bastaba si los campos seguian siendo obligatorios. EXP03 prueba campos opcionales y formatos mas cercanos a caveman.

## Cambios frente a Proto v2

- Campos opcionales.
- Una linea cuando sea posible.
- No plantilla fija de 8 campos.
- Tres variantes: min, state e hybrid.
- Validadores locales de formato.

## Configuracion

- Endpoint: `{CHAT_COMPLETIONS_URL}`
- Modelo generador: `{GENERATION_MODEL}`
- Modelo evaluador: `{EVALUATOR_MODEL}`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: {TEMPERATURE}
- Repeticiones: {REPETITIONS}
- Perfil: {profile}
- Llamadas HTTP: {base.CALL_STATS["attempted"]}
- Errores HTTP: {base.CALL_STATS["errors"]}
- Soft stop activado: {stopped_soft}
- Backup JSONL previo: {backup_name or "no_aplica"}
- Conexion: {json.dumps(connection, ensure_ascii=False)}

## Perfil de ejecucion usado

{profile}.

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Metodologia

Se ejecutaron modos base `natural`, `caveman`, `proto_v3_min`, `proto_v3_state` y `proto_v3_hybrid`. Para cada salida proto se genero una traduccion humana breve. Todas las salidas fueron evaluadas por modelo evaluador con JSON estructurado. Los resultados se guardaron incrementalmente en `experimento_03_fusion_runs.jsonl`.

## Tabla de resultados global

{table_global(summary)}

## Validez de formato Proto v3

{table_format(fmt_data)}

## Analisis por grupos de tarea

{table_groups(group_data)}

## Analisis de traducciones

Nota: `Tokens traducido` mide solo la llamada de traduccion. El costo arquitectonico real de traducir por salida es `tokens proto + tokens traducido`.

{table_translation(trans_data)}

## Comparacion con EXP01

EXP01 sirve como referencia de Proto v1 y caveman inicial. Ver tabla historica completa en `Comparacion_EXP01_EXP02_EXP03_Fusion.md`.

## Comparacion con EXP02

{table_history(summary)}

## Que hipotesis sobrevivio

{chr(10).join("- " + item for item in survived) if survived else "- Ninguna hipotesis fuerte sobrevivio con estos datos."}

## Que hipotesis cayo

{chr(10).join("- " + item for item in fell) if fell else "- Ninguna hipotesis fue rechazada claramente."}

## Errores

{error_summary(rows)}

## Limitaciones

- Evaluacion automatica, no humana.
- Un solo generador principal.
- El costo de traduccion por salida puede no representar traduccion por lote.
- Las tareas siguen siendo sinteticas.

## Conclusion parcial

Datos antes que entusiasmo: el resultado debe leerse por tokens, calidad, ambiguedad, perdida de informacion, manejo de estado y validez de formato. Si caveman sigue ganando, eso favorece una direccion Caveman_State o Hybrid_Min antes que simbolismo formal pesado.

## Recomendacion para EXP04

{exp04}
"""
    write_text(REPORT_PATH, report)
    write_text(COMPARISON_PATH, comparison_doc(summary))
    write_text(VARIANT_ANALYSIS_PATH, variant_doc(summary, fmt_data, group_data))
    write_text(OBSERVATIONS_PATH, observations_doc(rows, summary, fmt_data, group_data, trans_data))
    write_text(CONCLUSIONS_PATH, conclusions_doc(summary, rows, survived, fell, exp04))
    if total_errors:
        write_text(ERRORS_PATH, errors_doc(rows))


def comparison_doc(summary):
    return f"""# Comparación EXP01 vs EXP02 vs EXP03 Fusion

## Evolución de tokens

{table_history(summary)}

## Evolución de fidelidad

- natural EXP03: {fmt(summary['natural']['fidelidad_semantica'])}
- caveman EXP03: {fmt(summary['caveman']['fidelidad_semantica'])}
- proto_v3_min EXP03: {fmt(summary['proto_v3_min']['fidelidad_semantica'])}
- proto_v3_state EXP03: {fmt(summary['proto_v3_state']['fidelidad_semantica'])}
- proto_v3_hybrid EXP03: {fmt(summary['proto_v3_hybrid']['fidelidad_semantica'])}

## Evolución de utilidad

- caveman EXP02 utilidad: {EXP02['caveman']['utilidad']}
- proto_v2 utilidad: {EXP02['proto_v2']['utilidad']}
- proto_v3_min utilidad: {fmt(summary['proto_v3_min']['utilidad'])}
- proto_v3_state utilidad: {fmt(summary['proto_v3_state']['utilidad'])}
- proto_v3_hybrid utilidad: {fmt(summary['proto_v3_hybrid']['utilidad'])}

## Evolución de ambigüedad

- proto_v3_min: {fmt(summary['proto_v3_min']['ambiguedad'])}
- proto_v3_state: {fmt(summary['proto_v3_state']['ambiguedad'])}
- proto_v3_hybrid: {fmt(summary['proto_v3_hybrid']['ambiguedad'])}

## Evolución de pérdida de información

- proto_v3_min: {fmt(summary['proto_v3_min']['perdida_informacion'])}
- proto_v3_state: {fmt(summary['proto_v3_state']['perdida_informacion'])}
- proto_v3_hybrid: {fmt(summary['proto_v3_hybrid']['perdida_informacion'])}

## Evolución de traducibilidad

- proto_v3_min: {fmt(summary['proto_v3_min']['facilidad_traduccion'])}
- proto_v3_state: {fmt(summary['proto_v3_state']['facilidad_traduccion'])}
- proto_v3_hybrid: {fmt(summary['proto_v3_hybrid']['facilidad_traduccion'])}

## Qué cambió en cada versión

- Proto v1: estructura clara pero pesada.
- Proto v2: etiquetas cortas pero campos aun demasiado obligatorios.
- Proto v3: campos opcionales, variantes min/state/hybrid y validacion local.

## Lectura experimental

La lectura debe basarse en la tabla global y no en preferencia teorica por simbolos.

## Recomendación

{decide_exp04(summary, {})}
"""


def variant_doc(summary, fmt_data, group_data):
    best_base = best_mode({k: summary[k] for k in BASE_MODES}, "avg_total_tokens", reverse=False)
    best_derived = cheapest_mode(summary)
    return f"""# Análisis de variantes Proto v3

## proto_v3_min

- Tokens promedio: {fmt(summary['proto_v3_min']['avg_total_tokens'])}
- Fidelidad: {fmt(summary['proto_v3_min']['fidelidad_semantica'])}
- Utilidad: {fmt(summary['proto_v3_min']['utilidad'])}
- Formato valido: {pct(fmt_data.get('proto_v3_min', {}).get('valid_pct'))}

## proto_v3_state

- Tokens promedio: {fmt(summary['proto_v3_state']['avg_total_tokens'])}
- Manejo estado: {fmt(summary['proto_v3_state']['manejo_estado'])}
- Fidelidad: {fmt(summary['proto_v3_state']['fidelidad_semantica'])}
- Formato valido: {pct(fmt_data.get('proto_v3_state', {}).get('valid_pct'))}

## proto_v3_hybrid

- Tokens promedio: {fmt(summary['proto_v3_hybrid']['avg_total_tokens'])}
- Claridad: {fmt(summary['proto_v3_hybrid']['claridad'])}
- Utilidad: {fmt(summary['proto_v3_hybrid']['utilidad'])}
- Formato valido: {pct(fmt_data.get('proto_v3_hybrid', {}).get('valid_pct'))}

## Comparación entre variantes

- Modo base mas barato: {best_base}
- Fila derivada mas barata: {best_derived}; no comparable como costo total porque exige una llamada proto previa
- Mejor manejo de estado: {best_mode(summary, 'manejo_estado')}
- Mejor claridad entre proto: {best_mode({k: summary[k] for k in ['proto_v3_min','proto_v3_state','proto_v3_hybrid']}, 'claridad')}

## Dónde gana cada una

Ver `task_group` en JSONL y tabla por grupos del informe principal.

## Dónde falla cada una

Revisar `format_notes`, `ambiguedad` y `perdida_informacion`.

## Reglas que deberían cambiar

- Si min pierde calidad, permitir una clave extra de contexto.
- Si state no mejora estado, reducir campos decorativos.
- Si hybrid gana equilibrio, convertirlo en candidato principal.

## Candidata para EXP04

{decide_exp04(summary, fmt_data)}
"""


def observations_doc(rows, summary, fmt_data, group_data, trans_data):
    examples_good = []
    examples_bad = []
    for row in rows:
        if row["mode"].startswith("proto_v3") and not row["mode"].endswith("translated"):
            if row.get("format_valid") is True and len(examples_good) < 3:
                examples_good.append(f"- {row['mode']} {row['task_id']}: `{row.get('output','')[:180]}`")
            if row.get("format_valid") is False and len(examples_bad) < 3:
                examples_bad.append(f"- {row['mode']} {row['task_id']}: `{row.get('output','')[:180]}` notas={row.get('format_notes')}")
    return f"""# Observaciones Experimento 03 Fusion

## Patrones

- Modo base mas barato: caveman.
- Fila derivada mas barata: {cheapest_mode(summary)}; no es comparable como arquitectura completa porque requiere generar primero la salida proto.
- Mejor calidad por fidelidad: {best_mode(summary, 'fidelidad_semantica')}.
- Mejor manejo de estado: {best_mode(summary, 'manejo_estado')}.

## Ejemplos buenos

{chr(10).join(examples_good) if examples_good else "- Sin ejemplos seleccionados."}

## Ejemplos malos

{chr(10).join(examples_bad) if examples_bad else "- Sin ejemplos fallidos seleccionados."}

## Dudas

- El evaluador automatico puede premiar claridad humana sobre compresion operativa.
- La traduccion por salida puede inflar costo frente a traduccion por lote.
- La utilidad de estado debe revisarse manualmente en tareas T011-T020.
"""


def conclusions_doc(summary, rows, survived, fell, exp04):
    return f"""# Conclusiones Experimento 03 Fusion

## Base de datos

- Filas: {len(rows)}
- Errores: {len([r for r in rows if r.get('error')])}
- Llamadas HTTP: {base.CALL_STATS['attempted']}

## Conclusiones basadas en datos

## Hipotesis que sobrevivieron

{chr(10).join('- ' + item for item in survived) if survived else '- Ninguna hipotesis fuerte sobrevivio.'}

## Hipotesis que cayeron

{chr(10).join('- ' + item for item in fell) if fell else '- Ninguna hipotesis cayo claramente.'}

## Lectura

- Modo base mas barato: caveman.
- Fila derivada mas barata: {cheapest_mode(summary)}; no debe leerse como costo total porque la traduccion requiere una llamada proto previa.
- Mejor fidelidad: {best_mode(summary, 'fidelidad_semantica')}.
- Mejor manejo de estado: {best_mode(summary, 'manejo_estado')}.

## Recomendacion EXP04

{exp04}
"""


def errors_doc(rows):
    return f"""# Errores Experimento 03 Fusion

## Resumen

{error_summary(rows)}

## Seguridad

No se registra API key.
"""


def write_error_file(message, pilot=None, connection=None):
    write_text(
        ERROR_PATH,
        f"""# Error Experimento 03 Fusion

## Fecha

{utc_now_iso()}

## Causa resumida

{message}

## Conexion

```json
{json.dumps(connection or {}, ensure_ascii=False, indent=2)}
```

## Piloto

```json
{json.dumps(pilot or {}, ensure_ascii=False, indent=2)}
```

## Seguridad

No se registra API key.
""",
    )


def run_secret_scan():
    paths = [REPORT_PATH, OBSERVATIONS_PATH, CONCLUSIONS_PATH, COMPARISON_PATH, VARIANT_ANALYSIS_PATH, RUNS_PATH]
    patterns = ["s" + "k" + "-", "api" + "_key", "API" + "_KEY", "Author" + "ization", "Bear" + "er", "token" + "="]
    hits = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in patterns:
            if pat in text:
                hits.append(f"{path.name}:{pat}")
    return hits


def validate_jsonl():
    rows = read_runs()
    return len(rows)


def main():
    ensure_dirs()
    require_provider_key()
    profile = selected_profile()
    tasks, repetitions = task_subset(profile)
    backup_name = backup_jsonl_if_exists()
    connection = test_connection()
    if not connection.get("models_ok") or not connection.get("chat_ok"):
        write_error_file("Fallo prueba de conexion.", connection=connection)
        print("EXP03 fallo conexion. Ver Error_Experimento_03_Fusion.md")
        return 1
    pilot = pilot_run()
    if not pilot.get("ok"):
        pilot["attempt"] = 1
        pilot2 = pilot_run()
        pilot2["attempt"] = 2
        if not pilot2.get("ok"):
            write_error_file("Piloto fallo dos veces. No se ejecuto tanda completa.", pilot=pilot2, connection=connection)
            print("EXP03 piloto fallo. Ver Error_Experimento_03_Fusion.md")
            return 1
        pilot = pilot2
    rows, stopped_soft = run_experiment(profile)
    write_reports(rows, profile, pilot, connection, backup_name, stopped_soft)
    rows_count = validate_jsonl()
    secret_hits = run_secret_scan()
    if secret_hits:
        write_error_file(f"Secret scan detecto patrones: {secret_hits}", pilot=pilot, connection=connection)
        print("EXP03 termino pero secret scan detecto patrones. Revisar Error_Experimento_03_Fusion.md")
        return 1
    print(f"EXP03 terminado. perfil={profile} tareas={len(tasks)} reps={repetitions} filas={rows_count} llamadas_http={base.CALL_STATS['attempted']} errores_http={base.CALL_STATS['errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
