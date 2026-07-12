# Paper 3 — The Hippocampus as a Predictive Map (Stachenfeld et al., 2017)

> Resumen para estudio de SIMBA. El "mapa predictivo" = tu gusano, formalizado.

## La pregunta

¿Cómo representa el hipocampo (la parte del cerebro de la memoria) el espacio y
las experiencias? No como un GPS plano, sino como un **mapa de qué viene
después**.

## Successor Representation (representación de sucesor)

En lugar de codificar "dónde estoy", el hipocampo codifica "**desde aquí, a qué
estados voy a llegar y con qué probabilidad**". Es decir: cada lugar apunta a
sus lugares sucesores.

Esto es clave: permite **planear** y **transferir** aprendizaje rápido cuando el
entorno cambia, sin re-aprender todo.

## Por qué es exactamente tu "gusano"

Tu intuición: tomamos un pedazo de información y lo guardamos con otro
**relacionado por experiencia**, como un gusano expandiéndose. Esto es la
Successor Representation:

- Cada nodo (experiencia) se conecta con los nodos a los que suele llevar.
- Esas conexiones se refuerzan por **experiencia** (cuántas veces pasás de A a B).
- El resultado es una red asociativa: llegás a A y "sabés" qué viene.

## Conexión con SIMBA

- El módulo de **memoria asociativa (RAG)** de SIMBA es un mapa predictivo
  artificial: dado un fragmento, recuperás los fragmentos relacionados.
- La "experiencia" = cuántas veces se usa/refuerza una conexión (podés llevar
  un conteo de co-ocurrencia en la base vectorial).
- Esto justifica usar **grafos de memoria** además de embeddings planos.

## Lo que el paper NO resuelve

- Es sobre navegación espacial/RL; aplicarlo a texto requiere adaptación.
- SIMBA lo toma como principio de diseño, no como implementación directa.

## Preguntas para verificar

1. ¿Qué es la Successor Representation y por qué ayuda a planear?
2. ¿Cómo se parece a tu idea del gusano que se expande?
3. ¿Cómo lo usarías en el módulo de memoria de SIMBA?
