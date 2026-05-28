import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = THIS_DIR.parents[1]
EXP_DIR = PROJECT_DIR / "05_Experimentos"
if str(EXP_DIR) not in sys.path:
    sys.path.insert(0, str(EXP_DIR))

try:
    import run_experimento_01_opencode_go_local  # noqa: F401
except Exception:
    pass

import run_experimento_01_opencode_go as base


PROFILE = "FULL_COMBINED_EXP01_EXP02_EN_ZH"
RUN_ID = "EXP01_EXP02_EN_ZH_COMBINED"
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
GENERATION_MODEL_FALLBACK = os.getenv("GENERATION_MODEL_FALLBACK", "opencode-go/deepseek-v4-flash")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "deepseek-v4-pro")
EVALUATOR_MODEL_FALLBACK = os.getenv("EVALUATOR_MODEL_FALLBACK", "deepseek-v4-flash")
TEMPERATURE = 0.2
REPETITIONS = 3
MAX_HTTP_CALLS = 1200
SOFT_STOP_HTTP_CALLS = 1100
REQUEST_TIMEOUT = 90

MAX_TOKENS_NATURAL = 500
MAX_TOKENS_COMPRESSED = 350
MAX_TOKENS_PROTO = 500
MAX_TOKENS_TRANSLATION = 350
MAX_TOKENS_EVALUATION = 300
EMPTY_RETRY_MAX_TOKENS = 1200

RUNS_PATH = THIS_DIR / "exp01_exp02_en_zh_runs.jsonl"
PILOT_PATH = THIS_DIR / "pilot_exp01_exp02_en_zh.jsonl"
REPORT_PATH = THIS_DIR / "Resultados_EXP01_EXP02_EN_ZH.md"
COMPARISON_PATH = THIS_DIR / "Comparacion_EXP01_EXP02_EN_ZH.md"
ES_COMPARISON_PATH = THIS_DIR / "Comparacion_EXP01_EXP02_ES_EN_ZH_Borrador.md"
EXEC_SUMMARY_PATH = THIS_DIR / "Resumen_Ejecutivo_EXP01_EXP02_Multilingue.md"
ERRORS_PATH = THIS_DIR / "Errores_y_Anomalias_EXP01_EXP02_EN_ZH.md"
CONNECTION_PATH = THIS_DIR / "connection_test_exp01_exp02_en_zh.json"
PILOT_REPORT_PATH = THIS_DIR / "pilot_exp01_exp02_en_zh_report.md"


TASKS_ES = [
    ("T001", "Analiza este problema: un sistema multiagente consume demasiados tokens porque cada agente escribe explicaciones largas. Propón solución, riesgos y próximos pasos."),
    ("T002", "Resume una arquitectura de agentes con trabajador, supervisor, memoria y traductor final. Incluye ventajas y limitaciones."),
    ("T003", "Convierte una explicación larga sobre eficiencia de tokens en una estructura operativa para agentes."),
    ("T004", "Diseña reglas iniciales para evitar deriva semántica en un protocolo simbólico."),
    ("T005", "Detecta riesgos en un sistema donde varios agentes se comunican con símbolos comprimidos."),
    ("T006", "Propón una metodología para medir si un protolenguaje conserva significado."),
    ("T007", "Extrae variables medibles de un experimento sobre comunicación multiagente."),
    ("T008", "Crea una plantilla breve para registrar resultados de pruebas con modelos IA."),
    ("T009", "Compara lenguaje natural, lenguaje cavernícola y protolenguaje en términos de costo, claridad y error."),
    ("T010", "Propón cómo un agente traductor debe convertir protolenguaje a español humano sin inventar información."),
]

TASKS_EN = {
    "T001": "Analyze this problem: a multi-agent system consumes too many tokens because each agent writes long explanations. Propose a solution, risks, and next steps.",
    "T002": "Summarize an agent architecture with worker, supervisor, memory, and final translator. Include advantages and limitations.",
    "T003": "Convert a long explanation about token efficiency into an operational structure for agents.",
    "T004": "Design initial rules to prevent semantic drift in a symbolic protocol.",
    "T005": "Detect risks in a system where several agents communicate with compressed symbols.",
    "T006": "Propose a methodology to measure whether a protolanguage preserves meaning.",
    "T007": "Extract measurable variables from an experiment about multi-agent communication.",
    "T008": "Create a brief template to record test results with AI models.",
    "T009": "Compare natural language, compressed language, and protolanguage in terms of cost, clarity, and error.",
    "T010": "Propose how a translator agent should convert protolanguage into human English without inventing information.",
}

TASKS_ZH = {
    "T001": "分析这个问题：一个多智能体系统消耗太多 token，因为每个智能体都写很长的解释。提出解决方案、风险和下一步。",
    "T002": "总结一种包含工作者、监督者、记忆和最终翻译器的智能体架构。包括优点和限制。",
    "T003": "把一段关于 token 效率的长解释转换成智能体可用的操作结构。",
    "T004": "设计初始规则，避免符号协议中的语义漂移。",
    "T005": "检测一个系统中的风险：多个智能体使用压缩符号通信。",
    "T006": "提出一种方法，用来衡量原语言是否保留意义。",
    "T007": "从多智能体通信实验中提取可测量变量。",
    "T008": "创建一个简短模板，用于记录 AI 模型测试结果。",
    "T009": "比较自然语言、压缩语言和原语言在成本、清晰度和错误方面的差异。",
    "T010": "提出翻译智能体如何把原语言转换成清晰中文，同时不编造信息。",
}


