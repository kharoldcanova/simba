#!/usr/bin/env python3
"""SIMBA CLI - memoria asociativa local (Fase 1).

Uso:
  python -m simba.cli ingest <archivo.txt>   # cargar memoria
  python -m simba.cli ask "pregunta"         # recuperar + responder (RAG)
  python -m simba.cli retrieve "consulta"    # ver solo los nodos recuperados
  python -m simba.cli info                   # tamaño de la memoria
"""
from __future__ import annotations

import sys

from simba.memory import AssociativeMemory


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1

    mem = AssociativeMemory()

    cmd = argv[0]
    if cmd == "ingest":
        if len(argv) < 2:
            print("Uso: simba.cli ingest <archivo.txt>")
            return 1
        n = mem.ingest_file(argv[1])
        print(f"Memoria: +{n} nodos (total {mem.size()})")
        return 0

    if cmd == "retrieve":
        if len(argv) < 2:
            print("Uso: simba.cli retrieve \"consulta\"")
            return 1
        nodes = mem.retrieve(argv[1])
        for i, node in enumerate(nodes, 1):
            print(f"[{i}] {node[:200]}")
        return 0

    if cmd == "ask":
        if len(argv) < 2:
            print("Uso: simba.cli ask \"pregunta\"")
            return 1
        answer = mem.ask(" ".join(argv[1:]))
        print(answer)
        return 0

    if cmd == "info":
        print(f"Nodos en memoria: {mem.size()}")
        return 0

    print(f"Comando desconocido: {cmd}")
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
