# Arquitectura de especialistas enrutados (SIMBA)

> Idea de Kharold: en vez de un modelo grande y lento, usar VARIOS modelos
> chicos, cada uno experto en algo. Si a alguien le preguntan mates y ese modelo
> no sabe, llama a otro que sí. Trabajamos con modelos chicos conectados.
> Conviene a la hora de rendir: solo los conectamos.

## La intuición es correcta y tiene nombre

Es **Mixture of Experts (MoE) a nivel de sistema**, o **router-based ensemble**
/ **multi-agent routing**. Coincide con:

- Switch Transformers / Mixtral (MoE interno: un modelo con sub-redes).
- AutoGen / ChatDev (varios agentes con roles).
- Sistemas de *tool-use* / *orchestration* (un modelo decide a qué herramienta
  llamar).

## Por qué sí ahorra (a diferencia de K8s)

Un modelo gigante hace TODO el cómputo para CADA pedido, aunque el pedido sea
fácil. Con especialistas + router:

- Solo se ejecuta el experto relevante → **menos FLOPs por consulta**.
- Cada experto es chico → cabe en menos VRAM, corre más rápido.
- Podés tener un experto fuerte en mates y otro en creatividad, sin que el de
  mates "arrastre" al de creatividad.

Esto SÍ ataca la latencia y el hardware, que es lo que buscábamos.

## Esquema propuesto

```
        ┌─────────────┐
Usuario ─┤  Router /   │  (modelo chico que decide a quién delegar)
        │ Orquestador  │
        └──────┬──────┘
               │ enruta según el tema
   ┌───────────┼───────────────┐
   ▼           ▼               ▼
[Experto    [Experto      [Experto
 Mates]      Creatividad]   Memoria/RAG]
   │           │               │
   └───────────┼───────────────┘
               ▼
        Respuesta al usuario
```

- **Router**: recibe el pedido, clasifica la intención, delega. Puede ser un
  modelo chico o reglas simples (keywords).
- **Especialistas**: cada uno un modelo pequeño (p.ej. Mistral 7B, o Mixtral
  que ya es MoE). Uno puede ni siquiera ser LLM (p.ej. calculadora, buscador).
- **Memoria/RAG** (de `docs/papers-clave.md`): el módulo que da contexto
  asociativo (tu "gusano").

## Ventajas

- Latencia menor que un modelo gigante (solo corrés lo necesario).
- Hardware accesible: varios modelos chicos en una sola GPU mediana.
- Modular: podés mejorar un experto sin tocar los otros.
- "Cascada": un modelo que no sabe llama a otro — exactamente lo que dijiste.

## Riesgos / desafíos (para estudiar)

1. **Error de enrutamiento**: si el router manda mal, la respuesta es mala.
   Mitigación: router con confianza baja → preguntar al usuario o usar 2 expertos.
2. **Overhead de coordinación**: pasar contexto entre modelos cuesta tokens.
   Mitigación: prompts de handoff compactos.
3. **VRAM si los cargás todos a la vez**: si tenés 5 expertos de 7B cada uno,
   son ~35B de pesos en memoria. OPCIÓN: cargar bajo demanda (cold start) o
   cuantizar a 4-bit (GPTQ) para que quepan todos.
4. **Consistencia**: varios modelos pueden contradecirse. Mitigación: un
   "agregador" final que unifica.

## Relación con lo ya documentado

- `docs/papers-clave.md` → Switch Transformers, Mixtral, AutoGen, Mamba/RWKV.
- `notes/kubernetes-y-entrenamiento.md` → K8s orquesta estos contenedores en
  servicio, pero no acelera cada modelo.
- `notes/como-entrenar-ia.md` → por qué los Transformers no aprenden en uso y
  por eso necesitamos memoria externa (RAG) como módulo aparte.

## Próximo paso sugerido (cuando volvamos)

Prototipar el **router** en Python con Ollama local:
1. Un modelo chico clasifica la intención (mates / creatividad / memoria).
2. Llama al especialista correspondiente vía API.
3. Devuelve la respuesta.

Empezar con 2 especialistas + router, y crecer.
