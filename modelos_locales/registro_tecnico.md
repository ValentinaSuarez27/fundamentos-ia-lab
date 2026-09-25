# Registro técnico del entorno: Componente 2

## 1. Equipo utilizado

| Campo | Valor |
|---|---|
| Integrante que ejecuta | Laura Valentina Suarez |
| Sistema operativo | Windows 11 |
| Procesador (CPU) | AMD Ryzen 7 7735HS with Radeon Graphics (8 núcleos, 16 procesadores lógicos, 3.20 GHz base) |
| RAM total | 19.7 GB utilizables |
| GPU dedicada / VRAM | No tiene GPU dedicada; GPU integrada AMD Radeon |
| Espacio libre en disco | 587 GB libres (SSD NVMe) |
| Versión de Ollama (`ollama --version`) | 0.34.2 |
| Versión de Python | 3.14.7 (pip 26.2.1), instalado con Python Install Manager |
| Versión de LM Studio | 0.4.24 (build 1); no se actualizó a 0.4.25 durante las pruebas para mantener las mismas condiciones |
| Fecha de las pruebas | 22/09/2026 |

## 2. Consultas estándar (idénticas en Ollama y LM Studio)

Se usan las mismas tres consultas, copiadas textualmente, en ambos entornos:

- **C1 (general):** Explica en máximo 5 líneas qué es una serie temporal y da un ejemplo de Colombia.
- **C2 (generación de código):** Escribe una función en Python llamada `media_movil(valores, ventana)` que reciba una lista de números y un entero, y devuelva la media móvil simple. Incluye un ejemplo de uso.
- **C3 (explicación de código):** Explica línea por línea qué hace este código: `[x**2 for x in range(10) if x % 2 == 0]`

## 3. Resultados por modelo

| Entorno | Modelo (tag exacto) | Parámetros | Cuantización | RAM/VRAM observada | CPU o GPU | Tiempo C1 | Tiempo C2 | Tiempo C3 | Tokens/s | ¿Respuesta correcta? |
|---|---|---|---|---|---|---|---|---|---|---|
| Ollama | gemma4:e4b | 8.0B | Q4_K_M | 9.4 GB RAM | 100% CPU | 53.95 s | 197.67 s (3 min 17 s) | 206.87 s (3 min 27 s) | 10.59 (C1) / 10.34 (C2) / 8.24 (C3) | Sí (C1, C2, C3) |
| Ollama | qwen2.5-coder:7b | 7.6B | Q4_K_M | 5.1 GB RAM | 100% CPU | 17.36 s | 28.37 s | 41.78 s | 7.28 (C1) / 7.58 (C2) / 7.01 (C3) | Sí (C1, C3); C2 parcialmente (falla con ventana ≤ 0) |
| LM Studio | Qwen2.5-Coder-7B-Instruct-GGUF (lmstudio-community) | 7.6B | Q4_K_M (4.68 GB) | (ver Administrador de tareas) | GPU Offload 28/28 capas (GPU integrada) | ~8.5 s (1.61 s al primer token) | ~33.9 s (0.86 s al primer token) | ~21.7 s (0.85 s al primer token) | 7.54 (C1) / 9.89 (C2) / 9.68 (C3) | Sí (C1); C2 parcialmente (falla con ventana ≤ 0); C3 correcta pero incompleta |

**Modelos descargados (`ollama list`):** gemma4:e4b (9.6 GB, ID c6eb396dbd59) y qwen2.5-coder:7b (4.7 GB, ID dae161e27b0e).

**Detalle de la consulta C1 con gemma4:e4b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 53.95 s |
| load duration | 5.03 ms (el modelo ya estaba cargado) |
| prompt eval count | 35 tokens |
| prompt eval rate | 51.71 tokens/s |
| eval count | 564 tokens |
| eval duration | 53.26 s |
| eval rate | 10.59 tokens/s |

