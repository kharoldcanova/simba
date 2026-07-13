"""SIMBA Fase 2 - Router por score (elige al mejor modelo por dominio).

Lee la MATRIZ de aptitudes (capabilities.json) generada por el examen y, para
cada consulta:
  1. Clasifica la intención (dominio) con reglas duras priorizadas.
  2. Elige el modelo de MAYOR score en ese dominio según la matriz.
  3. Si la consulta es sobre SIMBA y la memoria RAG recupera el hecho,
     usa el especialista memoria (prohibido inventar).
  4. Cascada al modelo general si el especialista dice no saber.

Correcciones tras pruebas (ver notes/imprevisto-fase2-router.md):
- Prioridad codigo > matematicas en la clasificacion (palabras clave tecnicas).
- MEMORY_KW solo términos de SIMBA, no "memoria" suelto (evita desvío).
- El especialista de memoria y el general son cautelosos: si no hay contexto
  real, dicen 'No tengo eso', NUNCA inventan sobre SIMBA.
"""
from __future__ import annotations

import json
from pathlib import Path

from ollama import Client

from simba.memory import AssociativeMemory

HERE = Path(__file__).resolve().parent
CAP_PATH = HERE.parent / "capabilities.json"
OLLAMA_HOST = "http://localhost:11434"

CATEGORIES = ["matematicas", "codigo", "creatividad", "memoria", "general"]

SYSTEMS: dict[str, str] = {
    "matematicas": "Sos un experto en matematicas. Responde paso a paso, "
                   "preciso y sin inventar. Si no podes, decilo.",
    "codigo": "Sos un programador experto. Responde con codigo correcto y "
              "conciso. Si no podes, decilo.",
    "creatividad": "Sos un asistente creativo. Usa lenguaje vivo, metafors y "
                   "ideas originales. No hables de SIMBA salvo que te pregunten.",
    "memoria": "Responde usando SOLO el contexto recuperado de la memoria. Si "
               "la memoria esta vacia o no contiene la respuesta, deci "
               "exactamente 'No tengo eso en mi memoria' y NO inventes nada.",
    "general": "Responde de forma util y concisa. Si te preguntan sobre SIMBA "
               "pero no sabes el dato, deci 'No tengo esa informacion de SIMBA' "
               "y no inventes.",
}

# SOLO términos propios de SIMBA (no "memoria" suelto, que es ambiguo)
MEMORY_KW = ["simba", "enrutador", "cerebro modular", "mixtral", "mamba",
             "rag", "memoria asociativa"]


class Router:
    def __init__(self, ollama_host: str = OLLAMA_HOST) -> None:
        self._ollama = Client(host=ollama_host)
        self._memory = AssociativeMemory()
        self.matrix = self._load_matrix()

    def _load_matrix(self) -> dict:
        if CAP_PATH.exists():
            return json.loads(CAP_PATH.read_text(encoding="utf-8"))
        return {}

    # ----- clasificación de intención (reglas priorizadas) -----

    def classify(self, query: str) -> str:
        q = query.lower()
        # 1) SIMBA -> memoria
        if any(k in q for k in MEMORY_KW):
            return "memoria"
        # 2) codigo tiene prioridad sobre matematicas
        if any(k in q for k in ["python", "codigo", "código", "funcion",
                                "función", "def ", "script", "bug", "programa",
                                "clase", "variable"]):
            return "codigo"
        # 3) matematicas
        if any(k in q for k in ["matematica", "matemática", "integral",
                                "derivada", "ecuacion", "ecuación", "calculo",
                                "cálculo", "algebra", "geometria", "geometría",
                                "raiz", "raíz", "x^", "x al"]):
            return "matematicas"
        # 4) creatividad
        if any(k in q for k in ["poema", "cuento", "crea", "inventa",
                                "metafora", "metáfora", "historia", "idea",
                                "cancion", "canción", "cuento"]):
            return "creatividad"
        # 5) LLM como último recurso
        cat = self._llm_classify(query)
        if cat in CATEGORIES:
            return cat
        return "general"

    def _llm_classify(self, query: str) -> str:
        try:
            resp = self._ollama.chat(
                model="qwen2.5:0.5b",
                messages=[{"role": "user", "content":
                    "Clasifica en UNA palabra (matematicas, codigo, "
                    "creatividad, memoria, general). Consulta: " + query +
                    "\nCategoria:"}],
                options={"temperature": 0},
            )
            return resp["message"]["content"].strip().lower().split()[0].strip(".:,")
        except Exception:
            return ""

    # ----- elección por score -----

    def best_model(self, domain: str) -> str | None:
        if not self.matrix:
            return None
        best, best_score = None, -1.0
        for model, scores in self.matrix.items():
            s = scores.get(domain, 0.0)
            if s > best_score:
                best, best_score = model, s
        return best

    # ----- enrutado -----

    def route(self, query: str) -> dict:
        domain = self.classify(query)

        used = domain
        # prioridad memoria si recupera nodos que contienen la respuesta
        if domain != "memoria":
            nodes = self._memory.retrieve(query, k=1)
            if nodes and self._relevant(query, nodes[0]):
                used = "memoria"

        model = self.best_model(used) or "qwen2.5:0.5b"
        answer = self._call(used, query, model)
        delegated = (model != self.best_model(domain))

        if self._unknown(answer):
            fb = self.best_model("general") or "qwen2.5:0.5b"
            answer = self._call("general", query, fb)
            used = "general"
            delegated = True

        return {"domain": domain, "used": used, "model": model,
                "delegated": delegated, "answer": answer}

    def _call(self, domain: str, query: str, model: str) -> str:
        if domain == "memoria":
            return self._memory.ask(query, system=SYSTEMS["memoria"])
        return self._ollama.chat(
            model=model,
            messages=[{"role": "system", "content": SYSTEMS[domain]},
                      {"role": "user", "content": query}],
        )["message"]["content"]

    @staticmethod
    def _relevant(query: str, node: str) -> bool:
        stop = {"el", "la", "los", "las", "un", "una", "de", "del", "y", "a",
                "en", "que", "se", "por", "con", "su", "es", "sobre", "humana"}
        qw = {w for w in query.lower().split() if w not in stop and len(w) > 3}
        nw = set(node.lower().split())
        return bool(qw) and len(qw & nw) / len(qw) >= 0.25

    @staticmethod
    def _unknown(text: str) -> bool:
        t = text.lower()
        return any(s in t for s in ["no se", "no puedo", "no tengo",
                                    "no dispongo", "lo siento", "no estoy",
                                    "no alcanza", "no hay contexto",
                                    "no tengo eso", "no tengo esa"])
