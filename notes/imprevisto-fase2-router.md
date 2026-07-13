# Imprevisto Fase 2: el router alucinó y clasificó mal

> Documentado para estudiar por qué falló la primera versión del router y cómo
> lo resolvió el examen de capacidades.

## Síntoma (lo que vimos al probar)

La primera versión del router (`simba/router.py` original) tenía las categorías
y los modelos **hardcodeados** por intuición:

- `matematicas` -> `llama3.2:1b`
- `creatividad` -> `qwen2.5:1.5b`
- `memoria`     -> `qwen2.5:1.5b`
- `general`     -> `qwen2.5:0.5b`

Dos fallos reales al ejecutarlo:

### Fallo 1 — Clasificación incorrecta
- `classify "qué es el enrutador en SIMBA"` devolvió `general` en vez de
  `memoria`.
- El clasificador por LLM no asoció "SIMBA" con la memoria, y no había regla
  que lo forzara.

### Fallo 2 — Alucinación peligrosa
- `route "inventa una metáfora sobre la memoria"` cayó en `memoria` (porque la
  palabra "memoria" estaba en la pregunta) y el especialista de memoria, al no
  tener contexto útil, **inventó que SIMBA era "un mercado de compras virtual"**.
- El modelo base alucinó sobre el propio proyecto. Esto es crítico: una
  respuesta falsa sobre SIMBA destruye la confianza en el sistema.

## Causa raíz

1. **Suposición sin medir.** Elegí qué modelo iba a qué dominio por intuición,
   no por evidencia. No sabía (ni sé aún) qué modelo es realmente bueno en qué.
2. **El clasificador por LLM es ruidoso.** Con `temperature>0` o prompts
   ambiguos, etiqueta mal. Necesita reglas duras de respaldo.
3. **El especialista de memoria puede inventar.** Sin contexto y sin prohibición
   estricta, el LLM rellena con alucinaciones.

## La corrección propuesta por Kharold (clave)

> "Los modelos existen buenos en otras cosas: programación, mates. Habría que
> hacer una especie de examen para saber su aptitud."

Esto es **capability profiling / benchmarking**. En vez de adivinar, se mide.
Se construye una **matriz de aptitudes** (`capabilities.json`) y el router
elige por score:

```
                mate  codigo  creatividad  memoria
modelo A        0.82   0.40     0.55        0.60
modelo B        0.45   0.88     0.70        0.65
```

El router entonces hace dos pasos:
1. **Clasificar la intención** (¿de qué dominio es la consulta?).
2. **Elegir el mejor modelo para ese dominio** según la matriz (no por fe).

## Plan de corrección

1. `simba/exam.py` — banco de preguntas por dominio + runner + scorer ->
   `capabilities.json`.
2. Scoring mixto: matemáticas/código/memoria con respuesta exacta o ejecución;
   creatividad con LLM-judge local (modelo chico que puntúa 0-1).
3. Router lee `capabilities.json` y enruta al modelo de mayor score por dominio.
4. Reglas duras: consultas sobre SIMBA -> memoria; el especialista de memoria
   tiene prohibido inventar (system estricto).

## Por qué esto hace el sistema "más seguro para calificar aptitud"

- Ya no se asume; se mide.
- El examen es reproducible: cualquiera puede correrlo y ver la matriz.
- Si agregás un modelo nuevo, lo examinás y la matriz se actualiza solo.
- La decisión de enrutamiento deja de ser opinión del programador y pasa a ser
  dato empírico.

## Estado
- [x] Detectado el fallo (alucinación + clasificación errónea)
- [x] Decidido: examen de capacidades + matriz por score
- [ ] Implementado `exam.py` y correrlo
- [ ] Router por score usando `capabilities.json`