**Detalle de la consulta C2 con gemma4:e4b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 3 min 17.67 s |
| load duration | 7.94 s (el modelo se volvió a cargar en memoria) |
| prompt eval count | 218 tokens (incluye el historial de C1) |
| prompt eval rate | 60.97 tokens/s |
| eval count | 1924 tokens |
| eval duration | 3 min 6.15 s |
| eval rate | 10.34 tokens/s |

**Detalle de la consulta C3 con gemma4:e4b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 3 min 26.87 s |
| load duration | 5.10 ms (el modelo ya estaba cargado) |
| prompt eval count | 1201 tokens (213 en caché; incluye el historial de C1 y C2) |
| prompt eval duration | 29.25 s |
| prompt eval rate | 33.78 tokens/s |
| eval count | 1463 tokens |
| eval duration | 2 min 57.53 s |
| eval rate | 8.24 tokens/s |

**Ficha de gemma4:e4b (`ollama ps` y `ollama show`):**

| Dato | Valor |
|---|---|
| Arquitectura | gemma4 |
| Parámetros | 8.0B totales ("E4B" = ~4B efectivos) |
| Cuantización | Q4_K_M |
| Memoria ocupada (`ollama ps`) | 9.4 GB |
| Procesador | 100% CPU |
| Contexto cargado por Ollama | 4096 tokens |
| Contexto máximo del modelo | 131072 tokens |
| Capacidades | completion, vision, audio, tools, thinking |
| Parámetros de muestreo por defecto | temperature 1, top_k 64, top_p 0.95 |
| Licencia | Apache 2.0 |

**Ficha de qwen2.5-coder:7b (`ollama ps` y `ollama show`):**

| Dato | Valor |
|---|---|
| Arquitectura | qwen2 |
| Parámetros | 7.6B (modelo denso) |
| Cuantización | Q4_K_M |
| Memoria ocupada (`ollama ps`) | 5.1 GB |
| Procesador | 100% CPU |
| Contexto cargado por Ollama | 4096 tokens |
| Contexto máximo del modelo | 32768 tokens |
| Capacidades | completion, tools, insert |
| System prompt por defecto | "You are Qwen, created by Alibaba Cloud. You are a helpful assistant." |
| Licencia | Apache 2.0 |

**Detalle de la consulta C1 con qwen2.5-coder:7b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 17.36 s |
| load duration | 5.41 ms (el modelo ya estaba cargado) |
| prompt eval count | 49 tokens (48 en caché) |
| prompt eval duration | 0.32 s |
| eval count | 124 tokens |
| eval duration | 17.03 s |
| eval rate | 7.28 tokens/s |

**Detalle de la consulta C2 con qwen2.5-coder:7b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 28.37 s |
| load duration | 4.90 ms |
| prompt eval count | 227 tokens (172 en caché) |
| prompt eval duration | 2.10 s |
| prompt eval rate | 26.19 tokens/s |
| eval count | 199 tokens |
| eval duration | 26.25 s |
| eval rate | 7.58 tokens/s |

**Detalle de la consulta C3 con qwen2.5-coder:7b (salida de `--verbose`):**

| Métrica | Valor |
|---|---|
| total duration | 41.78 s |
| load duration | 4.83 ms |
| prompt eval count | 466 tokens (425 en caché) |
| prompt eval duration | 1.68 s |
| prompt eval rate | 24.39 tokens/s |
| eval count | 281 tokens |
| eval duration | 40.08 s |
| eval rate | 7.01 tokens/s |

**Resumen comparativo en Ollama (mismas 3 consultas, misma sesión por modelo):**

