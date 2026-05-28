import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
EXP_DIR = SCRIPT_DIR.parent
PROJECT_DIR = EXP_DIR.parent
if str(EXP_DIR) not in sys.path:
    sys.path.insert(0, str(EXP_DIR))

try:
    import run_experimento_01_opencode_go_local  # noqa: F401
except Exception:
    pass

import run_experimento_01_opencode_go as base


EXPERIMENT_ID = "EXP04_TRI"
RUN_ID = "EXP04_TRI_Hybrid_Min_vs_Compressed_State"
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "deepseek-v4-flash")
GENERATION_MODEL_FALLBACK = os.getenv("GENERATION_MODEL_FALLBACK", "opencode-go/deepseek-v4-flash")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "deepseek-v4-pro")
EVALUATOR_MODEL_FALLBACK = os.getenv("EVALUATOR_MODEL_FALLBACK", "deepseek-v4-flash")
TEMPERATURE = 0.2
REPETITIONS = 3
MAX_HTTP_CALLS = 3500
SOFT_STOP_HTTP_CALLS = 3200
REQUEST_TIMEOUT = 90
MAX_TOKENS_NATURAL = 500
MAX_TOKENS_COMPRESSED = 260
MAX_TOKENS_STATE = 320
MAX_TOKENS_EVALUATION = 300
MAX_TOKENS_BATCH_DECODE = 1400
EMPTY_RETRY_MAX_TOKENS = 1200

TASK_BANK_PATH = SCRIPT_DIR / "task_bank_exp04_tri.jsonl"
RUNS_PATH = SCRIPT_DIR / "exp04_tri_runs.jsonl"
PILOT_PATH = SCRIPT_DIR / "pilot_exp04_tri.jsonl"
BATCH_PATH = SCRIPT_DIR / "exp04b_batch_decode_results.jsonl"
CONNECTION_PATH = SCRIPT_DIR / "connection_test_exp04_tri.json"
STDOUT_LOG_NOTE = SCRIPT_DIR / "exp04_tri_execution_log.md"
RESULTS_PATH = SCRIPT_DIR / "Resultados_EXP04_TRI.md"
COMPARISON_PATH = SCRIPT_DIR / "Comparacion_EXP04_ES_EN_ZH.md"
MODE_ANALYSIS_PATH = SCRIPT_DIR / "Analisis_Modos_EXP04_TRI.md"
CONTINUITY_PATH = SCRIPT_DIR / "Analisis_Continuidad_Operativa_EXP04.md"
LANGUAGE_PATH = SCRIPT_DIR / "Analisis_Por_Idioma_EXP04.md"
EXP03_COMP_PATH = SCRIPT_DIR / "Comparacion_EXP03_vs_EXP04.md"
ERRORS_PATH = SCRIPT_DIR / "Errores_y_Anomalias_EXP04_TRI.md"
SUMMARY_PATH = SCRIPT_DIR / "Resumen_Ejecutivo_EXP04_TRI.md"
BATCH_REPORT_PATH = SCRIPT_DIR / "Analisis_EXP04B_Batch_Final_Decode.md"

LANGUAGES = ["ES", "EN", "ZH"]
FAMILIES = ["natural", "compressed", "compressed_state", "hybrid_min", "hybrid_state"]
PILOT_TASKS = {"T001", "T011", "T021"}

STRICT_OUTPUT_PREFIX = """Output plain text only.
No Markdown. No bold text. No headings. No bullet lists unless the task explicitly needs a list.
If a mode uses markers, keep each marker and its value on the same line.
Do not use empty fields. Keep the output compact."""

LENGTH_RULES = {
    "natural": "Length target: clear but concise; avoid headings and long lists.",
    "compressed": "Hard length limit: ES/EN <= 75 words; ZH <= 180 Chinese characters. No numbered lists.",
    "compressed_state": "Hard length limit: ES/EN <= 95 words; ZH <= 230 Chinese characters. Use only useful state marks.",
    "hybrid_min": "Hard length limit: ES/EN <= 65 words; ZH <= 170 Chinese characters. Use 2-4 markers only.",
    "hybrid_state": "Hard length limit: ES/EN <= 105 words; ZH <= 260 Chinese characters. Use no more than 6 useful fields.",
}

EXP03_REFERENCE = {
    "ES": {"compressed": 233.89, "hybrid": 266.78},
    "EN": {"compressed": 188.98, "hybrid": 199.81},
    "ZH": {"compressed": 194.86, "hybrid": 211.36},
}

