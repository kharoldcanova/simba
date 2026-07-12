# Paper 8 — Mamba / RWKV: memoria continua (estado que fluye)

> Resumen para estudio de SIMBA. La arquitectura más cercana a tu "gusano".

## El problema de los Transformers (repaso)

La atención (paper 1) compara cada token con todos los demás. Eso crece
**cuadráticamente** con el texto largo → se vuelve inviable y tiene "ventana"
limitada. No hay memoria que fluya; cada contexto es plano.

## Mamba (Gu & Dao, 2023): Selective State Space Model

En vez de atención, usa un **estado que se actualiza en el tiempo** (state
space model). A medida que lee, va **comprimiendo** lo visto en un estado
pequeño y continuo.

- Memoria = el estado, no la ventana de contexto.
- Costo **lineal** en la longitud del texto (no cuadrático).
- Puede procesar secuencias enormes (libros enteros) sin explotar.

Esto es tu "gusano": un estado que se expande y condensa la experiencia a medida
que avanza, en vez de recordar todo a la vez.

## RWKV (Peng et al., 2023): RNN + Transformer

Híbrido: se entrena como Transformer (paralelo, estable) pero en uso se comporta
como **RNN con estado persistente**. Lo mejor de ambos:

- Paralelizable en entrenamiento.
- Estado continuo en inferencia → memoria que fluye, barato.

## Por qué es CLAVE para SIMBA

- Tu intuición del "gusano que se expande conectando nodos" = **estado
  continuo**, no atención plana.
- Mamba/RWKV permiten un modelo que "recuerda" mientras procesa sin necesidad de
  RAG para todo (aunque RAG sigue sirviendo para conocimiento externo).
- Son más eficientes → corren en tu PC, cumpliendo el objetivo de hardware
  accesible.

## Trade-off real

- El ecosistema (tools, fine-tuning) de Transformer es más maduro. Mamba/RWKV
  son más nuevos; menos soporte listo para usar.
- SIMBA puede empezar con Transformers (Mixtral) y migrar módulos críticos a
  Mamba/RWKV donde la memoria continua importe.

## Conexión con todo lo anterior

- Reemplaza la "ventana plana" (paper 1) por memoria fluida.
- Implementa de verdad el "mapa predictivo" (paper 3) y el predictive coding
  (paper 2) a nivel arquitectura.

## Preguntas para verificar

1. ¿Por qué la atención no escala con texto largo?
2. ¿Qué es el "estado continuo" de Mamba y por qué se parece a tu gusano?
3. ¿Qué ventaja tiene RWKV sobre un Transformer puro?