| Métrica | gemma4:e4b | qwen2.5-coder:7b |
|---|---|---|
| Tiempo C1 / C2 / C3 | 54 s / 3 min 17 s / 3 min 27 s | 17 s / 28 s / 42 s |
| Tiempo total de las 3 consultas | ~7 min 38 s | ~1 min 27 s |
| RAM ocupada | 9.4 GB | 5.1 GB |
| Parámetros / cuantización | 8.0B (~4B efectivos) / Q4_K_M | 7.6B / Q4_K_M |
| Capacidades | completion, vision, audio, tools, thinking | completion, tools, insert |
| Tokens generados C1 / C2 / C3 | 564 / 1924 / 1463 | 124 / 199 / 281 |
| Velocidad promedio | ~9.7 tokens/s | ~7.3 tokens/s |
| Modo de razonamiento | Sí (en inglés, por defecto) | No |
| Calidad del código (C2) | Robusto: valida casos límite | Correcto en casos normales; falla con ventana ≤ 0 |
| Calidad de explicaciones (C1, C3) | Más completas y con simulación paso a paso | Correctas pero más breves |

**Configuración de carga en LM Studio (Qwen2.5-Coder 7B):**

| Parámetro | Valor |
|---|---|
| Context Length | 8192 (el modelo admite hasta 32768) |
| GPU Offload | 28 capas (todas las capas del modelo) |
| CPU Thread Pool Size | 6 |
| Evaluation Batch Size | 2048 |
| Physical Batch Size | 512 |
| Max Concurrent Predictions | 4 (experimental) |

**Detalle de la consulta C1 en LM Studio:**

| Métrica | Valor |
|---|---|
| Velocidad | 7.54 tok/sec |
| Tokens generados | 52 |
| Tiempo al primer token | 1.61 s |
| Tiempo total estimado | ~8.5 s (1.61 s + 52 tokens ÷ 7.54 tok/s) |
| Stop reason | EOS Token Found (terminó de forma natural) |

**Detalle de la consulta C2 en LM Studio:**

| Métrica | Valor |
|---|---|
| Velocidad | 9.89 tok/sec |
| Tokens generados | 327 |
| Tiempo al primer token | 0.86 s |
| Tiempo total estimado | ~33.9 s (0.86 s + 327 tokens ÷ 9.89 tok/s) |
| Stop reason | EOS Token Found |

**Cómo obtener cada dato:**
- **Parámetros y cuantización:** `ollama show <modelo>` (en LM Studio aparecen en la ficha del modelo).
- **RAM observada:** `ollama ps` (columna SIZE) o el Administrador de tareas mientras el modelo responde.
- **CPU o GPU:** `ollama ps` (columna PROCESSOR).
- **Tiempo y tokens/s:** `ollama run <modelo> --verbose` (líneas "total duration" y "eval rate"). En LM Studio, las estadísticas aparecen debajo de cada respuesta.

## 4. Verificación del código generado (C2)

El código de ambos modelos se transcribió sin modificaciones a `verificacion/gemma_media_movil.py` y `verificacion/qwen_media_movil.py`, con una sección de pruebas agregada por el equipo. Se ejecutó con Python 3.14.7 el 22/09/2026.

| Prueba | gemma4:e4b | qwen2.5-coder:7b |
|---|---|---|
| Ejemplo del propio modelo | ✅ `12.33, 12.67, 11.67, 11.33, 13.00` | ✅ `[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]` |
| Caso normal (serie cruzada) | ✅ `[2.0, 3.0, ..., 9.0]` | ✅ `[12.33, 12.67, 11.67, 11.33, 13.0]` (sin redondear) |
| Lista más corta que la ventana | ✅ Advertencia y devuelve `[]` | ✅ `ValueError` controlado |
| Ventana = 0 | ✅ `ValueError`: "La ventana debe ser un entero positivo." | ❌ `ZeroDivisionError: division by zero` |
| Ventana = -2 | ✅ `ValueError` controlado | ❌ Devuelve `[-1.5, -2.5, -0.0, -0.0, -0.0, -0.0, -0.0]` sin error |

**Conclusión de la verificación:** ambos modelos resuelven correctamente el caso típico, pero solo Gemma maneja las entradas inválidas. El código de Qwen, aunque parece correcto a simple vista, produce resultados silenciosamente erróneos con ventanas negativas. Esto confirma la necesidad de la verificación humana del código generado por IA.