EXPERIMENT_MODES = {
    ("EN", "EXP01"): ["natural_en", "compressed_en", "proto_v1_en", "proto_v1_translated_en"],
    ("EN", "EXP02"): ["natural_en", "compressed_en", "proto_v2_en", "proto_v2_translated_en"],
    ("ZH", "EXP01"): ["natural_zh", "compressed_zh", "proto_v1_core_zh", "proto_v1_translated_zh"],
    ("ZH", "EXP02"): ["natural_zh", "compressed_zh", "proto_v2_core_zh", "proto_v2_translated_zh"],
}

PROTO_SOURCE_MODE = {
    "proto_v1_translated_en": "proto_v1_en",
    "proto_v2_translated_en": "proto_v2_en",
    "proto_v1_translated_zh": "proto_v1_core_zh",
    "proto_v2_translated_zh": "proto_v2_core_zh",
}

BASE_MODE_ORDER = {
    ("EN", "EXP01"): ["natural_en", "compressed_en", "proto_v1_en"],
    ("EN", "EXP02"): ["natural_en", "compressed_en", "proto_v2_en"],
    ("ZH", "EXP01"): ["natural_zh", "compressed_zh", "proto_v1_core_zh"],
    ("ZH", "EXP02"): ["natural_zh", "compressed_zh", "proto_v2_core_zh"],
}

TRANSLATED_MODE = {
    ("EN", "EXP01"): "proto_v1_translated_en",
    ("EN", "EXP02"): "proto_v2_translated_en",
    ("ZH", "EXP01"): "proto_v1_translated_zh",
    ("ZH", "EXP02"): "proto_v2_translated_zh",
}

