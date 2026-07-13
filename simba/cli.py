#!/usr/bin/env python3
"""SIMBA CLI - memoria asociativa + router de especialistas.

Uso:
  python -m simba.cli ingest <archivo.txt>   # cargar memoria (Fase 1)
  python -m simba.cli ask "pregunta"         # RAG con modelo local (Fase 1)
  python -m simba.cli route "pregunta"       # cerebro de especialistas (Fase 2)
  python -m simba.cli classify "pregunta"    # solo ver a qué categoría va
  python -m simba.cli retrieve "consulta"    # ver nodos recuperados
  python -m simba.cli info                   # tamaño de la memoria
"""
from __future__ import annotations

import sys

from simba.memory import AssociativeMemory
from simba.router import Router


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1

    cmd = argv[0]

    if cmd == "ingest":
        if len(argv) < 2:
            print("Uso: simba.cli ingest <archivo.txt>")
            return 1
        mem = AssociativeMemory()
        n = mem.ingest_file(argv[1])
        print(f"Memoria: +{n} nodos (total {mem.size()})")
        return 0

    if cmd == "retrieve":
        if len(argv) < 2:
            print("Uso: simba.cli retrieve \"consulta\"")
            return 1
        mem = AssociativeMemory()
        for i, node in enumerate(mem.retrieve(argv[1]), 1):
            print(f"[{i}] {node[:200]}")
        return 0

    if cmd == "ask":
        if len(argv) < 2:
            print("Uso: simba.cli ask \"pregunta\"")
            return 1
        mem = AssociativeMemory()
        print(mem.ask(" ".join(argv[1:])))
        return 0

    if cmd == "classify":
        if len(argv) < 2:
            print("Uso: simba.cli classify \"consulta\"")
            return 1
        router = Router()
        print(router.classify(" ".join(argv[1:])))
        return 0

    if cmd == "route":
        if len(argv) < 2:
            print("Uso: simba.cli route \"pregunta\"")
            return 1
        router = Router()
        out = router.route(" ".join(argv[1:]))
        print(f"[dominio: {out['domain']}] [usó: {out['used']}] "
              f"[modelo: {out['model']}] [delegó: {out['delegated']}]")
        print("-" * 60)
        print(out["answer"])
        return 0

    if cmd == "info":
        mem = AssociativeMemory()
        print(f"Nodos en memoria: {mem.size()}")
        return 0

    print(f"Comando desconocido: {cmd}")
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