TASKS = [
    ("T001", "base_comparable", "reused_from_EXP03",
     "Analiza este problema: un sistema multiagente consume demasiados tokens porque cada agente escribe explicaciones largas. Propón solución, riesgos y próximos pasos.",
     "Analyze this problem: a multi-agent system consumes too many tokens because each agent writes long explanations. Propose a solution, risks, and next steps.",
     "分析这个问题：一个多智能体系统消耗太多 token，因为每个智能体都写很长解释。提出解决方案、风险和下一步。"),
    ("T002", "base_comparable", "reused_from_EXP03",
     "Resume una arquitectura de agentes con trabajador, supervisor, memoria y traductor final. Incluye ventajas y limitaciones.",
     "Summarize an agent architecture with worker, supervisor, memory, and final translator. Include advantages and limitations.",
     "总结一种包含工作者、监督者、记忆和最终翻译器的智能体架构。包括优点和限制。"),
    ("T003", "base_comparable", "reused_from_EXP03",
     "Convierte una explicación larga sobre eficiencia de tokens en una estructura operativa para agentes.",
     "Convert a long explanation about token efficiency into an operational structure for agents.",
     "把一段关于 token 效率的长解释转换成智能体可用的操作结构。"),
    ("T004", "base_comparable", "reused_from_EXP03",
     "Diseña reglas iniciales para evitar deriva semántica en un protocolo simbólico.",
     "Design initial rules to prevent semantic drift in a symbolic protocol.",
     "设计初始规则，避免符号协议中的语义漂移。"),
    ("T005", "base_comparable", "reused_from_EXP03",
     "Detecta riesgos en un sistema donde varios agentes se comunican con símbolos comprimidos.",
     "Detect risks in a system where several agents communicate with compressed symbols.",
     "检测一个多智能体使用压缩符号通信的系统中的风险。"),
    ("T006", "base_comparable", "reused_from_EXP03",
     "Propón una metodología para medir si un protolenguaje conserva significado.",
     "Propose a methodology to measure whether a protolanguage preserves meaning.",
     "提出一种方法，用来衡量原语言是否保留意义。"),
    ("T007", "base_comparable", "reused_from_EXP03",
     "Extrae variables medibles de un experimento sobre comunicación multiagente.",
     "Extract measurable variables from an experiment about multi-agent communication.",
     "从多智能体通信实验中提取可测量变量。"),
    ("T008", "base_comparable", "reused_from_EXP03",
     "Crea una plantilla breve para registrar resultados de pruebas con modelos IA.",
     "Create a brief template to record test results with AI models.",
     "创建一个简短模板，用于记录 AI 模型测试结果。"),
    ("T009", "base_comparable", "reused_from_EXP03",
     "Compara lenguaje natural, lenguaje natural comprimido y protolenguaje en términos de costo, claridad y error.",
     "Compare natural language, compressed natural language, and protolanguage in terms of cost, clarity, and error.",
     "比较自然语言、压缩自然语言和原语言在成本、清晰度和错误方面的差异。"),
    ("T010", "base_comparable", "reused_from_EXP03",
     "Propón cómo un agente traductor debe convertir protolenguaje a español humano sin inventar información.",
     "Propose how a translator agent should convert protolanguage into human English without inventing information.",
     "提出翻译智能体如何把原语言转换成清晰中文，同时不编造信息。"),
    ("T011", "memory_state", "reused_from_EXP03",
     "Un agente trabajador terminó una tarea, pero debe pasar al siguiente agente objetivo, contexto, error detectado, riesgo y próxima acción. Resume ese estado de forma eficiente.",
     "A worker agent finished a task, but must pass the next agent the objective, context, detected error, risk, and next action. Summarize that state efficiently.",
     "一个工作智能体完成了任务，但必须把目标、上下文、检测到的错误、风险和下一步动作传给下一个智能体。高效总结该状态。"),
    ("T012", "memory_state", "reused_from_EXP03",
     "Dos agentes coordinan una investigación. El agente A encontró que compressed ahorra más tokens, pero el agente B necesita conservar trazabilidad de hipótesis, métricas y límites. Propón una salida compacta.",
     "Two agents are coordinating research. Agent A found that compressed saves more tokens, but Agent B needs traceability of hypotheses, metrics, and limits. Propose a compact output.",
     "两个智能体正在协同研究。智能体 A 发现 compressed 更省 token，但智能体 B 需要保留假设、指标和限制的可追踪性。提出紧凑输出。"),
    ("T013", "memory_state", "reused_from_EXP03",
     "Comprime este estado de proyecto: EXP01 mostró que compressed ganó; EXP02 mostró que proto_v2 mejoró pero perdió calidad; EXP03 debe probar proto_v3 minimalista. Conserva decisión y siguiente paso.",
     "Compress this project state: EXP01 showed compressed won; EXP02 showed proto_v2 improved but lost quality; EXP03 must test minimalist proto_v3. Preserve decision and next step.",
     "压缩以下项目状态：EXP01 显示 compressed 获胜；EXP02 显示 proto_v2 有改进但质量下降；EXP03 必须测试极简 proto_v3。保留决策和下一步。"),
    ("T014", "memory_state", "reused_from_EXP03",
     "Un agente debe reportar error de formato: la salida híbrida usó etiquetas de Proto v1 y fue demasiado larga. Resume problema, corrección y verificación.",
     "An agent must report a format error: the hybrid output used Proto v1 tags and was too long. Summarize problem, correction, and verification.",
     "一个智能体必须报告格式错误：hybrid 输出使用了 Proto v1 标签，而且太长。总结问题、修正和验证。"),
    ("T015", "memory_state", "reused_from_EXP03",
     "Diseña una memoria compacta para guardar que el usuario prefiere optimización de tokens, documentación en Markdown y experimentos con resultados reales.",
     "Design compact memory to store that the user prefers token optimization, Markdown documentation, and experiments with real results.",
     "设计紧凑记忆，保存用户偏好：token 优化、Markdown 文档、使用真实结果的实验。"),
    ("T016", "memory_state", "reused_from_EXP03",
     "Evalúa una salida de agente que es corta pero ambigua. Debes conservar: problema, por qué es ambigua, riesgo y corrección.",
     "Evaluate an agent output that is short but ambiguous. Preserve: problem, why it is ambiguous, risk, and correction.",
     "评估一个很短但含糊的智能体输出。必须保留：问题、为什么含糊、风险和修正。"),
    ("T017", "memory_state", "reused_from_EXP03",
     "Crea un plan de tres pasos para probar si un traductor final puede decodificar lotes de salidas comprimidas en una sola llamada.",
     "Create a three-step plan to test whether a final translator can decode batches of compressed outputs in a single call.",
     "创建三步计划，测试最终翻译器是否能在一次调用中解码一批压缩输出。"),
    ("T018", "memory_state", "reused_from_EXP03",
     "Resume una comparación entre tres opciones: lenguaje natural, compressed y hybrid_min. Conserva costo, claridad y riesgo principal.",
     "Summarize a comparison between three options: natural language, compressed, and hybrid_min. Preserve cost, clarity, and main risk.",
     "总结三种方案的比较：自然语言、compressed、hybrid_min。保留成本、清晰度和主要风险。"),
    ("T019", "memory_state", "reused_from_EXP03",
     "Un sistema multiagente debe pasar contexto entre cinco agentes sin superar límite de tokens. Propón estrategia compacta con memoria y verificación.",
     "A multi-agent system must pass context across five agents without exceeding the token limit. Propose a compact strategy with memory and verification.",
     "一个多智能体系统必须在五个智能体之间传递上下文，同时不超过 token 限制。提出带记忆和验证的紧凑策略。"),
    ("T020", "memory_state", "reused_from_EXP03",
     "Convierte una salida técnica comprimida en una instrucción entendible para un agente supervisor.",
     "Convert a compressed technical output into an understandable instruction for a supervisor agent.",
     "把一个压缩技术输出转换成监督智能体可理解的指令。"),
    ("T021", "multiagent_continuation", "new_EXP04",
     "Agente A revisó un experimento y detectó que el modo más barato no es el de mejor calidad. Genera una salida interna para que Agente B continúe el análisis sin perder objetivo, resultado, riesgo y siguiente paso.",
     "Agent A reviewed an experiment and found that the cheapest mode is not the best-quality mode. Generate an internal message so Agent B can continue the analysis without losing goal, result, risk, and next step.",
     "代理A检查实验后发现：最省token的模式不是质量最高的模式。生成内部消息，让代理B继续分析且不丢失目标、结果、风险和下一步。"),
    ("T022", "multiagent_continuation", "new_EXP04",
     "Agente A dejó un informe parcial con métricas incompletas. Prepara un mensaje para Agente B con lo hecho, lo faltante, la decisión pendiente y cómo verificar los datos.",
     "Agent A left a partial report with incomplete metrics. Prepare a message for Agent B with what was done, what is missing, the pending decision, and how to verify the data.",
     "代理A留下了指标不完整的部分报告。为代理B准备消息，包含已完成内容、缺失内容、待决策项和数据验证方法。"),
    ("T023", "multiagent_continuation", "new_EXP04",
     "Un agente de memoria debe transferir preferencias del usuario a un agente ejecutor: idioma español, Markdown limpio, resultados reales, no inventar datos y comparar tokens. Genera salida interna.",
     "A memory agent must transfer user preferences to an executor agent: Spanish language, clean Markdown, real results, no invented data, and token comparison. Generate an internal output.",
     "记忆代理必须把用户偏好传给执行代理：西班牙语、干净 Markdown、真实结果、不编造数据、比较 token。生成内部输出。"),
    ("T024", "multiagent_continuation", "new_EXP04",
     "Agente A detectó una anomalía: el output es corto, pero perdió la decisión principal. Entrega a Agente B un diagnóstico compacto con causa probable y corrección.",
     "Agent A detected an anomaly: the output is short, but lost the main decision. Give Agent B a compact diagnosis with probable cause and correction.",
     "代理A发现异常：输出很短，但丢失了主要决策。给代理B一个紧凑诊断，包含可能原因和修正。"),
    ("T025", "multiagent_continuation", "new_EXP04",
     "Un supervisor debe pasar a un trabajador la siguiente etapa: comparar compressed_state contra hybrid_min en tareas de memoria. Incluye criterio de éxito, límite y riesgo.",
     "A supervisor must pass the next stage to a worker: compare compressed_state against hybrid_min on memory tasks. Include success criterion, limit, and risk.",
     "监督者必须把下一阶段交给工作者：在记忆任务中比较 compressed_state 与 hybrid_min。包括成功标准、限制和风险。"),
    ("T026", "multiagent_continuation", "new_EXP04",
     "Agente A ejecutó 30 tareas y encontró cero errores HTTP pero varios fallos de formato. Prepara handoff para análisis de anomalías sin perder conteos ni hipótesis.",
     "Agent A ran 30 tasks and found zero HTTP errors but several format failures. Prepare a handoff for anomaly analysis without losing counts or hypotheses.",
     "代理A执行了30个任务，发现HTTP错误为零，但有多个格式失败。准备交接给异常分析，不能丢失计数和假设。"),
    ("T027", "multiagent_continuation", "new_EXP04",
     "Un agente debe decidir si continúa con un protocolo o vuelve a compressed. Genera mensaje interno con evidencia mínima, incertidumbre y decisión recomendada.",
     "An agent must decide whether to continue with a protocol or return to compressed. Generate an internal message with minimal evidence, uncertainty, and recommended decision.",
     "一个代理必须决定是继续使用协议还是回到 compressed。生成内部消息，包含最小证据、不确定性和建议决策。"),
    ("T028", "multiagent_continuation", "new_EXP04",
     "Agente A preparó salidas internas para traducción final por lote. Indica a Agente B cómo agruparlas, qué no debe inventar y qué métricas debe medir.",
     "Agent A prepared internal outputs for final batch decoding. Tell Agent B how to group them, what not to invent, and which metrics to measure.",
     "代理A准备了用于最终批量解码的内部输出。告诉代理B如何分组、不能编造什么、要测量哪些指标。"),
    ("T029", "multiagent_continuation", "new_EXP04",
     "Agente A encontró que el chino comprimido tiene output corto pero input alto por instrucciones. Genera handoff para investigar si el costo viene de prompt o respuesta.",
     "Agent A found that compressed Chinese has short output but high input due to instructions. Generate a handoff to investigate whether cost comes from prompt or response.",
     "代理A发现中文压缩输出短，但因指令导致 input 高。生成交接消息，调查成本来自 prompt 还是回答。"),
    ("T030", "multiagent_continuation", "new_EXP04",
     "Crea una política interna para que tres agentes decidan: usar natural para salida humana, compressed para tareas simples, compressed_state para continuidad y hybrid_state para handoff crítico.",
     "Create an internal policy for three agents to decide: use natural for human output, compressed for simple tasks, compressed_state for continuity, and hybrid_state for critical handoff.",
     "创建内部策略，让三个代理决定：natural 用于人类输出，compressed 用于简单任务，compressed_state 用于连续性，hybrid_state 用于关键交接。"),
]