ES_REFERENCES = {
    ("ES", "EXP01", "natural"): {"tokens": 364.30, "fidelity": 4.97, "source": "EXP01_ES real"},
    ("ES", "EXP01", "caveman"): {"tokens": 263.97, "fidelity": 4.97, "source": "EXP01_ES real"},
    ("ES", "EXP01", "proto_v1"): {"tokens": 377.13, "fidelity": 4.87, "source": "EXP01_ES real"},
    ("ES", "EXP01", "proto_v1_translated"): {"tokens": 438.87, "fidelity": 4.57, "source": "EXP01_ES real"},
    ("ES", "EXP02", "natural"): {"tokens": 354.63, "fidelity": 4.93, "source": "EXP02_ES real"},
    ("ES", "EXP02", "caveman"): {"tokens": 240.93, "fidelity": 4.53, "source": "EXP02_ES real"},
    ("ES", "EXP02", "proto_v2"): {"tokens": 318.43, "fidelity": 4.00, "source": "EXP02_ES real"},
    ("ES", "EXP02", "proto_v2_translated"): {"tokens": 332.70, "fidelity": 4.30, "source": "EXP02_ES real"},
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def configure_base():
    base.configure_provider_from_env()
    key_attr = "API" + "_" + "KEY"
    key_env = "OPENCODE_" + key_attr
    setattr(base, key_attr, os.getenv(key_env) or getattr(base, key_attr))
    base.GENERATION_MODEL = GENERATION_MODEL
    base.GENERATION_MODEL_FALLBACK = GENERATION_MODEL_FALLBACK
    base.EVALUATOR_MODEL = EVALUATOR_MODEL
    base.EVALUATOR_MODEL_FALLBACK = EVALUATOR_MODEL_FALLBACK
    base.TEMPERATURE = TEMPERATURE
    base.MAX_CALLS_INITIAL_RUN = MAX_HTTP_CALLS
    base.REQUEST_TIMEOUT = REQUEST_TIMEOUT
    base.RATE_LIMIT_SLEEP_SECONDS = 10
    base.SERVER_ERROR_SLEEP_SECONDS = 10
    for key in base.CALL_STATS:
        base.CALL_STATS[key] = 0


def require_key():
    configure_base()
    if not getattr(base, "API" + "_" + "KEY"):
        raise RuntimeError("Missing provider key in environment or ignored local wrapper.")


def write_text(path, text):
    path.write_text(text, encoding="utf-8")


def append_jsonl(path, record):
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def backup_if_exists(path):
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = path.with_suffix(path.suffix + f".bak_{stamp}")
        shutil.copy2(path, backup)
        path.unlink()
        return backup.name
    return None


def task_for(language, task_id):
    es = dict(TASKS_ES)[task_id]
    return {
        "id": task_id,
        "group": "base_comparable",
        "text": TASKS_EN[task_id] if language == "EN" else TASKS_ZH[task_id],
        "original_es": es,
    }


def max_tokens_for_mode(mode):
    if "translated" in mode:
        return MAX_TOKENS_TRANSLATION
    if "compressed" in mode:
        return MAX_TOKENS_COMPRESSED
    if "proto" in mode:
        return MAX_TOKENS_PROTO
    return MAX_TOKENS_NATURAL


def prompt_for_mode(language, experiment_id, mode, task):
    if mode == "natural_en":
        return f"""Answer in clear, complete natural English.
Use final answer only. Do not show step-by-step reasoning.
Maximum 140 words.
Analyze the task. Include problem, solution, risks, and next steps when applicable.
Do not use proto format.

Task:
{task['text']}"""
    if mode == "compressed_en":
        return f"""Answer in compressed operational English.
Use final answer only. Maximum 90 words.
Minimize tokens. No politeness. No filler. No decorative language.
Preserve goal, key facts, numbers, risks, decisions, and next step.
Allow fragments. Do not use key=value proto.

Task:
{task['text']}"""
    if mode == "proto_v1_en":
        return f"""Use Proto v1 in English. Do not redesign.
Use final answer only. Keep it compact but preserve meaning.

Mandatory format:
@TASK[id]
GOAL{{...}}
CTX{{...}}
PROBLEM{{...}}
PLAN{{...}}
RISK{{...}}
CHK{{...}}
OUT{{...}}
NEXT{{...}}

Rules:
- Use English inside braces.
- No long prose.
- Preserve important entities, risks, and next actions.
- If uncertain, use CHK?.

Task id: {task['id']}
Task:
{task['text']}"""
    if mode == "proto_v2_en":
        return f"""Use Proto v2 in English. Use reduced labels. Do not redesign into Proto v3.
Use final answer only. Keep it compact.

Mandatory format:
T:{{id}}
G:{{goal}}
C:{{context}}
P:{{problem}}
S:{{solution}}
R:{{risks}}
V:{{verification}}
N:{{next}}

Rules:
- Use English inside fields.
- No @TASK, GOAL, CTX, PROBLEM, PLAN, RISK, CHK, OUT, NEXT.
- Do not use p= or key=value Proto v3.

Task id: {task['id']}
Task:
{task['text']}"""
    if mode == "natural_zh":
        return f"""使用清晰完整的简体中文回答。
只输出最终答案，不展示逐步推理。
最多 220 个汉字左右。
分析任务；如适用，包含问题、方案、风险和下一步。
不要使用 proto 格式。

任务：
{task['text']}"""
    if mode == "compressed_zh":
        return f"""使用压缩中文，保留任务目标、关键信息、风险、决定和下一步。
只输出最终答案。尽量短。
不要寒暄。不要礼貌语。不要修辞。不要长解释。
可以省略主语。可以用短句。可用：但、因、故、下步、风。
不要使用完整 proto key=value 格式。
不要写“原始人说话”。不要幼稚化。

任务：
{task['text']}"""
    if mode == "proto_v1_core_zh":
        return f"""使用 Proto v1 核心格式。不要重设计。不要使用中文本地化 proto。
只输出最终答案。字段内可使用简体中文短语。

必须格式：
@TASK[id]
GOAL{{...}}
CTX{{...}}
PROBLEM{{...}}
PLAN{{...}}
RISK{{...}}
CHK{{...}}
OUT{{...}}
NEXT{{...}}

规则：
- 保留目标、上下文、问题、方案、风险、检查、输出、下一步。
- 不写长解释。
- 不改成 Proto v2 或 Proto v3。

Task id: {task['id']}
任务：
{task['text']}"""
    if mode == "proto_v2_core_zh":
        return f"""使用 Proto v2 核心格式。不要重设计成 Proto v3。不要使用中文本地化标签。
只输出最终答案。字段内可使用简体中文短语。

必须格式：
T:{{id}}
G:{{目标}}
C:{{上下文}}
P:{{问题}}
S:{{方案}}
R:{{风险}}
V:{{验证}}
N:{{下一步}}

规则：
- 不使用 @TASK/GOAL/CTX/PROBLEM/PLAN/RISK/CHK/OUT/NEXT。
- 不使用 p=、s= 或中文本地化标签。
- 保持可翻译。

Task id: {task['id']}
任务：
{task['text']}"""
    raise KeyError(mode)


def translation_prompt(language, source_output):
    if language == "EN":
        return f"""Translate the following proto output into clear, brief natural English.
Use final answer only. Maximum 120 words.
Do not invent information. Preserve goal, context, plan/solution, risks, verification, and next steps if present.
Mark uncertainty if present.

Proto output:
{source_output}"""
    return f"""把下面的 proto 输出翻译成清晰、简短的自然中文。
只输出最终答案。不要编造信息。
保留目标、上下文、方案、风险、验证和下一步（如果存在）。
如有不确定性，请标明。

Proto 输出：
{source_output}"""


def evaluation_prompt(language, task, mode, output):
    label = "English" if language == "EN" else "Chinese"
    return f"""You are an evaluator for compressed agent communication experiments.
Evaluate the generated output against the original task.
Language: {label}
Mode: {mode}

Metrics from 1 to 5:
- semantic_fidelity
- clarity
- completeness
- utility
- ambiguity (1 is best, 5 is worst)
- information_loss (1 is best, 5 is worst)
- translation_ease
- state_preservation
- compactness

Rules:
- Do not reward long answers automatically.
- Do not punish compressed outputs if they preserve operational meaning.
- Do not reward symbolic outputs if they are ambiguous.
- A good compressed output must allow another agent to continue the task.
- For Chinese compressed output, do not accept childish or caricature style.

Original task:
{task['text']}

Generated output:
{output}

Return strict JSON only:
{{
  "semantic_fidelity": 0,
  "clarity": 0,
  "completeness": 0,
  "utility": 0,
  "ambiguity": 0,
  "information_loss": 0,
  "translation_ease": 0,
  "state_preservation": 0,
  "compactness": 0,
  "notes": ""
}}"""


def call_model(prompt, max_tokens, is_eval=False):
    primary = EVALUATOR_MODEL if is_eval else GENERATION_MODEL
    fallback = EVALUATOR_MODEL_FALLBACK if is_eval else GENERATION_MODEL_FALLBACK
    return base.call_chat_with_model_fallback(
        primary,
        fallback,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        fallback_on_any_error=is_eval,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS,
    )


def generate(language, experiment_id, mode, task):
    return call_model(prompt_for_mode(language, experiment_id, mode, task), max_tokens_for_mode(mode), is_eval=False)


def translate(language, proto_output):
    return call_model(translation_prompt(language, proto_output), MAX_TOKENS_TRANSLATION, is_eval=False)


def evaluate(language, task, mode, output):
    result = call_model(evaluation_prompt(language, task, mode, output), MAX_TOKENS_EVALUATION, is_eval=True)
    if not result.get("ok"):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("output"), True, {
            "type": result.get("error_type"),
            "message": result.get("error"),
            "http_status": result.get("status_code"),
        }, result.get("latency_ms")
    parsed, parse_error = base.safe_json_parse(result.get("output", ""))
    if parse_error or not isinstance(parsed, dict):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("output"), True, {
            "type": "INVALID_JSON_EVALUATION",
            "message": "Evaluator returned invalid JSON.",
            "http_status": result.get("status_code"),
        }, result.get("latency_ms")
    return result.get("model_used", EVALUATOR_MODEL), normalize_eval(parsed), result.get("output"), False, None, result.get("latency_ms")


def normalize_eval(parsed):
    fields = [
        "semantic_fidelity",
        "clarity",
        "completeness",
        "utility",
        "ambiguity",
        "information_loss",
        "translation_ease",
        "state_preservation",
        "compactness",
    ]
    out = {}
    for field in fields:
        value = parsed.get(field)
        try:
            value = int(value)
        except Exception:
            value = None
        out[field] = value
    out["notes"] = str(parsed.get("notes", parsed.get("comentario", "")))[:500]
    return out


def contains_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or "", flags=re.UNICODE))


