import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


PROVIDER = os.getenv("AI_PROVIDER", "opencode").strip().lower()
AUTH_HEADER_MODE = "bearer"
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
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "90"))
RATE_LIMIT_SLEEP_SECONDS = 10
SERVER_ERROR_SLEEP_SECONDS = 10
MAX_TOKENS_GENERATION = 500
MAX_TOKENS_TRANSLATION = 350
MAX_TOKENS_EVALUATION = 300
EMPTY_RETRY_MAX_TOKENS_GENERATION = 1800
EMPTY_RETRY_MAX_TOKENS_TRANSLATION = 1200
EMPTY_RETRY_MAX_TOKENS_EVALUATION = 1000

API_KEY = os.getenv("OPENCODE_API_KEY")


def _vertex_access_token():
    token = os.getenv("VERTEX_ACCESS_TOKEN") or os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    if token:
        return token
    gcloud = shutil.which("gcloud") or shutil.which("gcloud.cmd")
    if not gcloud:
        local_gcloud = Path.home() / "AppData" / "Local" / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin" / "gcloud.cmd"
        if local_gcloud.exists():
            gcloud = str(local_gcloud)
    if not gcloud:
        return None
    try:
        result = subprocess.run(
            [gcloud, "auth", "print-access-token"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def configure_provider_from_env():
    global PROVIDER, AUTH_HEADER_MODE, BASE_URL, CHAT_COMPLETIONS_URL, MODELS_URL, API_KEY
    PROVIDER = os.getenv("AI_PROVIDER", PROVIDER).strip().lower()
    if PROVIDER in ("gemini", "google-ai", "google_ai"):
        AUTH_HEADER_MODE = "bearer"
        BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai").rstrip("/")
        API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or API_KEY
    elif PROVIDER in ("azure", "azure-openai", "azure_openai", "azure-ai", "azure_ai"):
        PROVIDER = "azure_openai"
        AUTH_HEADER_MODE = "api-key"
        BASE_URL = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        API_KEY = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_API_KEY") or API_KEY
    elif PROVIDER in ("vertex", "vertex-ai", "vertex_ai", "vortex"):
        PROVIDER = "vertex"
        AUTH_HEADER_MODE = "bearer"
        project = os.getenv("VERTEX_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("VERTEX_LOCATION", "global")
        endpoint = os.getenv("VERTEX_OPENAI_ENDPOINT")
        if endpoint:
            BASE_URL = endpoint.rstrip("/")
        elif project:
            host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
            BASE_URL = f"https://{host}/v1/projects/{project}/locations/{location}/endpoints/openapi"
        API_KEY = _vertex_access_token() or API_KEY
    elif PROVIDER in ("codex", "codex-cli", "codex_cli", "openai-codex", "openai_codex"):
        PROVIDER = "codex_cli"
        AUTH_HEADER_MODE = "none"
        BASE_URL = os.getenv("CODEX_CLI_BASE_URL", "codex_cli").rstrip("/")
        API_KEY = os.getenv("CODEX_CLI_API_KEY") or API_KEY
    else:
        PROVIDER = "opencode"
        AUTH_HEADER_MODE = "bearer"
        BASE_URL = os.getenv("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1").rstrip("/")
        API_KEY = os.getenv("OPENCODE_API_KEY") or API_KEY
    CHAT_COMPLETIONS_URL = f"{BASE_URL}/chat/completions"
    MODELS_URL = f"{BASE_URL}/models"


configure_provider_from_env()

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "06_Resultados"
CONNECTION_TEST_PATH = RESULTS_DIR / "test_opencode_go_connection.json"
RUNS_PATH = RESULTS_DIR / "experimento_01_runs.jsonl"
REPORT_PATH = RESULTS_DIR / "Experimento_01_Resultados.md"
CONNECTION_ERROR_PATH = RESULTS_DIR / "Error_Conexion_OpencodeGo.md"
EXPERIMENT_ERRORS_PATH = RESULTS_DIR / "Errores_Experimento_01.md"
OBSERVATIONS_PATH = RESULTS_DIR / "Observaciones_Iniciales.md"
CONCLUSIONS_PATH = RESULTS_DIR / "Conclusiones_Parciales.md"
GITIGNORE_PATH = PROJECT_DIR.parent.parent / ".gitignore"

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
Frases cortas.
Sin tono humano.
Sin adornos.
Solo datos útiles.

Formato:
PROBLEMA:
SOLUCION:
RIESGOS:
PASOS:

Tarea:
{task}""",
    "proto": """Usa protolenguaje simbólico.
Usa solo respuesta final. No muestres razonamiento paso a paso.
Maximo 120 palabras dentro de la estructura.
No uses lenguaje humano completo.
Usa etiquetas compactas.
Debe ser traducible.

Formato obligatorio:

@TASK[id]
GOAL{{...}}
CTX{{...}}
PROBLEM{{...}}
PLAN{{...}}
RISK{{...}}
CHK{{...}}
OUT{{...}}
NEXT{{...}}

Reglas:
- No adornos.
- No frases largas.
- No símbolos no definidos.
- Mantén entidades importantes.
- Mantén riesgos.
- Mantén acciones.
- Si algo es incierto usa CHK?.
- Usa español mínimo dentro de las llaves si hace falta.
- Prioriza compresión sin perder significado.

Tarea:
{task}""",
}

TRANSLATOR_PROMPT = """Traduce el siguiente protolenguaje a español claro.
Usa solo respuesta final. No muestres razonamiento paso a paso.
Maximo 120 palabras.

Reglas:
- No inventes información.
- Conserva objetivo, contexto, plan, riesgos y próximos pasos.
- Expande símbolos a frases humanas.
- Marca incertidumbre si aparece CHK?.
- Salida breve pero entendible.

Protolenguaje:
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


class ExperimentAbort(Exception):
    pass


CALL_STATS = {
    "attempted": 0,
    "successful": 0,
    "errors": 0,
    "rate_limit_retries": 0,
}


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def sanitize_error_text(text):
    if text is None:
        return None
    value = str(text)
    if API_KEY:
        value = value.replace(API_KEY, "[REDACTED_API_KEY]")
    if "<html" in value.lower() or "<!doctype html" in value.lower():
        lower = value.lower()
        if "502" in lower and "bad gateway" in lower:
            return "HTTP 502 Bad gateway returned by endpoint."
        if "cloudflare" in lower:
            return "Cloudflare HTML error page returned by endpoint."
        return "HTML error page returned by endpoint."
    return value[:2000]


def ensure_directories():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)


def ensure_gitignore():
    required_lines = [
        "*.env",
        ".env",
        "*api_key*",
        "run_experimento_01_opencode_go_local.py",
        "test_opencode_go_connection.json",
        "experimento_01_runs.jsonl",
    ]
    existing = []
    if GITIGNORE_PATH.exists():
        existing = GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
    merged = existing[:]
    for line in required_lines:
        if line not in merged:
            merged.append(line)
    GITIGNORE_PATH.write_text("\n".join(merged).rstrip() + "\n", encoding="utf-8")


def require_api_key():
    if not API_KEY:
        if PROVIDER == "codex_cli":
            return
        if PROVIDER == "gemini":
            raise ExperimentAbort("Falta GEMINI_API_KEY o GOOGLE_API_KEY. Define la variable de entorno antes de ejecutar.")
        if PROVIDER == "azure_openai":
            raise ExperimentAbort("Falta AZURE_OPENAI_API_KEY. Define la variable de entorno antes de ejecutar.")
        if PROVIDER == "vertex":
            raise ExperimentAbort("Falta token Vertex. Usa gcloud auth login, VERTEX_ACCESS_TOKEN o GOOGLE_OAUTH_ACCESS_TOKEN.")
        raise ExperimentAbort("Falta OPENCODE_API_KEY. Define la variable de entorno antes de ejecutar la version limpia.")


def headers():
    values = {"Content-Type": "application/json"}
    if AUTH_HEADER_MODE == "none":
        return values
    if AUTH_HEADER_MODE == "api-key":
        values["api-key"] = API_KEY
    else:
        values["Authorization"] = f"Bearer {API_KEY}"
    return values


def classify_error(status_code=None, text=None, exception=None):
    message = str(exception) if exception else str(text or "")
    low = message.lower()
    if status_code in (401, 403):
        return "AUTH_ERROR"
    if status_code == 404 or "model" in low and ("not found" in low or "does not exist" in low):
        return "MODEL_NOT_FOUND"
    if status_code == 429 or "rate limit" in low or "too many requests" in low:
        return "RATE_LIMIT"
    if isinstance(exception, requests.exceptions.Timeout):
        return "TIMEOUT"
    if isinstance(exception, requests.exceptions.RequestException):
        return "NETWORK_ERROR"
    if status_code and status_code >= 400:
        return "HTTP_ERROR"
    return "HTTP_ERROR"


def request_with_retry(method, url, *, json_payload=None):
    last_error = None
    for attempt in range(2):
        if CALL_STATS["attempted"] >= MAX_CALLS_INITIAL_RUN:
            return {
                "ok": False,
                "status_code": None,
                "error_type": "MAX_CALLS_REACHED",
                "error": f"MAX_CALLS_INITIAL_RUN reached: {MAX_CALLS_INITIAL_RUN}",
                "latency_ms": None,
            }
        CALL_STATS["attempted"] += 1
        started = time.perf_counter()
        try:
            response = requests.request(
                method,
                url,
                headers=headers(),
                json=json_payload,
                timeout=REQUEST_TIMEOUT,
            )
            latency_ms = int((time.perf_counter() - started) * 1000)
            if response.status_code == 429 and attempt == 0:
                CALL_STATS["rate_limit_retries"] += 1
                time.sleep(RATE_LIMIT_SLEEP_SECONDS)
                continue
            if response.status_code in (500, 502, 503, 504) and attempt == 0:
                time.sleep(SERVER_ERROR_SLEEP_SECONDS)
                continue
            if response.status_code >= 400:
                CALL_STATS["errors"] += 1
                return {
                    "ok": False,
                    "status_code": response.status_code,
                    "error_type": classify_error(response.status_code, response.text),
                    "error": sanitize_error_text(response.text),
                    "latency_ms": latency_ms,
                }
            CALL_STATS["successful"] += 1
            return {
                "ok": True,
                "status_code": response.status_code,
                "data": response.json(),
                "latency_ms": latency_ms,
            }
        except requests.exceptions.RequestException as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            last_error = {
                "ok": False,
                "status_code": None,
                "error_type": classify_error(exception=exc),
                "error": sanitize_error_text(str(exc)),
                "latency_ms": latency_ms,
            }
            if last_error["error_type"] == "RATE_LIMIT" and attempt == 0:
                CALL_STATS["rate_limit_retries"] += 1
                time.sleep(RATE_LIMIT_SLEEP_SECONDS)
                continue
            CALL_STATS["errors"] += 1
            return last_error
    CALL_STATS["errors"] += 1
    return last_error or {"ok": False, "error_type": "HTTP_ERROR", "error": "unknown error", "latency_ms": None}


def list_models():
    if PROVIDER == "codex_cli":
        return {"ok": True, "status_code": None, "data": {"data": []}, "latency_ms": None, "skipped": True}
    if os.getenv("SKIP_MODELS_LIST", "").strip().lower() in ("1", "true", "yes"):
        return {"ok": True, "status_code": None, "data": {"data": []}, "latency_ms": None, "skipped": True}
    return request_with_retry("GET", MODELS_URL)


def extract_output(data):
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("text"):
                parts.append(str(item["text"]))
        return "\n".join(parts).strip()
    return ""


def usage_from_data(data):
    usage = data.get("usage") or {}
    return {
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "token_count_method": None if usage else "missing_from_api",
    }


def _uses_max_completion_tokens(model):
    normalized = (model or "").strip().lower()
    if os.getenv("TOKEN_LIMIT_PARAM", "").strip().lower() == "max_completion_tokens":
        return True
    return PROVIDER == "azure_openai" and (
        normalized.startswith("gpt-")
        or normalized.startswith("o")
    )


def _supports_custom_temperature(model):
    normalized = (model or "").strip().lower()
    if os.getenv("OMIT_TEMPERATURE", "").strip().lower() in ("1", "true", "yes"):
        return False
    return not (
        PROVIDER == "azure_openai"
        and (normalized.startswith("gpt-") or normalized.startswith("o"))
    )


def _reasoning_effort_for_model(model):
    configured = os.getenv("REASONING_EFFORT", "").strip()
    if configured:
        return configured
    normalized = (model or "").strip().lower()
    if PROVIDER == "azure_openai" and normalized.startswith("gpt-5.4"):
        return "xhigh"
    return None


def _request_extra_from_env():
    raw = os.getenv("REQUEST_EXTRA_JSON", "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _codex_cli_args(model, prompt, max_tokens=None):
    raw_command = os.getenv("CODEX_CLI_COMMAND_JSON", "").strip()
    raw_args = os.getenv("CODEX_CLI_ARGS_JSON", "").strip()
    replacements = {
        "model": model or "",
        "prompt": prompt,
        "max_tokens": "" if max_tokens is None else str(max_tokens),
    }
    if raw_command:
        parsed = json.loads(raw_command)
        if not isinstance(parsed, list) or not parsed:
            raise ValueError("CODEX_CLI_COMMAND_JSON must be a non-empty JSON array.")
        return [str(item).format(**replacements) for item in parsed]
    command = os.getenv("CODEX_CLI_COMMAND", "codex")
    if raw_args:
        parsed_args = json.loads(raw_args)
        if not isinstance(parsed_args, list):
            raise ValueError("CODEX_CLI_ARGS_JSON must be a JSON array.")
        args = [str(item).format(**replacements) for item in parsed_args]
    else:
        args = ["exec", "--model", model, "{prompt}"]
        args = [str(item).format(**replacements) for item in args]
    return [command, *args]


def call_codex_cli(model, prompt, *, max_tokens=None):
    mock_output = os.getenv("CODEX_CLI_MOCK_OUTPUT")
    if mock_output is not None:
        return {
            "ok": True,
            "status_code": 0,
            "output": mock_output.strip(),
            "latency_ms": 0,
            "raw": {"provider": "codex_cli", "model": model, "mock": True},
            "input_tokens": None,
            "output_tokens": None,
            "total_tokens": None,
            "token_count_method": "missing_from_cli",
        }
    try:
        args = _codex_cli_args(model, prompt, max_tokens=max_tokens)
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        return {
            "ok": False,
            "status_code": None,
            "error_type": "CLI_CONFIG_ERROR",
            "error": sanitize_error_text(str(exc)),
            "latency_ms": None,
        }
    timeout = int(os.getenv("CODEX_CLI_TIMEOUT_SECONDS", "120"))
    use_stdin = os.getenv("CODEX_CLI_STDIN", "").strip().lower() in ("1", "true", "yes")
    started = time.perf_counter()
    try:
        result = subprocess.run(
            args,
            input=prompt if use_stdin else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "status_code": None,
            "error_type": "CLI_NOT_FOUND",
            "error": sanitize_error_text(str(exc)),
            "latency_ms": int((time.perf_counter() - started) * 1000),
        }
    except PermissionError as exc:
        return {
            "ok": False,
            "status_code": None,
            "error_type": "CLI_PERMISSION_ERROR",
            "error": sanitize_error_text(str(exc)),
            "latency_ms": int((time.perf_counter() - started) * 1000),
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "status_code": None,
            "error_type": "TIMEOUT",
            "error": f"CODEX_CLI_TIMEOUT_SECONDS reached: {timeout}",
            "latency_ms": int((time.perf_counter() - started) * 1000),
        }
    latency_ms = int((time.perf_counter() - started) * 1000)
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    if result.returncode != 0:
        return {
            "ok": False,
            "status_code": result.returncode,
            "error_type": "CLI_ERROR",
            "error": sanitize_error_text(stderr or stdout or f"exit code {result.returncode}"),
            "latency_ms": latency_ms,
        }
    if not stdout:
        return {
            "ok": False,
            "status_code": result.returncode,
            "error_type": "EMPTY_OUTPUT",
            "error": "EMPTY_OUTPUT",
            "latency_ms": latency_ms,
        }
    return {
        "ok": True,
        "status_code": result.returncode,
        "output": stdout,
        "latency_ms": latency_ms,
        "raw": {
            "provider": "codex_cli",
            "model": model,
            "command": args[:1],
            "stdin": use_stdin,
            "stderr": stderr[-500:] if stderr else "",
        },
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
        "token_count_method": "missing_from_cli",
    }


def call_chat_completion(model, prompt, *, temperature=TEMPERATURE, max_tokens=None):
    if PROVIDER == "codex_cli":
        return call_codex_cli(model, prompt, max_tokens=max_tokens)
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    if _supports_custom_temperature(model):
        payload["temperature"] = temperature
    if "deepseek-v4" in model:
        payload["thinking"] = {"type": "disabled"}
    if max_tokens:
        token_limit_param = "max_completion_tokens" if _uses_max_completion_tokens(model) else "max_tokens"
        payload[token_limit_param] = max_tokens
    reasoning_effort = _reasoning_effort_for_model(model)
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort
    payload.update(_request_extra_from_env())
    result = request_with_retry("POST", CHAT_COMPLETIONS_URL, json_payload=payload)
    if not result.get("ok"):
        return result
    data = result["data"]
    output = extract_output(data)
    token_data = usage_from_data(data)
    if not output:
        return {
            "ok": False,
            "status_code": result.get("status_code"),
            "error_type": "EMPTY_OUTPUT",
            "error": "EMPTY_OUTPUT",
            "latency_ms": result.get("latency_ms"),
            "data": data,
            "raw": data,
            **token_data,
        }
    return {
        "ok": True,
        "status_code": result.get("status_code"),
        "output": output,
        "latency_ms": result.get("latency_ms"),
        "raw": data,
        **token_data,
    }


def call_chat_with_model_fallback(
    primary_model,
    fallback_model,
    prompt,
    *,
    temperature=TEMPERATURE,
    max_tokens=None,
    fallback_on_any_error=False,
    empty_retry_max_tokens=None,
):
    result = call_chat_completion(primary_model, prompt, temperature=temperature, max_tokens=max_tokens)
    if (
        not result.get("ok")
        and result.get("error_type") == "EMPTY_OUTPUT"
        and empty_retry_max_tokens
        and empty_retry_max_tokens != max_tokens
    ):
        retry = call_chat_completion(primary_model, prompt, temperature=temperature, max_tokens=empty_retry_max_tokens)
        retry["model_used"] = primary_model
        retry["retried_after_empty_output"] = True
        retry["initial_empty_output"] = {
            "latency_ms": result.get("latency_ms"),
            "http_status": result.get("status_code"),
        }
        if retry.get("ok"):
            return retry
        result = retry
    if result.get("ok"):
        result["model_used"] = primary_model
        return result
    should_fallback = result.get("error_type") == "MODEL_NOT_FOUND" or fallback_on_any_error
    if should_fallback and fallback_model and fallback_model != primary_model:
        fallback = call_chat_completion(fallback_model, prompt, temperature=temperature, max_tokens=max_tokens)
        if (
            not fallback.get("ok")
            and fallback.get("error_type") == "EMPTY_OUTPUT"
            and empty_retry_max_tokens
            and empty_retry_max_tokens != max_tokens
        ):
            fallback_retry = call_chat_completion(
                fallback_model,
                prompt,
                temperature=temperature,
                max_tokens=empty_retry_max_tokens,
            )
            fallback_retry["retried_after_empty_output"] = True
            fallback_retry["initial_empty_output"] = {
                "latency_ms": fallback.get("latency_ms"),
                "http_status": fallback.get("status_code"),
            }
            fallback = fallback_retry
        fallback["model_used"] = fallback_model
        if not fallback.get("ok"):
            fallback["primary_error"] = {
                "error_type": result.get("error_type"),
                "error": result.get("error"),
                "status_code": result.get("status_code"),
            }
        return fallback
    result["model_used"] = primary_model
    return result


def safe_json_parse(text):
    try:
        return json.loads(text), False
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1]), False
            except json.JSONDecodeError:
                pass
    return None, True


def append_jsonl(path, record):
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_output(task, mode):
    prompt = MODE_PROMPTS[mode].format(task=task["text"])
    return call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        prompt,
        max_tokens=MAX_TOKENS_GENERATION,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_GENERATION,
    )