METRICS = [
    "semantic_fidelity", "clarity", "completeness", "utility", "ambiguity", "information_loss",
    "state_preservation", "operational_continuity", "context_recoverability", "handoff_quality", "compactness",
]


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
    if not getattr(base, "API" + "_" + "KEY"):
        raise RuntimeError("Missing provider key in environment or ignored local wrapper.")


def ensure_dirs():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)


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
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def backup_if_exists(path):
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = path.with_suffix(path.suffix + f".bak_{stamp}")
        shutil.copy2(path, backup)
        path.unlink()
        return backup.name
    return None


def write_task_bank():
    if TASK_BANK_PATH.exists():
        backup_if_exists(TASK_BANK_PATH)
    for tid, group, source, es, en, zh in TASKS:
        append_jsonl(TASK_BANK_PATH, {
            "task_id": tid,
            "task_group": group,
            "task_es": es,
            "task_en": en,
            "task_zh": zh,
            "source": source,
            "notes": "aligned_for_EXP04_TRI",
        })


def task_payload(task, language):
    tid, group, source, es, en, zh = task
    text = {"ES": es, "EN": en, "ZH": zh}[language]
    return {"id": tid, "group": group, "text": text, "original_es": es, "source": source}


def mode_name(language, family):
    return f"{family}_{language.lower()}"


def max_tokens_for_family(family):
    if family == "natural":
        return MAX_TOKENS_NATURAL
    if family == "compressed":
        return MAX_TOKENS_COMPRESSED
    return MAX_TOKENS_STATE


def prompt_for(language, family, task):
    t = task["text"]
    if language == "ES":
        if family == "natural":
            return f"""Responde en español natural claro y completo.
Usa solo respuesta final. No muestres razonamiento paso a paso.
No optimices para ahorrar tokens. Resuelve bien la tarea.
Incluye problema, solución, riesgo y siguiente paso cuando aplique.

Tarea:
{t}"""
        if family == "compressed":
            return f"""Usa lenguaje natural comprimido en español.
Mínimo texto útil. Sin cortesía, sin relleno, sin explicación decorativa.
Frases cortas. Conserva objetivo, hechos clave, números, decisión, riesgo y siguiente paso cuando aplique.
No uses plantilla fija obligatoria. No uses campos si no hacen falta.
Debe permitir que otro agente continúe la tarea.
No uses la palabra caveman.

Tarea:
{t}"""
        if family == "compressed_state":
            return f"""Usa lenguaje natural comprimido en español con marcas mínimas de estado.
Añade solo 3-5 marcas si aportan continuidad: hecho:, estado:, riesgo:, falta:, sig:.
No uses campos vacíos. No uses más de 5 campos salvo necesidad clara.
No te conviertas en proto rígido ni plantilla pesada.
Debe conservar estado, riesgo y siguiente paso cuando aplique.

Tarea:
{t}"""
        if family == "hybrid_min":
            return f"""Usa hybrid_min en español.
Mezcla lenguaje comprimido + 2-4 marcadores. Output corto.
Marcadores sugeridos: r=resultado; s=estado; risk=riesgo; next=siguiente.
No uses plantilla pesada. No uses campos vacíos. Conserva estado mínimo y claridad operativa.

Tarea:
{t}"""
        return f"""Usa hybrid_state en español.
Más estructura que hybrid_min, menos que proto rígido. Máximo 6 campos salvo necesidad extrema.
Campos sugeridos: estado:, hechos:, falta:, riesgo:, decisión:, sig:.
No uses campos vacíos. Debe servir como handoff multiagente claro.

Tarea:
{t}"""
    if language == "EN":
        if family == "natural":
            return f"""Answer in clear, complete natural English.
Use final answer only. Do not show step-by-step reasoning.
Do not optimize for token saving. Solve the task well.
Include problem, solution, risk, and next step when applicable.

Task:
{t}"""
        if family == "compressed":
            return f"""Use compressed natural language in English.
Minimum useful text. No politeness, no filler, no decorative explanation.
Short phrases. Preserve goal, key facts, numbers, decision, risk, and next step when applicable.
No mandatory fixed template. Do not use fields if not needed.
Output must allow another agent to continue the task.

Task:
{t}"""
        if family == "compressed_state":
            return f"""Use compressed English with minimal state marks.
Add only 3-5 marks when they improve continuity: done:, state:, risk:, missing:, next:.
No empty fields. No more than 5 fields unless clearly needed.
Do not become rigid proto or a heavy template.
Preserve state, risk, and next step when applicable.

Task:
{t}"""
        if family == "hybrid_min":
            return f"""Use hybrid_min in English.
Mix compressed English + 2-4 markers. Keep output short.
Suggested markers: r=result; s=state; risk=risk; next=next step.
No heavy template. No empty fields. Preserve minimal state and operational clarity.

Task:
{t}"""
        return f"""Use hybrid_state in English.
More structure than hybrid_min, less than rigid proto. Max 6 fields unless strictly necessary.
Suggested fields: state:, known:, missing:, risk:, decision:, next:.
No empty fields. Must work as a clear multi-agent handoff.

Task:
{t}"""
    if family == "natural":
        return f"""使用清晰完整的简体中文自然语言回答。
只输出最终答案，不展示逐步推理。
不要为了省 token 而牺牲任务完成度。请充分解决任务。
如适用，包含问题、方案、风险和下一步。

任务：
{t}"""
    if family == "compressed":
        return f"""使用中文压缩表达。
最少有用文本。不要寒暄、不要礼貌语、不要修辞、不要长解释。
短句。保留目标、关键事实、数字、决定、风险和下一步（如适用）。
不要使用固定模板。没必要时不要用字段。
输出必须让另一个智能体能继续任务。

任务：
{t}"""
    if family == "compressed_state":
        return f"""使用中文压缩表达 + 最小状态标记。
只在有助于连续性时添加 3-5 个标记：已:、态:、风:、缺:、下:。
不要空字段。除非明确必要，不超过 5 个字段。
不要变成僵硬 proto 或重模板。保留状态、风险和下一步（如适用）。

任务：
{t}"""
    if family == "hybrid_min":
        return f"""使用中文 hybrid_min。
压缩中文 + 2-4 个标记。输出短。
建议标记：结=结果；态=状态；风=风险；下=下一步。
不要重模板。不要空字段。保留最小状态和操作清晰度。

任务：
{t}"""
    return f"""使用中文 hybrid_state。
比 hybrid_min 更有结构，但少于僵硬 proto。除非极端必要，最多 6 个字段。
建议字段：态:、知:、缺:、风:、决:、下:。
不要空字段。必须适合作为多智能体 handoff。

任务：
{t}"""


