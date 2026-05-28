import json
import os
from datetime import datetime, timezone
from pathlib import Path

import run_experimento_01_opencode_go as base


EXPERIMENT_ID = "EXP02_PROTO_V2"

BASE_URL = "https://opencode.ai/zen/go/v1"
CHAT_COMPLETIONS_URL = f"{BASE_URL}/chat/completions"
MODELS_URL = f"{BASE_URL}/models"

GENERATION_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
GENERATION_MODEL_FALLBACK = os.getenv("GENERATION_MODEL_FALLBACK", "opencode-go/deepseek-v4-flash")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "deepseek-v4-pro")
EVALUATOR_MODEL_FALLBACK = os.getenv("EVALUATOR_MODEL_FALLBACK", "deepseek-v4-flash")
TEMPERATURE = 0.2
REPETITIONS = 3
MAX_CALLS_INITIAL_RUN = 300
REQUEST_TIMEOUT = 90

MAX_TOKENS_GENERATION = 500
MAX_TOKENS_TRANSLATION = 350
MAX_TOKENS_EVALUATION = 300
EMPTY_RETRY_MAX_TOKENS_GENERATION = 1800
EMPTY_RETRY_MAX_TOKENS_TRANSLATION = 1200
EMPTY_RETRY_MAX_TOKENS_EVALUATION = 1000

EXP01_REFS = {
    "natural_avg_tokens": 364.30,
    "caveman_avg_tokens": 263.97,
    "proto_v1_avg_tokens": 377.13,
    "proto_v1_translated_avg_tokens": 438.87,
    "natural_fidelidad": 4.97,
    "caveman_fidelidad": 4.97,
    "proto_v1_fidelidad": 4.87,
    "proto_v1_translated_fidelidad": 4.57,
}

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "06_Resultados"
RUNS_PATH = RESULTS_DIR / "experimento_02_runs.jsonl"
REPORT_PATH = RESULTS_DIR / "Experimento_02_Resultados.md"
OBSERVATIONS_PATH = RESULTS_DIR / "Observaciones_Experimento_02.md"
CONCLUSIONS_PATH = RESULTS_DIR / "Conclusiones_Experimento_02.md"
ERROR_PATH = RESULTS_DIR / "Error_Experimento_02.md"

TASKS = [
    {
        "id": "T001",
        "text": "Analiza este problema: un sistema multiagente consume demasiados tokens porque cada agente escribe explicaciones largas. Propón solución, riesgos y próximos pasos.",
    },
    {
        "id": "T002",
        "text": "Resume una arquitectura de agentes con trabajador, supervisor, memoria y traductor final. Incluye ventajas y limitaciones.",
    },
    {
        "id": "T003",
        "text": "Convierte una explicación larga sobre eficiencia de tokens en una estructura operativa para agentes.",
    },
    {
        "id": "T004",
        "text": "Diseña reglas iniciales para evitar deriva semántica en un protocolo simbólico.",
    },
    {
        "id": "T005",
        "text": "Detecta riesgos en un sistema donde varios agentes se comunican con símbolos comprimidos.",
    },
    {
        "id": "T006",
        "text": "Propón una metodología para medir si un protolenguaje conserva significado.",
    },
    {
        "id": "T007",
        "text": "Extrae variables medibles de un experimento sobre comunicación multiagente.",
    },
    {
        "id": "T008",
        "text": "Crea una plantilla breve para registrar resultados de pruebas con modelos IA.",
    },
    {
        "id": "T009",
        "text": "Compara lenguaje natural, lenguaje cavernícola y protolenguaje en términos de costo, claridad y error.",
    },
    {
        "id": "T010",
        "text": "Propón cómo un agente traductor debe convertir protolenguaje a español humano sin inventar información.",
    },
]

