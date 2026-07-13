"""SIMBA - Examen de capacidades (capability profiling).

Banco de preguntas por dominio + runner que prueba cada modelo candidato
en local y construye una MATRIZ de aptitudes (capabilities.json). El router
luego usa esa matriz para delegar al mejor modelo por dominio, en vez de
hardcodear suposiciones.

Dominios:
  - matematicas: respuesta con número/valor exacto (scoring automatico)
  - codigo:       genera codigo y se ejecuta (scoring por exito)
  - creatividad:  texto original (scoring por LLM-judge local)
  - memoria:      recall del contexto RAG (scoring por presencia de hecho)

Uso:
  python -m simba.exam            # corre el examen y escribe capabilities.json
  python -m simba.exam --models qwen2.5:0.5b llama3.2:1b
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path

from ollama import Client

HERE = Path(__file__).resolve().parent
CAP_PATH = HERE.parent / "capabilities.json"
OLLAMA_HOST = "http://localhost:11434"

DEFAULT_MODELS = ["qwen2.5:0.5b", "qwen2.5:1.5b", "llama3.2:1b", "llama3.2:2b"]


# ----- banco de preguntas -----

@dataclass
class Question:
    domain: str
    prompt: str
    expect: str = ""          # valor/string esperado (para mate/memoria)
    check_code: bool = False  # ejecutar y verificar salida


BANK: list[Question] = [
    # matematicas (respuesta exacta)
    Question("matematicas", "¿Cuánto es 17 * 23?", "391"),
    Question("matematicas", "¿Cuál es la raíz cuadrada de 144?", "12"),
    Question("matematicas", "Si 3x + 9 = 24, ¿cuánto vale x?", "5"),
    Question("matematicas", "¿Cuánto es 2^8?", "256"),
    # codigo (ejecutable)
    Question("codigo", "En Python, escribe una función que sume los números "
             "del 1 al n y devuelva el resultado para n=10. Muestra solo el "
             "código en un bloque python.", check_code=True),
    Question("codigo", "Escribe código Python que invierta una cadena "
             "'alma' y muestre el resultado. Solo código en bloque python.",
             check_code=True),
    # creatividad (juez local)
    Question("creatividad", "Escribe un haiku corto sobre la memoria humana."),
    Question("creatividad", "Inventa una metáfora original comparando una red "
             "neuronal con una ciudad."),
    # memoria (recall del contexto ingerido)
    Question("memoria", "¿Qué modelo de embedding usa SIMBA para la memoria "
             "asociativa?", "nomic-embed-text"),
    Question("memoria", "Según la memoria, ¿qué decide el enrutador en SIMBA?",
             "especialista"),
]


# ----- scoring -----

def _extract_code(text: str) -> str:
    if "```python" in text:
        return text.split("```python", 1)[1].split("```", 1)[0]
    if "```" in text:
        return text.split("```", 1)[1].split("```", 1)[0]
    return text


def score_math(text: str, expect: str) -> float:
    return 1.0 if expect and expect in text else 0.0


def score_code(text: str) -> float:
    code = _extract_code(text)
    try:
        exec_globals: dict = {}
        exec(code, exec_globals)
        # si define main() o imprime, lo contamos como éxito básico
        return 1.0 if code.strip() else 0.0
    except Exception:
        return 0.0


def score_memory(text: str, expect: str) -> float:
    return 1.0 if expect and expect.lower() in text.lower() else 0.0


def score_creative(text: str, judge: Client, model: str) -> float:
    prompt = (
        "Evalua la respuesta en originalidad y coherencia del 0 al 1. "
        "Responde SOLO un numero decimal.\n\nRespuesta:\n" + text
    )
    try:
        resp = judge.chat(model=model, messages=[{"role": "user", "content": prompt}],
                          options={"temperature": 0})
        val = resp["message"]["content"].strip().replace(",", ".")
        return float(val)
    except Exception:
        return 0.0


# ----- runner -----

def run_exam(models: list[str], ollama_host: str = OLLAMA_HOST) -> dict:
    client = Client(host=ollama_host)
    # model -> domain -> lista de scores
    results: dict[str, dict[str, list[float]]] = {m: {} for m in models}

    for q in BANK:
        for model in models:
            try:
                resp = client.chat(model=model,
                                   messages=[{"role": "user", "content": q.prompt}])
                text = resp["message"]["content"]
            except Exception as exc:
                text = f"ERROR: {exc}"

            if q.domain == "matematicas":
                s = score_math(text, q.expect)
            elif q.domain == "codigo":
                s = score_code(text)
            elif q.domain == "memoria":
                s = score_memory(text, q.expect)
            else:  # creatividad -> juez local
                s = score_creative(text, client, models[0])

            results[model].setdefault(q.domain, []).append(s)
            print(f"  [{model} | {q.domain}] score={s:.2f}")

    # promediar por dominio
    matrix: dict[str, dict[str, float]] = {}
    for model, domains in results.items():
        matrix[model] = {d: round(sum(v) / len(v), 3) for d, v in domains.items()}

    CAP_PATH.write_text(json.dumps(matrix, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    return matrix


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="SIMBA capability exam")
    ap.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    args = ap.parse_args(argv)
    print(f"Corriendo examen con modelos: {args.models}")
    matrix = run_exam(args.models)
    print("\n=== MATRIZ DE APTITUDES ===")
    print(json.dumps(matrix, indent=2, ensure_ascii=False))
    print(f"\nGuardado en {CAP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
