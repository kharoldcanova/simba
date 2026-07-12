# Paper 6 — Switch Transformers (Fedus et al., 2021)

> Resumen para estudio de SIMBA. El origen formal de tu "cerebro de especialistas".

## El problema

Querés un modelo más capaz → le ponés más parámetros. Pero más parámetros =
más cómputo por token = más lento y caro. No escala.

## La idea: Mixture of Experts (MoE)

En lugar de una red gigante, tenés **muchas sub-redes pequeñas** ("expertos") y
un **enrutador (router)** que decide cuál experto usa cada token.

- Solo se activa el experto relevante → misma capacidad con **menos cómputo**.
- Esto es **sparse activation** (activación dispersa): no todo se usa siempre.

## Switch Transformer (la versión simple)

Usa **top-1 routing**: para cada token, el router elige UN solo experto. Eso
basta y reduce costo drásticamente. Escalan a miles de millones de parámetros
sin explotar el hardware.

## Por qué es EXACTAMENTE tu idea

Tu propuesta: "varios modelos, cada uno experto en algo; si uno no sabe de
mates, llama a otro que sí". Switch Transformers hace eso **adentro de un solo
modelo**. SIMBA lo lleva al siguiente nivel: **varios modelos separados**
orquestados por un router a nivel sistema (ver `arquitectura-especialistas.md`).

## Ventajas

- Más parámetros = más conocimiento, sin más costo por token.
- Especialización natural: cada experto aprende un patrón distinto.

## Desafíos (importantes para SIMBA)

- **Balance de carga**: el router puede volcarse siempre al mismo experto.
  Usan una "pérdida de equilibrio" para forzarlo a repartir.
- **Memoria**: todos los expertos deben caber en RAM/VRAM aunque no se usen
  todos. → solución en SIMBA: cuantizar a 4-bit o cargar bajo demanda.

## Conexión con SIMBA

- MoE = la justificación teórica de tu arquitectura de especialistas.
- El router de SIMBA es el mismo concepto, aplicado a modelos completos.

## Preguntas para verificar

1. ¿Qué es "sparse activation" y por qué ahorra cómputo?
2. ¿Qué hace el router en un MoE?
3. ¿Cuál es el riesgo de "balance de carga" y cómo lo evitan?