MODE_PROMPTS = {
    "natural": """Responde en lenguaje natural claro y completo.
Usa solo respuesta final. No muestres razonamiento paso a paso.
Maximo 140 palabras.

Analiza la tarea, explica el problema, propone solución, riesgos y próximos pasos.

Tarea:
{task}""",
    "caveman": """Modo comprimido.
Usa solo respuesta final. No muestres razonamiento paso a paso.
Maximo 90 palabras.
Sin tono humano.
Sin adornos.
Solo datos útiles.

Formato obligatorio:
P:
S:
R:
N:

Donde:
P = problema
S = solución
R = riesgos
N = próximos pasos

Tarea:
{task}""",
    "proto_v2": """Usa Proto v2 compacto.
Usa solo respuesta final. No muestres razonamiento paso a paso.
No uses lenguaje humano completo.
Maximo 70 palabras.
No uses @TASK, GOAL, CTX, PROBLEM, PLAN, RISK, CHK, OUT, NEXT.

Formato obligatorio:
T:{{id}}
G:{{objetivo}}
C:{{contexto}}
P:{{problema}}
S:{{solucion}}
R:{{riesgos}}
V:{{verificacion}}
N:{{siguiente}}

Reglas:
- Etiquetas de 1 letra.
- Separar elementos con punto y coma.
- Riesgos separados con |.
- Acciones separadas con >.
- Usar palabras raiz.
- Mantener entidades, riesgos y proximos pasos.
- Si hay incertidumbre usar V:?.
- Si no hay dato usar Ø.
- No inventar.

Tarea:
{task}""",
}

TRANSLATOR_PROMPT = """Traduce el siguiente Proto v2 a español humano claro.
Usa solo respuesta final. No muestres razonamiento paso a paso.
Maximo 120 palabras.

Reglas:
- No inventes información.
- Conserva objetivo, contexto, problema, solución, riesgos, verificación y próximos pasos.
- Expande etiquetas a frases humanas.
- Marca incertidumbre si aparece V:?.

Proto v2:
{proto_output}"""

EVALUATOR_PROMPT = """Eres un evaluador técnico.
Usa solo respuesta final. No muestres razonamiento paso a paso.

Compara la respuesta generada contra la tarea original.

Evalúa de 1 a 5:
- fidelidad_semantica
- claridad
- completitud
- utilidad
- ambiguedad
- perdida_informacion
- facilidad_traduccion

Reglas:
- Para fidelidad_semantica, claridad, completitud, utilidad y facilidad_traduccion: 5 es mejor.
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
  "comentario": "..."
}}"""


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def configure_base():
    base.configure_provider_from_env()
    base.API_KEY = os.getenv("OPENCODE_API_KEY") or base.API_KEY
    base.MAX_CALLS_INITIAL_RUN = MAX_CALLS_INITIAL_RUN
    base.REQUEST_TIMEOUT = REQUEST_TIMEOUT
    base.GENERATION_MODEL = GENERATION_MODEL
    base.GENERATION_MODEL_FALLBACK = GENERATION_MODEL_FALLBACK
    base.EVALUATOR_MODEL = EVALUATOR_MODEL
    base.EVALUATOR_MODEL_FALLBACK = EVALUATOR_MODEL_FALLBACK
    base.TEMPERATURE = TEMPERATURE
    base.CALL_STATS["attempted"] = 0
    base.CALL_STATS["successful"] = 0
    base.CALL_STATS["errors"] = 0
    base.CALL_STATS["rate_limit_retries"] = 0


def require_api_key():
    configure_base()
    if not base.API_KEY:
        raise base.ExperimentAbort("Falta clave del proveedor. Define OPENCODE_API_KEY, GEMINI_API_KEY o token Vertex antes de ejecutar.")


def ensure_directories():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path, record):
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_output(task, mode):
    prompt = MODE_PROMPTS[mode].format(task=task["text"])
    return base.call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_GENERATION,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_GENERATION,
    )


def translate_proto_v2(proto_output):
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


