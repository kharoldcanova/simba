# Papers clave para SIMBA

> Curada para la etapa de estudio. Cada entrada tiene: link, resumen de 1 línea,
> y cómo se relaciona con la visión de SIMBA (memoria asociativa + cerebro modular).
> Prioridad sugerida: ⭐ = leer primero.

## 1. Base: cómo aprenden los modelos de lenguaje

- ⭐ [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
  - Introduce el Transformer y la atención. Es la columna vertebral de casi todo
    modelo actual.
  - **SIMBA**: entender el bloque base antes de proponer variantes.

- ⭐ [A Theory of Cortical Responses — Predictive Coding (Friston, 2005)](https://www.fil.ion.ucl.ac.uk/~karl/Theory_of_Cortical_Responses.pdf)
  - El cerebro como máquina que predice y corrige error. Marco biológico clave.
  - **SIMBA**: fundamenta la idea de "memoria como predicción", no como almacén.

- [The Hippocampus as a Predictive Map (Stachenfeld et al., 2017)](https://www.nature.com/articles/nn.4650)
  - El hipocampo construye un "mapa predictivo" del entorno; conecta experiencias
    cercanas. Muy cerca de tu idea del gusano que relaciona nodos.
  - **SIMBA**: base para el módulo de memoria asociativa.

## 2. Memoria externa y asociativa (tu "compactar y relacionar")

- ⭐ [Retrieval-Augmented Generation (RAG) (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
  - El modelo *recupera* fragmentos relevantes de una base en vez de memorizarlo
    todo. Memoria viva externa.
  - **SIMBA**: es la implementación directa de "guardar pedazos y relacionarlos".

- [Dense Passage Retrieval (Karpukhin et al., 2020)](https://arxiv.org/abs/2004.04906)
  - Cómo indexar y buscar esos fragmentos eficientemente (embeddings + búsqueda).
  - **SIMBA**: motor de búsqueda del módulo de memoria.

- [Experience Replay in Deep RL (Mnih et al., 2015)](https://www.nature.com/articles/nature14236)
  - Repetir experiencias pasadas mejora el aprendizaje (inspirado en memoria
    biológica).
  - **SIMBA**: mecanismo de consolidación de memoria.

## 3. Cerebro modular: varios modelos especializados

- ⭐ [Switch Transformers (Fedus et al., 2021)](https://arxiv.org/abs/2101.03961)
  - Mixture of Experts (MoE): muchas sub-redes, un enrutador elige cuál usar por
    token. Lógica y creatividad podrían ser expertos distintos.
  - **SIMBA**: tu idea de "un modelo para lógica, otro para creatividad" ya
    existe como MoE.

- ⭐ [Mixtral of Experts (Jiang et al., 2024)](https://arxiv.org/abs/2401.04088)
  - MoE abierto y pequeño (8 expertos, activa 2). Buen modelo para experimentar
    localmente.
  - **SIMBA**: candidato real para prototipar el cerebro modular en hardware
    propio.

- [AutoGen: Multi-Agent Conversation (Wu et al., 2023)](https://arxiv.org/abs/2308.08155)
  - Varios modelos cooperan (planifica, escribe, revisa). Cerebro multi-agente.
  - **SIMBA**: arquitectura de orquestación entre módulos.

- [Communicative Agents for Software Development — ChatDev (Qian et al., 2023)](https://arxiv.org/abs/2307.07924)
  - Agentes con roles fijos que colaboran en una tarea.
  - **SIMBA**: ejemplo de especialización por rol.

## 4. Arquitecturas con "memoria continua" (tipo gusano)

- ⭐ [Mamba: Selective State Space Models (Gu & Dao, 2023)](https://arxiv.org/abs/2312.00752)
  - Reemplaza atención por estado que fluye en el tiempo. Memoria continua, no
    contexto plano. Muy eficiente.
  - **SIMBA**: la arquitectura más cercana a tu intuición de "gusano que se
    expande".

- [RWKV: Reinventing RNNs for the Transformer Era (Peng et al., 2023)](https://arxiv.org/abs/2305.13048)
  - RNN paralelizable con estado persistente. Combina lo bueno de RNN y Transformer.
  - **SIMBA**: otra vía de estado continuo, más liviana que Transformers.

## 5. Reducir hardware y horas de entrenamiento (lo que sí comprime)

> Esto responde tu duda sobre Kubernetes: el ahorro real viene de ACÁ, no de la
> orquestación.

- ⭐ [LoRA: Low-Rank Adaptation (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
  - Fine-tuning barato: entrenás solo una pequeña matriz, no todo el modelo.
  - **SIMBA**: permite adaptar módulos sin re-entrenar desde cero.

- [DistilBERT (Sanh et al., 2019)](https://arxiv.org/abs/1910.01108)
  - Destilación: un modelo pequeño que imita a uno grande. 40% menor, 97% de
    calidad.
  - **SIMBA**: "compactar el modelo" de verdad.

- [GPTQ: Post-Training Quantization (Frantar et al., 2022)](https://arxiv.org/abs/2210.17323)
  - Comprime pesos a 4 bits con poco daño. Baja el hardware necesario para
    servir.
  - **SIMBA**: compressión para correr en tu PC.

- [FlashAttention (Dao et al., 2022)](https://arxiv.org/abs/2205.14135)
  - Atención más rápida y con menos memoria (IO-aware).
  - **SIMBA**: entrenar/servir más rápido sin cambiar el modelo.

- [Efficient Memory Management for LLM Serving — vLLM (Kwon et al., 2023)](https://arxiv.org/abs/2309.06180)
  - PagedAttention: sirve muchos modelos con poca VRAM.
  - **SIMBA**: clave si querés correr varios módulos a la vez en una sola GPU.

## 6. Roadmap de lectura sugerido

1. Attention Is All You Need → entender Transformer.
2. Predictive Coding (Friston) + Hippocampus as Predictive Map → base biológica.
3. RAG + DPR → memoria asociativa.
4. Switch Transformers + Mixtral → cerebro modular.
5. Mamba / RWKV → memoria continua.
6. LoRA + DistilBERT + GPTQ → cómo comprimir de verdad.

---
*Nota:* Kubernetes (que consultaste) NO reduce las horas de entrenamiento ni el
hardware intrínseco. Eso lo logran las técnicas de la sección 5 (destilación,
cuantización, LoRA, arquitecturas eficientes). K8s sirve para *orquestar* los
módulos y usar el cluster mejor — ver `notes/kubernetes-y-entrenamiento.md`.
