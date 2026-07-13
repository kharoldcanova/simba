# Ejemplo visual: cómo funcionan los embeddings (estudio)

> Ejecutado en local con `nomic-embed-text` + numpy. Demuestra el "gusano":
> cada frase cae en un punto del espacio de significado; las relacionadas
> quedan cerca.

## Las 4 frases de prueba

```
A = "El enrutador delega a un experto en matematicas"
B = "Resuelve la integral y la derivada paso a paso"
C = "El hipocampo construye un mapa predictivo de experiencias"
D = "Me gusta el cafe con leche por las mananas"
```

## Resultado: similitud de coseno (1.0 = iguales, 0.0 = sin relación)

```
0.679   A (enrutador/matematicas)   <-> B (integral/derivada)   [más cercanas]
0.582   A                           <-> C (hipocampo)
0.569   B                           <-> C
0.558   A                           <-> D (cafe)
0.592   B                           <-> D
0.544   C                           <-> D (cafe)                [más lejos]
```

## Lectura

- A y B (ambas de matemáticas) cayeron **más cerca** (0.679) que cualquier otra
  combinación. El embedding ya "sabe" que matemáticas ≈ cálculo, sin que se lo
  dijéramos.
- D (café con leche) cayó **lejos de todas** (~0.54-0.59). Es el nodo aislado.
- Ninguna relación la inventó el modelo en el momento: vino del entrenamiento
  previo del embedding. SIMBA solo lo usa como caja texto→vector.

## Un vector, de cerca

Cada frase se convierte en **768 números** (coordenadas en el espacio):

```
A[0:8] = [0.017, 0.0378, -0.1622, 0.0353, 0.02, -0.0222, -0.0355, -0.0596, ...]
```

Dos frases cercanas = coordenadas parecidas = se recuperan juntas.

## El flujo que esto habilita

1. **Ingerir** (una vez): cada texto → vector → se guarda en Chroma.
2. **Consultar**: pregunta → 1 vector → Chroma compara por coseno.
3. Devuelve los vecinos más cercanos (los trozos relacionados).
4. Esos trozos son el contexto que se le pasa al LLM (RAG).

El ahorro: indexar una vez, comparar por coordenadas baratas, y darle al
modelo solo lo relevante — sin re-entrenar.