def base_record(task, mode, run):
    return {
        "experiment_id": EXPERIMENT_ID,
        "task_id": task["id"],
        "task_text": task["text"],
        "mode": mode,
        "run": run,
        "model": None,
        "evaluator_model": None,
        "temperature": TEMPERATURE,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
        "token_count_method": None,
        "latency_ms": None,
        "output": None,
        "evaluation": {},
        "evaluation_raw": None,
        "evaluation_parse_error": False,
        "error": None,
        "http_status": None,
        "timestamp": utc_now_iso(),
    }


def fill_generation_fields(record, result):
    record["model"] = result.get("model_used")
    record["input_tokens"] = result.get("input_tokens")
    record["output_tokens"] = result.get("output_tokens")
    record["total_tokens"] = result.get("total_tokens")
    record["latency_ms"] = result.get("latency_ms")
    record["http_status"] = result.get("status_code")
    record["token_count_method"] = result.get("token_count_method")
    if result.get("retried_after_empty_output"):
        record["retried_after_empty_output"] = True


def run_generation_and_evaluation(task, mode, run, output_result=None):
    record = base_record(task, mode, run)
    result = output_result or generate_output(task, mode)
    fill_generation_fields(record, result)
    if not result.get("ok"):
        record["error"] = {
            "type": result.get("error_type"),
            "message": base.sanitize_error_text(result.get("error")),
        }
        append_jsonl(RUNS_PATH, record)
        return record
    record["output"] = result["output"]
    evaluator_model, evaluation, eval_error, evaluation_raw, parse_error = evaluate_output(task, mode, result["output"])
    record["evaluator_model"] = evaluator_model
    record["evaluation"] = evaluation or {}
    record["evaluation_raw"] = evaluation_raw
    record["evaluation_parse_error"] = bool(parse_error)
    if eval_error:
        record["error"] = {"type": eval_error, "message": base.sanitize_error_text(eval_error)}
    append_jsonl(RUNS_PATH, record)
    return record


def pilot_check():
    task = TASKS[0]
    pilot = {
        "timestamp": utc_now_iso(),
        "task_id": task["id"],
        "ok": True,
        "thinking_disabled_applied": True,
        "checks": [],
    }
    proto_output = None
    for mode in ("natural", "caveman", "proto_v2"):
        result = generate_output(task, mode)
        check = {
            "mode": mode,
            "generation_ok": bool(result.get("ok")),
            "model": result.get("model_used"),
            "latency_ms": result.get("latency_ms"),
            "http_status": result.get("status_code"),
            "tokens_present": result.get("total_tokens") is not None or result.get("token_count_method") is not None,
            "token_count_method": result.get("token_count_method"),
            "evaluation_ok": False,
            "evaluator_model": None,
            "error": None,
        }
        if not result.get("ok"):
            check["error"] = {"type": result.get("error_type"), "message": base.sanitize_error_text(result.get("error"))}
            pilot["ok"] = False
            pilot["checks"].append(check)
            continue
        if mode == "proto_v2":
            proto_output = result["output"]
        evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(task, mode, result["output"])
        check["evaluator_model"] = evaluator_model
        check["evaluation_ok"] = not bool(eval_error or parse_error)
        check["evaluation_error"] = eval_error
        check["evaluation"] = evaluation
        if not check["evaluation_ok"] or not check["tokens_present"]:
            pilot["ok"] = False
        pilot["checks"].append(check)
    if not proto_output:
        pilot["ok"] = False
        pilot["checks"].append(
            {
                "mode": "proto_v2_translated",
                "generation_ok": False,
                "evaluation_ok": False,
                "error": {"type": "PILOT_NO_PROTO_V2_OUTPUT", "message": "No proto_v2 output to translate."},
            }
        )
        return pilot
    translation = translate_proto_v2(proto_output)
    check = {
        "mode": "proto_v2_translated",
        "generation_ok": bool(translation.get("ok")),
        "model": translation.get("model_used"),
        "latency_ms": translation.get("latency_ms"),
        "http_status": translation.get("status_code"),
        "tokens_present": translation.get("total_tokens") is not None or translation.get("token_count_method") is not None,
        "token_count_method": translation.get("token_count_method"),
        "evaluation_ok": False,
        "evaluator_model": None,
        "error": None,
    }
    if not translation.get("ok"):
        check["error"] = {"type": translation.get("error_type"), "message": base.sanitize_error_text(translation.get("error"))}
        pilot["ok"] = False
        pilot["checks"].append(check)
        return pilot
    evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(task, "proto_v2_translated", translation["output"])
    check["evaluator_model"] = evaluator_model
    check["evaluation_ok"] = not bool(eval_error or parse_error)
    check["evaluation_error"] = eval_error
    check["evaluation"] = evaluation
    if not check["evaluation_ok"] or not check["tokens_present"]:
        pilot["ok"] = False
    pilot["checks"].append(check)
    return pilot


