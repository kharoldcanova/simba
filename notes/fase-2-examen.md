# Fase 2 — Router de especialistas por score (capability profiling)

> Implementado y probado. El router ya NO asume qué modelo es bueno en qué: lo
> mide con un examen y elige por matriz de aptitudes.

## Por qué existe (contexto)

La primera versión del router tenía modelos y dominios **hardcodeados por
intuición**. Falló: clasificó mal y el especialista de memoria **alucinó que
SIMBA era un mercado de compras**. Ver `imprevisto-fase2-router.md`.

Kharold propuso lo correcto: hacer un **examen de aptitud** a los modelos, como
se hace en ML (benchmarking / capability profiling). De ahí sale la matriz.

## Examen (`simba/exam.py`)

- Banco de preguntas por dominio: matematicas, codigo, creatividad, memoria.
- Scoring mixto:
  - matematicas/memoria → respuesta exacta (automático).
  - codigo → se ejecuta el código (éxito = 1.0).
  - creatividad → LLM-judge local (modelo chico puntúa 0-1).
- **Se corre UNA vez.** Escribe `capabilities.json` (la matriz).
- El router solo LEE el JSON: arranque rápido, sin re-examinar.

## Matriz real obtenida (2026-07-12, 4 modelos locales)

```
                    mate  codigo  creat  memoria
qwen2.5:0.5b        0.75   1.00    1.00    0.00
qwen2.5:1.5b        1.00   1.00    1.00    0.00
llama3.2:1b         1.00   1.00    0.50    0.00
llama3.2:2b         0.00   0.00    0.00    0.00   <- falló en TODO
```

Hallazgos:
- `llama3.2:2b` es el PEOR en absolutamente todo (modelo más grande ≠ mejor).
- `qwen2.5:1.5b` es el mejor generalista (1.0 salvo memoria).
- `memoria` da 0.00 en todos porque el examen corrió contra memoria VACÍA
  (las preguntas de memoria requieren haber ingerido `examples/simba-doc.txt`).
  No es falla de los modelos: memoria = usar RAG, no un modelo puntúa.

## Router por score (`simba/router.py`)

Para cada consulta:
1. **Clasifica la intención** con reglas duras priorizadas:
   SIMBA → memoria; python/código → código; mate → matemáticas;
   poema/crea → creatividad; LLM como último recurso.
2. **Elige el modelo de mayor score** en ese dominio según `capabilities.json`.
3. **Prioriza memoria RAG** si recupera nodos que contienen la respuesta.
4. **Cascada** al modelo `general` si el especialista dice no saber.

Correcciones aplicadas tras pruebas:
- MEMORY_KW solo términos de SIMBA (no "memoria" suelto, ambiguo).
- Especialista de memoria y general PROHIBIDOS de inventar sobre SIMBA:
  si no hay contexto, dicen "No tengo eso" / "No tengo esa información".

## Resultado de pruebas end-to-end

- `route "derivada de x al cubo"` → dominio matematicas, modelo qwen2.5:1.5b ✅
- `route "funcion python que sume n"` → dominio codigo, modelo qwen2.5:0.5b ✅
- `route "que es el enrutador en SIMBA"` → memoria + contexto, respuesta correcta ✅
- `route "color favorito de SIMBA"` (sin contexto) → cascada a general,
  NO alucina dato falso ✅

Limitación conocida: consultas creativas que contienen "memoria" (p.ej.
"metáfora sobre la memoria humana") pueden caer en el dominio memoria si el
clasificador LLM así lo etiqueta. La respuesta suele ser válida, pero la
intención del usuario era creatividad. Se puede afinar dando prioridad
explícita a creatividad cuando hay palabras de creatividad.

## Siguiente: Fase 3 — Cerebro completo

- Más dominios (ej. razonamiento, búsqueda web) y más modelos.
- Agregador final para consistencia entre especialistas.
- Re-examinar solo al agregar un modelo nuevo (la matriz se actualiza solo).
