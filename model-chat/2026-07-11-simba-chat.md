# Conversación de fundación — SIMBA

**Fecha:** 2026-07-11
**Participantes:** Kharold (autor de la idea) + Hermes Agent (asistente)
**Tema:** Cómo entrenar un modelo de IA, memoria asociativa, cerebro modular de
especialistas, y el rol de Kubernetes.
**Resultado:** Se funda el proyecto SIMBA y se documenta la teoría en
`README.md`, `docs/` y `notes/`.

> Esta es la charla original de la que salió el proyecto. Está resumida por
> turnos para que cualquiera entienda cómo llegamos a la arquitectura propuesta.

---

## Turno 1 — Pregunta inicial sobre entrenamiento

**Kharold:** Explicame cómo se entrena un modelo de IA para personas iniciadas.
Sé el concepto de token, pero el entrenamiento siento que se puede hacer mejor,
reducirlo si usamos compactado de información para relacionarlo con otras
similares. Tales como funcionan las redes cerebrales, donde usamos un recuerdo y
eso se relaciona con otro. En resumen tomamos un pedazo de esa información y la
guardamos con otra relacionada a través de experiencia, como un gusano
expandiéndose. También podríamos conectar varios modelos de IA básicos para
funcionar como un cerebro: uno para lógica, otro para creatividad. Hay que buscar
papers de cómo funciona el cerebro.

**Hermes:** Explicó las 3 etapas (pre-entrenamiento → SFT → RLHF), que el modelo
predice el siguiente token. Mapeó su intuición: embeddings = "relacionar
similares", RAG = memoria asociativa tipo hipocampo, MoE = cerebro modular.
Aclaró que los Transformers no aprenden en uso (memoria congelada tras
entrenar), por eso se usa memoria externa.

> Se creó la carpeta `projects-personal/simba` con `README.md`,
> `notes/como-entrenar-ia.md` y `docs/papers.md`.

---

## Turno 2 — Kubernetes y ahorro de rendimiento

**Kharold:** Siento que podríamos reducir las horas de entrenamiento y el hardware
si compactamos bien el modelo, usando contenedores conectados como Kubernetes
para que se relacionen desde ahí. ¿Eso ahorra rendimiento no?

**Hermes:** **No.** Kubernetes no reduce horas de entrenamiento ni hardware
intrínseco (están fijos por tamaño × datos × algoritmo). K8s es orquestación:
mejora uso de recursos, tolerancia a fallos, y sirve para relacionar módulos en
*servicio*, no en el cálculo. El ahorro real viene de destilación, cuantización
(GPTQ 4-bit), LoRA, Mamba/RWKV, FlashAttention.

> Se creó `docs/papers-clave.md` (lista curada con links) y
> `notes/kubernetes-y-entrenamiento.md`.

---

## Turno 3 — Aclaración sobre latencia

**Kharold:** Lo que tratas de decir es que el tiempo de respuesta del modelo es
más corto usando Kubernetes, no?

**Hermes:** No. K8s no acorta la latencia (a veces la sube por la red). Mejora
*throughput* (pedidos a la vez) y disponibilidad. La velocidad de cada respuesta
la decide: tamaño del modelo + hardware + motor de serving (vLLM/Ollama). En tu
PC local, K8s es puro overhead.

---

## Turno 4 — Cerebro de especialistas

**Kharold:** La latencia no nos favorece en ese modelo. Podemos usar varios
modelos expertos en varias cosas. Si alguien pregunta mates, un modelo que no
sabe llama a otro que sí sabe. Cada modelo especializado en algo. Eso hace que
trabajemos con modelos chicos, no? Nos conviene a la hora de rendir para solo
conectarlos.

**Hermes:** Exacto. Eso es **Mixture of Experts a nivel sistema** / router-based
ensemble. SÍ reduce latencia y hardware: solo se ejecuta el experto relevante.
Documentó la arquitectura: router + especialistas + módulo de memoria/RAG.
Aclaró los riesgos reales: error de enrutamiento, VRAM si se cargan todos a la
vez (solución: cuantizar a 4-bit o cargar bajo demanda), consistencia entre
modelos.

> Se creó `notes/arquitectura-especialistas.md` y se amplió
> `notes/kubernetes-y-entrenamiento.md` con la sección de latencia.

---

## Turno 5 — Consolidación

**Kharold:** Bien, funciona para empezar (la teoría). Después vemos la práctica.
Pon lo que queremos hacer en un README con todo lo necesario y los puntos clave.
Exporta esta conversación a `model-chat/` con la fecha de hoy.

**Hermes:** Creó el `README.md` definitivo (visión, puntos clave, hoja de ruta,
estructura, requisitos) y este archivo de conversación en
`model-chat/2026-07-11-simba-chat.md`.

---

## Conclusión de la charla

- El ahorro de entrenamiento/hardware viene de **compresión y arquitecturas
  eficientes**, no de K8s.
- La arquitectura propuesta es un **cerebro modular**: varios modelos chicos
  enrutados + memoria asociativa (RAG).
- K8s solo orquesta los contenedores en servicio.
- Teoría fundada. Siguiente paso real: prototipar el router + RAG con Ollama
  local (Fase 1 y 2 del `README.md`).

---
*Archivo generado el 2026-07-11 para el repo SIMBA.*