**Detalle de la consulta C3 en LM Studio:**

| Métrica | Valor |
|---|---|
| Velocidad | 9.68 tok/sec |
| Tokens generados | 202 |
| Tiempo al primer token | 0.85 s |
| Tiempo total estimado | ~21.7 s (0.85 s + 202 tokens ÷ 9.68 tok/s) |
| Stop reason | EOS Token Found |

**Comparación del mismo modelo (Qwen2.5-Coder 7B, Q4_K_M) en ambos runtimes:**

| Métrica | Ollama | LM Studio |
|---|---|---|
| Procesador | 100% CPU | GPU integrada (28/28 capas) |
| Contexto cargado | 4096 | 8192 |
| Velocidad C1 / C2 / C3 (tok/s) | 7.28 / 7.58 / 7.01 | 7.54 / 9.89 / 9.68 |
| Velocidad promedio | ~7.3 tok/s | ~9.0 tok/s |
| Tiempo total C1 / C2 / C3 | 17.4 s / 28.4 s / 41.8 s | ~8.5 s / ~33.9 s / ~21.7 s |
| Tokens generados C1 / C2 / C3 | 124 / 199 / 281 | 52 / 327 / 202 |
| Código C2 con ventana -2 | Resultados erróneos en silencio | `ZeroDivisionError` |
| Métricas disponibles | Completas (`--verbose`) | Básicas (tok/s, tokens, primer token) |
| Interfaz | Terminal (CLI) | Gráfica (GUI) |

**Código de Qwen en LM Studio (`verificacion/lmstudio_qwen_media_movil.py`)** — ejecutado con Python 3.14.7 el 22/09/2026 (evidencia `10b_lmstudio_C2_ejecucion.png`):

| Prueba | Resultado obtenido |
|---|---|
| Ejemplo del modelo `[1..9]`, ventana 3 | ✅ `[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]` (coincide con el comentario `# Output` del modelo) |
| Caso normal (ventas), ventana 3 | ✅ `[12.33, 12.67, 11.67, 11.33, 13.0]` (sin redondear) |
| Lista más corta que la ventana | ✅ `ValueError` controlado |
| Ventana = 0 | ❌ `ZeroDivisionError` |
| Ventana = -2 | ❌ `ZeroDivisionError` (falla, pero al menos no devuelve resultados erróneos en silencio) |

## 5. Consumo de los modelos desde Python (API local)

Arquitectura demostrada:

```
MODELO → OLLAMA / LM STUDIO (runtime) → API LOCAL (HTTP) → APLICACIÓN PYTHON
```

Librería usada: `requests` 2.34.2 (`pip install -r requirements.txt`). Se envió la misma consulta C2 con **temperatura 0.2**.

### 5.1 `ollama_test.py` → Ollama (`http://localhost:11434/api/chat`) — 23/09/2026

| Métrica | Valor |
|---|---|
| Modelo | qwen2.5-coder:7b |
| Tiempo medido por Python | 70.17 s |
| Tiempo total reportado por Ollama | 68.12 s |
| Tiempo de carga del modelo | 12.20 s (carga en frío tras reiniciar el equipo) |
| Tokens de entrada | 74 (incluye el prompt del sistema del modelo) |
| Tokens generados | 447 |
| Velocidad de generación | 8.38 tokens/s |

