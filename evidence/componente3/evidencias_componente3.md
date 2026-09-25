# Evidencias del Componente 3: Vibe Coding

Cada modelo sigue el ciclo *prompt → respuesta → ejecución → error → corrección → resultado*. Las conversaciones completas (todos los prompts, respuestas y estadísticas) están en:

- `gemma_conversacion_completa.txt`
- `qwen_conversacion_completa.txt`
- `cloud_conversacion_completa.txt`

## Gemma 4 E4B (local generalista, Ollama)

| Archivo | Qué muestra |
|---|---|
| `30_gemma_it1_prompt.png` | Prompt estándar enviado e inicio del razonamiento |
| `31_gemma_it1_stats.png` | Estadísticas de la iteración 1 (6 min 3 s, 3174 tokens) |
| `32_gemma_it1_ejecucion_404.png` | Ejecución de la v1: error 404 del endpoint inventado `/forecast_historical` |
| `33_gemma_it2_cortada_y_num_ctx.png` | Respuesta cortada por la ventana de contexto (3177 + 919 = 4096) y ampliación a `num_ctx 16384` |
| `34_gemma_it3_stats.png` | Estadísticas de la iteración 3 |
| `35_gemma_it3_ejecucion_404.png` | Ejecución de la v3: error 404 del endpoint inventado `/historical` |
| `36_gemma_it4_stats.png` | Estadísticas de la iteración 4 (21 min, 2.94 tok/s) |
| `37_gemma_it4_syntaxerror.png` | Ejecución de la v4: `SyntaxError` |
| `38_gemma_it5_stats.png` | Estadísticas de la iteración 5 |
| `39_gemma_it5_ejecucion.png` | Ejecución de la v5: vuelve el 404 (no resuelto) |
| `40_gemma_prueba_sin_wifi.png` | Manejo del error de conexión (sin wifi) |
| `41_gemma_intervencion_humana.png` | Programa funcionando tras 3 cambios humanos |
| `42_gemma_grafica_intervencion.png` | Gráfica generada con la intervención humana |

## Qwen2.5-Coder 7B (local de código, Ollama)

| Archivo | Qué muestra |
|---|---|
| `50_qwen_num_ctx_y_prompt.png` | `num_ctx 16384` configurado desde el inicio y prompt estándar |
| `51_qwen_it1_stats.png` | Estadísticas de la iteración 1 (3 min 46 s, 1670 tokens) |
| `52_qwen_it1_ejecucion_400.png` | Ejecución de la v1: error 400 (fechas fijas de 2023) |
| `53_qwen_it2_stats.png` | Estadísticas de la iteración 2 |
| `54_qwen_it2_ejecucion_400_detallado.png` | Error 400 detallado: `start_date` fuera de rango |
| `55_qwen_it3_stats.png` | Estadísticas de la iteración 3 |
| `56_qwen_it3_ejecucion_claves.png` | "Respuesta JSON no contiene las claves esperadas" (error de su propia validación) |
| `57_qwen_it4_stats.png` | Estadísticas de la iteración 4 |
| `58_qwen_it4_ejecucion.png` | Mismo error de claves |
| `59_qwen_it5_stats.png` | Estadísticas de la iteración 5 (10 min 3 s, 3.14 tok/s) |
| `60_qwen_it5_ejecucion.png` | Mismo error de claves (no resuelto) |
| `61_qwen_prueba_sin_wifi.png` | Manejo del error de conexión (mensaje técnico, sin wifi) |
| `62_qwen_intervencion_humana.png` | Programa funcionando tras 2 cambios humanos |
| `63_qwen_grafica_intervencion.png` | Gráfica generada con la intervención humana |

## Claude Opus 5.5 (cloud, chat incógnito, sin búsqueda web)

| Archivo | Qué muestra |
|---|---|
| `70_cloud_prompt.png` | Chat incógnito, modelo Opus 5.5 y prompt estándar |
| `71_cloud_respuesta_PT1.png` a `PT3.png` | Respuesta: autoverificación con datos simulados, decisiones de diseño y 5 pruebas sugeridas |
| `72_cloud_ejecucion.png` | Ejecución exitosa en la primera iteración (empate del máximo: 08/09 y 17/09) |
| `73_cloud_grafica.png` | Gráfica generada |
| `74_cloud_prueba_sin_wifi.png` | Manejo del error de conexión con mensaje claro |

**Nota:** `vibe_coding/gemma/solucion_v4.py` contiene intencionalmente el `SyntaxError` de la iteración 4. Se conserva sin modificar porque es evidencia del proceso.
