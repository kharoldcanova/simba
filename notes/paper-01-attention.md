# Paper 1 — Attention Is All You Need (Vaswani et al., 2017)

> Resumen para estudio de SIMBA. Leé este ANTES o DESPUÉS del paper original;
> está en lenguaje simple y conectado a nuestra arquitectura.

## El problema que resolvían

Antes de este paper, los modelos de lenguaje usaban **RNN/LSTM** (redes
recurrentes): procesaban el texto palabra por palabra, en orden. Eso tenía dos
problemas graves:

1. **No se podían paralelizar bien** → entrenar era lentísimo.
2. **Olvidaban lo del principio** → en frases largas, la información del
   comienzo se diluía hacia el final.

## La idea central: Attention (atención)

En vez de leer secuencialmente, el modelo mira **todas las palabras a la vez** y
calcula cuánto se *relaciona* cada una con las demás. Es como cuando leés una
oración y, para entender "lo", mirás hacia atrás a qué palabra se refiere.

Eso es la **self-attention**: cada token presta "atención" a los otros tokens
según su relevancia.

## Los 3 ingredientes de la atención

Para cada palabra se calculan 3 vectores:

- **Query (Q)**: "¿qué estoy buscando?"
- **Key (K)**: "¿qué ofrezco?"
- **Value (V)**: "¿qué información aporto?"

La atención = comparar Q con todas las K, y usar eso para ponderar las V.
Matemática real: `Attention(Q,K,V) = softmax(Q·Kᵀ / √d) · V`.

- `Q·Kᵀ` mide similitud entre palabras.
- `softmax` la convierte en pesos que suman 1.
- `√d` estabiliza (evita que los números exploten).

## Multi-Head Attention (atención con varias cabezas)

No usan una sola atención, sino **varias en paralelo** ("heads"). Cada cabeza
aprende a enfocarse en algo distinto: una en gramática, otra en referencias, otra
en orden... y se combinan. Esto es parecido a tener "varios especialistas"
mirando el mismo texto → conecta con la idea de SIMBA de módulos.

## Encoder-Decoder (codificador-decodificador)

El Transformer original tiene dos partes:
- **Encoder**: lee el texto de entrada y lo convierte en representaciones.
- **Decoder**: genera la salida, palabra por palabra, usando atención al encoder.

Los chatbots actuales (GPT) usan solo el **decoder** (autoregresivo: predice el
siguiente token). Por eso en SIMBA hablamos de "predecir el siguiente token".

## Positional Encoding (código de posición)

Como la atención no es secuencial, el modelo no sabe el orden de las palabras.
Le suman un vector de "posición" a cada palabra para que sepa quién va primero.
Importante: esto es la única pista de orden que tiene.

## Por qué importa para SIMBA

| Concepto del paper | Relación con SIMBA |
|---|---|
| Self-attention | Es el mecanismo que relaciona tokens (tu "gusano" a nivel token) |
| Multi-head | Varios "especialistas" viendo lo mismo → inspira el cerebro modular |
| Paralelismo | Permite entrenar rápido, pero NO reduce FLOPs totales (ver K8s) |
| Contexto limitado | La atención solo ve lo que cabe en la ventana → por eso necesitamos RAG (memoria externa) |

## Lo que el paper NO resuelve (y donde entra SIMBA)

- **Memoria a largo plazo**: el Transformer no "recuerda" entre sesiones; su
  memoria es la ventana de contexto. SIMBA propone RAG como memoria externa.
- **Especialización**: un solo modelo gigante hace todo. SIMBA propone varios
  chicos enrutados.
- **Eficiencia de memoria**: la atención crece cuadráticamente con el texto
  largo. Mamba/RWKV (paper 8) lo arreglan con estado continuo.

## Preguntas para verificar que entendiste

1. ¿Por qué los RNN eran lentos y el Transformer no?
2. ¿Qué son Q, K, V y para qué sirven?
3. ¿Por qué el modelo necesita "positional encoding"?
4. ¿Cómo se relaciona "multi-head" con la idea de especialistas de SIMBA?

---
*Siguiente: Paper 2 — Predictive Coding (Friston), la base biológica.*