def evaluator_prompt(language, family, task, output):
    return f"""You are a technical evaluator for internal AI-agent communication.
Evaluate the generated output against the original task.
Language: {language}
Mode family: {family}

Metrics from 1 to 5:
- semantic_fidelity
- clarity
- completeness
- utility
- ambiguity (1 is best, 5 is worst)
- information_loss (1 is best, 5 is worst)
- state_preservation
- operational_continuity
- context_recoverability
- handoff_quality
- compactness

Rules:
- Do not reward long answers automatically.
- Do not punish compressed output if it preserves enough operational state.
- Do not reward structure if it does not improve continuity.
- Do not penalize compressed for not being full prose.
- Penalize loss of goal, risk, decision, or next step when needed.
- Penalize empty fields and heavy templates in compressed_state or hybrid_min.
- Reward outputs that let another agent continue without the original context.
- Evaluate fairly across Spanish, English, and Chinese.
- Do not assume Chinese visual compactness means fewer tokens.

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
  "state_preservation": 0,
  "operational_continuity": 0,
  "context_recoverability": 0,
  "handoff_quality": 0,
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


def normalize_eval(parsed):
    out = {}
    for metric in METRICS:
        try:
            out[metric] = int(parsed.get(metric))
        except Exception:
            out[metric] = None
    out["notes"] = str(parsed.get("notes", parsed.get("comentario", "")))[:500]
    return out


def evaluate(language, family, task, output):
    result = call_model(evaluator_prompt(language, family, task, output), MAX_TOKENS_EVALUATION, is_eval=True)
    if not result.get("ok"):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("output"), True, {
            "type": result.get("error_type"), "message": result.get("error"), "http_status": result.get("status_code")
        }, result.get("latency_ms")
    parsed, parse_error = base.safe_json_parse(result.get("output", ""))
    if parse_error or not isinstance(parsed, dict):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("output"), True, {
            "type": "INVALID_JSON_EVALUATION", "message": "Evaluator returned invalid JSON.", "http_status": result.get("status_code")
        }, result.get("latency_ms")
    return result.get("model_used", EVALUATOR_MODEL), normalize_eval(parsed), result.get("output"), False, None, result.get("latency_ms")


def contains_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def cjk_count(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def word_count(text):
    return len(re.findall(r"\b[\w'=-]+\b", text or "", flags=re.UNICODE))


def field_info(text):
    value = text or ""
    fields = []
    fields.extend(re.findall(r"\b([A-Za-z_]{1,16})\s*=", value))
    fields.extend(re.findall(r"(?m)^\s*([A-Za-z_áéíóúñÁÉÍÓÚÑ]{1,16})\s*[:：]", value))
    fields.extend(re.findall(
        r"\b(hecho|estado|riesgo|falta|sig|contexto|error|accion|acción|proxima|próxima|r|s|risk|next|done|state|missing|known|decision|result)\s*[:=]",
        value,
        flags=re.I,
    ))
    fields.extend(re.findall(r"([已态風风缺下结結知决決])\s*[=:：]", value))
    return len(set(fields)), sorted(set(fields))


def has_empty_field(text):
    return bool(re.search(r"[:=]\s*(?:$|;|\n)", text or "", re.I))


def validate_format(language, family, output):
    text = output or ""
    notes = []
    valid = True
    wc = word_count(text)
    cc = len(text)
    fields_count, fields = field_info(text)
    cjk = cjk_count(text)
    if language == "ES" and contains_cjk(text):
        valid = False; notes.append("wrong_language_cjk_in_es")
    if language == "EN" and contains_cjk(text):
        valid = False; notes.append("wrong_language_cjk_in_en")
    if language == "ZH" and cjk < 8:
        valid = False; notes.append("wrong_language_too_little_zh")
    if "caveman" in text.lower():
        valid = False; notes.append("uses_deprecated_caveman_term")
    if family == "natural":
        if fields_count >= 8:
            valid = False; notes.append("natural_too_field_dominant")
    elif family == "compressed":
        if fields_count >= 4:
            valid = False; notes.append("compressed_too_field_dominant")
        if language != "ZH" and wc > 115:
            valid = False; notes.append("compressed_too_long")
        if language == "ZH" and cc > 260:
            valid = False; notes.append("compressed_zh_too_long")
        if language == "ZH" and ("原始人" in text or "洞穴" in text):
            valid = False; notes.append("compressed_zh_caricature")
    elif family == "compressed_state":
        if has_empty_field(text):
            valid = False; notes.append("empty_field")
        if fields_count > 6:
            valid = False; notes.append("compressed_state_too_many_fields")
        if fields_count < 2:
            valid = False; notes.append("compressed_state_missing_marks")
        if language != "ZH" and wc > 125:
            valid = False; notes.append("compressed_state_too_long")
        if language == "ZH" and cc > 300:
            valid = False; notes.append("compressed_state_zh_too_long")
    elif family == "hybrid_min":
        if has_empty_field(text):
            valid = False; notes.append("empty_field")
        if fields_count < 2:
            valid = False; notes.append("hybrid_min_missing_markers")
        if fields_count > 5:
            valid = False; notes.append("hybrid_min_too_many_fields")
        if language != "ZH" and wc > 90:
            valid = False; notes.append("hybrid_min_too_long")
        if language == "ZH" and cc > 220:
            valid = False; notes.append("hybrid_min_zh_too_long")
    elif family == "hybrid_state":
        if has_empty_field(text):
            valid = False; notes.append("empty_field")
        if fields_count < 3:
            valid = False; notes.append("hybrid_state_missing_state_fields")
        if fields_count > 7:
            valid = False; notes.append("hybrid_state_too_many_fields")
        if language != "ZH" and wc > 135:
            valid = False; notes.append("hybrid_state_too_long")
        if language == "ZH" and cc > 320:
            valid = False; notes.append("hybrid_state_zh_too_long")
    return valid, notes, wc, cc, fields_count, fields


def run_one(language, family, task, run):
    mode = mode_name(language, family)
    prompt = STRICT_OUTPUT_PREFIX + "\n" + LENGTH_RULES[family] + "\n\n" + prompt_for(language, family, task)
    generated = call_model(prompt, max_tokens_for_family(family), is_eval=False)
    output = generated.get("output") if generated.get("ok") else ""
    if output:
        eval_model, evaluation, eval_raw, parse_error, eval_error, eval_latency = evaluate(language, family, task, output)
    else:
        eval_model, evaluation, eval_raw, parse_error, eval_error, eval_latency = EVALUATOR_MODEL, {}, None, False, {
            "type": "EMPTY_OUTPUT", "message": "No output to evaluate.", "http_status": generated.get("status_code")
        }, None
    valid, notes, wc, cc, field_count, fields = validate_format(language, family, output)
    error = None
    if not generated.get("ok"):
        error = {"type": generated.get("error_type"), "message": generated.get("error"), "http_status": generated.get("status_code")}
    if eval_error:
        error = eval_error
    return {
        "run_id": RUN_ID,
        "timestamp": utc_now(),
        "experiment_id": EXPERIMENT_ID,
        "language": language,
        "task_id": task["id"],
        "task_group": task["group"],
        "task_text": task["text"],
        "task_text_original_es": task["original_es"],
        "mode": mode,
        "base_family": family,
        "run": run,
        "generator_model": generated.get("model_used", GENERATION_MODEL),
        "evaluator_model": eval_model,
        "temperature": TEMPERATURE,
        "thinking_disabled": True,
        "input_tokens": generated.get("input_tokens"),
        "output_tokens": generated.get("output_tokens"),
        "total_tokens": generated.get("total_tokens"),
        "token_count_method": generated.get("token_count_method"),
        "output": output,
        "format_valid": valid,
        "format_notes": notes,
        "word_count": wc,
        "char_count": cc,
        "field_count": field_count,
        "fields_used": fields,
        "evaluation": evaluation,
        "evaluation_raw": eval_raw,
        "evaluation_parse_error": parse_error,
        "latency_ms_generation": generated.get("latency_ms"),
        "latency_ms_evaluation": eval_latency,
        "error": error,
        "http_status": generated.get("status_code"),
    }


def test_connection():
    models = base.list_models()
    result = {"timestamp": utc_now(), "models_ok": False, "chat_ok": False, "models_count": None, "error": None}
    if not models.get("ok"):
        result["error"] = {"type": models.get("error_type"), "message": models.get("error"), "http_status": models.get("status_code")}
        write_text(CONNECTION_PATH, json.dumps(result, ensure_ascii=False, indent=2))
        return result
    data = models.get("data") or {}
    model_list = data.get("data") if isinstance(data, dict) else None
    result["models_ok"] = True
    result["models_count"] = len(model_list) if isinstance(model_list, list) else None
    chat = call_model("Responde solo: OK_EXP04_TRI_TEST", 40, is_eval=False)
    result["chat_model"] = chat.get("model_used")
    result["chat_latency_ms"] = chat.get("latency_ms")
    result["chat_response"] = chat.get("output")
    result["chat_ok"] = bool(chat.get("ok"))
    result["usage"] = {"input_tokens": chat.get("input_tokens"), "output_tokens": chat.get("output_tokens"), "total_tokens": chat.get("total_tokens")}
    if not chat.get("ok"):
        result["error"] = {"type": chat.get("error_type"), "message": chat.get("error"), "http_status": chat.get("status_code")}
    write_text(CONNECTION_PATH, json.dumps(result, ensure_ascii=False, indent=2))
    return result


def soft_stop():
    return base.CALL_STATS["attempted"] >= SOFT_STOP_HTTP_CALLS


def run_block(out_path, task_ids, runs, progress=False):
    rows = []
    for task_raw in TASKS:
        if task_raw[0] not in task_ids:
            continue
        for language in LANGUAGES:
            task = task_payload(task_raw, language)
            for run in runs:
                for family in FAMILIES:
                    if soft_stop():
                        return rows, True
                    row = run_one(language, family, task, run)
                    append_jsonl(out_path, row)
                    rows.append(row)
                    if progress and len(rows) % 50 == 0:
                        print(f"progress rows={len(rows)} http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} lang={language} task={task['id']} mode={row['mode']}", flush=True)
    return rows, False


def run_pilot():
    if PILOT_PATH.exists():
        PILOT_PATH.unlink()
    rows, stopped = run_block(PILOT_PATH, PILOT_TASKS, [1], progress=False)
    checks = {
        "rows": len(rows),
        "expected_rows": 45,
        "errors": sum(1 for r in rows if r.get("error")),
        "parse_errors": sum(1 for r in rows if r.get("evaluation_parse_error")),
        "missing_tokens": sum(1 for r in rows if r.get("total_tokens") is None),
        "format_invalid": sum(1 for r in rows if r.get("format_valid") is False),
        "deprecated_term": sum(1 for r in rows if "uses_deprecated_caveman_term" in r.get("format_notes", [])),
        "stopped": stopped,
    }
    checks["ok"] = (
        checks["rows"] == 45
        and checks["errors"] == 0
        and checks["parse_errors"] == 0
        and checks["missing_tokens"] == 0
        and checks["format_invalid"] == 0
        and checks["deprecated_term"] == 0
    )
    return checks


def run_full():
    backup = backup_if_exists(RUNS_PATH)
    rows, stopped = run_block(RUNS_PATH, {t[0] for t in TASKS}, range(1, REPETITIONS + 1), progress=True)
    return read_jsonl(RUNS_PATH), stopped, backup


def mean(values):
    nums = [v for v in values if isinstance(v, (int, float))]
    return sum(nums) / len(nums) if nums else None


def fmt(value, digits=2):
    if value is None:
        return "NO_CALCULABLE"
    return f"{value:.{digits}f}" if isinstance(value, float) else str(value)


def pct(value):
    if value is None:
        return "NO_CALCULABLE"
    return f"{value * 100:.2f}%"


def summarize(rows, keys=("language", "base_family")):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = {}
    for key, items in grouped.items():
        data = {
            "rows": len(items),
            "errors": sum(1 for r in items if r.get("error")),
            "avg_input_tokens": mean([r.get("input_tokens") for r in items]),
            "avg_output_tokens": mean([r.get("output_tokens") for r in items]),
            "avg_total_tokens": mean([r.get("total_tokens") for r in items]),
            "latency_generation": mean([r.get("latency_ms_generation") for r in items]),
            "latency_evaluation": mean([r.get("latency_ms_evaluation") for r in items]),
            "format_invalid": sum(1 for r in items if r.get("format_valid") is False),
            "format_checked": sum(1 for r in items if r.get("format_valid") is not None),
        }
        for metric in METRICS:
            data[metric] = mean([r.get("evaluation", {}).get(metric) for r in items])
        out[key] = data
    return out


def quality_score(data):
    return mean([data.get("semantic_fidelity"), data.get("clarity"), data.get("utility")])


def balance_score(data):
    total = data.get("avg_total_tokens") or 999999
    return (
        1000 / total
        + (quality_score(data) or 0)
        + (data.get("state_preservation") or 0)
        + (data.get("operational_continuity") or 0)
        + (data.get("handoff_quality") or 0)
        + (data.get("compactness") or 0)
        - (data.get("ambiguity") or 0)
        - (data.get("information_loss") or 0)
    )


def best(summary, language, metric, reverse=True):
    vals = []
    for family in FAMILIES:
        data = summary.get((language, family))
        if not data:
            continue
        value = quality_score(data) if metric == "quality" else balance_score(data) if metric == "balance" else data.get(metric)
        if value is not None:
            vals.append((value, family))
    if not vals:
        return "NO_CALCULABLE"
    vals.sort(reverse=reverse)
    return vals[0][1]


def table_global(summary):
    lines = [
        "| language | mode | rows | errors | avg_input_tokens | avg_output_tokens | avg_total_tokens | fidelity | clarity | utility | ambiguity | info_loss | state_preservation | operational_continuity | context_recoverability | handoff_quality | compactness |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for language in LANGUAGES:
        for family in FAMILIES:
            d = summary.get((language, family), {})
            lines.append(f"| {language} | {family} | {d.get('rows', 0)} | {d.get('errors', 0)} | {fmt(d.get('avg_input_tokens'))} | {fmt(d.get('avg_output_tokens'))} | {fmt(d.get('avg_total_tokens'))} | {fmt(d.get('semantic_fidelity'))} | {fmt(d.get('clarity'))} | {fmt(d.get('utility'))} | {fmt(d.get('ambiguity'))} | {fmt(d.get('information_loss'))} | {fmt(d.get('state_preservation'))} | {fmt(d.get('operational_continuity'))} | {fmt(d.get('context_recoverability'))} | {fmt(d.get('handoff_quality'))} | {fmt(d.get('compactness'))} |")
    return "\n".join(lines)


def table_winners(summary):
    lines = [
        "| language | cheapest_mode | best_quality_mode | best_state_mode | best_continuity_mode | best_handoff_mode | best_balance_mode | reading |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for language in LANGUAGES:
        cheapest = best(summary, language, "avg_total_tokens", reverse=False)
        quality = best(summary, language, "quality")
        state = best(summary, language, "state_preservation")
        cont = best(summary, language, "operational_continuity")
        handoff = best(summary, language, "handoff_quality")
        balance = best(summary, language, "balance")
        reading = "compressed sigue dominando costo" if cheapest == "compressed" else f"{cheapest} gana costo"
        lines.append(f"| {language} | {cheapest} | {quality} | {state} | {cont} | {handoff} | {balance} | {reading} |")
    return "\n".join(lines)


def table_groups(rows):
    group_summary = summarize(rows, keys=("language", "task_group", "base_family"))
    lines = [
        "| language | task_group | cheapest_mode | best_state_mode | best_continuity_mode | best_balance_mode | observation |",
        "|---|---|---|---|---|---|---|",
    ]
    for language in LANGUAGES:
        for group in ["base_comparable", "memory_state", "multiagent_continuation"]:
            vals = {family: group_summary.get((language, group, family), {}) for family in FAMILIES}
            cheapest = min(vals, key=lambda f: vals[f].get("avg_total_tokens") if vals[f].get("avg_total_tokens") is not None else 10**9)
            state = max(vals, key=lambda f: vals[f].get("state_preservation") if vals[f].get("state_preservation") is not None else -1)
            cont = max(vals, key=lambda f: vals[f].get("operational_continuity") if vals[f].get("operational_continuity") is not None else -1)
            balance = max(vals, key=lambda f: balance_score(vals[f]) if vals[f] else -999)
            obs = "grupo_EXP04"
            lines.append(f"| {language} | {group} | {cheapest} | {state} | {cont} | {balance} | {obs} |")
    return "\n".join(lines)


def table_exp03_comparison(summary):
    lines = [
        "| language | exp03_compressed | exp04_compressed | exp03_hybrid | exp04_hybrid_min | exp04_compressed_state | token_change_hybrid | reading |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for language in LANGUAGES:
        c04 = summary.get((language, "compressed"), {}).get("avg_total_tokens")
        hm = summary.get((language, "hybrid_min"), {}).get("avg_total_tokens")
        cs = summary.get((language, "compressed_state"), {}).get("avg_total_tokens")
        ref = EXP03_REFERENCE[language]
        change = hm - ref["hybrid"] if hm is not None else None
        reading = "hybrid_min_baja_vs_EXP03" if change is not None and change < 0 else "hybrid_min_no_baja_vs_EXP03"
        lines.append(f"| {language} | {fmt(ref['compressed'])} | {fmt(c04)} | {fmt(ref['hybrid'])} | {fmt(hm)} | {fmt(cs)} | {fmt(change)} | {reading} |")
    return "\n".join(lines)


def table_success(summary):
    lines = [
        "| language | mode | tokens_vs_compressed | state_delta_vs_compressed | continuity_delta_vs_compressed | success_level | reading |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for language in LANGUAGES:
        comp = summary.get((language, "compressed"), {})
        comp_tokens = comp.get("avg_total_tokens")
        for family in FAMILIES:
            if family == "natural":
                continue
            d = summary.get((language, family), {})
            ratio = (d.get("avg_total_tokens") / comp_tokens - 1) if d.get("avg_total_tokens") is not None and comp_tokens else None
            state_delta = (d.get("state_preservation") - comp.get("state_preservation")) if d.get("state_preservation") is not None and comp.get("state_preservation") is not None else None
            cont_delta = (d.get("operational_continuity") - comp.get("operational_continuity")) if d.get("operational_continuity") is not None and comp.get("operational_continuity") is not None else None
            level = "strong" if ratio is not None and ratio <= 0.10 and ((state_delta or 0) >= 0.25 or (cont_delta or 0) >= 0.25) else "weak" if d.get("utility", 0) >= 4 and d.get("information_loss", 9) <= 2 else "fail"
            lines.append(f"| {language} | {family} | {pct(ratio)} | {fmt(state_delta)} | {fmt(cont_delta)} | {level} | criterio_EXP04 |")
    return "\n".join(lines)


def table_io(summary):
    lines = [
        "| language | mode | avg_input_tokens | avg_output_tokens | input_share | output_share | reading |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for language in LANGUAGES:
        for family in FAMILIES:
            d = summary.get((language, family), {})
            inp, out, total = d.get("avg_input_tokens"), d.get("avg_output_tokens"), d.get("avg_total_tokens")
            ins = inp / total if inp is not None and total else None
            outs = out / total if out is not None and total else None
            reading = "input_domina" if ins and ins > 0.55 else "output_domina" if outs and outs > 0.55 else "balanceado"
            lines.append(f"| {language} | {family} | {fmt(inp)} | {fmt(out)} | {pct(ins)} | {pct(outs)} | {reading} |")
    return "\n".join(lines)


def table_language(summary):
    lines = [
        "| language | natural | compressed | compressed_state | hybrid_min | hybrid_state | best_token | best_state | best_balance |",
        "|---|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for language in LANGUAGES:
        vals = [summary.get((language, f), {}).get("avg_total_tokens") for f in FAMILIES]
        lines.append(f"| {language} | {fmt(vals[0])} | {fmt(vals[1])} | {fmt(vals[2])} | {fmt(vals[3])} | {fmt(vals[4])} | {best(summary, language, 'avg_total_tokens', reverse=False)} | {best(summary, language, 'state_preservation')} | {best(summary, language, 'balance')} |")
    return "\n".join(lines)


def anomalies(rows):
    counts = Counter()
    examples = []
    for row in rows:
        if row.get("error"):
            err = row["error"]
            counts[f"error:{err.get('type') if isinstance(err, dict) else err}"] += 1
            if len(examples) < 15:
                examples.append(f"- {row['language']} {row['task_id']} {row['mode']}: error={err}")
        if row.get("evaluation_parse_error"):
            counts["parse_error"] += 1
        if row.get("total_tokens") is None:
            counts["missing_tokens"] += 1
        if row.get("format_valid") is False:
            for note in row.get("format_notes", []):
                counts[f"format:{note}"] += 1
            if len(examples) < 15:
                examples.append(f"- {row['language']} {row['task_id']} {row['mode']}: notes={row.get('format_notes')}")
    return counts, examples


def anomaly_markdown(counts, examples):
    if not counts:
        return "- No se registraron anomalías."
    lines = [f"- {k}: {v}" for k, v in counts.most_common()]
    if examples:
        lines.append("\n### Ejemplos")
        lines.extend(examples)
    return "\n".join(lines)


def batch_decode_prompt(language, family, selected):
    joined = "\n".join(f"{i+1}. [{r['task_id']}] {r['output']}" for i, r in enumerate(selected))
    if language == "ES":
        return f"""Decodifica por lote estas salidas internas comprimidas a español natural claro.
