# Fase 1 — Memoria asociativa (RAG) implementada

> Prototipo funcionando. Implementado el módulo de memoria de SIMBA con Ollama
> local + Chroma. Fecha: primera implementación (post-estudio paper 1-8).

## Qué se construyó

```
simba/
├── simba/
│   ├── __init__.py
│   ├── memory.py        # AssociativeMemory: ingest + retrieve + ask (RAG)
│   └── cli.py           # CLI mínima para probar el flujo
├── examples/
│   └── simba-doc.txt    # documento de ejemplo para ingerir
├── .venv/               # entorno uv (NO se commitea)
└── .simba/memory/       # base vectorial persistente de Chroma (NO se commitea)
```

## Dependencias

- `uv` (gestor de entorno)
- `ollama` (servidor local corriendo)
- modelos: `nomic-embed-text` (embeddings) + `qwen2.5:1.5b` (chat)
- `chromadb` (base vectorial)

## Cómo correrlo

```bash
cd /home/kharold/projects-personal/simba

# 1) levantar Ollama (si no está)
ollama serve &

# 2) activar entorno
source .venv/bin/activate

# 3) cargar memoria (el "gusano se expande")
python -m simba.cli ingest examples/simba-doc.txt

# 4) recuperar solo los nodos relacionados
python -m simba.cli retrieve "¿qué es el enrutador en SIMBA?"

# 5) recuperar + responder con el modelo local (RAG)
python -m simba.cli ask "¿Cómo funciona la memoria asociativa y por qué no hay que re-entrenar?"
```

## Resultado de la prueba

- Ingesta: 4 nodos desde `examples/simba-doc.txt`.
- Retrieve: devolvió los fragmentos más similares a la consulta (ordenados por
  coseno).
- Ask (RAG): el modelo `qwen2.5:1.5b` respondió usando el contexto recuperado,
  mencionando hipocampo, enrutador y especialistas — confirmando que la memoria
  externa funciona.

## Qué demuestra

- La intuición de Kharold es real: **guardar pedazos y recuperar por similitud**
  funciona sin re-entrenar nada. Es el "gusano que conecta nodos".
- Se ejecuta 100% local (sin API de la nube) → cumple el objetivo de privacidad
  y hardware propio.

## Siguiente: Fase 2 — Router de especialistas

Con la memoria andando, el próximo módulo es el **router** que clasifica la
intención (mates / creatividad / memoria) y delega a un modelo especialista.
Ver `notes/arquitectura-especialistas.md`.