def run_experiment():
    if RUNS_PATH.exists():
        backup = RUNS_PATH.with_suffix(f".jsonl.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        RUNS_PATH.replace(backup)
    expected_calls = len(TASKS) * REPETITIONS * 3
    expected_calls += len(TASKS) * REPETITIONS
    expected_calls += len(TASKS) * REPETITIONS * 4
    if expected_calls > MAX_CALLS_INITIAL_RUN:
        raise base.ExperimentAbort(f"Plan excede MAX_CALLS_INITIAL_RUN: {expected_calls}")
    rows = []
    for task in TASKS:
        for run in range(1, REPETITIONS + 1):
            for mode in ("natural", "caveman", "proto_v2"):
                record = run_generation_and_evaluation(task, mode, run)
                rows.append(record)
                if mode == "proto_v2" and record.get("output"):
                    translation_result = translate_proto_v2(record["output"])
                    translated = run_generation_and_evaluation(
                        task,
                        "proto_v2_translated",
                        run,
                        output_result=translation_result,
                    )
                    rows.append(translated)
    return rows


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


def summarize_results(rows=None):
    rows = rows or read_runs()
    summary = {}
    natural_total = mean([r.get("total_tokens") for r in rows if r.get("mode") == "natural" and not r.get("error")])
    caveman_total = mean([r.get("total_tokens") for r in rows if r.get("mode") == "caveman" and not r.get("error")])
    for mode in ("natural", "caveman", "proto_v2", "proto_v2_translated"):
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
            "ahorro_vs_natural": None if not natural_total or total is None else 1 - (total / natural_total),
            "ahorro_vs_caveman": None if not caveman_total or total is None else 1 - (total / caveman_total),
            "avg_latency_ms": mean([r.get("latency_ms") for r in ok_rows]),
            "fidelidad_semantica": mean([r["evaluation"].get("fidelidad_semantica") for r in eval_rows]),
            "claridad": mean([r["evaluation"].get("claridad") for r in eval_rows]),
            "completitud": mean([r["evaluation"].get("completitud") for r in eval_rows]),
            "utilidad": mean([r["evaluation"].get("utilidad") for r in eval_rows]),
            "ambiguedad": mean([r["evaluation"].get("ambiguedad") for r in eval_rows]),
            "perdida_informacion": mean([r["evaluation"].get("perdida_informacion") for r in eval_rows]),
            "facilidad_traduccion": mean([r["evaluation"].get("facilidad_traduccion") for r in eval_rows]),
        }
    return summary