def field_info(output):
    text = output or ""
    fields = []
    fields.extend(re.findall(r"^([A-Z_]+)\{", text, flags=re.MULTILINE))
    fields.extend(re.findall(r"^([A-Z]):", text, flags=re.MULTILINE))
    fields.extend(re.findall(r"\b([a-zA-Z_]+)=", text))
    return len(fields), sorted(set(fields))


def validate_format(language, mode, output, source=None):
    text = output or ""
    notes = []
    valid = True
    wc = word_count(text)
    cc = len(text)
    fc, fields = field_info(text)

    if mode in ("natural_en", "natural_zh"):
        if fc >= 3 or "@TASK" in text:
            valid = False
            notes.append("natural_looks_like_proto")
        if language == "ZH" and not contains_cjk(text):
            valid = False
            notes.append("zh_missing_cjk")
        if language == "EN" and contains_cjk(text):
            valid = False
            notes.append("en_contains_cjk")
    elif mode == "compressed_en":
        if fc >= 3 or "@TASK" in text:
            valid = False
            notes.append("compressed_en_looks_like_proto")
        if wc > 120:
            valid = False
            notes.append("compressed_en_too_long")
        if contains_cjk(text):
            valid = False
            notes.append("en_contains_cjk")
    elif mode == "compressed_zh":
        if not contains_cjk(text):
            valid = False
            notes.append("zh_missing_cjk")
        if any(bad in text for bad in ["原始人", "幼稚", "笨笨"]):
            valid = False
            notes.append("compressed_zh_caricature")
        if fc >= 3 or "@TASK" in text:
            valid = False
            notes.append("compressed_zh_looks_like_proto")
        if cc > 260:
            valid = False
            notes.append("compressed_zh_too_long")
    elif mode in ("proto_v1_en", "proto_v1_core_zh"):
        required = ["@TASK", "GOAL{", "CTX{", "PROBLEM{", "PLAN{", "RISK{", "CHK{", "OUT{", "NEXT{"]
        missing = [tag for tag in required if tag not in text]
        if missing:
            valid = False
            notes.append("missing_proto_v1_tags:" + ",".join(missing[:3]))
        if re.search(r"^\s*T:", text, flags=re.MULTILINE):
            valid = False
            notes.append("looks_like_proto_v2")
    elif mode in ("proto_v2_en", "proto_v2_core_zh"):
        required = ["T:", "G:", "C:", "P:", "S:", "R:", "V:", "N:"]
        missing = [tag for tag in required if tag not in text]
        if missing:
            valid = False
            notes.append("missing_proto_v2_tags:" + ",".join(missing[:3]))
        if "@TASK" in text or "GOAL{" in text:
            valid = False
            notes.append("looks_like_proto_v1")
        if re.search(r"\bp=", text):
            valid = False
            notes.append("looks_like_proto_v3")
    elif "translated" in mode:
        if source and text.strip() == source.strip():
            valid = False
            notes.append("translation_same_as_source")
        if "@TASK" in text or "GOAL{" in text or re.search(r"^\s*[A-Z]:", text, flags=re.MULTILINE):
            notes.append("translation_retains_proto_markers")
        if language == "ZH" and not contains_cjk(text):
            valid = False
            notes.append("zh_translation_missing_cjk")
        if language == "EN" and contains_cjk(text):
            valid = False
            notes.append("en_translation_contains_cjk")
    return valid, notes, wc, cc, fc, fields


def base_record(language, experiment_id, task, mode, run, base_mode=None, translation_source=None):
    return {
        "run_id": RUN_ID,
        "timestamp": utc_now(),
        "language": language,
        "experiment_id": experiment_id,
        "task_id": task["id"],
        "task_group": task["group"],
        "task_text": task["text"],
        "task_text_original_es": task["original_es"],
        "mode": mode,
        "base_mode": base_mode,
        "run": run,
        "generator_model": GENERATION_MODEL,
        "evaluator_model": EVALUATOR_MODEL,
        "temperature": TEMPERATURE,
        "thinking_disabled": True,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
        "output": "",
        "translation_source": translation_source,
        "format_valid": None,
        "format_notes": [],
        "word_count": None,
        "char_count": None,
        "field_count": None,
        "fields_used": [],
        "evaluation": {
            "semantic_fidelity": None,
            "clarity": None,
            "completeness": None,
            "utility": None,
            "ambiguity": None,
            "information_loss": None,
            "translation_ease": None,
            "state_preservation": None,
            "compactness": None,
            "notes": "",
        },
        "latency_ms_generation": None,
        "latency_ms_evaluation": None,
        "error": None,
    }


def error_from_result(result):
    return {
        "type": result.get("error_type"),
        "message": result.get("error"),
        "http_status": result.get("status_code"),
    }