**Observaciones:**
- La API respondió correctamente: la verificación del servidor devolvió "Ollama is running" y el programa recibió la respuesta completa en formato JSON (`stream: false`).
- La diferencia de ~2 s entre el tiempo medido por Python y el reportado por Ollama corresponde a la comunicación HTTP y al procesamiento del JSON.
- El tiempo de carga (12.2 s) es alto porque el modelo no estaba en memoria: fue la primera consulta después de reiniciar el equipo.
- **Efecto de la temperatura:** con temperatura 0.2 (frente a la temperatura por defecto en la prueba interactiva), Qwen generó un código más robusto. Esta vez sí valida `ventana <= 0` con `ValueError` e incluye docstring.
- **Error detectado en la respuesta:** el comentario `# Salida: [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]` es incorrecto. Para `[1..10]` con ventana 3 la salida real es `[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]` (8 valores, no 7). El modelo "inventó" la salida sin calcularla, un ejemplo de alucinación. También usa el nombre `media_movel` (portugués) en lugar de `media_movil`.

### 5.2 `lmstudio_test.py` → LM Studio (`http://localhost:1234/v1/chat/completions`, formato OpenAI) — 23/09/2026

Servidor: pestaña Developer → Local Server, **Status: Running**, accesible en `http://127.0.0.1:1234`. El modelo quedó en estado READY (identificador de API `qwen2.5-coder-7b-instruct`, 4.68 GB, Parallel 4). La consulta a `GET /v1/models` desde el navegador devolvió un JSON con dos modelos: `qwen2.5-coder-7b-instruct` y `text-embedding-nomic-embed-text-v1.5`. Este último es un modelo de embeddings que LM Studio incluye por defecto (categoría "Embeddings" de la cartografía).

| Métrica | Valor |
|---|---|
| Modelo | qwen2.5-coder-7b-instruct (seleccionado automáticamente por el programa) |
| Tiempo total medido por Python | 59.14 s |
| Tokens de entrada | 74 |
| Tokens generados | 554 |
| Velocidad aproximada | 9.37 tokens/s (incluye el tiempo al primer token) |
| Tokens de razonamiento (log del servidor) | 0 |

**Observaciones:**
- La respuesta JSON del servidor (visible en *Developer Logs*) coincide con las métricas que calculó el programa: `prompt_tokens: 74`, `completion_tokens: 554`, `total_tokens: 628`.
- El código generado es correcto y robusto: valida `ventana <= 0` y lista más corta que la ventana (ambos con `ValueError`), incluye docstring y un ejemplo con salida correcta: `[1..9]` con ventana 3 da `[2.0, ..., 8.0]` (7 valores). También explica paso a paso el cálculo. Detalle menor: nombra la variable `medias_moving`, que mezcla español e inglés.
- Igual que en Ollama, la temperatura 0.2 produjo código más robusto que en las pruebas interactivas con la temperatura por defecto.

### 5.3 Comparación de las APIs locales (mismo modelo y prompt, temperatura 0.2)

| Aspecto | Ollama | LM Studio |
|---|---|---|
| Endpoint | `POST /api/chat` (API propia) | `POST /v1/chat/completions` (compatible con OpenAI) |
| Puerto | 11434 | 1234 |
| Inicio del servidor | Automático al abrir Ollama | Manual (Developer → Status: Running) |
| Métricas en la respuesta | Detalladas, en nanosegundos (carga, prompt, generación) | Solo conteo de tokens (`usage`) |
| Tiempo total | 70.17 s (incluye 12.2 s de carga en frío) | 59.14 s (modelo ya cargado) |
| Tokens generados | 447 | 554 |
| Velocidad | 8.38 tok/s | ~9.37 tok/s |
| Valida ventana ≤ 0 | Sí | Sí |
| Salida del ejemplo | ❌ Comentario incorrecto (alucinación) | ✅ Correcta |

**Conclusión del Componente 2:** ambos runtimes permiten consumir el mismo modelo desde Python mediante una API HTTP local, lo que demuestra la cadena **modelo → runtime → API local → aplicación**. LM Studio fue más rápido en este equipo gracias al uso de la GPU integrada, y su API compatible con OpenAI facilita cambiar a un modelo en la nube modificando solo la URL. Ollama ofrece métricas más completas y un servidor que arranca automáticamente. En todas las pruebas, el código generado necesitó verificación humana: la calidad dependió del runtime, de la temperatura y de la aleatoriedad del muestreo, no solo del modelo.

