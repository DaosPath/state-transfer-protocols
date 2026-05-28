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


GENERATION_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
GENERATION_MODEL_FALLBACK = os.getenv("GENERATION_MODEL_FALLBACK", "opencode-go/deepseek-v4-flash")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "deepseek-v4-pro")
EVALUATOR_MODEL_FALLBACK = os.getenv("EVALUATOR_MODEL_FALLBACK", "deepseek-v4-flash")
TEMPERATURE = 0.2
REPETITIONS = 3
REQUEST_TIMEOUT = 90
RATE_LIMIT_SLEEP_SECONDS = 10
SERVER_ERROR_SLEEP_SECONDS = 10

MAX_TOKENS_NATURAL = 500
MAX_TOKENS_COMPRESSED = 350
MAX_TOKENS_PROTO = 300
MAX_TOKENS_TRANSLATION = 350
MAX_TOKENS_EVALUATION = 300
EMPTY_RETRY_MAX_TOKENS_GENERATION = 1800
EMPTY_RETRY_MAX_TOKENS_TRANSLATION = 1200
EMPTY_RETRY_MAX_TOKENS_EVALUATION = 1000

LANG_LIMITS = {
    "EN": {"hard": 2000, "soft": 1850},
    "ZH": {"hard": 2400, "soft": 2200},
}

ES_EXP03_REFERENCES = {
    "natural": {"tokens": 324.54, "fidelity": 4.84, "utility": 4.86, "state": 4.81},
    "compressed": {"tokens": 233.89, "fidelity": 4.14, "utility": 4.17, "state": 3.67},
    "proto_min": {"tokens": 370.87, "fidelity": 3.69, "utility": 3.19, "state": 2.91},
    "proto_state": {"tokens": 377.23, "fidelity": 3.79, "utility": 3.17, "state": 3.47},
    "proto_hybrid": {"tokens": 266.78, "fidelity": 4.46, "utility": 4.47, "state": 3.90},
}

