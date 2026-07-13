"""SIMBA - memoria asociativa (RAG) sobre Ollama local.

Este módulo implementa la intuición de Kharold: en vez de aplastar toda la
información en un modelo gigante, guardamos pedazos de texto como vectores y
los RECUPERAMOS por similitud. Eso es el "gusano que conecta nodos": cada
fragmento queda cerca de los fragmentos relacionados en el espacio vectorial.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from ollama import Client

EMBED_MODEL = "nomic-embed-text"
DEFAULT_CHAT_MODEL = "qwen2.5:1.5b"


@dataclass
class MemoryConfig:
    persist_dir: Path = Path(".simba/memory")
    collection: str = "simba_memory"
    embed_model: str = EMBED_MODEL
    chat_model: str = DEFAULT_CHAT_MODEL
    ollama_host: str = "http://localhost:11434"


class AssociativeMemory:
    """Memoria asociativa: ingiere fragmentos y recupera los similares."""

    def __init__(self, config: MemoryConfig | None = None) -> None:
        self.config = config or MemoryConfig()
        self.config.persist_dir.mkdir(parents=True, exist_ok=True)

        self._ollama = Client(host=self.config.ollama_host)
        self._ef = embedding_functions.OllamaEmbeddingFunction(
            url=f"{self.config.ollama_host}/api/embeddings",
            model_name=self.config.embed_model,
        )
        self._client = chromadb.PersistentClient(path=str(self.config.persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=self.config.collection,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )
        self._counter = self._collection.count()

    # ----- ingestión (el "gusano se expande") -----

    def ingest_text(self, text: str, chunk_size: int = 400, source: str = "manual") -> int:
        """Ingerir un documento: lo corta en trozos y los guarda como nodos."""
        chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        chunks = [c.strip() for c in chunks if c.strip()]
        if not chunks:
            return 0
        start = self._counter
        ids = [f"{source}-{start + i}" for i in range(len(chunks))]
        metas = [{"source": source, "index": start + i} for i in range(len(chunks))]
        self._collection.add(documents=chunks, ids=ids, metadatas=metas)
        self._counter += len(chunks)
        return len(chunks)

    def ingest_file(self, path: str | Path, chunk_size: int = 400) -> int:
        p = Path(path)
        return self.ingest_text(p.read_text(encoding="utf-8"), chunk_size, source=p.name)

    # ----- recuperación (el "gusano encuentra nodos vecinos") -----

    def retrieve(self, query: str, k: int = 4) -> list[str]:
        """Recupera los k fragmentos más relacionados con la consulta."""
        if self._collection.count() == 0:
            return []
        res = self._collection.query(query_texts=[query], n_results=k)
        return res["documents"][0] if res["documents"] else []

    # ----- respuesta (RAG) -----

    def ask(self, query: str, k: int = 4, system: str = "") -> str:
        """Recupera contexto y le pide al modelo local que responda con él."""
        context = self.retrieve(query, k)
        if not context:
            prompt = (
                "No tengo memoria cargada todavía. Responde con tu conocimiento "
                f"general.\n\nPregunta: {query}"
            )
        else:
            joined = "\n---\n".join(context)
            prompt = (
                "Responde usando SOLO el contexto siguiente. Si el contexto no "
                "alcanza, decilo claramente.\n\n"
                f"CONTEXTO:\n{joined}\n\nPREGUNTA: {query}"
            )
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self._ollama.chat(model=self.config.chat_model, messages=messages)
        return resp["message"]["content"]

    def size(self) -> int:
        return self._collection.count()