## 6. Observaciones

- Instalación verificada: `ollama --version` devolvió 0.34.2 y http://localhost:11434 respondió "Ollama is running" (evidencias 02 y 03).
- Descarga de modelos sin errores (evidencia 04).
- Gemma 4 E4B activa por defecto un modo de razonamiento (*thinking*) en inglés antes de responder. En C1 generó 564 tokens para una respuesta corta, lo que explica los ~54 s de respuesta. La respuesta final, en español, fue correcta (definición, tendencia/estacionalidad y ejemplos colombianos: petróleo, IPC, turismo), pero excedió levemente el límite de 5 líneas pedido.
- Antes de las pruebas, el sistema tenía 10.1 GB de RAM ocupados de 19.7 GB, por lo que se cerraron aplicaciones para liberar memoria antes de ejecutar los modelos.
- **C2 con gemma4:e4b.** El modelo generó una función `media_movil` correcta y documentada. Incluye docstring, type hints, validación de la ventana (entero positivo, con `ValueError`), manejo de listas más cortas que la ventana y un ejemplo de uso con ventas diarias. Con `[10, 12, 15, 11, 9, 14, 16]` y ventana 3, el resultado esperado es `[12.33, 12.67, 11.67, 11.33, 13.0]` según el cálculo manual. Confirmado al ejecutarlo en el equipo (evidencia `05b_gemma_C2_ejecucion.png`).
- **Tiempos de C2.** La respuesta tardó 3 min 17 s porque el modelo generó 1924 tokens: gran parte correspondió al razonamiento en inglés, que incluso contenía un borrador completo del código antes de la versión final. La velocidad se mantuvo estable (~10.3 tokens/s), igual que en C1, lo que indica que el cuello de botella es la CPU.
- **Recarga del modelo.** El `load duration` de 7.94 s indica que el modelo se descargó de memoria entre C1 y C2. Ollama libera el modelo tras unos minutos de inactividad.
- **Detalle de diseño.** La función imprime una advertencia con `print` dentro de la lógica. En código de producción sería preferible lanzar una excepción o usar `logging`, pero para el laboratorio es aceptable.
- **C3 con gemma4:e4b.** La explicación fue correcta y bien estructurada. Descompuso la comprensión de listas en sus componentes (`range(10)`, `for`, filtro `if x % 2 == 0`, expresión `x**2` y corchetes), simuló la ejecución paso a paso y dio el resultado correcto: `[0, 4, 16, 36, 64]`. Tuvo un error menor de redacción: dice que `%` "resta el residuo de una división", cuando lo correcto es que *devuelve* el residuo.
- **Degradación por contexto acumulado.** Las tres consultas se hicieron en la misma sesión, así que en C3 el modelo tuvo que procesar 1201 tokens de entrada (todo el historial) frente a 35 en C1. Esto agregó 29 s solo en leer el prompt y redujo la velocidad de generación de ~10.5 a 8.24 tokens/s. Es una evidencia práctica de cómo la ventana de contexto afecta el rendimiento en CPU.
- **Ejecución 100% en CPU.** `ollama ps` confirmó que el modelo corre totalmente en CPU (la GPU integrada AMD Radeon no se utiliza) y ocupa 9.4 GB de RAM. Esto explica la velocidad de ~8-10 tokens/s.
- **Contexto cargado frente a contexto máximo.** Aunque el modelo admite 131072 tokens, Ollama lo cargó con 4096 por defecto para ahorrar memoria. Ampliarlo (`/set parameter num_ctx`) aumentaría el consumo de RAM.
- **Parámetros vs. "E4B".** `ollama show` reporta 8.0B parámetros totales. El nombre "E4B" se refiere a ~4B parámetros *efectivos* por token, no al tamaño total del archivo.
- **Temperatura.** El modelo usa por defecto temperature 1 (salida relativamente creativa). Para generar código podría bajarse a ~0.2 para obtener respuestas más deterministas.
- **C1 con qwen2.5-coder:7b.** Respondió en 17 s, unas 3 veces más rápido que Gemma (54 s), porque no tiene modo de razonamiento: generó solo 124 tokens frente a 564. La definición fue correcta y respetó el límite de 5 líneas, con un ejemplo válido (población de Colombia 1950-2020). Fue menos completa que la de Gemma, ya que no mencionó tendencia ni estacionalidad.
- **Velocidad por token: Qwen más lento que Gemma.** Qwen generó a 7.28 tokens/s frente a ~10.5 de Gemma. Qwen2.5-Coder 7B es un modelo denso (usa todos sus ~7.6B parámetros en cada token), mientras que Gemma 4 E4B activa ~4B parámetros efectivos por token. Menos parámetros activos implican menos cálculo por token en CPU. Aun así, Qwen terminó antes porque escribió mucho menos.
- **Caché del prompt.** El `prompt eval cached` de 48 tokens indica que el prompt ya estaba en caché de una ejecución previa. Por eso el `prompt eval rate` (3.15 tokens/s) no es representativo: solo se procesó 1 token nuevo.
- **C2 con qwen2.5-coder:7b.** Respondió en 28 s, unas 7 veces más rápido que Gemma (3 min 17 s), con un código corto y directo (199 tokens frente a 1924). La lógica principal es correcta: con `[1..10]` y ventana 3 debe producir `[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]`. Sin embargo, es menos robusta que la de Gemma:
  - Solo valida que la ventana no sea mayor que la lista; **no valida ventana ≤ 0**. Con `ventana=0` lanza `ZeroDivisionError`, y con `ventana=-2` devuelve resultados sin sentido (`[-1.5, -2.5, -0.0, ...]`) **sin avisar del error**.
  - No incluye docstring, type hints ni la salida esperada del ejemplo.
  - Usa el nombre de variable `medias_móviles` con tilde; Python 3 lo permite, pero no es una buena práctica.
  Estos casos se confirmaron al ejecutar el código en el equipo (evidencia `07b_qwen_C2_ejecucion.png`).
