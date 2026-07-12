# Paper 5 — Dense Passage Retrieval (DPR) (Karpukhin et al., 2020)

> Resumen para estudio de SIMBA. El MOTOR de búsqueda detrás del módulo RAG.

## El problema

RAG (paper 4) necesita "buscar lo relevante". La forma vieja era búsqueda por
palabras clave (BM25): muy frágil, no entiende sinónimos ni significado.

## La solución: DPR

Usa **dos redes BERT** (encoders):
- **Question encoder**: convierte la pregunta en un vector.
- **Passage encoder**: convierte cada párrafo en un vector (se hace una sola vez
  y se guarda en una base).

Para buscar: comparás el vector de la pregunta con el de cada párrafo (producto
interno) y tomás los más cercanos. Esto entiende **significado**, no solo
palabras iguales.

## Por qué importa para SIMBA

- Este es el "buscador" de tu módulo de memoria: dada una consulta, encuentra
  los fragmentos asociados (tu gusano encontrando nodos vecinos).
- Herramientas reales: **FAISS** (de Meta) o **Chroma** hacen esta búsqueda
  vectorial rápido. SIMBA puede usarlas.

## Diferencia clave vs búsqueda clásica

| BM25 (viejo) | DPR (denso) |
|---|---|
| Coincidencia de palabras | Similitud semántica |
| "perro" no matchea "can" | Sí matchea (mismo significado) |
| Rápido pero tonto | Mejor pero requiere embeddings |

## Conexión con SIMBA

- DPR es la implementación concreta de "relacionar pedazos similares" por
  experiencia/semántica.
- El "mapa predictivo" (paper 3) podría usarse ENCIMA de DPR para dar orden
  temporal a las recuperaciones.

## Lo que el paper NO cubre

- No dice cómo actualizar la base cuando cambian los datos (SIMBA lo resolverá
  con re-indexado incremental).

## Preguntas para verificar

1. ¿Por qué DPR es mejor que buscar por palabra clave?
2. ¿Qué son el question encoder y el passage encoder?
3. ¿Qué herramienta usarías en SIMBA para la búsqueda vectorial?