No inventes información. Conserva objetivo, estado, riesgo y siguiente paso cuando existan.
Produce una lista breve numerada, una entrada por salida.

Entradas:
{joined}"""
    if language == "EN":
        return f"""Batch-decode these internal compressed outputs into clear natural English.
Do not invent information. Preserve goal, state, risk, and next step when present.
Produce a brief numbered list, one item per input.

Inputs:
{joined}"""
    return f"""把这些内部压缩输出批量解码成清晰自然中文。
不要编造信息。保留目标、状态、风险和下一步（如果存在）。
输出简短编号列表，每个输入对应一项。

输入：
{joined}"""


def batch_eval_prompt(language, family, source_text, decoded):
    return f"""Evaluate this batch final decode.
Language: {language}
Mode family: {family}

Score 1-5:
- fidelity
- clarity
- no_invention
- batch_usefulness
- compactness

Rules: 5 is best for all metrics. Return strict JSON only.

Source compressed outputs:
{source_text}

Decoded batch:
{decoded}

Return:
{{"fidelity":0,"clarity":0,"no_invention":0,"batch_usefulness":0,"compactness":0,"notes":""}}"""


def run_batch_decode(rows):
    if base.CALL_STATS["attempted"] + 30 >= SOFT_STOP_HTTP_CALLS:
        write_text(BATCH_REPORT_PATH, "# EXP04B Batch Final Decode\n\nPENDIENTE: omitido por margen insuficiente de llamadas.\n")
        return False
    if BATCH_PATH.exists():
        backup_if_exists(BATCH_PATH)
    target_families = ["compressed_state", "hybrid_min", "hybrid_state"]
    for language in LANGUAGES:
        for family in target_families:
            selected = [r for r in rows if r["language"] == language and r["base_family"] == family and not r.get("error")][:10]
            if len(selected) < 10:
                continue
            prompt = batch_decode_prompt(language, family, selected)
            decode = call_model(prompt, MAX_TOKENS_BATCH_DECODE, is_eval=False)
            source_text = "\n".join(f"{r['task_id']}: {r['output']}" for r in selected)
            eval_result = call_model(batch_eval_prompt(language, family, source_text, decode.get("output", "")), MAX_TOKENS_EVALUATION, is_eval=True)
            parsed, parse_error = base.safe_json_parse(eval_result.get("output", "")) if eval_result.get("ok") else ({}, True)
            append_jsonl(BATCH_PATH, {
                "experiment_id": "EXP04B_BATCH_FINAL_DECODE",
                "timestamp": utc_now(),
                "language": language,
                "base_family": family,
                "source_count": len(selected),
                "source_task_ids": [r["task_id"] for r in selected],
                "generator_model": decode.get("model_used", GENERATION_MODEL),
                "evaluator_model": eval_result.get("model_used", EVALUATOR_MODEL),
                "input_tokens": decode.get("input_tokens"),
                "output_tokens": decode.get("output_tokens"),
                "total_tokens": decode.get("total_tokens"),
                "decoded_output": decode.get("output", ""),
                "evaluation": parsed if isinstance(parsed, dict) else {},
                "evaluation_parse_error": parse_error,
                "error": None if decode.get("ok") and eval_result.get("ok") else {"decode": decode.get("error"), "eval": eval_result.get("error")},
            })
    batch_rows = read_jsonl(BATCH_PATH)
    write_text(BATCH_REPORT_PATH, batch_report(batch_rows))
    return True


def batch_report(batch_rows):
    lines = ["# Análisis EXP04B Batch Final Decode", "", f"- Filas batch: {len(batch_rows)}", ""]
    lines.append("| language | mode | source_count | total_tokens | fidelity | clarity | no_invention | usefulness | compactness |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in batch_rows:
        ev = row.get("evaluation", {})
        lines.append(f"| {row['language']} | {row['base_family']} | {row['source_count']} | {fmt(row.get('total_tokens'))} | {fmt(ev.get('fidelity'))} | {fmt(ev.get('clarity'))} | {fmt(ev.get('no_invention'))} | {fmt(ev.get('batch_usefulness'))} | {fmt(ev.get('compactness'))} |")
    lines.append("\nLectura: este módulo evalúa decodificación por lote, no traducción por salida individual.")
    return "\n".join(lines) + "\n"


def write_reports(rows, pilot, connection, stopped, backup, batch_executed):
    summary = summarize(rows)
    counts, examples = anomalies(rows)
    parse_errors = sum(1 for r in rows if r.get("evaluation_parse_error"))
    missing = sum(1 for r in rows if r.get("total_tokens") is None)
    format_fail = sum(1 for r in rows if r.get("format_valid") is False)
    content = f"""# Resultados EXP04_TRI