TASKS = [
    {
        "id": "T001",
        "group": "base_comparable",
        "es": "Analiza este problema: un sistema multiagente consume demasiados tokens porque cada agente escribe explicaciones largas. Propón solución, riesgos y próximos pasos.",
        "en": "Analyze this problem: a multi-agent system consumes too many tokens because each agent writes long explanations. Propose a solution, risks, and next steps.",
        "zh": "分析这个问题：一个多智能体系统消耗太多 token，因为每个智能体都写很长解释。提出解决方案、风险和下一步。",
    },
    {
        "id": "T002",
        "group": "base_comparable",
        "es": "Resume una arquitectura de agentes con trabajador, supervisor, memoria y traductor final. Incluye ventajas y limitaciones.",
        "en": "Summarize an agent architecture with worker, supervisor, memory, and final translator. Include advantages and limitations.",
        "zh": "总结一种包含工作者、监督者、记忆和最终翻译器的智能体架构。包括优点和限制。",
    },
    {
        "id": "T003",
        "group": "base_comparable",
        "es": "Convierte una explicación larga sobre eficiencia de tokens en una estructura operativa para agentes.",
        "en": "Convert a long explanation about token efficiency into an operational structure for agents.",
        "zh": "把一段关于 token 效率的长解释转换成智能体可用的操作结构。",
    },
    {
        "id": "T004",
        "group": "base_comparable",
        "es": "Diseña reglas iniciales para evitar deriva semántica en un protocolo simbólico.",
        "en": "Design initial rules to prevent semantic drift in a symbolic protocol.",
        "zh": "设计初始规则，避免符号协议中的语义漂移。",
    },
    {
        "id": "T005",
        "group": "base_comparable",
        "es": "Detecta riesgos en un sistema donde varios agentes se comunican con símbolos comprimidos.",
        "en": "Detect risks in a system where several agents communicate with compressed symbols.",
        "zh": "检测一个多智能体使用压缩符号通信的系统中的风险。",
    },
    {
        "id": "T006",
        "group": "base_comparable",
        "es": "Propón una metodología para medir si un protolenguaje conserva significado.",
        "en": "Propose a methodology to measure whether a protolanguage preserves meaning.",
        "zh": "提出一种方法，用来衡量原语言是否保留意义。",
    },
    {
        "id": "T007",
        "group": "base_comparable",
        "es": "Extrae variables medibles de un experimento sobre comunicación multiagente.",
        "en": "Extract measurable variables from an experiment about multi-agent communication.",
        "zh": "从多智能体通信实验中提取可测量变量。",
    },
    {
        "id": "T008",
        "group": "base_comparable",
        "es": "Crea una plantilla breve para registrar resultados de pruebas con modelos IA.",
        "en": "Create a brief template to record test results with AI models.",
        "zh": "创建一个简短模板，用于记录 AI 模型测试结果。",
    },
    {
        "id": "T009",
        "group": "base_comparable",
        "es": "Compara lenguaje natural, lenguaje cavernícola y protolenguaje en términos de costo, claridad y error.",
        "en": "Compare natural language, compressed language, and protolanguage in terms of cost, clarity, and error.",
        "zh": "比较自然语言、压缩语言和原语言在成本、清晰度和错误方面的差异。",
    },
    {
        "id": "T010",
        "group": "base_comparable",
        "es": "Propón cómo un agente traductor debe convertir protolenguaje a español humano sin inventar información.",
        "en": "Propose how a translator agent should convert protolanguage into human English without inventing information.",
        "zh": "提出翻译智能体如何把原语言转换成清晰中文，同时不编造信息。",
    },
    {
        "id": "T011",
        "group": "memory_state",
        "es": "Un agente trabajador terminó una tarea, pero debe pasar al siguiente agente objetivo, contexto, error detectado, riesgo y próxima acción. Resume ese estado de forma eficiente.",
        "en": "A worker agent finished a task, but must pass the next agent the objective, context, detected error, risk, and next action. Summarize that state efficiently.",
        "zh": "一个工作智能体完成了任务，但必须把目标、上下文、检测到的错误、风险和下一步动作传给下一个智能体。高效总结该状态。",
    },
    {
        "id": "T012",
        "group": "memory_state",
        "es": "Dos agentes están coordinando una investigación. El agente A encontró que caveman ahorra más tokens, pero el agente B necesita conservar trazabilidad de hipótesis, métricas y límites. Propón una salida compacta.",
        "en": "Two agents are coordinating research. Agent A found that compressed language saves more tokens, but Agent B needs traceability of hypotheses, metrics, and limits. Propose a compact output.",
        "zh": "两个智能体正在协同研究。智能体 A 发现压缩语言更省 token，但智能体 B 需要保留假设、指标和限制的可追踪性。提出紧凑输出。",
    },
    {
        "id": "T013",
        "group": "memory_state",
        "es": "Comprime el siguiente estado de proyecto: EXP01 mostró que caveman ganó; EXP02 mostró que proto_v2 mejoró pero perdió calidad; EXP03 debe probar proto_v3 minimalista. Conserva decisión y siguiente paso.",
        "en": "Compress this project state: EXP01 showed compressed language won; EXP02 showed proto_v2 improved but lost quality; EXP03 must test minimalist proto_v3. Preserve decision and next step.",
        "zh": "压缩以下项目状态：EXP01 显示压缩语言获胜；EXP02 显示 proto_v2 有改进但质量下降；EXP03 必须测试极简 proto_v3。保留决策和下一步。",
    },
    {
        "id": "T014",
        "group": "memory_state",
        "es": "Un agente debe reportar error de formato: la salida proto_v3 usó etiquetas de Proto v1 y fue demasiado larga. Resume problema, corrección y verificación.",
        "en": "An agent must report a format error: the proto_v3 output used Proto v1 tags and was too long. Summarize problem, correction, and verification.",
        "zh": "一个智能体必须报告格式错误：proto_v3 输出使用了 Proto v1 标签，而且太长。总结问题、修正和验证。",
    },
    {
        "id": "T015",
        "group": "memory_state",
        "es": "Diseña una memoria compacta para guardar que el usuario prefiere optimización de tokens, documentación en Markdown y experimentos con resultados reales.",
        "en": "Design compact memory to store that the user prefers token optimization, Markdown documentation, and experiments with real results.",
        "zh": "设计紧凑记忆，保存用户偏好：token 优化、Markdown 文档、使用真实结果的实验。",
    },
    {
        "id": "T016",
        "group": "memory_state",
        "es": "Evalúa una salida de agente que es corta pero ambigua. Debes conservar: problema, por qué es ambigua, riesgo y corrección.",
        "en": "Evaluate an agent output that is short but ambiguous. Preserve: problem, why it is ambiguous, risk, and correction.",
        "zh": "评估一个很短但含糊的智能体输出。必须保留：问题、为什么含糊、风险和修正。",
    },
    {
        "id": "T017",
        "group": "memory_state",
        "es": "Crea un plan de tres pasos para probar si un traductor final puede traducir lotes de protolenguaje en una sola llamada.",
        "en": "Create a three-step plan to test whether a final translator can translate batches of protolanguage in a single call.",
        "zh": "创建三步计划，测试最终翻译器是否能在一次调用中翻译一批原语言。",
    },
    {
        "id": "T018",
        "group": "memory_state",
        "es": "Resume una comparación entre tres opciones: lenguaje natural, caveman y proto_v3_hybrid. Conserva costo, claridad y riesgo principal.",
        "en": "Summarize a comparison between three options: natural language, compressed language, and proto_v3_hybrid. Preserve cost, clarity, and main risk.",
        "zh": "总结三种方案的比较：自然语言、压缩语言、proto_v3_hybrid。保留成本、清晰度和主要风险。",
    },
    {
        "id": "T019",
        "group": "memory_state",
        "es": "Un sistema multiagente debe pasar contexto entre cinco agentes sin superar límite de tokens. Propón estrategia compacta con memoria y verificación.",
        "en": "A multi-agent system must pass context across five agents without exceeding the token limit. Propose a compact strategy with memory and verification.",
        "zh": "一个多智能体系统必须在五个智能体之间传递上下文，同时不超过 token 限制。提出带记忆和验证的紧凑策略。",
    },
    {
        "id": "T020",
        "group": "memory_state",
        "es": "Convierte una salida técnica comprimida en una instrucción entendible para un agente supervisor.",
        "en": "Convert a compressed technical output into an understandable instruction for a supervisor agent.",
        "zh": "把一个压缩技术输出转换成监督智能体可理解的指令。",
    },
    {
        "id": "T021",
        "group": "medium_complexity",
        "es": "Un agente debe priorizar tareas: corregir reglas, ejecutar experimento, analizar resultados, preparar informe. Ordena y justifica brevemente.",
        "en": "An agent must prioritize tasks: fix rules, run experiment, analyze results, prepare report. Order them and justify briefly.",
        "zh": "一个智能体必须排列任务优先级：修正规则、执行实验、分析结果、准备报告。排序并简要说明理由。",
    },
    {
        "id": "T022",
        "group": "medium_complexity",
        "es": "Detecta qué información no debe perderse al comprimir un informe experimental: fecha, modelo, tokens, errores, métricas, conclusión y límites.",
        "en": "Detect which information must not be lost when compressing an experimental report: date, model, tokens, errors, metrics, conclusion, and limits.",
        "zh": "检测压缩实验报告时不能丢失的信息：日期、模型、tokens、错误、指标、结论和限制。",
    },
    {
        "id": "T023",
        "group": "medium_complexity",
        "es": "Propón cómo medir deriva semántica cuando varios agentes usan la misma abreviatura con significados diferentes.",
        "en": "Propose how to measure semantic drift when several agents use the same abbreviation with different meanings.",
        "zh": "提出如何测量语义漂移：多个智能体使用同一缩写但含义不同。",
    },
    {
        "id": "T024",
        "group": "medium_complexity",
        "es": "Resume una conclusión parcial sin exagerar: proto_v3 redujo tokens frente a proto_v2, pero no venció a caveman y perdió algo de claridad.",
        "en": "Summarize a partial conclusion without exaggeration: proto_v3 reduced tokens compared with proto_v2, but did not beat compressed language and lost some clarity.",
        "zh": "不夸大地总结一个部分结论：proto_v3 相比 proto_v2 减少了 tokens，但没有战胜压缩语言，并且损失了一些清晰度。",
    },
    {
        "id": "T025",
        "group": "medium_complexity",
        "es": "Diseña una estructura mínima para que un agente entregue: resultado, evidencia, confianza, riesgo y siguiente acción.",
        "en": "Design a minimal structure for an agent to deliver: result, evidence, confidence, risk, and next action.",
        "zh": "设计一种最小结构，让智能体交付：结果、证据、置信度、风险和下一步动作。",
    },
    {
        "id": "T026",
        "group": "medium_complexity",
        "es": "Convierte un resumen humano de 120 palabras en una salida operativa para agentes sin perder entidades ni números.",
        "en": "Convert a 120-word human summary into an operational output for agents without losing entities or numbers.",
        "zh": "把一个 120 词的人类摘要转换成智能体操作输出，同时不丢失实体或数字。",
    },
    {
        "id": "T027",
        "group": "medium_complexity",
        "es": "Un agente traductor recibe una salida proto_v3 ambigua. Explica cómo debe traducir sin inventar y cómo debe marcar incertidumbre.",
        "en": "A translator agent receives an ambiguous proto_v3 output. Explain how it should translate without inventing information and how it should mark uncertainty.",
        "zh": "翻译智能体收到一个含糊的 proto_v3 输出。说明如何在不编造信息的情况下翻译，并如何标记不确定性。",
    },
    {
        "id": "T028",
        "group": "medium_complexity",
        "es": "Compara dos arquitecturas: traducir cada salida proto inmediatamente vs traducir por lote al final. Incluye costo y riesgo.",
        "en": "Compare two architectures: translate each proto output immediately versus batch-translate at the end. Include cost and risk.",
        "zh": "比较两种架构：立即翻译每个 proto 输出，或在最后批量翻译。包括成本和风险。",
    },
    {
        "id": "T029",
        "group": "medium_complexity",
        "es": "Prepara una mini bitácora de experimento con tarea, modo, tokens, calidad, error y observación.",
        "en": "Prepare a mini experiment log with task, mode, tokens, quality, error, and observation.",
        "zh": "准备一个迷你实验日志，包含任务、模式、tokens、质量、错误和观察。",
    },
    {
        "id": "T030",
        "group": "medium_complexity",
        "es": "Crea una regla para decidir cuándo usar caveman, cuándo usar proto_v3_min, cuándo usar proto_v3_state y cuándo usar proto_v3_hybrid.",
        "en": "Create a rule to decide when to use compressed language, proto_v3_min, proto_v3_state, and proto_v3_hybrid.",
        "zh": "创建规则，决定何时使用压缩语言、proto_v3_min、proto_v3_state 和 proto_v3_hybrid。",
    },
]

MODE_CONFIG = {
    "EN": {
        "dir": "EXP03_EN",
        "experiment_id": "EXP03_EN",
        "modes": [
            "natural_en",
            "compressed_en",
            "proto_v3_min_core_en",
            "proto_v3_state_core_en",
            "proto_v3_hybrid_en",
        ],
        "translation_map": {
            "proto_v3_min_core_en": "proto_v3_min_translated_en",
            "proto_v3_state_core_en": "proto_v3_state_translated_en",
            "proto_v3_hybrid_en": "proto_v3_hybrid_translated_en",
        },
    },
    "ZH": {
        "dir": "EXP03_ZH",
        "experiment_id": "EXP03_ZH",
        "modes": [
            "natural_zh",
            "compressed_zh",
            "proto_v3_min_core_zh",
            "proto_v3_state_core_zh",
            "proto_v3_hybrid_zh",
            "proto_v3_zh_native",
        ],
        "translation_map": {
            "proto_v3_min_core_zh": "proto_v3_min_translated_zh",
            "proto_v3_state_core_zh": "proto_v3_state_translated_zh",
            "proto_v3_hybrid_zh": "proto_v3_hybrid_translated_zh",
            "proto_v3_zh_native": "proto_v3_zh_native_translated",
        },
    },
}

