# Cómo se entrena un modelo de IA (para iniciados)

> Asumimos que ya sabés qué es un **token**. Esta guía explica el resto del
> camino, de forma conceptual pero con nombres reales que podés buscar.

## 1. El objetivo del entrenamiento

Un modelo de lenguaje se entrena para **predecir el siguiente token** dado
el contexto anterior. No "sabe" cosas como nosotros; aprende una distribución
de probabilidad: *dado lo que leíste, ¿qué token es más probable ahora?*

Esto se llama **modelado del lenguaje autoregresivo** (ej. GPT). Otros modelos
no son autoregresivos (BERT predice máscaras), pero el grueso de los chatbots
actuales sí lo es.

## 2. Las tres etapas típicas

| Etapa | Qué hace | Datos | Costo |
|---|---|---|---|
| **Pre-entrenamiento** | Aprende gramática, hechos, patrones desde cero | Trillones de tokens de web/libros | Altísimo |
| **Fine-tuning supervisado (SFT)** | Aprende a *responder en formato útil* | Miles/millones de pares pregunta-respuesta | Medio |
| **RLHF / preferencias** | Aprende *qué respuesta prefiere un humano* | Comparaciones humanas | Medio |

## 3. Pre-entrenamiento (la parte pesada)

- **Tokenización**: el texto se corta en tokens (ya lo sabés).
- **Arquitectura**: casi todos usan **Transformers** (atención).
- **Pérdida**: *cross-entropy* entre lo que predijo y el token real.
- **Optimización**: el modelo ajusta miles de millones de pesos (parámetros)
  usando **descenso por gradiente** y backpropagation.
- El resultado es un "modelo base": sabe mucho, pero no siempre responde bien.

## 4. Tu intuición sobre "compactar información"

Lo que proponés ya existe, con otros nombres:

- **Embeddings**: cada pedazo de texto se convierte en un vector. Pedazos
  *similares* quedan cerca en el espacio vectorial. Eso es tu "gusano que
  conecta nodos".
- **RAG (Retrieval-Augmented Generation)**: en vez de memorizar todo, el
  modelo *recupera* fragmentos relevantes y los usa al responder. Es memoria
  externa asociativa, como el hipocampo.
- **Memoria de trabajo / context window**: el "recuerdo a corto plazo" del
  modelo durante una conversación.

El problema real: los Transformers **no aprenden nuevos pesos durante el uso**.
Su "memoria" es estática tras entrenar. Por eso se usan RAG y bases de datos
vectoriales para darle memoria viva. Tu idea apunta justo ahí.

## 5. Tu idea de "varios modelos = cerebro"

Esto también existe y se investiga activamente:

- **Mixture of Experts (MoE)**: un modelo grande con muchas "sub-redes"
  (expertos); un enrutador decide cuál usa cada token. Lógica y creatividad
  podrían ser expertos distintos.
- **Sistemas multi-agente**: varios modelos pequeños cooperan (uno planea,
  otro escribe, otro revisa). Es lo que hacen frameworks como AutoGen.
- **Especialización modular**: cerebros biológicos tienen áreas especializadas;
  imitar eso con módulos separados es una línea de investigación real.

## 6. Lo que falta antes de construir

Para no reinventar la rueda, conviene leer primero:

- **Sobre cerebro/memoria**: papers de memoria episódica, hipocampo y
  *predictive coding*.
- **Sobre MoE**: "Switch Transformer", "Mixtral" (MoE open).
- **Sobre arquitecturas alternativas a Transformers**: Mamba, RWKV (state
  space models) — estos sí tienen "memoria continua" tipo gusano.

## 7. Próximo paso sugerido para SIMBA

1. Armar `docs/papers.md` con una lista curada.
2. Prototipar un **módulo de memoria asociativa** (embeddings + RAG simple)
   en Python con Ollama local.
3. Después un **enrutador** que decida entre un "módulo lógico" y uno
   "creativo".

---
*Nota:* tu intuición de "compactar y relacionar" es esencialmente la dirección
de la investigación en **memoria externa** y **estado continuo** (Mamba/RWKV),
no en apilar más parámetros. Estás en el camino correcto.