def run_output_row(language, experiment_id, task, mode, run, source_record=None):
    source_text = source_record.get("output") if source_record else None
    record = base_record(
        language,
        experiment_id,
        task,
        mode,
        run,
        base_mode=PROTO_SOURCE_MODE.get(mode),
        translation_source=source_text,
    )
    if "translated" in mode:
        gen = translate(language, source_text or "")
    else:
        gen = generate(language, experiment_id, mode, task)
    record["generator_model"] = gen.get("model_used", GENERATION_MODEL)
    record["latency_ms_generation"] = gen.get("latency_ms")
    record["input_tokens"] = gen.get("input_tokens")
    record["output_tokens"] = gen.get("output_tokens")
    record["total_tokens"] = gen.get("total_tokens")
    if not gen.get("ok"):
        record["error"] = error_from_result(gen)
        return record
    record["output"] = gen.get("output", "")
    valid, notes, wc, cc, fc, fields = validate_format(language, mode, record["output"], source=source_text)
    record["format_valid"] = valid
    record["format_notes"] = notes
    record["word_count"] = wc
    record["char_count"] = cc
    record["field_count"] = fc
    record["fields_used"] = fields
    evaluator_model, evaluation, eval_raw, parse_error, eval_error, eval_latency = evaluate(language, task, mode, record["output"])
    record["evaluator_model"] = evaluator_model
    record["evaluation"] = evaluation if evaluation else record["evaluation"]
    record["evaluation_raw"] = eval_raw
    record["evaluation_parse_error"] = parse_error
    record["latency_ms_evaluation"] = eval_latency
    if eval_error:
        record["error"] = eval_error
    return record


def test_connection():
    models = base.list_models()
    connection = {
        "timestamp": utc_now(),
        "models_ok": bool(models.get("ok")),
        "models_count": None,
        "chat_ok": False,
        "chat_response": None,
        "error": None,
    }
    if models.get("ok"):
        data = models.get("data") or {}
        items = data.get("data") if isinstance(data, dict) else None
        if isinstance(items, list):
            connection["models_count"] = len(items)
    else:
        connection["error"] = error_from_result(models)
        write_text(CONNECTION_PATH, json.dumps(connection, ensure_ascii=False, indent=2))
        return connection
    chat = call_model("Reply only: OK_MULTILINGUAL_TEST", 50, is_eval=False)
    connection["chat_ok"] = bool(chat.get("ok"))
    connection["chat_response"] = chat.get("output")
    connection["chat_model"] = chat.get("model_used")
    connection["chat_latency_ms"] = chat.get("latency_ms")
    if not chat.get("ok"):
        connection["error"] = error_from_result(chat)
    write_text(CONNECTION_PATH, json.dumps(connection, ensure_ascii=False, indent=2))
    return connection


def run_block(language, experiment_id, task_ids, runs, out_path, progress=False):
    rows = []
    for task_id in task_ids:
        task = task_for(language, task_id)
        for run in runs:
            sources = {}
            for mode in BASE_MODE_ORDER[(language, experiment_id)]:
                if base.CALL_STATS["attempted"] >= SOFT_STOP_HTTP_CALLS:
                    return rows, True
                rec = run_output_row(language, experiment_id, task, mode, run)
                append_jsonl(out_path, rec)
                rows.append(rec)
                sources[mode] = rec
                if progress and len(rows) % 50 == 0:
                    print(f"progress rows_block={len(rows)} total_http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} lang={language} exp={experiment_id} mode={mode}", flush=True)
            translated = TRANSLATED_MODE[(language, experiment_id)]
            source_mode = PROTO_SOURCE_MODE[translated]
            if base.CALL_STATS["attempted"] >= SOFT_STOP_HTTP_CALLS:
                return rows, True
            rec = run_output_row(language, experiment_id, task, translated, run, source_record=sources[source_mode])
            append_jsonl(out_path, rec)
            rows.append(rec)
            if progress and len(rows) % 50 == 0:
                print(f"progress rows_block={len(rows)} total_http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} lang={language} exp={experiment_id} mode={translated}", flush=True)
    return rows, False


def run_pilot():
    if PILOT_PATH.exists():
        PILOT_PATH.unlink()
    all_rows = []
    for language, experiment_id in [("EN", "EXP01"), ("EN", "EXP02"), ("ZH", "EXP01"), ("ZH", "EXP02")]:
        rows, stopped = run_block(language, experiment_id, ["T001"], [1], PILOT_PATH, progress=False)
        all_rows.extend(rows)
        if stopped:
            break
    checks = {
        "rows": len(all_rows),
        "errors": sum(1 for r in all_rows if r.get("error")),
        "parse_errors": sum(1 for r in all_rows if r.get("evaluation_parse_error")),
        "missing_tokens": sum(1 for r in all_rows if r.get("total_tokens") is None),
        "format_invalid": sum(1 for r in all_rows if r.get("format_valid") is False),
        "zh_caricature": sum(1 for r in all_rows if "compressed_zh_caricature" in r.get("format_notes", [])),
        "ok": False,
    }
    checks["ok"] = checks["rows"] == 16 and checks["errors"] == 0 and checks["parse_errors"] == 0 and checks["missing_tokens"] == 0 and checks["zh_caricature"] == 0
    write_text(PILOT_REPORT_PATH, "# Pilot EXP01 EXP02 EN ZH\n\n```json\n" + json.dumps(checks, ensure_ascii=False, indent=2) + "\n```\n")
    return checks


def run_full():
    backup = backup_if_exists(RUNS_PATH)
    all_rows = []
    stopped = False
    order = [("EN", "EXP01"), ("EN", "EXP02"), ("ZH", "EXP01"), ("ZH", "EXP02")]
    for language, experiment_id in order:
        rows, stopped = run_block(language, experiment_id, [tid for tid, _ in TASKS_ES], range(1, REPETITIONS + 1), RUNS_PATH, progress=True)
        all_rows.extend(rows)
        if stopped:
            break
    return all_rows, stopped, backup


