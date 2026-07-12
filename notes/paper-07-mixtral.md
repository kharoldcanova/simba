# Paper 7 — Mixtral of Experts (Jiang et al., 2024)

> Resumen para estudio de SIMBA. El MoE ABIERTO que podés correr en tu PC.

## Qué es

Mixtral es un modelo **abierto** (pesos libres) que usa MoE (paper 6). En
concreto: tiene **8 expertos** y por cada token activa solo **2**.

## Por qué importa para SIMBA

- Es la prueba de que tu arquitectura de especialistas **se puede hacer en
  hardware propio**, no solo en laboratorios gigantes.
- Al activar 2 de 8 expertos, corre más liviano que un modelo del mismo tamaño
  total.
- Al ser open, lo podés usar como base para tus propios especialistas (fine-tune
  con LoRA, ver papers-clave sección 5).

## Detalle técnico

- 8 expertos, top-2 routing → ~2x la velocidad de un modelo denso equivalente.
- Rendimiento comparable a modelos mucho más grandes, con menos cómputo.
- Existen versiones cuantizadas (GGUF) para correr en GPU modesta o incluso CPU.

## Cómo encaja en tu plan

- **Fase 2 de SIMBA**: podés usar Mixtral como "cerebro base" y encimar tu
  router de especialistas arriba, o usar varios Mixtral pequeños como expertos
  distintos.
- Es tu candidato real para prototipar sin gastar en cloud.

## Lo que NO es

- No es "varios modelos separados"; es MoE dentro de uno. Para SIMBA querés
  modelos separados enrutados, pero Mixtral es el puente de aprendizaje.

## Preguntas para verificar

1. ¿Cuántos expertos tiene Mixtral y cuántos activa por token?
2. ¿Por qué podés correrlo en tu PC a pesar de ser grande?
3. ¿Cómo lo usarías en la Fase 2 de SIMBA?
