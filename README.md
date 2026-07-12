# SIMBA — Sistema de Inteligencia Modular Basada en Asociación

> Asistente de IA por voz / cerebro modular de modelos especializados.
> Inspirado en memoria asociativa biológica y Mixture of Experts.

**Estado:** Teoría fundada (2026-07-11). Práctica: pendiente de prototipo.

**Repositorio:** https://github.com/kharoldcanova/simba

> Proyecto de investigación personal. No se aceptan colaboradores externos por
> el momento. Licencia MIT (ver `LICENSE`).

---

## Qué es SIMBA

SIMBA es un proyecto de investigación y construcción de un asistente de IA que
no depende de un modelo gigante, sino de **varios modelos chicos
especializados conectados entre sí**, más un módulo de **memoria asociativa**
(estilo hipocampo).

La intuición fundadora (de Kharold): en vez de aplastar toda la información en
un solo modelo enorme, **compactamos y relacionamos** pedazos de información —
como un gusano que se expande y conecta nodos por experiencia. El cerebro
funciona por áreas especializadas; imitemos eso con módulos.

---

## Puntos clave (la teoría)

1. **Memoria asociativa, no todo memorizado**
   - Los Transformers no aprenden en uso: su memoria queda congelada tras
     entrenar. Por eso usamos **RAG** (recuperar fragmentos relevantes) como
     memoria viva externa.
   - Embeddings + base vectorial = "pedazos similares cerca en el espacio".

2. **Cerebro modular de especialistas (Mixture of Experts a nivel sistema)**
   - Varios modelos chicos, cada uno experto en algo (lógica, creatividad,
     mates, memoria). Un **router** decide a quién delegar.
   - Si un modelo no sabe de un tema, llama a otro que sí → cascada de
     especialistas.
   - Esto **SÍ reduce latencia y hardware** (a diferencia de K8s): solo se
     ejecuta el experto relevante.

3. **Kubernetes NO ahorra horas de entrenamiento ni acelera un modelo**
   - K8s es orquestación: mejora *throughput* (cuántos pedidos a la vez) y
     disponibilidad, no *latencia* (tiempo de una respuesta).
   - La velocidad la decide: tamaño del modelo + hardware + motor de serving
     (vLLM/Ollama) + arquitectura eficiente (Mamba/RWKV).
   - K8s sirve para desplegar los contenedores de cada especialista en
     servicio, no para hacerlos inteligentes.

4. **Cómo se entrena un modelo (contexto)**
   - Pre-entrenamiento (predecir siguiente token) → SFT (formato útil) → RLHF
     (preferencias humanas).
   - Para reducir hardware de verdad: destilación, cuantización (GPTQ 4-bit),
     LoRA, FlashAttention, Mamba/RWKV.

---

## Cómo construimos la idea (hoja de ruta)

### Fase 0 — Estudio (en curso)
- [x] Carpeta y repo creados.
- [x] Papers clave curados → `docs/papers-clave.md`.
- [x] Conversación exportada → `model-chat/2026-07-11-simba-chat.md`.
- [ ] Leer los papers prioritarios (⭐ en `docs/papers-clave.md`).

### Fase 1 — Memoria asociativa (prototipo)
- [ ] Módulo RAG con embeddings + base vectorial (Chroma/FAISS/Qdrant).
- [ ] Conectarlo a Ollama local para recuperar contexto.
- [ ] Tu "gusano": relacionar fragmentos por similitud y experiencia.

### Fase 2 — Router de especialistas
- [ ] Router chico que clasifica intención (mates / creatividad / memoria).
- [ ] 2 especialistas mínimos (p.ej. lógica + creatividad) en Ollama local.
- [ ] Cascada: delegar al que sabe.

### Fase 3 — Cerebro completo
- [ ] Más especialistas (matemáticas, código, memoria/RAG, creatividad).
- [ ] Agregador final para consistencia.
- [ ] (Opcional) Orquestación con Docker Compose / K3s en tu PC, o K8s si
      escalás a cluster.

---

## Estructura del repo

```
simba/
├── README.md                         # Este archivo (visión + puntos clave)
├── docs/
│   ├── papers.md                     # Lista de papers a recopilar
│   └── papers-clave.md               # Papers curados con links + resumen
├── notes/
│   ├── como-entrenar-ia.md           # Explicación de entrenamiento para iniciados
│   ├── kubernetes-y-entrenamiento.md # K8s NO ahorra latencia/horas
│   └── arquitectura-especialistas.md # Cerebro de especialistas enrutados
└── model-chat/
    └── 2026-07-11-simba-chat.md       # Conversación de fundación del proyecto
```

---

## Requisitos (para la práctica)

- Python 3.11+
- [Ollama](https://ollama.com) corriendo localmente (modelos chicos: Mistral,
  Mixtral, o Mamba/RWKV si están disponibles).
- `opencode` (para programar asistido).
- Para la memoria asociativa: Chroma/FAISS/Qdrant + embeddings locales.
- Para serving eficiente: vLLM u Ollama ajustado.

> Todo corre en hardware propio (tu PC). La cuantización a 4-bit (GPTQ) permite
> tener varios especialistas chicos en una sola GPU media.

---

## Para alguien que se interese en el tema

Empezá por `docs/papers-clave.md` (los ⭐ son obligatorios) y leé
`notes/arquitectura-especialistas.md` para la propuesta concreta. La conversación
de origen está en `model-chat/` por si querés ver cómo llegamos a esto.

**Resumen en una frase:** un asistente local, modular y con memoria asociativa,
hecho de varios modelos chicos enrutados — no un modelo gigante.

---
*Fundado el 2026-07-11 por Kharold. Teoría lista; la práctica se construye en
las fases siguientes.*