def mean(values):
    nums = [v for v in values if isinstance(v, (int, float))]
    return sum(nums) / len(nums) if nums else None


def fmt(value, digits=2):
    if value is None:
        return "NO_CALCULABLE"
    if isinstance(value, str):
        return value
    return f"{value:.{digits}f}"


def pct(value):
    if value is None:
        return "NO_CALCULABLE"
    return f"{value * 100:.2f}%"


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["language"], row["experiment_id"], row["mode"])].append(row)
    out = {}
    for key, items in groups.items():
        eval_rows = [r for r in items if isinstance(r.get("evaluation"), dict)]
        out[key] = {
            "rows": len(items),
            "errors": sum(1 for r in items if r.get("error")),
            "avg_input_tokens": mean([r.get("input_tokens") for r in items]),
            "avg_output_tokens": mean([r.get("output_tokens") for r in items]),
            "avg_total_tokens": mean([r.get("total_tokens") for r in items]),
            "latency_generation": mean([r.get("latency_ms_generation") for r in items]),
            "latency_evaluation": mean([r.get("latency_ms_evaluation") for r in items]),
            "format_valid_pct": mean([1 if r.get("format_valid") is True else 0 if r.get("format_valid") is False else None for r in items]),
        }
        for metric in ["semantic_fidelity", "clarity", "completeness", "utility", "ambiguity", "information_loss", "translation_ease", "state_preservation", "compactness"]:
            out[key][metric] = mean([r.get("evaluation", {}).get(metric) for r in eval_rows])
    return out