def translate_proto(proto_output):
    prompt = TRANSLATOR_PROMPT.format(proto_output=proto_output)
    return call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        prompt,
        max_tokens=MAX_TOKENS_TRANSLATION,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_TRANSLATION,
    )


def evaluate_output(task, mode, output):
    prompt = EVALUATOR_PROMPT.format(task=task["text"], mode=mode, output=output)
    result = call_chat_with_model_fallback(
        EVALUATOR_MODEL,
        EVALUATOR_MODEL_FALLBACK,
        prompt,
        max_tokens=MAX_TOKENS_EVALUATION,
        fallback_on_any_error=True,
        empty_retry_max_tokens=EMPTY_RETRY_MAX_TOKENS_EVALUATION,
    )
    if not result.get("ok"):
        return result.get("model_used", EVALUATOR_MODEL), {}, result.get("error"), None, False
    parsed, parse_error = safe_json_parse(result["output"])
    if parse_error:
        return result.get("model_used", EVALUATOR_MODEL), {}, "INVALID_JSON_EVALUATION", result["output"], True
    return result.get("model_used", EVALUATOR_MODEL), parsed, None, result["output"], False


def base_record(task, mode, run):
    return {
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
    if result.get("token_count_method"):
        record["token_count_method"] = result["token_count_method"]
    if result.get("retried_after_empty_output"):
        record["retried_after_empty_output"] = True


def run_generation_and_evaluation(task, mode, run, output_result=None):
    record = base_record(task, mode, run)
    result = output_result or generate_output(task, mode)
    fill_generation_fields(record, result)
    if not result.get("ok"):
        record["error"] = {
            "type": result.get("error_type"),
            "message": sanitize_error_text(result.get("error")),
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
        record["error"] = {"type": eval_error, "message": eval_error}
    append_jsonl(RUNS_PATH, record)
    return record


def test_connection():
    models_result = list_models()
    connection = {
        "timestamp": utc_now_iso(),
        "base_url": BASE_URL,
        "models_endpoint": MODELS_URL,
        "chat_completions_endpoint": CHAT_COMPLETIONS_URL,
        "models_ok": False,
        "chat_ok": False,
        "models_count": None,
        "simple_prompt": "Responde solo: OK_OPENCODE_GO_TEST",
        "simple_response": None,
        "error": None,
        "http_status": None,
    }
    if not models_result.get("ok"):
        connection["error"] = {
            "type": models_result.get("error_type"),
            "message": sanitize_error_text(models_result.get("error")),
        }
        connection["http_status"] = models_result.get("status_code")
        write_json(CONNECTION_TEST_PATH, connection)
        write_connection_error(connection)
        return False
    data = models_result.get("data") or {}
    models = data.get("data") if isinstance(data, dict) else None
    if isinstance(models, list):
        connection["models_count"] = len(models)
    connection["models_ok"] = True
    chat_result = call_chat_with_model_fallback(
        GENERATION_MODEL,
        GENERATION_MODEL_FALLBACK,
        "Responde solo: OK_OPENCODE_GO_TEST",
    )
    connection["chat_model"] = chat_result.get("model_used")
    connection["chat_latency_ms"] = chat_result.get("latency_ms")
    if not chat_result.get("ok"):
        connection["error"] = {
            "type": chat_result.get("error_type"),
            "message": sanitize_error_text(chat_result.get("error")),
        }
        connection["http_status"] = chat_result.get("status_code")
        write_json(CONNECTION_TEST_PATH, connection)
        write_connection_error(connection)
        return False
    connection["chat_ok"] = True
    connection["simple_response"] = chat_result["output"]
    connection["usage"] = {
        "input_tokens": chat_result.get("input_tokens"),
        "output_tokens": chat_result.get("output_tokens"),
        "total_tokens": chat_result.get("total_tokens"),
        "token_count_method": chat_result.get("token_count_method"),
    }
    write_json(CONNECTION_TEST_PATH, connection)
    return True


def write_connection_error(connection):
    content = f"""# Error Conexion Opencode Go

## Fecha

{connection.get("timestamp")}

## Endpoint usado

- Modelos: `{MODELS_URL}`
- Chat completions: `{CHAT_COMPLETIONS_URL}`

## Codigo HTTP

{connection.get("http_status") or "No disponible"}

## Mensaje de error resumido

{(connection.get("error") or {}).get("type")}: {(connection.get("error") or {}).get("message")}

## Posible causa

- API key invalida o endpoint rechazo autenticacion.
- Endpoint no disponible.
- Red local sin acceso.
- Nombre de modelo no disponible.

## Proximo paso

Verificar conectividad, API key temporal y modelos disponibles. No se ejecuto el experimento grande.
"""
    CONNECTION_ERROR_PATH.write_text(content, encoding="utf-8")


def run_pilot():
    task = TASKS[0]
    pilot = {
        "timestamp": utc_now_iso(),
        "task_id": task["id"],
        "ok": True,
        "checks": [],
    }
    proto_output = None
    for mode in ("natural", "caveman", "proto"):
        result = generate_output(task, mode)
        check = {
            "mode": mode,
            "generation_ok": bool(result.get("ok")),
            "model": result.get("model_used"),
            "latency_ms": result.get("latency_ms"),
            "http_status": result.get("status_code"),
            "evaluation_ok": False,
            "evaluator_model": None,
            "error": None,
        }
        if not result.get("ok"):
            check["error"] = {
                "type": result.get("error_type"),
                "message": sanitize_error_text(result.get("error")),
            }
            raw_data = result.get("data") or result.get("raw")
            if raw_data is not None:
                check["raw_preview"] = sanitize_error_text(json.dumps(raw_data, ensure_ascii=False)[:2000])
            pilot["ok"] = False
            pilot["checks"].append(check)
            continue
        if mode == "proto":
            proto_output = result["output"]
        evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(task, mode, result["output"])
        check["evaluator_model"] = evaluator_model
        check["evaluation_ok"] = not bool(eval_error or parse_error)
        check["evaluation_error"] = eval_error
        check["evaluation"] = evaluation
        if not check["evaluation_ok"]:
            pilot["ok"] = False
        pilot["checks"].append(check)
    if not proto_output:
        pilot["ok"] = False
        pilot["checks"].append(
            {
                "mode": "proto_translated",
                "generation_ok": False,
                "evaluation_ok": False,
                "error": {"type": "PILOT_NO_PROTO_OUTPUT", "message": "No proto output to translate."},
            }
        )
        return False, pilot
    translation = translate_proto(proto_output)
    check = {
        "mode": "proto_translated",
        "generation_ok": bool(translation.get("ok")),
        "model": translation.get("model_used"),
        "latency_ms": translation.get("latency_ms"),
        "http_status": translation.get("status_code"),
        "evaluation_ok": False,
        "evaluator_model": None,
        "error": None,
    }
    if not translation.get("ok"):
        check["error"] = {
            "type": translation.get("error_type"),
            "message": sanitize_error_text(translation.get("error")),
        }
        pilot["ok"] = False
        pilot["checks"].append(check)
        return False, pilot
    evaluator_model, evaluation, eval_error, _, parse_error = evaluate_output(
        task,
        "proto_translated",
        translation["output"],
    )
    check["evaluator_model"] = evaluator_model
    check["evaluation_ok"] = not bool(eval_error or parse_error)
    check["evaluation_error"] = eval_error
    check["evaluation"] = evaluation
    if not check["evaluation_ok"]:
        pilot["ok"] = False
    pilot["checks"].append(check)
    return pilot["ok"], pilot


def run_experiment():
    if RUNS_PATH.exists():
        backup = RUNS_PATH.with_suffix(f".jsonl.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        RUNS_PATH.replace(backup)
    rows = []
    estimated_calls = len(TASKS) * REPETITIONS * 3
    estimated_calls += len(TASKS) * REPETITIONS
    estimated_calls += len(TASKS) * REPETITIONS * 4
    if estimated_calls > MAX_CALLS_INITIAL_RUN:
        raise ExperimentAbort(f"Plan excede MAX_CALLS_INITIAL_RUN: {estimated_calls}")
    for task in TASKS:
        for run in range(1, REPETITIONS + 1):
            for mode in ("natural", "caveman", "proto"):
                record = run_generation_and_evaluation(task, mode, run)
                rows.append(record)
                if mode == "proto" and record.get("output"):
                    translation_result = translate_proto(record["output"])
                    translated_record = run_generation_and_evaluation(
                        task,
                        "proto_translated",
                        run,
                        output_result=translation_result,
                    )
                    rows.append(translated_record)
    return rows


def read_runs():
    if not RUNS_PATH.exists():
        return []
    rows = []
    for line in RUNS_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def mean(values):
    clean = [v for v in values if isinstance(v, (int, float))]
    if not clean:
        return None
    return sum(clean) / len(clean)


def percent(value):
    if value is None:
        return "NO_CALCULABLE"
    return f"{value:.2%}"


def fmt_number(value, decimals=2):
    if value is None:
        return "NO_CALCULABLE"
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def summarize_results(rows=None):
    rows = rows or read_runs()
    summary = {}
    natural_total = mean([r.get("total_tokens") for r in rows if r.get("mode") == "natural" and not r.get("error")])
    for mode in ("natural", "caveman", "proto", "proto_translated"):
        mode_rows = [r for r in rows if r.get("mode") == mode]
        ok_rows = [r for r in mode_rows if not r.get("error") or r.get("evaluation_parse_error")]
        eval_rows = [r for r in mode_rows if isinstance(r.get("evaluation"), dict) and r.get("evaluation")]
        total_tokens = mean([r.get("total_tokens") for r in ok_rows])
        ahorro = None
        if natural_total and total_tokens is not None:
            ahorro = 1 - (total_tokens / natural_total)
        summary[mode] = {
            "rows": len(mode_rows),
            "errors": len([r for r in mode_rows if r.get("error")]),
            "api_errors": len([r for r in mode_rows if r.get("error") and (r["error"] or {}).get("type") != "INVALID_JSON_EVALUATION"]),
            "avg_input_tokens": mean([r.get("input_tokens") for r in ok_rows]),
            "avg_output_tokens": mean([r.get("output_tokens") for r in ok_rows]),
            "avg_total_tokens": total_tokens,
            "ahorro_vs_natural": ahorro,
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


def mode_conclusion(mode, metrics):
    if metrics["avg_total_tokens"] is None:
        return "Tokens no calculables"
    if mode == "natural":
        return "Baseline claro"
    if mode == "caveman":
        return "Reduce forma; mantiene lectura directa"
    if mode == "proto":
        return "Compacto; requiere traduccion para usuario"
    if mode == "proto_translated":
        return "Mide costo de salida humana final"
    return ""


def build_results_table(summary):
    lines = [
        "| Modo | Tokens promedio | Ahorro vs natural | Fidelidad | Claridad | Completitud | Ambigüedad | Pérdida info | Utilidad | Conclusión |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for mode in ("natural", "caveman", "proto", "proto_translated"):
        metrics = summary[mode]
        lines.append(
            "| {mode} | {tokens} | {saving} | {fid} | {clar} | {comp} | {amb} | {loss} | {util} | {conclusion} |".format(
                mode=mode,
                tokens=fmt_number(metrics["avg_total_tokens"]),
                saving=percent(metrics["ahorro_vs_natural"]),
                fid=fmt_number(metrics["fidelidad_semantica"]),
                clar=fmt_number(metrics["claridad"]),
                comp=fmt_number(metrics["completitud"]),
                amb=fmt_number(metrics["ambiguedad"]),
                loss=fmt_number(metrics["perdida_informacion"]),
                util=fmt_number(metrics["utilidad"]),
                conclusion=mode_conclusion(mode, metrics),
            )
        )
    return "\n".join(lines)


def detect_patterns(summary):
    patterns = []
    valid = {m: s for m, s in summary.items() if s["avg_total_tokens"] is not None}
    if valid:
        cheapest = min(valid.items(), key=lambda item: item[1]["avg_total_tokens"])[0]
        patterns.append(f"- Menor consumo promedio observado: `{cheapest}`.")
    clarity_valid = {m: s for m, s in summary.items() if s["claridad"] is not None}
    if clarity_valid:
        clearest = max(clarity_valid.items(), key=lambda item: item[1]["claridad"])[0]
        patterns.append(f"- Mayor claridad promedio evaluada: `{clearest}`.")
    fidelity_valid = {m: s for m, s in summary.items() if s["fidelidad_semantica"] is not None}
    if fidelity_valid:
        faithful = max(fidelity_valid.items(), key=lambda item: item[1]["fidelidad_semantica"])[0]
        patterns.append(f"- Mayor fidelidad semantica promedio evaluada: `{faithful}`.")
    if not patterns:
        patterns.append("- No hay suficientes datos calculables para detectar patrones.")
    return "\n".join(patterns)


def error_summary(rows):
    errors = {}
    for row in rows:
        err = row.get("error")
        if err:
            err_type = err.get("type") if isinstance(err, dict) else str(err)
            errors[err_type] = errors.get(err_type, 0) + 1
    if not errors:
        return "- No se registraron errores por fila."
    return "\n".join([f"- {key}: {value}" for key, value in sorted(errors.items())])


def write_markdown_report(rows=None, pilot=None):
    rows = rows or read_runs()
    summary = summarize_results(rows)
    total_errors = len([r for r in rows if r.get("error")])
    successful_rows = len(rows) - total_errors
    connection = {}
    if CONNECTION_TEST_PATH.exists():
        connection = json.loads(CONNECTION_TEST_PATH.read_text(encoding="utf-8"))
    content = f"""# Experimento 01: Comparación de lenguaje natural, cavernícola y protolenguaje

## Objetivo

Comparar tres formas de comunicacion para agentes IA: lenguaje natural completo, lenguaje reducido tipo cavernicola y protolenguaje simbolico. La variante `proto_translated` mide el costo adicional de convertir el protolenguaje a espanol humano.

## Configuracion

- Endpoint usado: `{CHAT_COMPLETIONS_URL}`
- Endpoint de modelos: `{MODELS_URL}`
- Modelo generador principal: `{GENERATION_MODEL}`
- Modelo generador fallback: `{GENERATION_MODEL_FALLBACK}`
- Modelo evaluador principal: `{EVALUATOR_MODEL}`
- Modelo evaluador fallback: `{EVALUATOR_MODEL_FALLBACK}`
- DeepSeek V4 thinking: `disabled`
- Numero de tareas: {len(TASKS)}
- Repeticiones por modo: {REPETITIONS}
- Temperatura: {TEMPERATURE}
- Fecha de ejecucion: {utc_now_iso()}
- Filas de resultados: {len(rows)}
- Filas exitosas sin error registrado: {successful_rows}
- Filas con error registrado: {total_errors}
- Llamadas HTTP intentadas por script: {CALL_STATS["attempted"]}
- Llamadas HTTP exitosas por script: {CALL_STATS["successful"]}
- Llamadas HTTP con error por script: {CALL_STATS["errors"]}
- Reintentos por rate limit: {CALL_STATS["rate_limit_retries"]}
- Prueba de conexion: models_ok={connection.get("models_ok")}, chat_ok={connection.get("chat_ok")}
- Piloto: {json.dumps(pilot, ensure_ascii=False) if pilot else "No registrado"}

No se incluye API key.

## Metodologia

Se generaron respuestas para 10 tareas en tres modos: `natural`, `caveman` y `proto`, con 3 repeticiones por modo. Cada salida `proto` se tradujo adicionalmente a `proto_translated`. Luego se envio cada salida final al evaluador automatico, que devolvio puntajes JSON de 1 a 5. Los resultados se guardaron incrementalmente en `experimento_01_runs.jsonl`.

Para modelos `deepseek-v4-*` se envio `thinking: disabled`, porque con pensamiento activado y limites bajos la API podia consumir tokens en `reasoning_content` y devolver `content` vacio.

Si la API devolvio `usage`, se registraron `prompt_tokens`, `completion_tokens` y `total_tokens`. Si no hubo `usage`, los tokens quedaron como `null` y se marco `token_count_method: missing_from_api`.

## Tabla de resultados

{build_results_table(summary)}

## Observaciones

{detect_patterns(summary)}

## Errores detectados

{error_summary(rows)}

## Conclusion parcial

Esta tanda exploratoria indica patrones iniciales, no una demostracion definitiva. Los resultados deben interpretarse como primera evidencia controlada. Para sostener la hipotesis hacen falta mas tareas, mas dominios, mas modelos y revision humana de una muestra.

## Proximos pasos

- Aumentar tareas.
- Aumentar repeticiones.
- Probar otros modelos.
- Comparar con mas dominios.
- Medir tokens exactos si faltaron.
- Mejorar reglas del protolenguaje.
- Agregar evaluacion humana.
"""
    REPORT_PATH.write_text(content, encoding="utf-8")
    write_observations(summary, rows)
    write_conclusions(summary, rows)
    if total_errors:
        write_experiment_errors(rows)


def write_observations(summary, rows):
    content = f"""# Observaciones Iniciales

## Proposito

Registrar observaciones reales del Experimento 01.

## Estado

EJECUTADO.

## Datos base

- Fecha de actualizacion: {utc_now_iso()}
- Filas registradas: {len(rows)}
- Errores registrados: {len([r for r in rows if r.get("error")])}
- Ruta JSONL: `experimento_01_runs.jsonl`
- Ruta informe: `Experimento_01_Resultados.md`

## Observaciones reales

{detect_patterns(summary)}

## Nota

Estas observaciones dependen de una tanda pequena: 10 tareas, 3 repeticiones y modelos disponibles en OpenCode Go al momento de ejecucion.

## Proximos pasos

- Revisar manualmente una muestra de salidas.
- Escalar a mas tareas solo con autorizacion.
- Comparar contra evaluacion humana.
"""
    OBSERVATIONS_PATH.write_text(content, encoding="utf-8")


def write_conclusions(summary, rows):
    if not rows:
        body = "PENDIENTE_DE_MAS_DATOS"
    else:
        body = f"""Los resultados iniciales sugieren diferencias medibles entre modos, pero no son concluyentes todavia.

{detect_patterns(summary)}

PENDIENTE_DE_MAS_DATOS para afirmar si la hipotesis central se sostiene de forma robusta."""
    content = f"""# Conclusiones Parciales

## Proposito

Registrar conclusiones parciales basadas solo en datos reales.

## Estado

EJECUTADO_CON_DATOS_INICIALES.

## Conclusion parcial

{body}

## Limitaciones

- Tanda pequena.
- Evaluacion automatica, no humana.
- Dependencia de modelos y tokenizer de la API.
- Posible variacion por latencia, disponibilidad o formato de respuesta.

## Proximos pasos

- Ampliar muestra.
- Agregar evaluadores humanos.
- Probar mas modelos.
"""
    CONCLUSIONS_PATH.write_text(content, encoding="utf-8")


def write_experiment_errors(rows):
    content = f"""# Errores Experimento 01

## Fecha

{utc_now_iso()}

## Resumen

{error_summary(rows)}

## Regla de seguridad

No se registra API key en este archivo.

## Proximos pasos

- Revisar filas con `error` en `experimento_01_runs.jsonl`.
- Repetir solo las filas fallidas si corresponde.
"""
    EXPERIMENT_ERRORS_PATH.write_text(content, encoding="utf-8")


def main():
    ensure_directories()
    ensure_gitignore()
    require_api_key()
    ok = test_connection()
    if not ok:
        print("Conexion fallo. Ver Error_Conexion_OpencodeGo.md")
        return 1
    pilot_ok, pilot = run_pilot()
    if not pilot_ok:
        connection = json.loads(CONNECTION_TEST_PATH.read_text(encoding="utf-8"))
        connection["pilot"] = pilot
        write_json(CONNECTION_TEST_PATH, connection)
        write_connection_error(
            {
                "timestamp": utc_now_iso(),
                "http_status": None,
                "error": {"type": "PILOT_FAILED", "message": sanitize_error_text(pilot.get("error"))},
            }
        )
        print("Piloto fallo. Ver Error_Conexion_OpencodeGo.md")
        return 1
    connection = json.loads(CONNECTION_TEST_PATH.read_text(encoding="utf-8"))
    connection["pilot"] = pilot
    write_json(CONNECTION_TEST_PATH, connection)
    rows = run_experiment()
    write_markdown_report(rows, pilot=pilot)
    print(f"Experimento terminado. Filas={len(rows)} llamadas_http={CALL_STATS['attempted']} errores_http={CALL_STATS['errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