METRICS = [
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


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def configure_base(language):
    base.configure_provider_from_env()
    key_attr = "API" + "_" + "KEY"
    key_env = "OPENCODE_" + key_attr
    setattr(base, key_attr, os.getenv(key_env) or getattr(base, key_attr))
    base.GENERATION_MODEL = GENERATION_MODEL
    base.GENERATION_MODEL_FALLBACK = GENERATION_MODEL_FALLBACK
    base.EVALUATOR_MODEL = EVALUATOR_MODEL
    base.EVALUATOR_MODEL_FALLBACK = EVALUATOR_MODEL_FALLBACK
    base.TEMPERATURE = TEMPERATURE
    base.MAX_CALLS_INITIAL_RUN = LANG_LIMITS[language]["hard"]
    base.REQUEST_TIMEOUT = REQUEST_TIMEOUT
    base.RATE_LIMIT_SLEEP_SECONDS = RATE_LIMIT_SLEEP_SECONDS
    base.SERVER_ERROR_SLEEP_SECONDS = SERVER_ERROR_SLEEP_SECONDS
    for key in base.CALL_STATS:
        base.CALL_STATS[key] = 0


def require_key():
    if not getattr(base, "API" + "_" + "KEY"):
        raise RuntimeError("Missing provider key in environment or ignored local wrapper.")


def paths_for(language):
    cfg = MODE_CONFIG[language]
    out_dir = THIS_DIR / cfg["dir"]
    stem = f"exp03_{language.lower()}"
    return {
        "dir": out_dir,
        "runs": out_dir / f"{stem}_runs.jsonl",
        "pilot": out_dir / f"pilot_{stem}.jsonl",
        "connection": out_dir / f"connection_test_{stem}.json",
        "log": out_dir / f"{stem}_execution_log.md",
        "results": out_dir / f"Resultados_EXP03_{language}.md",
        "summary": out_dir / f"Resumen_Ejecutivo_EXP03_{language}.md",
        "translation": out_dir / f"Analisis_Traducciones_EXP03_{language}.md",
        "errors": out_dir / f"Errores_y_Anomalias_EXP03_{language}.md",
    }


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_jsonl(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def backup_if_exists(path):
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = path.with_suffix(path.suffix + f".bak_{stamp}")
        shutil.copy2(path, backup)
        path.unlink()
        return backup.name
    return None


def task_text(language, task):
    return task["en"] if language == "EN" else task["zh"]


def task_payload(language, task):
    return {
        "id": task["id"],
        "group": task["group"],
        "text": task_text(language, task),
        "original_es": task["es"],
    }


def max_tokens_for_mode(mode):
    if "translated" in mode:
        return MAX_TOKENS_TRANSLATION
    if "natural" in mode:
        return MAX_TOKENS_NATURAL
    if "compressed" in mode:
        return MAX_TOKENS_COMPRESSED
    return MAX_TOKENS_PROTO


def soft_stop(language):
    return base.CALL_STATS["attempted"] >= LANG_LIMITS[language]["soft"]


def prompt_for_mode(language, mode, task):
    text = task["text"]
    if mode == "natural_en":
        return f"""Answer in clear, complete natural English.
Use final answer only. Do not show step-by-step reasoning.
Maximum 140 words.
Analyze the task. Include problem, solution, risks, and next steps when applicable.
Do not use proto format. Do not use decorative language.

Task:
{text}"""
    if mode == "compressed_en":
        return f"""Answer in compressed operational English.
Use final answer only. Maximum 90 words.
Minimize tokens. No politeness. No filler. No decorative language.
Preserve goal, key facts, numbers, decisions, risks, and next step.
Fragments are allowed. Do not use full key=value proto.
Output must allow another agent to continue the task.

Task:
{text}"""
    if mode == "proto_v3_min_core_en":
        return f"""Answer using minimal Proto v3 core.
Use final answer only. One line if possible. Maximum 55 words.
Use only necessary key=value fields.
Allowed fields: g=goal, p=problem, c=context, s=solution, a=action, r=risk, n=next, v=verify, m=metric, e=error, x=constraint, o=output, conf=confidence.
Rules: no @TASK; no GOAL/CTX/PROBLEM/PLAN/RISK/CHK/OUT/NEXT; no T:/G:/C:/P:/S:/R:/V:/N: template; no long prose; preserve essential facts.
Do not use placeholders such as [insert objective]. Fill concrete compact content from the task.
Example: p=tokens_high/verbose_agents;s=compact_state+final_translator;r=ambig|drift;n=measure>adjust

Task:
{text}"""
    if mode == "proto_v3_state_core_en":
        return f"""Answer using Proto v3 state core.
Use final answer only. Maximum 75 words. One or two lines.
Keep compact, but preserve useful state when relevant.
Allowed fields: g=goal, p=problem, c=context, m=memory, k=key_fact, s=solution, a=action, r=risk, v=verify, n=next, lim=limit, conf=confidence.
Use m= for prior memory, k= for important fact, v= for verification, lim= for constraints.
Use 4 to 7 fields total. Do not list all allowed fields.
Do not fill empty fields. Do not become Proto v1/v2. No heavy 8-field template.
Do not use placeholders such as [insert context] or [specific error]. Fill concrete compact content from the task.

Task:
{text}"""
    if mode == "proto_v3_hybrid_en":
        return f"""Answer using Proto v3 hybrid.
Use final answer only. Maximum 85 words.
Mix compressed English with minimal state markers.
More readable than pure proto, shorter than natural, more structured than compressed free text.
Suggested format:
p: ...
s: ...
r: ...
n: ...
Rules: no long sentences, no filler, preserve problem/solution/risk/next step, keep easy to translate.
Do not use placeholders such as [insert objective]. Fill concrete compact content from the task.

Task:
{text}"""
    if mode == "natural_zh":
        return f"""使用清晰完整的简体中文回答。
只输出最终答案，不展示逐步推理。
最多约 220 个汉字。
分析任务；如适用，包含问题、方案、风险和下一步。
不要使用 proto 格式。不要写装饰性语言。

任务：
{text}"""
    if mode == "compressed_zh":
        return f"""使用压缩中文。只输出最终答案。
尽量减少 token。不要寒暄。不要礼貌语。不要修辞。不要长解释。
保留目标、关键事实、数字、风险、决定和下一步。
可以省略主语，可以使用短句。可用连接词：但、因、故、下步、风。
不要使用完整 proto key=value 格式，除非绝对必要。
不要写“原始人说话”。不要幼稚化。输出必须让另一个智能体继续任务。

任务：
{text}"""
    if mode == "proto_v3_min_core_zh":
        return f"""使用通用 Proto v3 core。只输出最终答案。
一行优先，最多 55 词或等价短输出。
使用拉丁/中性 key=value 字段，便于 ES/EN/ZH 公平比较。
允许字段：g=目标, p=问题, c=上下文, s=方案, a=动作, r=风险, n=下一步, v=验证, m=指标, e=错误, x=限制, o=输出, conf=置信。
最多使用 3 到 7 个字段。不要列出所有允许字段。
规则：不使用 @TASK；不使用 GOAL/CTX/PROBLEM/PLAN/RISK/CHK/OUT/NEXT；不使用 T:/G:/C:/P:/S:/R:/V:/N: 模板；不写完整中文解释；保留必要信息。
不要使用占位符，例如“[填写目标]”“错误详情”“风险描述”“指标数据”或“待补充”。必须从任务中填入具体压缩内容。

任务：
{text}"""
    if mode == "proto_v3_state_core_zh":
        return f"""使用通用 Proto v3 state core。只输出最终答案。
最多 75 词或等价短输出，一到两行。
重点保存状态、决定、风险、缺失信息、下一步。
允许字段：g=目标, p=问题, c=上下文, m=记忆, k=关键事实, s=方案, a=动作, r=风险, v=验证, n=下一步, lim=限制, conf=置信。
总字段数 4 到 7 个。不要列出所有允许字段。
不要填空字段。不要变成 Proto v1/v2。不要固定 8 字段模板。
不要使用占位符，例如“[填写上下文]”“[specific error]”或“待补充”。必须从任务中填入具体压缩内容。

任务：
{text}"""
    if mode == "proto_v3_hybrid_zh":
        return f"""使用 proto_v3_hybrid_zh。只输出最终答案。
压缩中文 + 最小状态标记。最多约 140 个汉字。
比纯 proto 更可读，比 natural_zh 更短。
可用格式：结：... 风：... 缺：... 下：...
也可用 p：... s：... r：... n：...
规则：保留问题/方案/风险/下一步；不要长解释；不要使用 Proto v1/v2；要可翻译。
不要使用占位符或“待补充”。必须从任务中填入具体压缩内容。

任务：
{text}"""
    if mode == "proto_v3_zh_native":
        return f"""使用中文本地化 Proto v3。只输出最终答案。
最多约 120 个汉字，一行或两行。
必须使用已定义中文短标签，保持可解释、可继续、低歧义。
字典：任=任务；目=目标；态=状态；结=结果；风=风险；缺=缺失；决=决定；数=指标；下=下一步；证=证据；错=错误；译=翻译；质=质量；损=损失；歧=歧义。
不要写长中文自然段。不要使用无法解释的符号。不要混成通用 proto core。
不要使用占位符或“待补充”。必须从任务中填入具体压缩内容。
示例：任=exp2复查;结=v2较v1省token但输caveman;质↓=清晰+实用;风=信息损失;下=测轻量v3

任务：
{text}"""
    raise KeyError(mode)


def translation_prompt(language, mode, source_output):
    if language == "EN":
        return f"""Translate the following Proto v3 output into brief, clear natural English.
Use final answer only. Maximum 120 words.
Do not invent information. Do not add missing fields.
Preserve problem, objective, solution, risks, metrics, memory, state, and next steps if present.
If there is ambiguity, mark it.
Translate the proto source; do not answer the original task from scratch.

Proto output:
{source_output}"""
    return f"""把下面的 Proto v3 输出翻译成简短、清晰的自然中文。
只输出最终答案。不要编造信息。不要添加源输出没有的字段。
保留问题、目标、方案、风险、指标、记忆、状态和下一步（如果存在）。
如果有歧义，请标明。
必须翻译 proto 源输出，不要重新回答原任务。

Proto 输出：
{source_output}"""


def evaluation_prompt(language, task, mode, output):
    if language == "EN":
        lang_rules = "Evaluate English outputs. Do not reward long answers automatically. Do not punish compressed outputs if they preserve operational meaning."
    else:
        lang_rules = "Evaluate Simplified Chinese outputs. Do not reward Chinese just because it looks visually short. compressed_zh is operational compressed Chinese, not childish language."
    return f"""You are an evaluator for compressed agent communication experiments.
Use final answer only. Do not show reasoning.
{lang_rules}
Compare the generated output against the original task.

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
- A good output must allow another agent to continue the task.

Original task:
{task['text']}

Mode:
{mode}

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
    empty_retry = EMPTY_RETRY_MAX_TOKENS_EVALUATION if is_eval else (
        EMPTY_RETRY_MAX_TOKENS_TRANSLATION if max_tokens == MAX_TOKENS_TRANSLATION else EMPTY_RETRY_MAX_TOKENS_GENERATION
    )
    return base.call_chat_with_model_fallback(
        primary,
        fallback,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        fallback_on_any_error=is_eval,
        empty_retry_max_tokens=empty_retry,
    )


def generate(language, mode, task):
    return call_model(prompt_for_mode(language, mode, task), max_tokens_for_mode(mode), is_eval=False)


def translate(language, mode, source_output):
    return call_model(translation_prompt(language, mode, source_output), MAX_TOKENS_TRANSLATION, is_eval=False)


def normalize_evaluation(parsed):
    out = {}
    for metric in METRICS:
        value = parsed.get(metric)
        try:
            value = int(value)
        except Exception:
            value = None
        out[metric] = value
    out["notes"] = str(parsed.get("notes", parsed.get("comentario", "")))[:500]
    return out


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
    return result.get("model_used", EVALUATOR_MODEL), normalize_evaluation(parsed), result.get("output"), False, None, result.get("latency_ms")


def contains_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def cjk_count(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def word_count(text):
    return len(re.findall(r"\b[\w'=-]+\b", text or "", flags=re.UNICODE))


def field_info(text):
    value = text or ""
    fields = []
    fields.extend(re.findall(r"\b([a-zA-Z]{1,8})\s*=", value))
    fields.extend(re.findall(r"(?m)^\s*([a-zA-Z]{1,16})\s*[:：]", value))
    fields.extend(re.findall(r"([任目态結结風风缺決决數数下證证錯错譯译質质損损歧])\s*=", value))
    fields.extend(re.findall(r"(?m)^\s*(结|風|风|缺|下|目|态|决|数|证|错|译|质|损|歧|p|s|r|n)\s*[:：]", value))
    return len(set(fields)), sorted(set(fields))


def has_proto_v1_or_v2(text):
    value = text or ""
    if re.search(r"(?mi)^\s*@TASK|^\s*GOAL\s*[\{:]|^\s*CTX\s*[\{:]|^\s*PROBLEM\s*[\{:]|^\s*PLAN\s*[\{:]|^\s*RISK\s*[\{:]|^\s*CHK\s*[\{:]|^\s*OUT\s*[\{:]|^\s*NEXT\s*[\{:]", value):
        return True
    labels = set(re.findall(r"(?m)^\s*([TGCPRSVN])\s*:", value))
    return len(labels.intersection({"T", "G", "C", "P", "S", "R", "V", "N"})) >= 5


def validate_format(language, mode, output, source_output=None, task=None):
    text = output or ""
    notes = []
    valid = True
    wc = word_count(text)
    cc = len(text)
    cjk = cjk_count(text)
    field_count, fields = field_info(text)
    has_placeholder = bool(re.search(r"\[[^\]]*(insert|fill|objective|context|error|risk|action|specific|todo|tbd)[^\]]*\]|待补充|填写", text, re.I))
    has_placeholder = has_placeholder or bool(
        re.search(r"(?:^|[;\s])(e|r|m|v)\s*=\s*(错误详情|风险描述|指标数据|验证结果)(?:[;\s]|$)", text)
    )

    if mode.startswith("natural_"):
        if field_count >= 3:
            valid = False
            notes.append("natural_dominated_by_fields")
        if language == "EN" and contains_cjk(text):
            valid = False
            notes.append("wrong_language_cjk_in_en")
        if language == "ZH" and cjk < 8:
            valid = False
            notes.append("wrong_language_too_little_zh")
    elif mode == "compressed_en":
        if wc > 120:
            valid = False
            notes.append("compressed_en_too_long")
        if field_count >= 3:
            valid = False
            notes.append("compressed_en_looks_like_proto")
        if contains_cjk(text):
            valid = False
            notes.append("wrong_language_cjk_in_en")
    elif mode == "compressed_zh":
        if cjk < 8:
            valid = False
            notes.append("compressed_zh_too_little_zh")
        if "原始人" in text or "洞穴" in text:
            valid = False
            notes.append("compressed_zh_caricature")
        if cc > 360:
            valid = False
            notes.append("compressed_zh_too_long")
        if field_count >= 4:
            valid = False
            notes.append("compressed_zh_looks_like_proto")
    elif "translated" in mode:
        if source_output and not source_output.strip():
            valid = False
            notes.append("missing_translation_source")
        if language == "EN" and contains_cjk(text):
            valid = False
            notes.append("wrong_language_cjk_in_en_translation")
        if language == "ZH" and cjk < 8:
            valid = False
            notes.append("wrong_language_too_little_zh_translation")
        if field_count >= 5 and (wc < 20 or cjk < 20):
            valid = False
            notes.append("translation_still_looks_like_proto")
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
    elif "proto_v3_min_core" in mode:
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
        if has_proto_v1_or_v2(text):
            valid = False
            notes.append("uses_proto_v1_or_v2")
        if field_count == 0:
            valid = False
            notes.append("missing_key_value_fields")
        max_min_fields = 7 if language == "ZH" else 6
        if field_count > max_min_fields:
            valid = False
            notes.append("too_many_fields_for_min")
        if language == "EN" and wc > 70:
            valid = False
            notes.append("too_long_for_min")
        if language == "ZH" and cc > 220:
            valid = False
            notes.append("too_long_for_min_zh")
    elif "proto_v3_state_core" in mode:
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
        if has_proto_v1_or_v2(text):
            valid = False
            notes.append("uses_proto_v1_or_v2")
        if field_count == 0:
            valid = False
            notes.append("missing_key_value_fields")
        if field_count > 8:
            valid = False
            notes.append("too_many_fields_for_state")
        needs_state = task and task.get("group") in {"memory_state", "medium_complexity"}
        if needs_state and not set(fields).intersection({"m", "k", "v", "lim", "conf", "c", "state"}):
            valid = False
            notes.append("missing_state_field")
    elif mode == "proto_v3_hybrid_en":
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
        if has_proto_v1_or_v2(text):
            valid = False
            notes.append("uses_proto_v1_or_v2")
        if wc > 110:
            valid = False
            notes.append("hybrid_en_too_long")
        if field_count == 0:
            valid = False
            notes.append("hybrid_en_missing_markers")
    elif mode == "proto_v3_hybrid_zh":
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
        if has_proto_v1_or_v2(text):
            valid = False
            notes.append("uses_proto_v1_or_v2")
        if cc > 260:
            valid = False
            notes.append("hybrid_zh_too_long")
        if field_count == 0:
            valid = False
            notes.append("hybrid_zh_missing_markers")
        if cjk < 8:
            valid = False
            notes.append("hybrid_zh_too_little_zh")
    elif mode == "proto_v3_zh_native":
        if has_placeholder:
            valid = False
            notes.append("contains_placeholder")
        native_fields = set(fields).intersection({"任", "目", "态", "结", "風", "风", "缺", "决", "数", "下", "证", "错", "译", "质", "损", "歧"})
        if not native_fields:
            valid = False
            notes.append("missing_zh_native_labels")
        if cc > 240:
            valid = False
            notes.append("zh_native_too_long")
        if field_count > 8:
            valid = False
            notes.append("too_many_fields_for_zh_native")
        if has_proto_v1_or_v2(text):
            valid = False
            notes.append("uses_proto_v1_or_v2")
    return valid, notes, wc, cc, field_count, fields


def error_from_result(result):
    if result.get("ok"):
        return None
    return {
        "type": result.get("error_type"),
        "message": result.get("error"),
        "http_status": result.get("status_code"),
    }


def row_template(language, task, mode, run, generation, evaluation_model, evaluation, evaluation_raw, evaluation_parse_error, eval_error, source_record=None):
    output = generation.get("output") if generation.get("ok") else ""
    source_output = source_record.get("output") if source_record else None
    valid, notes, wc, cc, field_count, fields = validate_format(language, mode, output, source_output, task)
    error = error_from_result(generation) or eval_error
    return {
        "run_id": f"{MODE_CONFIG[language]['experiment_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": utc_now(),
        "language": language,
        "experiment_id": "EXP03",
        "task_id": task["id"],
        "task_group": task["group"],
        "task_text": task["text"],
        "task_text_original_es": task["original_es"],
        "mode": mode,
        "base_mode": source_record.get("mode") if source_record else None,
        "run": run,
        "generator_model": generation.get("model_used", GENERATION_MODEL),
        "evaluator_model": evaluation_model,
        "temperature": TEMPERATURE,
        "thinking_disabled": True,
        "input_tokens": generation.get("input_tokens"),
        "output_tokens": generation.get("output_tokens"),
        "total_tokens": generation.get("total_tokens"),
        "token_count_method": generation.get("token_count_method"),
        "output": output,
        "translation_source": source_output,
        "format_valid": valid,
        "format_notes": notes,
        "word_count": wc,
        "char_count": cc,
        "field_count": field_count,
        "fields_used": fields,
        "evaluation": evaluation,
        "evaluation_raw": evaluation_raw,
        "evaluation_parse_error": evaluation_parse_error,
        "latency_ms_generation": generation.get("latency_ms"),
        "latency_ms_evaluation": None,
        "error": error,
        "http_status": generation.get("status_code"),
        "retried_after_empty_output": bool(generation.get("retried_after_empty_output")),
    }


def run_one(language, task, mode, run, source_record=None):
    if source_record:
        generation = translate(language, mode, source_record.get("output", ""))
    else:
        generation = generate(language, mode, task)
    output = generation.get("output") if generation.get("ok") else ""
    eval_model, evaluation, evaluation_raw, parse_error, eval_error, eval_latency = evaluate(language, task, mode, output) if output else (
        EVALUATOR_MODEL,
        {},
        None,
        False,
        {"type": "EMPTY_OUTPUT", "message": "No output to evaluate.", "http_status": generation.get("status_code")},
        None,
    )
    row = row_template(language, task, mode, run, generation, eval_model, evaluation, evaluation_raw, parse_error, eval_error, source_record)
    row["latency_ms_evaluation"] = eval_latency
    return row


def test_connection(language, paths):
    models = base.list_models()
    connection = {
        "timestamp": utc_now(),
        "language": language,
        "models_ok": False,
        "models_count": None,
        "chat_ok": False,
        "chat_response": None,
        "chat_model": None,
        "chat_latency_ms": None,
        "usage": None,
        "error": None,
    }
    if not models.get("ok"):
        connection["error"] = error_from_result(models)
        write_text(paths["connection"], json.dumps(connection, ensure_ascii=False, indent=2))
        return connection
    data = models.get("data") or {}
    model_list = data.get("data") if isinstance(data, dict) else None
    connection["models_ok"] = True
    connection["models_count"] = len(model_list) if isinstance(model_list, list) else None
    chat = call_model("Reply only: OK_EXP03_LANGUAGE_TEST", 30, is_eval=False)
    connection["chat_model"] = chat.get("model_used")
    connection["chat_latency_ms"] = chat.get("latency_ms")
    if not chat.get("ok"):
        connection["error"] = error_from_result(chat)
        write_text(paths["connection"], json.dumps(connection, ensure_ascii=False, indent=2))
        return connection
    connection["chat_ok"] = True
    connection["chat_response"] = chat.get("output")
    connection["usage"] = {
        "input_tokens": chat.get("input_tokens"),
        "output_tokens": chat.get("output_tokens"),
        "total_tokens": chat.get("total_tokens"),
        "token_count_method": chat.get("token_count_method"),
    }
    write_text(paths["connection"], json.dumps(connection, ensure_ascii=False, indent=2))
    return connection


def block_modes(language):
    cfg = MODE_CONFIG[language]
    return cfg["modes"], cfg["translation_map"]


def run_block(language, task_ids, runs, out_path, progress=False):
    base_modes, translation_map = block_modes(language)
    rows = []
    for raw_task in TASKS:
        if raw_task["id"] not in task_ids:
            continue
        task = task_payload(language, raw_task)
        for run in runs:
            source_rows = {}
            for mode in base_modes:
                if soft_stop(language):
                    return rows, True
                row = run_one(language, task, mode, run)
                append_jsonl(out_path, row)
                rows.append(row)
                source_rows[mode] = row
                if progress and len(rows) % 50 == 0:
                    print(
                        f"progress lang={language} rows_block={len(rows)} http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} mode={mode} task={task['id']} run={run}",
                        flush=True,
                    )
            for source_mode, translated_mode in translation_map.items():
                if soft_stop(language):
                    return rows, True
                row = run_one(language, task, translated_mode, run, source_record=source_rows[source_mode])
                append_jsonl(out_path, row)
                rows.append(row)
                if progress and len(rows) % 50 == 0:
                    print(
                        f"progress lang={language} rows_block={len(rows)} http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} mode={translated_mode} task={task['id']} run={run}",
                        flush=True,
                    )
    return rows, False


def run_pilot(language, paths):
    if paths["pilot"].exists():
        paths["pilot"].unlink()
    rows, stopped = run_block(language, {"T001", "T011"}, [1], paths["pilot"], progress=False)
    checks = {
        "language": language,
        "rows": len(rows),
        "expected_rows": 16 if language == "EN" else 20,
        "errors": sum(1 for r in rows if r.get("error")),
        "parse_errors": sum(1 for r in rows if r.get("evaluation_parse_error")),
        "missing_tokens": sum(1 for r in rows if r.get("total_tokens") is None),
        "format_invalid": sum(1 for r in rows if r.get("format_valid") is False),
        "format_invalid_base": sum(1 for r in rows if r.get("format_valid") is False and "translated" not in r.get("mode", "")),
        "zh_caricature": sum(1 for r in rows if "compressed_zh_caricature" in r.get("format_notes", [])),
        "stopped": stopped,
    }
    checks["ok"] = (
        checks["rows"] == checks["expected_rows"]
        and checks["errors"] == 0
        and checks["parse_errors"] == 0
        and checks["missing_tokens"] == 0
        and checks["format_invalid_base"] == 0
        and checks["zh_caricature"] == 0
    )
    return checks


def run_full(language, paths):
    backup = backup_if_exists(paths["runs"])
    task_ids = {task["id"] for task in TASKS}
    rows, stopped = run_block(language, task_ids, range(1, REPETITIONS + 1), paths["runs"], progress=True)
    return read_jsonl(paths["runs"]), stopped, backup


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
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["mode"]].append(row)
    out = {}
    for mode, items in grouped.items():
        out[mode] = {
            "rows": len(items),
            "errors": sum(1 for r in items if r.get("error")),
            "avg_input_tokens": mean([r.get("input_tokens") for r in items]),
            "avg_output_tokens": mean([r.get("output_tokens") for r in items]),
            "avg_total_tokens": mean([r.get("total_tokens") for r in items]),
            "latency_generation": mean([r.get("latency_ms_generation") for r in items]),
            "latency_evaluation": mean([r.get("latency_ms_evaluation") for r in items]),
            "format_valid_pct": mean([1 if r.get("format_valid") is True else 0 if r.get("format_valid") is False else None for r in items]),
            "word_count": mean([r.get("word_count") for r in items]),
            "char_count": mean([r.get("char_count") for r in items]),
            "field_count": mean([r.get("field_count") for r in items]),
        }
        for metric in METRICS:
            out[mode][metric] = mean([r.get("evaluation", {}).get(metric) for r in items])
    return out


def summarize_by_group(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["task_group"], row["mode"])].append(row)
    summary = {}
    for key, items in grouped.items():
        total = mean([r.get("total_tokens") for r in items])
        quality = mean([
            mean([
                r.get("evaluation", {}).get("semantic_fidelity"),
                r.get("evaluation", {}).get("clarity"),
                r.get("evaluation", {}).get("utility"),
            ])
            for r in items
        ])
        state = mean([r.get("evaluation", {}).get("state_preservation") for r in items])
        summary[key] = {"tokens": total, "quality": quality, "state": state}
    return summary


def balance_score(data):
    total = data.get("avg_total_tokens")
    token_component = 1000 / total if total else 0
    return (
        token_component
        + (data.get("semantic_fidelity") or 0)
        + (data.get("clarity") or 0)
        + (data.get("utility") or 0)
        + (data.get("state_preservation") or 0)
        + (data.get("compactness") or 0)
        - (data.get("ambiguity") or 0)
        - (data.get("information_loss") or 0)
    )


def best_mode(summary, metric, reverse=True, modes=None):
    selected = modes or list(summary)
    vals = {m: summary[m].get(metric) for m in selected if m in summary and summary[m].get(metric) is not None}
    if not vals:
        return "NO_CALCULABLE"
    return sorted(vals.items(), key=lambda kv: kv[1], reverse=reverse)[0][0]


def cheapest(summary, modes=None):
    return best_mode(summary, "avg_total_tokens", reverse=False, modes=modes)


def best_quality(summary, modes=None):
    selected = modes or list(summary)
    vals = {}
    for mode in selected:
        data = summary.get(mode)
        if not data:
            continue
        vals[mode] = mean([data.get("semantic_fidelity"), data.get("clarity"), data.get("utility")])
    vals = {k: v for k, v in vals.items() if v is not None}
    if not vals:
        return "NO_CALCULABLE"
    return sorted(vals.items(), key=lambda kv: kv[1], reverse=True)[0][0]


def best_balance(summary, modes=None):
    selected = modes or list(summary)
    vals = {mode: balance_score(summary[mode]) for mode in selected if mode in summary}
    if not vals:
        return "NO_CALCULABLE"
    return sorted(vals.items(), key=lambda kv: kv[1], reverse=True)[0][0]


def translation_pairs(language):
    return MODE_CONFIG[language]["translation_map"]


def table_global(summary):
    lines = [
        "| language | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | completeness | utility | ambiguity | info_loss | translation_ease | state_preservation | compactness |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode, data in summary.items():
        lang = "EN" if mode.endswith("_en") else "ZH"
        lines.append(
            f"| {lang} | {mode} | {data['rows']} | {data['errors']} | {fmt(data['avg_input_tokens'])} | {fmt(data['avg_output_tokens'])} | {fmt(data['avg_total_tokens'])} | {fmt(data['semantic_fidelity'])} | {fmt(data['clarity'])} | {fmt(data['completeness'])} | {fmt(data['utility'])} | {fmt(data['ambiguity'])} | {fmt(data['information_loss'])} | {fmt(data['translation_ease'])} | {fmt(data['state_preservation'])} | {fmt(data['compactness'])} |"
        )
    return "\n".join(lines)


def table_groups(rows, summary):
    group_summary = summarize_by_group(rows)
    modes = list(summary)
    base_modes = [m for m in modes if "translated" not in m]
    lines = [
        "| language | task_group | best_tokens | best_quality | best_state | best_balance | observation |",
        "|---|---|---|---|---|---|---|",
    ]
    for group in ["base_comparable", "memory_state", "medium_complexity"]:
        values = {m: group_summary.get((group, m), {}) for m in base_modes}
        best_tok = min(values, key=lambda m: values[m].get("tokens") if values[m].get("tokens") is not None else 10**9)
        best_q = max(values, key=lambda m: values[m].get("quality") if values[m].get("quality") is not None else -1)
        best_s = max(values, key=lambda m: values[m].get("state") if values[m].get("state") is not None else -1)
        obs = "calculo_solo_modos_base"
        lines.append(f"| {rows[0]['language'] if rows else ''} | {group} | {best_tok} | {best_q} | {best_s} | {best_balance(summary, base_modes)} | {obs} |")
    return "\n".join(lines)


def table_proto_variants(language, summary):
    if language == "EN":
        proto_modes = ["proto_v3_min_core_en", "proto_v3_state_core_en", "proto_v3_hybrid_en"]
    else:
        proto_modes = ["proto_v3_min_core_zh", "proto_v3_state_core_zh", "proto_v3_hybrid_zh", "proto_v3_zh_native"]
    lines = [
        "| language | proto_variant | avg_total_tokens | avg_output_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | reading |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    compressed = "compressed_en" if language == "EN" else "compressed_zh"
    comp_tokens = summary.get(compressed, {}).get("avg_total_tokens")
    for mode in proto_modes:
        data = summary.get(mode, {})
        tokens = data.get("avg_total_tokens")
        reading = "promising" if tokens and comp_tokens and tokens <= comp_tokens * 1.1 and (data.get("utility") or 0) >= 4 else "not_stronger_than_compressed"
        lines.append(f"| {language} | {mode} | {fmt(tokens)} | {fmt(data.get('avg_output_tokens'))} | {fmt(data.get('semantic_fidelity'))} | {fmt(data.get('clarity'))} | {fmt(data.get('utility'))} | {fmt(data.get('ambiguity'))} | {fmt(data.get('information_loss'))} | {fmt(data.get('state_preservation'))} | {reading} |")
    return "\n".join(lines)


def table_translations(language, summary):
    lines = [
        "| language | proto_mode | proto_tokens | translated_tokens | architectural_total | clarity_proto | clarity_translated | fidelity_proto | fidelity_translated | reading |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for proto, translated in translation_pairs(language).items():
        p = summary.get(proto, {})
        t = summary.get(translated, {})
        total = None
        if p.get("avg_total_tokens") is not None and t.get("avg_total_tokens") is not None:
            total = p["avg_total_tokens"] + t["avg_total_tokens"]
        reading = "extra_call"
        if total and "compressed" not in proto:
            compressed = summary.get("compressed_en" if language == "EN" else "compressed_zh", {}).get("avg_total_tokens")
            if compressed and total > compressed:
                reading += ";destroys_saving_vs_compressed"
        lines.append(f"| {language} | {proto} | {fmt(p.get('avg_total_tokens'))} | {fmt(t.get('avg_total_tokens'))} | {fmt(total)} | {fmt(p.get('clarity'))} | {fmt(t.get('clarity'))} | {fmt(p.get('semantic_fidelity'))} | {fmt(t.get('semantic_fidelity'))} | {reading} |")
    return "\n".join(lines)


def anomalies(rows):
    counts = Counter()
    examples = []
    for row in rows:
        if row.get("error"):
            err = row["error"]
            counts[f"error:{err.get('type') if isinstance(err, dict) else err}"] += 1
            if len(examples) < 12:
                examples.append(f"- {row['task_id']} {row['mode']}: error={err}")
        if row.get("evaluation_parse_error"):
            counts["parse_error"] += 1
        if row.get("total_tokens") is None:
            counts["missing_tokens"] += 1
        if row.get("format_valid") is False:
            for note in row.get("format_notes", []):
                counts[f"format:{note}"] += 1
            if len(examples) < 12:
                examples.append(f"- {row['task_id']} {row['mode']}: format_notes={row.get('format_notes')}")
    return counts, examples


def anomaly_markdown(counts, examples):
    if not counts:
        return "- No se registraron anomalías relevantes."
    lines = [f"- {key}: {value}" for key, value in counts.most_common()]
    if examples:
        lines.append("\n### Ejemplos")
        lines.extend(examples)
    return "\n".join(lines)


def success_reading(language, summary):
    compressed = "compressed_en" if language == "EN" else "compressed_zh"
    natural = "natural_en" if language == "EN" else "natural_zh"
    hybrid = "proto_v3_hybrid_en" if language == "EN" else "proto_v3_hybrid_zh"
    state = "proto_v3_state_core_en" if language == "EN" else "proto_v3_state_core_zh"
    min_mode = "proto_v3_min_core_en" if language == "EN" else "proto_v3_min_core_zh"
    readings = []
    if summary.get(compressed, {}).get("avg_total_tokens") and summary.get(natural, {}).get("avg_total_tokens"):
        if summary[compressed]["avg_total_tokens"] < summary[natural]["avg_total_tokens"]:
            readings.append(f"`{compressed}` reduce tokens frente a `{natural}`.")
        else:
            readings.append(f"`{compressed}` no reduce tokens frente a `{natural}`.")
    for mode in [min_mode, state, hybrid]:
        if mode in summary and compressed in summary:
            tokens = summary[mode].get("avg_total_tokens")
            comp = summary[compressed].get("avg_total_tokens")
            state_gain = (summary[mode].get("state_preservation") or 0) - (summary[compressed].get("state_preservation") or 0)
            if tokens and comp and tokens <= comp:
                readings.append(f"`{mode}` supera a `{compressed}` en tokens.")
            elif tokens and comp and tokens <= comp * 1.10 and state_gain > 0.25:
                readings.append(f"`{mode}` no gana tokens, pero queda cerca y mejora estado.")
            else:
                readings.append(f"`{mode}` no supera el criterio fuerte contra `{compressed}`.")
    if language == "ZH" and "proto_v3_zh_native" in summary:
        native = summary["proto_v3_zh_native"]
        core = summary.get("proto_v3_min_core_zh", {})
        if native.get("avg_total_tokens") and core.get("avg_total_tokens") and native["avg_total_tokens"] < core["avg_total_tokens"]:
            readings.append("`proto_v3_zh_native` mejora tokens frente al core mínimo chino.")
        else:
            readings.append("`proto_v3_zh_native` no mejora tokens frente al core mínimo chino.")
    return "\n".join(f"- {item}" for item in readings)


def write_reports(language, rows, connection, pilot, stopped, backup, paths):
    summary = summarize(rows)
    counts, examples = anomalies(rows)
    base_modes = [m for m in MODE_CONFIG[language]["modes"] if m in summary]
    expected_rows = (720 if language == "EN" else 900)
    cheapest_mode = cheapest(summary, base_modes)
    best_q = best_quality(summary, base_modes)
    best_s = best_mode(summary, "state_preservation", modes=base_modes)
    best_proto_modes = [m for m in base_modes if "proto" in m]
    best_proto = best_balance(summary, best_proto_modes)
    report = f"""# Resultados EXP03 {language}

## Configuración

- Experimento: `EXP03_{language}`
- Perfil: `{MODE_CONFIG[language]['experiment_id']}_FULL_SEPARATE`
- Endpoint: `{base.CHAT_COMPLETIONS_URL}`
- Modelo generador: `{GENERATION_MODEL}`
- Modelo evaluador: `{EVALUATOR_MODEL}`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: {TEMPERATURE}
- Repeticiones: {REPETITIONS}
- Filas esperadas: {expected_rows}
- Filas generadas: {len(rows)}
- Llamadas HTTP: {base.CALL_STATS['attempted']}
- Errores HTTP contabilizados: {base.CALL_STATS['errors']}
- Parse errors: {sum(1 for r in rows if r.get('evaluation_parse_error'))}
- Missing tokens: {sum(1 for r in rows if r.get('total_tokens') is None)}
- Fallos de formato: {sum(1 for r in rows if r.get('format_valid') is False)}
- Soft stop: {stopped}
- Backup JSONL previo: {backup or 'no_aplica'}

## Conexión

```json
{json.dumps(connection, ensure_ascii=False, indent=2)}
```

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Tabla global

{table_global(summary)}

## Tabla por grupo de tarea

{table_groups(rows, summary)}

## Variantes proto

{table_proto_variants(language, summary)}

## Traducciones

La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.

{table_translations(language, summary)}

## Ganadores

- Modo base más barato: `{cheapest_mode}`
- Mejor calidad base: `{best_q}`
- Mejor manejo de estado base: `{best_s}`
- Mejor variante proto base: `{best_proto}`

## Lectura

{success_reading(language, summary)}

## Errores y anomalías

{anomaly_markdown(counts, examples)}
"""
    write_text(paths["results"], report)
    write_text(paths["translation"], f"# Análisis de traducciones EXP03 {language}\n\nLa fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.\n\n{table_translations(language, summary)}\n")
    write_text(paths["errors"], f"# Errores y anomalías EXP03 {language}\n\n- Filas: {len(rows)}\n- Errores por fila: {sum(1 for r in rows if r.get('error'))}\n- Parse errors: {sum(1 for r in rows if r.get('evaluation_parse_error'))}\n- Missing tokens: {sum(1 for r in rows if r.get('total_tokens') is None)}\n- Fallos de formato: {sum(1 for r in rows if r.get('format_valid') is False)}\n\n{anomaly_markdown(counts, examples)}\n")
    write_text(paths["summary"], f"""# Resumen Ejecutivo EXP03 {language}

## Estado

- Piloto OK: {pilot.get('ok')}
- FULL ejecutado: {'parcial_por_soft_stop' if stopped else 'sí'}
- Filas esperadas: {expected_rows}
- Filas generadas: {len(rows)}
- Llamadas HTTP: {base.CALL_STATS['attempted']}
- Errores HTTP: {base.CALL_STATS['errors']}

## Ganadores

- Modo más barato: `{cheapest_mode}`
- Mejor calidad: `{best_q}`
- Mejor manejo de estado: `{best_s}`
- Mejor variante proto: `{best_proto}`

## Lectura principal

{success_reading(language, summary)}

## Recomendación preliminar

{recommendation(language, summary)}

Datos antes que entusiasmo.
""")
    write_text(paths["log"], f"""# Log de ejecución EXP03 {language}

## Fechas

- Generado: {utc_now()}

## Conexión

```json
{json.dumps(connection, ensure_ascii=False, indent=2)}
```

## Piloto

```json
{json.dumps(pilot, ensure_ascii=False, indent=2)}
```

## Resultado

- Filas: {len(rows)}
- Llamadas HTTP: {base.CALL_STATS['attempted']}
- Errores HTTP: {base.CALL_STATS['errors']}
- Soft stop: {stopped}
- Backup: {backup or 'no_aplica'}
""")


def recommendation(language, summary):
    compressed = "compressed_en" if language == "EN" else "compressed_zh"
    hybrid = "proto_v3_hybrid_en" if language == "EN" else "proto_v3_hybrid_zh"
    state = "proto_v3_state_core_en" if language == "EN" else "proto_v3_state_core_zh"
    native = "proto_v3_zh_native"
    if hybrid in summary and compressed in summary:
        h = summary[hybrid]
        c = summary[compressed]
        if h.get("avg_total_tokens") and c.get("avg_total_tokens") and h["avg_total_tokens"] <= c["avg_total_tokens"] * 1.15 and (h.get("utility") or 0) >= 4.4:
            return "Hybrid_Min"
    if state in summary and compressed in summary:
        s = summary[state]
        c = summary[compressed]
        if (s.get("state_preservation") or 0) > (c.get("state_preservation") or 0) + 0.25 and s.get("avg_total_tokens") and c.get("avg_total_tokens") and s["avg_total_tokens"] <= c["avg_total_tokens"] * 1.35:
            return "Caveman_State"
    if language == "ZH" and native in summary and compressed in summary:
        n = summary[native]
        c = summary[compressed]
        if n.get("avg_total_tokens") and c.get("avg_total_tokens") and n["avg_total_tokens"] <= c["avg_total_tokens"] * 1.15 and (n.get("state_preservation") or 0) > (c.get("state_preservation") or 0):
            return "Native_Proto_By_Language"
    return "Caveman_State" if compressed in summary else "Evaluacion_Humana"


def run_secret_scan(paths):
    secret_pattern = re.compile(r"s" + "k" + r"-[A-Za-z0-9]{16,}")
    literal_patterns = ["api" + "_key", "API" + "_KEY", "Author" + "ization", "Bear" + "er", "token" + "="]
    hits = []
    for path in paths.values():
        if not isinstance(path, Path) or not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if secret_pattern.search(text):
            hits.append(f"{path.name}:secret_pattern")
        for pattern in literal_patterns:
            if pattern in text:
                hits.append(f"{path.name}:{pattern}")
    return hits


def validate_jsonl(path):
    rows = read_jsonl(path)
    return len(rows)


def main(language):
    language = language.upper()
    if language not in MODE_CONFIG:
        raise ValueError("language must be EN or ZH")
    configure_base(language)
    require_key()
    paths = paths_for(language)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    connection = test_connection(language, paths)
    if not connection.get("models_ok") or not connection.get("chat_ok"):
        write_text(paths["errors"], "# Error de conexión\n\nNo se ejecutó el piloto ni FULL.\n")
        print(f"connection_failed language={language}", flush=True)
        return 1
    pilot = run_pilot(language, paths)
    print(f"pilot language={language} rows={pilot['rows']} ok={pilot['ok']} errors={pilot['errors']} missing_tokens={pilot['missing_tokens']} format_invalid_base={pilot['format_invalid_base']}", flush=True)
    if not pilot["ok"]:
        write_text(paths["errors"], "# Piloto fallido\n\n```json\n" + json.dumps(pilot, ensure_ascii=False, indent=2) + "\n```\n")
        return 1
    rows, stopped, backup = run_full(language, paths)
    count = validate_jsonl(paths["runs"])
    write_reports(language, rows, connection, pilot, stopped, backup, paths)
    hits = run_secret_scan(paths)
    if hits:
        write_text(paths["errors"], "# Secret scan hit\n\n" + "\n".join(hits) + "\n")
        print(f"secret_scan_hit language={language}", flush=True)
        return 1
    print(f"done language={language} rows={count} http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} stopped={stopped}", flush=True)
    return 0


def load_summary_for_language(language):
    paths = paths_for(language)
    rows = read_jsonl(paths["runs"])
    return rows, summarize(rows) if rows else {}


def write_cross_language_reports():
    out_dir = THIS_DIR / "EXP03_EN_ZH"
    out_dir.mkdir(parents=True, exist_ok=True)
    en_rows, en = load_summary_for_language("EN")
    zh_rows, zh = load_summary_for_language("ZH")
    if not en or not zh:
        write_text(out_dir / "Comparacion_EXP03_EN_vs_ZH.md", "# Comparación EXP03 EN vs ZH\n\nPENDIENTE: falta JSONL de EN o ZH.\n")
        return 1

    def get(summary, mode, key):
        return summary.get(mode, {}).get(key)

    lines = [
        "# Comparación EXP03 EN vs ZH",
        "",
        "## Tabla EN/ZH",
        "",
        "| language | natural | compressed | proto_min | proto_state | proto_hybrid | best_token_mode | best_proto_mode | reading |",
        "|---|---:|---:|---:|---:|---:|---|---|---|",
    ]
    en_base = ["natural_en", "compressed_en", "proto_v3_min_core_en", "proto_v3_state_core_en", "proto_v3_hybrid_en"]
    zh_base = ["natural_zh", "compressed_zh", "proto_v3_min_core_zh", "proto_v3_state_core_zh", "proto_v3_hybrid_zh"]
    lines.append(f"| EN | {fmt(get(en,'natural_en','avg_total_tokens'))} | {fmt(get(en,'compressed_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_min_core_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_state_core_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_hybrid_en','avg_total_tokens'))} | {cheapest(en, en_base)} | {best_balance(en, [m for m in en_base if 'proto' in m])} | {recommendation('EN', en)} |")
    lines.append(f"| ZH | {fmt(get(zh,'natural_zh','avg_total_tokens'))} | {fmt(get(zh,'compressed_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_min_core_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_state_core_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_hybrid_zh','avg_total_tokens'))} | {cheapest(zh, zh_base)} | {best_balance(zh, [m for m in zh_base if 'proto' in m])} | {recommendation('ZH', zh)} |")
    lines.extend([
        "",
        "## Chino nativo",
        "",
        "| mode | tokens | fidelity | clarity | utility | state_preservation | ambiguity | info_loss | reading |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ])
    native = zh.get("proto_v3_zh_native", {})
    core = zh.get("proto_v3_min_core_zh", {})
    native_reading = "native_less_than_core" if native.get("avg_total_tokens") and core.get("avg_total_tokens") and native["avg_total_tokens"] < core["avg_total_tokens"] else "native_not_less_than_core"
    lines.append(f"| proto_v3_zh_native | {fmt(native.get('avg_total_tokens'))} | {fmt(native.get('semantic_fidelity'))} | {fmt(native.get('clarity'))} | {fmt(native.get('utility'))} | {fmt(native.get('state_preservation'))} | {fmt(native.get('ambiguity'))} | {fmt(native.get('information_loss'))} | {native_reading} |")
    lines.extend([
        "",
        "## Traducciones",
        "",
        "La fila traducida mide solo la llamada de traducción. El costo arquitectónico real de traducir por salida es proto + translated.",
        "",
        "### EN",
        "",
        table_translations("EN", en),
        "",
        "### ZH",
        "",
        table_translations("ZH", zh),
    ])
    write_text(out_dir / "Comparacion_EXP03_EN_vs_ZH.md", "\n".join(lines) + "\n")

    cross = [
        "# Comparación EXP03 ES EN ZH",
        "",
        "| language | natural | compressed | proto_min | proto_state | proto_hybrid | best_token_mode | best_proto_mode | reading |",
        "|---|---:|---:|---:|---:|---:|---|---|---|",
        f"| ES | {fmt(ES_EXP03_REFERENCES['natural']['tokens'])} | {fmt(ES_EXP03_REFERENCES['compressed']['tokens'])} | {fmt(ES_EXP03_REFERENCES['proto_min']['tokens'])} | {fmt(ES_EXP03_REFERENCES['proto_state']['tokens'])} | {fmt(ES_EXP03_REFERENCES['proto_hybrid']['tokens'])} | caveman | proto_v3_hybrid | referencia_es_real |",
        f"| EN | {fmt(get(en,'natural_en','avg_total_tokens'))} | {fmt(get(en,'compressed_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_min_core_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_state_core_en','avg_total_tokens'))} | {fmt(get(en,'proto_v3_hybrid_en','avg_total_tokens'))} | {cheapest(en, en_base)} | {best_balance(en, [m for m in en_base if 'proto' in m])} | datos_exp03_en |",
        f"| ZH | {fmt(get(zh,'natural_zh','avg_total_tokens'))} | {fmt(get(zh,'compressed_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_min_core_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_state_core_zh','avg_total_tokens'))} | {fmt(get(zh,'proto_v3_hybrid_zh','avg_total_tokens'))} | {cheapest(zh, zh_base)} | {best_balance(zh, [m for m in zh_base if 'proto' in m])} | datos_exp03_zh |",
        "",
        "## Nota metodológica",
        "",
        "`proto_v3_zh_native` es una variante adicional localizada y no debe tratarse como equivalente directo de ES o EN.",
    ]
    write_text(out_dir / "Comparacion_EXP03_ES_EN_ZH.md", "\n".join(cross) + "\n")
    executive = f"""# Resumen Ejecutivo EXP03 EN ZH

## Estado

- EXP03_EN filas: {len(en_rows)}
- EXP03_ZH filas: {len(zh_rows)}

## Lectura principal

- EN modo más barato: `{cheapest(en, en_base)}`
- ZH modo más barato: `{cheapest(zh, zh_base)}`
- EN mejor variante proto: `{best_balance(en, [m for m in en_base if 'proto' in m])}`
- ZH mejor variante proto core/hybrid: `{best_balance(zh, [m for m in zh_base if 'proto' in m])}`
- ZH nativo: `{native_reading}`

## Recomendación EXP04

- EN: {recommendation('EN', en)}
- ZH: {recommendation('ZH', zh)}

Datos antes que entusiasmo.
"""
    write_text(out_dir / "Resumen_Ejecutivo_EXP03_EN_ZH.md", executive)
    return 0