- **Conclusión parcial C2.** Qwen es mucho más rápido, pero su código requiere más revisión humana. Gemma tarda más, pero anticipa casos límite. Esto ilustra el principio del laboratorio: el código generado por IA debe ejecutarse y verificarse.
- **C3 con qwen2.5-coder:7b.** Explicación correcta y concisa en 42 s (frente a 3 min 27 s de Gemma), con el resultado correcto `[0, 4, 16, 36, 64]`. Agrupó el código en dos bloques en lugar de ir componente por componente y no simuló la ejecución paso a paso. Usa el término "lista comprensiva", una traducción literal; el término habitual en español es "comprensión de listas".
- **Contexto en Qwen.** Como Qwen genera respuestas cortas, el historial creció poco (466 tokens en C3, casi todos en caché). Por eso su velocidad se mantuvo estable (7.0-7.6 tokens/s), a diferencia de Gemma, que bajó de 10.6 a 8.2 tokens/s.
- **Conclusión de la Parte A.** Qwen2.5-Coder es ~5 veces más rápido en tiempo total, pero Gemma 4 produce respuestas más completas y código más robusto, a costa de mucho más tiempo por su modo de razonamiento. Para el Componente 3 conviene considerar desactivar el razonamiento de Gemma o usar temperatura baja para hacer la comparación más equilibrada.
- **Ficha de Qwen.** Qwen ocupa 5.1 GB de RAM (casi la mitad que Gemma, 9.4 GB) y también corre 100% en CPU. Su capacidad `insert` (*fill-in-the-middle*) le permite completar código en medio de un archivo, útil para autocompletado en editores. No tiene capacidades de visión, audio ni razonamiento, lo que confirma que es un modelo especializado en código y no un generalista.
- **LM Studio: elección del modelo.** Se usó el mismo modelo y la misma cuantización que en Ollama (Qwen2.5-Coder 7B, Q4_K_M) para que las diferencias medidas se deban al runtime y no al modelo. Se eligió Qwen y no Gemma por ser más liviano y rápido.
- **LM Studio: uso de GPU.** A diferencia de Ollama (100% CPU), LM Studio detectó la GPU integrada AMD Radeon ("Full GPU Offload Possible") y cargó las 28 capas del modelo en ella. Sin embargo, la velocidad fue prácticamente igual: 7.54 tok/s frente a 7.28 en Ollama. La explicación más probable es que una GPU integrada no tiene memoria propia: comparte la RAM del sistema, y la generación de texto está limitada por el ancho de banda de memoria más que por la capacidad de cálculo.
- **LM Studio: contexto y respuesta.** LM Studio cargó el modelo con 8192 tokens de contexto, el doble que Ollama (4096). La respuesta a C1 fue más corta que en Ollama (52 frente a 124 tokens), aunque igualmente correcta, con el ejemplo de los precios del café en Colombia (2010-2023). Con el mismo modelo, las respuestas varían entre runtimes por diferencias en el prompt del sistema, la plantilla de chat y los parámetros de muestreo por defecto.
- **LM Studio: presentación de estadísticas.** LM Studio muestra menos métricas que `ollama run --verbose`: no reporta el tiempo total ni el tiempo de lectura del prompt por separado, sino tok/sec, tokens, tiempo al primer token y motivo de parada (se consultan con el ícono de cronómetro debajo de cada respuesta).
- **C2 en LM Studio vs. Ollama (mismo modelo).** Con el mismo Qwen2.5-Coder 7B, LM Studio generó un código distinto al de Ollama: divide entre `len(subconjunto)` en lugar de `ventana` e incluye el resultado esperado como comentario. Tampoco valida ventanas ≤ 0, pero con ventana negativa falla con `ZeroDivisionError` en lugar de devolver valores erróneos en silencio. Esto muestra que un mismo modelo puede producir código diferente según el runtime y la aleatoriedad del muestreo.
- **Velocidad en C2.** LM Studio alcanzó 9.89 tok/s frente a 7.58 en Ollama con el mismo modelo, una mejora de ~30% que podría deberse al uso de la GPU integrada. Como en C1 la diferencia fue mínima (7.54 frente a 7.28), el resultado no es concluyente con una sola medición. Para confirmarlo habría que repetir las consultas varias veces.
- **C3 en LM Studio.** Explicación correcta y clara: usa el término adecuado ("comprensión de lista"), explica el `for`, el filtro `%` y la expresión `x**2`, y concluye que genera los cuadrados de los pares entre 0 y 9. Sin embargo, no muestra la lista resultante `[0, 4, 16, 36, 64]` ni explica el papel de los corchetes, por lo que es menos completa que las respuestas en Ollama.
- **Velocidad en LM Studio: tendencia confirmada.** En C2 y C3, LM Studio fue consistentemente ~30% más rápido que Ollama con el mismo modelo (9.89 y 9.68 frente a 7.58 y 7.01 tok/s). La excepción fue C1, una respuesta muy corta (52 tokens) en la que probablemente influyó el arranque inicial. La explicación más probable es que LM Studio aprovechó la GPU integrada (GPU Offload 28/28), mientras que Ollama usó solo CPU. Aunque la GPU integrada comparte la RAM del sistema, puede procesar en paralelo mejor que la CPU. Para confirmarlo con más rigor, se recomienda repetir cada consulta varias veces y promediar.
- **Conclusión de la Parte B.** Con el mismo modelo y la misma cuantización, el runtime sí importa: LM Studio fue más rápido en este equipo gracias al uso de la GPU integrada y ofrece una interfaz gráfica más accesible, mientras que Ollama da métricas más completas y es más práctico desde la terminal. En ambos casos, el código generado requirió verificación humana.