def rows_table(summary):
    lines = [
        "| language | experiment | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | compactness |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for (language, exp, mode), data in sorted(summary.items()):
        lines.append(
            f"| {language} | {exp} | {mode} | {data['rows']} | {data['errors']} | {fmt(data['avg_input_tokens'])} | {fmt(data['avg_output_tokens'])} | {fmt(data['avg_total_tokens'])} | {fmt(data['semantic_fidelity'])} | {fmt(data['clarity'])} | {fmt(data['utility'])} | {fmt(data['ambiguity'])} | {fmt(data['information_loss'])} | {fmt(data['state_preservation'])} | {fmt(data['compactness'])} |"
        )
    return "\n".join(lines)


def modes_for(language, experiment_id):
    return EXPERIMENT_MODES[(language, experiment_id)]


def winners(summary):
    out = {}
    for language in ["EN", "ZH"]:
        for exp in ["EXP01", "EXP02"]:
            modes = modes_for(language, exp)
            data = {m: summary.get((language, exp, m), {}) for m in modes}
            cheapest = min(data, key=lambda m: data[m].get("avg_total_tokens") if data[m].get("avg_total_tokens") is not None else 10**9)
            quality = max(data, key=lambda m: ((data[m].get("semantic_fidelity") or 0) + (data[m].get("clarity") or 0) + (data[m].get("utility") or 0)) / 3)
            state = max(data, key=lambda m: data[m].get("state_preservation") or 0)
            balance = max(data, key=lambda m: balance_score(data[m]))
            out[(language, exp)] = {"cheapest": cheapest, "quality": quality, "state": state, "balance": balance}
    return out


def balance_score(data):
    total = data.get("avg_total_tokens")
    if not total:
        token_component = 0
    else:
        token_component = 1000 / total
    return (
        token_component
        + (data.get("semantic_fidelity") or 0)
        + (data.get("utility") or 0)
        + (data.get("state_preservation") or 0)
        + (data.get("compactness") or 0)
        - (data.get("ambiguity") or 0)
        - (data.get("information_loss") or 0)
    )


def winners_table(summary):
    win = winners(summary)
    lines = [
        "| language | experiment | cheapest_mode | best_quality_mode | best_state_mode | best_balance_mode | reading |",
        "|---|---|---|---|---|---|---|",
    ]
    for (language, exp), data in sorted(win.items()):
        reading = "compressed_wins_tokens" if "compressed" in data["cheapest"] else "proto_wins_tokens" if "proto" in data["cheapest"] else "natural_wins_tokens"
        lines.append(f"| {language} | {exp} | {data['cheapest']} | {data['quality']} | {data['state']} | {data['balance']} | {reading} |")
    return "\n".join(lines)


def compressed_vs_natural_table(summary):
    lines = [
        "| language | experiment | natural_tokens | compressed_tokens | saving | quality_delta | reading |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for language in ["EN", "ZH"]:
        for exp in ["EXP01", "EXP02"]:
            nat_mode = "natural_en" if language == "EN" else "natural_zh"
            comp_mode = "compressed_en" if language == "EN" else "compressed_zh"
            nat = summary[(language, exp, nat_mode)]
            comp = summary[(language, exp, comp_mode)]
            saving = None
            if nat["avg_total_tokens"] and comp["avg_total_tokens"]:
                saving = 1 - comp["avg_total_tokens"] / nat["avg_total_tokens"]
            q_delta = None
            if nat["semantic_fidelity"] is not None and comp["semantic_fidelity"] is not None:
                q_delta = comp["semantic_fidelity"] - nat["semantic_fidelity"]
            reading = "compressed_cheaper" if saving and saving > 0 else "compressed_not_cheaper"
            lines.append(f"| {language} | {exp} | {fmt(nat['avg_total_tokens'])} | {fmt(comp['avg_total_tokens'])} | {pct(saving)} | {fmt(q_delta)} | {reading} |")
    return "\n".join(lines)


def proto_v1_v2_table(summary):
    lines = [
        "| language | metric | proto_v1 | proto_v2 | change | reading |",
        "|---|---|---:|---:|---:|---|",
    ]
    pairs = {
        "EN": ("proto_v1_en", "proto_v2_en"),
        "ZH": ("proto_v1_core_zh", "proto_v2_core_zh"),
    }
    for language, (v1, v2) in pairs.items():
        for metric in ["avg_total_tokens", "avg_input_tokens", "avg_output_tokens", "semantic_fidelity", "utility", "ambiguity", "information_loss", "state_preservation"]:
            a = summary[(language, "EXP01", v1)][metric]
            b = summary[(language, "EXP02", v2)][metric]
            change = None if a is None or b is None else b - a
            if metric in ("ambiguity", "information_loss", "avg_total_tokens", "avg_input_tokens", "avg_output_tokens"):
                reading = "improved" if change is not None and change < 0 else "worse_or_equal"
            else:
                reading = "improved" if change is not None and change > 0 else "worse_or_equal"
            lines.append(f"| {language} | {metric} | {fmt(a)} | {fmt(b)} | {fmt(change)} | {reading} |")
    return "\n".join(lines)


def translation_table(summary):
    lines = [
        "| language | experiment | proto_mode | proto_tokens | translated_tokens | total_architectural_cost | fidelity_proto | fidelity_translated | reading |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    mapping = [
        ("EN", "EXP01", "proto_v1_en", "proto_v1_translated_en"),
        ("EN", "EXP02", "proto_v2_en", "proto_v2_translated_en"),
        ("ZH", "EXP01", "proto_v1_core_zh", "proto_v1_translated_zh"),
        ("ZH", "EXP02", "proto_v2_core_zh", "proto_v2_translated_zh"),
    ]
    for language, exp, proto, trans in mapping:
        p = summary[(language, exp, proto)]
        t = summary[(language, exp, trans)]
        total = None
        if p["avg_total_tokens"] is not None and t["avg_total_tokens"] is not None:
            total = p["avg_total_tokens"] + t["avg_total_tokens"]
        reading = "translation_extra_call"
        if t["semantic_fidelity"] is not None and p["semantic_fidelity"] is not None and t["semantic_fidelity"] < p["semantic_fidelity"]:
            reading += "_quality_down"
        lines.append(f"| {language} | {exp} | {proto} | {fmt(p['avg_total_tokens'])} | {fmt(t['avg_total_tokens'])} | {fmt(total)} | {fmt(p['semantic_fidelity'])} | {fmt(t['semantic_fidelity'])} | {reading} |")
    return "\n".join(lines)


def anomalies(rows):
    notes = Counter()
    examples = []
    for row in rows:
        if row.get("error"):
            notes[f"error:{row['error'].get('type')}"] += 1
            if len(examples) < 8:
                examples.append(f"- {row['language']} {row['experiment_id']} {row['task_id']} {row['mode']}: {row['error']}")
        if row.get("evaluation_parse_error"):
            notes["evaluation_parse_error"] += 1
        if row.get("total_tokens") is None:
            notes["missing_tokens"] += 1
        if row.get("format_valid") is False:
            for note in row.get("format_notes", []):
                notes[f"format:{note}"] += 1
            if len(examples) < 8:
                examples.append(f"- {row['language']} {row['experiment_id']} {row['task_id']} {row['mode']}: format_notes={row.get('format_notes')}")
    return notes, examples


def write_reports(rows, connection, pilot, stopped, backup):
    summary = summarize(rows)
    notes, examples = anomalies(rows)
    total_errors = sum(1 for r in rows if r.get("error"))
    parse_errors = sum(1 for r in rows if r.get("evaluation_parse_error"))
    missing_tokens = sum(1 for r in rows if r.get("total_tokens") is None)
    content = f"""# Resultados EXP01 EXP02 EN ZH

## Configuracion

- Perfil: `{PROFILE}`
- Endpoint: `{base.CHAT_COMPLETIONS_URL}`
- Modelo generador: `{GENERATION_MODEL}`
- Modelo evaluador: `{EVALUATOR_MODEL}`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: {TEMPERATURE}
- Repeticiones: {REPETITIONS}
- Filas: {len(rows)}
- Llamadas HTTP: {base.CALL_STATS['attempted']}
- Errores HTTP contabilizados por cliente: {base.CALL_STATS['errors']}
- Parse errors: {parse_errors}
- Missing tokens: {missing_tokens}
- Backup JSONL previo: {backup or 'no_aplica'}
- Soft stop: {stopped}

## Conexion

```json
{json.dumps(connection, ensure_ascii=False, indent=2)}
```

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Tabla global

{rows_table(summary)}

## Ganadores por bloque

{winners_table(summary)}

## Compressed vs natural

{compressed_vs_natural_table(summary)}

## Proto v1 vs Proto v2

{proto_v1_v2_table(summary)}

## Traducciones

Nota: `translated_tokens` mide la llamada traducida sola. El costo arquitectonico real es `proto_tokens + translated_tokens`.

{translation_table(summary)}

## Anomalias

{anomaly_markdown(notes, examples)}
"""
    write_text(REPORT_PATH, content)
    write_text(COMPARISON_PATH, comparison_doc(summary))
    write_text(ES_COMPARISON_PATH, es_comparison_doc(summary))
    write_text(EXEC_SUMMARY_PATH, exec_summary_doc(summary, rows, stopped))
    write_text(ERRORS_PATH, errors_doc(rows, notes, examples))


def anomaly_markdown(notes, examples):
    if not notes:
        return "- No se registraron anomalias relevantes."
    lines = [f"- {k}: {v}" for k, v in notes.most_common()]
    if examples:
        lines.append("\n### Ejemplos")
        lines.extend(examples)
    return "\n".join(lines)


def comparison_doc(summary):
    return f"""# Comparacion EXP01 EXP02 EN ZH

## EXP01 EN vs EXP01 ZH

Comparar `natural_en/compressed_en/proto_v1_en` contra `natural_zh/compressed_zh/proto_v1_core_zh`.

## EXP02 EN vs EXP02 ZH

Comparar `natural_en/compressed_en/proto_v2_en` contra `natural_zh/compressed_zh/proto_v2_core_zh`.

## Tabla global

{rows_table(summary)}

## Ganadores

{winners_table(summary)}

## Proto v1 vs Proto v2

{proto_v1_v2_table(summary)}

## Compressed vs natural

{compressed_vs_natural_table(summary)}

## Lectura

- Si `compressed_en` o `compressed_zh` reduce tokens frente a natural, anotarlo como baseline fuerte.
- Si Proto v2 baja tokens frente a Proto v1 pero sigue perdiendo contra compressed, la hipotesis debil sobrevive pero no la fuerte.
- Si input_tokens dominan, el costo del prompt/estructura debe separarse del costo de salida.
"""


def es_comparison_doc(summary):
    lines = [
        "# Comparacion EXP01 EXP02 ES EN ZH Borrador",
        "",
        "## Referencias ES reales",
        "",
        "| language | experiment | mode | avg_tokens | fidelity | source |",
        "|---|---|---|---:|---:|---|",
    ]
    for (language, exp, mode), data in sorted(ES_REFERENCES.items()):
        lines.append(f"| {language} | {exp} | {mode} | {fmt(data['tokens'])} | {fmt(data['fidelity'])} | {data['source']} |")
    lines.extend([
        "",
        "## Datos EN/ZH ejecutados",
        "",
        rows_table(summary),
        "",
        "## Nota metodologica",
        "",
        "Los datos ES se leen como referencia historica ya documentada en el proyecto. Los datos EN/ZH son los de esta corrida. No mezclar sin considerar idioma, tokenizer y prompts traducidos.",
    ])
    return "\n".join(lines)


def exec_summary_doc(summary, rows, stopped):
    win = winners(summary)
    lines = [
        "# Resumen Ejecutivo EXP01 EXP02 Multilingue",
        "",
        "## Estado",
        "",
        f"- FULL ejecutado: {'parcial_por_soft_stop' if stopped else 'si'}",
        f"- Filas generadas: {len(rows)}",
        f"- Llamadas HTTP: {base.CALL_STATS['attempted']}",
        "",
        "## Ganadores",
        "",
        winners_table(summary),
        "",
        "## Lectura principal",
        "",
    ]
    for key, data in sorted(win.items()):
        lines.append(f"- {key[0]} {key[1]}: mas barato `{data['cheapest']}`, mejor calidad `{data['quality']}`, mejor estado `{data['state']}`.")
    lines.extend([
        "",
        "## Riesgos metodologicos",
        "",
        "- Evaluador automatico puede favorecer idioma o estilo.",
        "- Traduccion de tareas puede alterar dificultad.",
        "- Tokenizer puede afectar EN/ZH de forma distinta.",
        "- Separar input_tokens y output_tokens antes de concluir.",
        "",
        "## Recomendacion",
        "",
        "Ejecutar EXP03_EN/ZH solo si no hay fallo grave de formato o evaluacion en EXP01/EXP02.",
    ])
    return "\n".join(lines)


def errors_doc(rows, notes, examples):
    return f"""# Errores y Anomalias EXP01 EXP02 EN ZH

## Resumen

- Filas: {len(rows)}
- Errores por fila: {sum(1 for r in rows if r.get('error'))}
- Parse errors: {sum(1 for r in rows if r.get('evaluation_parse_error'))}
- Missing tokens: {sum(1 for r in rows if r.get('total_tokens') is None)}
- Fallos de formato: {sum(1 for r in rows if r.get('format_valid') is False)}

## Detalle

{anomaly_markdown(notes, examples)}

## Seguridad

No se registra API key.
"""


def run_secret_scan():
    patterns = [r"s" + "k" + r"-[A-Za-z0-9]{16,}", "api" + "_key", "API" + "_KEY", "Author" + "ization", "Bear" + "er", "token" + "="]
    paths = [RUNS_PATH, PILOT_PATH, REPORT_PATH, COMPARISON_PATH, ES_COMPARISON_PATH, EXEC_SUMMARY_PATH, ERRORS_PATH, CONNECTION_PATH]
    hits = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            if pattern.startswith("s" + "k" + "-"):
                found = re.search(pattern, text)
            else:
                found = pattern in text
            if found:
                hits.append(f"{path.name}:{pattern}")
    return hits


def main():
    require_key()
    THIS_DIR.mkdir(parents=True, exist_ok=True)
    connection = test_connection()
    if not connection.get("models_ok") or not connection.get("chat_ok"):
        write_text(ERRORS_PATH, "# Conexion fallida\n\nNo se ejecuto FULL.\n")
        print("connection_failed")
        return 1
    pilot = run_pilot()
    print(f"pilot rows={pilot['rows']} ok={pilot['ok']} errors={pilot['errors']} missing_tokens={pilot['missing_tokens']} format_invalid={pilot['format_invalid']}", flush=True)
    if not pilot["ok"]:
        write_text(ERRORS_PATH, "# Piloto fallido\n\n```json\n" + json.dumps(pilot, ensure_ascii=False, indent=2) + "\n```\n")
        return 1
    rows, stopped, backup = run_full()
    rows = read_jsonl(RUNS_PATH)
    write_reports(rows, connection, pilot, stopped, backup)
    hits = run_secret_scan()
    if hits:
        write_text(ERRORS_PATH, "# Secret scan hit\n\n" + "\n".join(hits) + "\n")
        print("secret_scan_hit")
        return 1
    print(f"done rows={len(rows)} http={base.CALL_STATS['attempted']} http_errors={base.CALL_STATS['errors']} stopped={stopped}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
