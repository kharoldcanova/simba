# Paper 4 — Retrieval-Augmented Generation (RAG) (Lewis et al., 2020)

> Resumen para estudio de SIMBA. El módulo de MEMORIA EXTERNA de tu arquitectura.

## El problema que resolvían

Los modelos de lenguaje "se acuerdan" solo de lo que vieron en entrenamiento.
No pueden consultar hechos nuevos ni tus datos privados. Y si querés
actualizarlos, hay que re-entrenar (carísimo).

## La solución: RAG

Antes de responder, el modelo **busca documentos relevantes** en una base
externa y los pega al prompt como contexto. El modelo genera la respuesta
usando eso.

Es decir: el conocimiento NO está adentro de los pesos, sino **al lado**,
recuperable.

## Por qué encaja con tu intuición

- "Compactar y relacionar" = indexar fragmentos en una base y recuperar los
  similares (embeddings + búsqueda).
- "Gusano que conecta nodos" = al recuperar un fragmento, traés sus vecinos
  relacionados.
- El modelo queda chico y la "memoria" vive afuera → ahorra hardware (lo que
  buscabas).

## Cómo funciona (pasos)

1. **Indexar**: tus documentos se cortan en trozos y se convierten en vectores
   (embeddings).
2. **Recuperar**: ante una pregunta, la conviertes en vector y buscas los
   trozos más cercanos (similitud de coseno).
3. **Generar**: le das esos trozos al modelo como contexto y pide la respuesta.

## Conexión con SIMBA

- El módulo de **memoria/RAG** en `arquitectura-especialistas.md` es esto.
- Es la respuesta a "los Transformers no aprenden en uso" (paper 1).

## Lo que el paper dejó abierto

- ¿Cómo recuperar lo REALMENTE relevante y no solo lo parecido? (ver DPR, paper 5)
- ¿Cómo evitar que el contexto recuperado sea ruidoso? → técnica activa de
  investigación.

## Preguntas para verificar

1. ¿Por qué RAG evita re-entrenar para agregar conocimiento?
2. ¿Cuáles son los 3 pasos de RAG?
3. ¿Cómo resuelve RAG el problema de "memoria congelada" de los Transformers?