def success_status(summary):
    proto = summary["proto_v2"]
    proto_t = summary["proto_v2_translated"]
    proto_promising = (
        proto["avg_total_tokens"] is not None
        and proto["avg_total_tokens"] < EXP01_REFS["proto_v1_avg_tokens"]
        and proto["fidelidad_semantica"] is not None
        and proto["fidelidad_semantica"] >= 4.5
        and proto["utilidad"] is not None
        and proto["utilidad"] >= 4.5
        and proto["ambiguedad"] is not None
        and proto["ambiguedad"] <= 1.5
        and proto["perdida_informacion"] is not None
        and proto["perdida_informacion"] <= 1.5
    )
    translated_ok = (
        proto_t["avg_total_tokens"] is not None
        and proto_t["avg_total_tokens"] < EXP01_REFS["proto_v1_translated_avg_tokens"]
        and proto_t["fidelidad_semantica"] is not None
        and proto_t["fidelidad_semantica"] >= 4.3
        and proto_t["claridad"] is not None
        and proto_t["claridad"] >= 4.5
        and proto_t["perdida_informacion"] is not None
        and proto_t["perdida_informacion"] <= 1.5
    )
    return proto_promising, translated_ok


def results_table(summary):
    lines = [
        "| Modo | Filas | Errores | Tokens promedio | Ahorro vs natural | Ahorro vs caveman | Fidelidad | Claridad | Completitud | Ambiguedad | Perdida info | Utilidad | Latencia ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode in ("natural", "caveman", "proto_v2", "proto_v2_translated"):
        m = summary[mode]
        lines.append(
            f"| {mode} | {m['rows']} | {m['errors']} | {fmt(m['avg_total_tokens'])} | {pct(m['ahorro_vs_natural'])} | {pct(m['ahorro_vs_caveman'])} | {fmt(m['fidelidad_semantica'])} | {fmt(m['claridad'])} | {fmt(m['completitud'])} | {fmt(m['ambiguedad'])} | {fmt(m['perdida_informacion'])} | {fmt(m['utilidad'])} | {fmt(m['avg_latency_ms'], 0)} |"
        )
    return "\n".join(lines)


def comparison_table(summary):
    proto = summary["proto_v2"]
    proto_t = summary["proto_v2_translated"]
    natural = summary["natural"]
    caveman = summary["caveman"]
    rows = [
        "| Comparacion | EXP01 tokens | EXP02 tokens | Cambio tokens | EXP01 fidelidad | EXP02 fidelidad | Lectura |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    comparisons = [
        ("natural EXP02 vs natural EXP01", EXP01_REFS["natural_avg_tokens"], natural["avg_total_tokens"], EXP01_REFS["natural_fidelidad"], natural["fidelidad_semantica"]),
        ("caveman EXP02 vs caveman EXP01", EXP01_REFS["caveman_avg_tokens"], caveman["avg_total_tokens"], EXP01_REFS["caveman_fidelidad"], caveman["fidelidad_semantica"]),
        ("proto_v2 vs proto_v1 EXP01", EXP01_REFS["proto_v1_avg_tokens"], proto["avg_total_tokens"], EXP01_REFS["proto_v1_fidelidad"], proto["fidelidad_semantica"]),
        ("proto_v2_translated vs proto_v1_translated EXP01", EXP01_REFS["proto_v1_translated_avg_tokens"], proto_t["avg_total_tokens"], EXP01_REFS["proto_v1_translated_fidelidad"], proto_t["fidelidad_semantica"]),
        ("proto_v2 vs caveman EXP02", caveman["avg_total_tokens"], proto["avg_total_tokens"], caveman["fidelidad_semantica"], proto["fidelidad_semantica"]),
        ("proto_v2_translated vs caveman EXP02", caveman["avg_total_tokens"], proto_t["avg_total_tokens"], caveman["fidelidad_semantica"], proto_t["fidelidad_semantica"]),
    ]
    for label, old_tokens, new_tokens, old_fid, new_fid in comparisons:
        change = None if new_tokens is None else (new_tokens - old_tokens)
        if change is None:
            lectura = "NO_CALCULABLE"
        elif change < 0:
            lectura = "menos tokens"
        elif change > 0:
            lectura = "mas tokens"
        else:
            lectura = "igual"
        rows.append(f"| {label} | {fmt(old_tokens)} | {fmt(new_tokens)} | {fmt(change)} | {fmt(old_fid)} | {fmt(new_fid)} | {lectura} |")
    return "\n".join(rows)


def error_summary(rows):
    errors = {}
    for row in rows:
        err = row.get("error")
        if err:
            key = err.get("type") if isinstance(err, dict) else str(err)
            errors[key] = errors.get(key, 0) + 1
    if not errors:
        return "- No se registraron errores por fila."
    return "\n".join(f"- {key}: {value}" for key, value in sorted(errors.items()))


def cheapest_mode(summary):
    valid = {mode: m for mode, m in summary.items() if m["avg_total_tokens"] is not None}
    if not valid:
        return "NO_CALCULABLE"
    return min(valid.items(), key=lambda item: item[1]["avg_total_tokens"])[0]


def write_report(rows, pilot):
    summary = summarize_results(rows)
    proto_promising, translated_ok = success_status(summary)
    total_errors = len([r for r in rows if r.get("error")])
    content = f"""# Experimento 02: Proto v2 vs Caveman

## Objetivo

Probar si Proto v2, con etiquetas minimas y menor sobrecarga estructural, reduce tokens frente a Proto v1 y puede acercarse o superar al modo caveman.

## Hipotesis

Un protolenguaje simbolico v2, con etiquetas minimas y diccionario compacto, puede acercarse o superar al modo caveman en consumo de tokens sin perder demasiada fidelidad semantica.

## Cambios respecto al Experimento 01

- Proto v1 no se ejecuto de nuevo; se usa como referencia historica.
- Proto v2 reemplaza etiquetas largas por `T/G/C/P/S/R/V/N`.
- Caveman usa formato `P/S/R/N`.
- DeepSeek V4 se ejecuto con `thinking: disabled`.

## Configuracion

- Endpoint usado: `{CHAT_COMPLETIONS_URL}`
- Modelo generador: `{GENERATION_MODEL}`
- Modelo generador fallback: `{GENERATION_MODEL_FALLBACK}`
- Modelo evaluador: `{EVALUATOR_MODEL}`
- Modelo evaluador fallback: `{EVALUATOR_MODEL_FALLBACK}`
- Tareas: {len(TASKS)}
- Repeticiones: {REPETITIONS}
- Temperatura: {TEMPERATURE}
- Max llamadas: {MAX_CALLS_INITIAL_RUN}
- Llamadas HTTP intentadas: {base.CALL_STATS["attempted"]}
- Llamadas HTTP exitosas: {base.CALL_STATS["successful"]}
- Errores HTTP: {base.CALL_STATS["errors"]}
- Fecha: {utc_now_iso()}

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Tabla de resultados EXP02

{results_table(summary)}

## Comparacion con EXP01

{comparison_table(summary)}

## Analisis

- Modo mas barato EXP02: `{cheapest_mode(summary)}`.
- Proto v2 prometedor segun criterios: `{proto_promising}`.
- Proto v2 traducido aceptable segun criterios: `{translated_ok}`.
- Proto v2 debe evaluarse no solo por tokens, sino tambien por fidelidad, utilidad, ambiguedad y perdida de informacion.

## Errores

{error_summary(rows)}

## Conclusion parcial

Esta tanda exploratoria no demuestra la tesis por si sola. Si Proto v2 reduce tokens frente a Proto v1, eso indica que la sobrecarga estructural era parte del problema. Si caveman sigue ganando, el protocolo necesita una v3 aun mas compacta o una tarea donde la estructura aporte mas valor que costo. Si Proto v2 traducido sigue siendo caro, la arquitectura debe reservar traduccion solo para salidas finales realmente necesarias.

## Recomendacion para Experimento 03

- Probar Proto v3 sin todas las etiquetas obligatorias.
- Medir variantes `key:value` en una sola linea.
- Comparar tareas con mayor necesidad de estado y memoria.
- Agregar evaluacion humana de una muestra.
- Probar si un traductor final puede procesar lotes de Proto en una sola llamada.
"""
    REPORT_PATH.write_text(content, encoding="utf-8")
    write_observations(summary, rows)
    write_conclusions(summary, rows, proto_promising, translated_ok)


def write_observations(summary, rows):
    content = f"""# Observaciones Experimento 02

## Proposito

Registrar observaciones reales de EXP02.

## Estado

EJECUTADO.

## Datos base

- Fecha: {utc_now_iso()}
- Filas registradas: {len(rows)}
- Errores registrados: {len([r for r in rows if r.get("error")])}
- Modo mas barato: `{cheapest_mode(summary)}`

## Observaciones

- Tokens promedio natural: {fmt(summary["natural"]["avg_total_tokens"])}.
- Tokens promedio caveman: {fmt(summary["caveman"]["avg_total_tokens"])}.
- Tokens promedio proto_v2: {fmt(summary["proto_v2"]["avg_total_tokens"])}.
- Tokens promedio proto_v2_translated: {fmt(summary["proto_v2_translated"]["avg_total_tokens"])}.
- Proto v2 vs Proto v1 EXP01: {fmt(summary["proto_v2"]["avg_total_tokens"])} vs {EXP01_REFS["proto_v1_avg_tokens"]}.
- Proto v2 vs caveman EXP02: {fmt(summary["proto_v2"]["avg_total_tokens"])} vs {fmt(summary["caveman"]["avg_total_tokens"])}.

## Proximos pasos

- Revisar manualmente salidas de Proto v2.
- Identificar etiquetas o campos que sobran.
- Diseñar Proto v3 si caveman sigue ganando.
"""
    OBSERVATIONS_PATH.write_text(content, encoding="utf-8")


def write_conclusions(summary, rows, proto_promising, translated_ok):
    content = f"""# Conclusiones Experimento 02

## Proposito

Registrar conclusiones parciales basadas solo en datos reales de EXP02.

## Estado

EJECUTADO_CON_DATOS_INICIALES.

## Conclusion parcial

- Proto v2 prometedor segun criterios: `{proto_promising}`.
- Proto v2 traducido aceptable segun criterios: `{translated_ok}`.
- Modo mas barato: `{cheapest_mode(summary)}`.
- Errores registrados: {len([r for r in rows if r.get("error")])}.

La conclusion sigue siendo parcial. EXP02 prueba una mejora de diseño frente a Proto v1, pero no reemplaza pruebas con mas tareas, dominios, modelos y evaluacion humana.

## Proximos pasos

- Comparar cualitativamente salidas de caveman y Proto v2.
- Probar Proto v3 con campos opcionales.
- Evaluar compresion por lotes para traduccion final.
"""
    CONCLUSIONS_PATH.write_text(content, encoding="utf-8")


def write_error(pilot, message):
    content = f"""# Error Experimento 02

## Fecha

{utc_now_iso()}

## Causa resumida

{message}

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Seguridad

No se registra API key en este archivo.

## Proximo paso

Corregir causa del piloto y repetir antes de ejecutar tanda completa.
"""
    ERROR_PATH.write_text(content, encoding="utf-8")


def main():
    ensure_directories()
    require_api_key()
    models = base.list_models()
    if not models.get("ok"):
        write_error({}, f"Fallo /models: {models.get('error_type')}")
        return 1
    pilot = pilot_check()
    if not pilot.get("ok"):
        write_error(pilot, "Piloto EXP02 fallo. No se ejecuto tanda completa.")
        print("Piloto EXP02 fallo. Ver Error_Experimento_02.md")
        return 1
    rows = run_experiment()
    write_report(rows, pilot)
    print(f"Experimento 02 terminado. Filas={len(rows)} llamadas_http={base.CALL_STATS['attempted']} errores_http={base.CALL_STATS['errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