## Configuración

- Experimento: `{EXPERIMENT_ID}`
- Nombre corto: `{RUN_ID}`
- Modelo generador: `{GENERATION_MODEL}`
- Modelo evaluador: `{EVALUATOR_MODEL}`
- Thinking disabled: `true` para `deepseek-v4-*`
- Temperatura: {TEMPERATURE}
- Repeticiones: {REPETITIONS}
- Filas esperadas FULL: 1350
- Filas generadas FULL: {len(rows)}
- Llamadas HTTP: {base.CALL_STATS['attempted']}
- Errores HTTP contabilizados: {base.CALL_STATS['errors']}
- Parse errors: {parse_errors}
- Missing tokens: {missing}
- Fallos de formato: {format_fail}
- Soft stop: {stopped}
- Backup JSONL previo: {backup or 'no_aplica'}
- Batch final decode ejecutado: {batch_executed}

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

## Ganadores por idioma

{table_winners(summary)}

## Ganadores por grupo de tarea

{table_groups(rows)}

## Comparación con EXP03

{table_exp03_comparison(summary)}

## Criterio de éxito

{table_success(summary)}

## Input/output tokens

{table_io(summary)}

## Tabla por idioma

{table_language(summary)}

## Errores y anomalías

{anomaly_markdown(counts, examples)}
"""
    write_text(RESULTS_PATH, content)
    write_text(COMPARISON_PATH, "# Comparación EXP04 ES EN ZH\n\n" + table_language(summary) + "\n\n" + table_winners(summary) + "\n")
    write_text(MODE_ANALYSIS_PATH, "# Análisis Modos EXP04 TRI\n\n" + table_success(summary) + "\n\n" + table_io(summary) + "\n")
    write_text(CONTINUITY_PATH, "# Análisis Continuidad Operativa EXP04\n\n" + table_groups(rows) + "\n\n" + table_success(summary) + "\n")
    write_text(LANGUAGE_PATH, "# Análisis Por Idioma EXP04\n\n" + table_language(summary) + "\n")
    write_text(EXP03_COMP_PATH, "# Comparación EXP03 vs EXP04\n\n" + table_exp03_comparison(summary) + "\n")
    write_text(ERRORS_PATH, "# Errores y Anomalías EXP04 TRI\n\n" + f"- Filas: {len(rows)}\n- Errores: {sum(1 for r in rows if r.get('error'))}\n- Parse errors: {parse_errors}\n- Missing tokens: {missing}\n- Fallos de formato: {format_fail}\n\n" + anomaly_markdown(counts, examples) + "\n")
    write_text(SUMMARY_PATH, summary_doc(summary, rows, pilot, batch_executed))
    write_text(STDOUT_LOG_NOTE, f"# Log EXP04_TRI\n\n- Generado: {utc_now()}\n- Filas: {len(rows)}\n- Llamadas HTTP: {base.CALL_STATS['attempted']}\n- Errores HTTP: {base.CALL_STATS['errors']}\n- Batch final decode: {batch_executed}\n")


def summary_doc(summary, rows, pilot, batch_executed):
    lines = [
        "# Resumen Ejecutivo EXP04_TRI",
        "",
        "## Estado",
        "",
        f"- Piloto OK: {pilot.get('ok')}",
        f"- FULL ejecutado: {'sí' if len(rows) == 1350 else 'parcial'}",
        f"- Batch final decode ejecutado: {batch_executed}",
        f"- Filas generadas: {len(rows)}",
        f"- Llamadas HTTP: {base.CALL_STATS['attempted']}",
        f"- Errores HTTP: {base.CALL_STATS['errors']}",
        "",
        "## Ganadores",
        "",
        table_winners(summary),
        "",
        "## Lectura principal",
        "",
    ]
    for language in LANGUAGES:
        comp = summary.get((language, "compressed"), {})
        cs = summary.get((language, "compressed_state"), {})
        hm = summary.get((language, "hybrid_min"), {})
        hs = summary.get((language, "hybrid_state"), {})
        lines.append(f"- {language}: compressed={fmt(comp.get('avg_total_tokens'))}; compressed_state={fmt(cs.get('avg_total_tokens'))}; hybrid_min={fmt(hm.get('avg_total_tokens'))}; hybrid_state={fmt(hs.get('avg_total_tokens'))}.")
    lines.extend([
        "",
        "## Recomendación siguiente",
        "",
        recommendation(summary),
        "",
        "Datos antes que entusiasmo.",
    ])
    return "\n".join(lines) + "\n"


def recommendation(summary):
    strong = []
    for language in LANGUAGES:
        comp = summary.get((language, "compressed"), {})
        cs = summary.get((language, "compressed_state"), {})
        hm = summary.get((language, "hybrid_min"), {})
        hs = summary.get((language, "hybrid_state"), {})
        comp_tokens = comp.get("avg_total_tokens")
        for family, data in [("compressed_state", cs), ("hybrid_min", hm), ("hybrid_state", hs)]:
            if comp_tokens and data.get("avg_total_tokens"):
                ratio = data["avg_total_tokens"] / comp_tokens - 1
                state_delta = (data.get("state_preservation") or 0) - (comp.get("state_preservation") or 0)
                cont_delta = (data.get("operational_continuity") or 0) - (comp.get("operational_continuity") or 0)
                hand_delta = (data.get("handoff_quality") or 0) - (comp.get("handoff_quality") or 0)
                if ratio <= 0.10 and max(state_delta, cont_delta, hand_delta) >= 0.25:
                    strong.append(f"{language}:{family}")
    if any("compressed_state" in x for x in strong):
        return "Adoptar compressed_state como protocolo interno mínimo."
    if any("hybrid_min" in x for x in strong):
        return "Adoptar hybrid_min como protocolo interno mínimo."
    if any("hybrid_state" in x for x in strong):
        return "Usar compressed para tareas simples y hybrid_state para handoff/memoria."
    return "Usar compressed para tareas simples y revisar diseño porque ningún modo supera claramente compressed."


def run_secret_scan():
    paths = [TASK_BANK_PATH, RUNS_PATH, PILOT_PATH, BATCH_PATH, RESULTS_PATH, COMPARISON_PATH, MODE_ANALYSIS_PATH, CONTINUITY_PATH, LANGUAGE_PATH, EXP03_COMP_PATH, ERRORS_PATH, SUMMARY_PATH, BATCH_REPORT_PATH, CONNECTION_PATH]
    secret_pattern = re.compile(r"s" + "k" + r"-[A-Za-z0-9]{16,}")
    hits = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if secret_pattern.search(text):
            hits.append(f"{path.name}:secret")
        for literal in ["Author" + "ization", "Bear" + "er", "api" + "_key", "API" + "_KEY", "token="]:
            if literal in text:
                hits.append(f"{path.name}:{literal}")
    return hits


def main():
    ensure_dirs()
    configure_base()
    require_key()
    write_task_bank()
    connection = test_connection()
    if not connection.get("models_ok") or not connection.get("chat_ok"):
        write_text(ERRORS_PATH, "# Error conexión EXP04_TRI\n\nNo se ejecutó piloto.\n")
        print("connection_failed")
        return 1
    pilot = run_pilot()
    print(f"pilot rows={pilot['rows']} ok={pilot['ok']} errors={pilot['errors']} missing={pilot['missing_tokens']} format_invalid={pilot['format_invalid']}", flush=True)
    if not pilot["ok"]:
        write_text(ERRORS_PATH, "# Piloto fallido EXP04_TRI\n\n```json\n" + json.dumps(pilot, ensure_ascii=False, indent=2) + "\n```\n")
        return 1
    rows, stopped, backup = run_full()
    batch_executed = False
    if not stopped and len(rows) == 1350 and base.CALL_STATS["attempted"] + 30 < SOFT_STOP_HTTP_CALLS:
        batch_executed = run_batch_decode(rows)
    elif not BATCH_REPORT_PATH.exists():
        write_text(BATCH_REPORT_PATH, "# EXP04B Batch Final Decode\n\nPENDIENTE: omitido por margen insuficiente o FULL parcial.\n")
    rows = read_jsonl(RUNS_PATH)
    write_reports(rows, pilot, connection, stopped, backup, batch_executed)
    hits = run_secret_scan()
    if hits:
        write_text(ERRORS_PATH, "# Secret scan hit\n\n" + "\n".join(hits) + "\n")
        print("secret_scan_hit")
        return 1
    print(f"done rows={len(rows)} http={base.CALL_STATS['attempted']} errors={base.CALL_STATS['errors']} stopped={stopped} batch={batch_executed}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
