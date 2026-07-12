# Kubernetes, contenedores y entrenamiento

> Respuesta a: "¿usar contenedores conectados como Kubernetes ahorra rendimiento
> y horas de entrenamiento al relacionar modelos?"

## Resumen directo

**No.** Kubernetes no reduce las horas de entrenamiento ni el hardware
*intrínseco* que necesita un modelo. Lo que reduce eso son las técnicas de
compresión/arquitectura (ver sección 5 de `docs/papers-clave.md`: destilación,
cuantización, LoRA, Mamba/RWKV, FlashAttention).

Lo que SÍ hace Kubernetes es **usar mejor los recursos que ya tenés**.

## Qué es Kubernetes realmente

K8s es un orquestador de contenedores. No entrena nada por sí solo: agenda
trabajo en nodos, reparte GPUs, reinicia lo que cae y escala según demanda.
Es infraestructura, no algoritmo de ML.

## Dónde ayuda de verdad (tu idea de "contenedores conectados")

Tu intuición de conectar módulos por red es correcta para el **cerebro modular**
de SIMBA, pero en el lado de *inferencia/servicio*, no de entrenamiento:

| Uso | Qué aporta K8s | Ahorra entrenamiento |
|---|---|---|
| Entrenar un modelo gigante | Distribuye en varias GPUs/nodos | ❌ No (los FLOPs son fijos) |
| Servir varios módulos (lógica/creatividad) | Cada módulo = microservicio, autoscale | ⚠️ Ahorra VRAM con vLLM/PagedAttention |
| Recuperar memoria (RAG) | Despliega la base vectorial aparte | ❌ No reduce FLOPs del modelo |
| Tolerancia a fallos | Usa instancias preemptivas baratas | ✅ Baja costo $ (no horas de cómputo) |

## La verdad sobre "ahorrar rendimiento"

- Las horas de entrenamiento están fijadas por: tamaño del modelo × datos ×
  algoritmo. K8s no cambia esa matemática.
- K8s ayuda a **no desperdiciar** recursos: ocupa GPUs ociosas, consolida
  cargas, usa spot instances (más baratas, pero pueden caer — K8s las reemplaza).
- Para SIMBA, el ahorro real viene de: modelo pequeño (Mixtral/Mamba),
  destilación, cuantización a 4-bit, y RAG en vez de modelo enorme.

## Dónde K8s SÍ encaja en SIMBA

1. **Brain modular en producción**: cada "órgano" (lógica, creatividad, memoria)
   como contenedor que se comunica por API. K8s maneja routing, scaling y
   health checks.
2. **Entrenamiento distribuido**: si algún día entrenás algo grande, K8s con
   operadores como Kubeflow/PyTorch Operator reparte el trabajo y sobrevive a
   caídas.
3. **Edge/local**: para tu PC, K8s es overkill; basta con Docker Compose o
   incluso procesos sueltos. K3s (K8s ligero) si querés aprender la API.

## Conclusión

- Para **reducir horas/hardware**: apuntá a compresión y arquitecturas eficientes
  (sección 5 de papers-clave).
- Para **relacionar módulos como cerebro**: K8s es la herramienta de
  orquestación correcta, pero en servicio, no en el cálculo del entrenamiento.

## Aclaración importante: K8s NO acorta la latencia

Confusión común: creer que K8s hace que el modelo "responda más rápido".
**No es así.**

| Concepto | Qué mide | K8s lo mejora |
|---|---|---|
| **Latencia** (tiempo de respuesta de UN pedido) | Cuánto tarda una respuesta | ❌ No (a veces suma red) |
| **Throughput** (cantidad de pedidos a la vez) | Cuántos atiende en paralelo | ✅ Sí (más réplicas) |
| **Disponibilidad** | Que no se caiga | ✅ Sí |

- K8s **no hace que un modelo piense más rápido**. Lo que acorta la respuesta es:
  modelo más chico/cuantizado, GPU rápida, motor de serving eficiente
  (vLLM/Ollama/TensorRT) y arquitectura eficiente (Mamba/RWKV).
- K8s ayuda a la *sensación* de fluidez cuando hay **varios módulos**: los tiene
  activos y enruta sin *cold start*; y si mucha gente usa el sistema a la vez,
  crea réplicas para no encolar.
- En tu **PC local**, K8s es puro overhead: no acelera, solo gasta recursos.
  Ahí alcanza con procesos sueltos o Docker Compose.

> Regla: la velocidad de cada respuesta la decide tamaño del modelo + hardware +
> motor de serving. K8s decide cuánta carga aguanta el sistema completo.

## Tu idea: cerebro de especialistas enrutados (ver `notes/arquitectura-especialistas.md`)

Como la latencia no nos favorece con un modelo grande, la alternativa real es
**varios modelos chicos especializados** con un enrutador: el que no sabe de un
tema llama al que sí. Eso es Mixture of Experts a nivel sistema. Detallado en el
note dedicado.
