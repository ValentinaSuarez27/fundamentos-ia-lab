# Componente 1: Cartografía del ecosistema de modelos de IA

**Curso:** Fundamentos de Inteligencia Artificial, Ingeniería de Sistemas
**Fecha de verificación de los datos:** 22 de septiembre de 2026
**Archivo de datos:** `modelos.csv` (misma información, con la columna de fuente y la fecha)

## 1. Alcance y método

Se investigaron 20 modelos actuales repartidos en las seis categorías exigidas: texto/generalistas, razonamiento, desarrollo de software, visión/multimodalidad, voz (STT/TTS) y embeddings. En cada categoría se incluyó al menos una alternativa **local (open-weight)** y una **cloud (propietaria)**, porque la pregunta central del laboratorio pide elegir según recursos, privacidad y costo, y esa comparación solo es posible si hay opciones de ambos lados.

Los datos de tamaño, contexto y precio se tomaron de fuentes oficiales: la biblioteca de Ollama, las páginas de precios de OpenAI, Anthropic y Google, las fichas de Hugging Face y los repositorios de los fabricantes. Cuando un dato solo aparece en una fuente secundaria, la columna "Tipo de fuente" del CSV lo indica. Los precios están en USD por millón de tokens (1M) y corresponden al nivel estándar, sin descuentos por lote (batch) ni caché.

## 2. Matriz comparativa

| # | Categoría | Modelo | Proveedor | Tipo | Local / Cloud | Tamaño / Contexto | Hardware | API / Costo | Uso recomendado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Texto / generalista | [Gemma 4 E4B (gemma4:e4b)](https://ollama.com/library/gemma4:e4b) | Google DeepMind | LLM/SLM multimodal (texto, imagen, audio) | Local (Ollama, LM Studio) | ~4B efectivos; 9.6 GB en disco; contexto 128K | ~10 GB VRAM o 16 GB RAM / Apple Silicon | Gratis, open-weight (Apache 2.0) | Generalista local para portátil de 16 GB; chat, explicación de código, prototipos privados |
| 2 | Texto / generalista | [Gemma 4 E2B (gemma4:e2b)](https://ollama.com/library/gemma4) | Google DeepMind | SLM multimodal | Local (Ollama, LM Studio) | ~2B efectivos; 7.2 GB en disco; contexto 128K | 8 GB RAM (lento en CPU) | Gratis, open-weight (Apache 2.0) | Equipos modestos; pruebas rápidas del Comp. 2 |
| 3 | Texto / generalista | [Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/pricing) | Anthropic | LLM propietario | Cloud (API) | No publicado; contexto 1M | No aplica (servidor del proveedor) | USD 2 entrada / 10 salida por 1M tokens | Generalista cloud con buena relación calidad/costo; redacción y análisis |
| 4 | Texto / generalista | [GPT-6 Sol](https://developers.openai.com/api/docs/pricing) | OpenAI | LLM propietario | Cloud (API) | No publicado; contexto: verificar en ficha oficial | No aplica | USD 2 entrada / 10 salida por 1M tokens (Standard) | Generalista cloud; tareas diarias y agentes |
| 5 | Razonamiento | [DeepSeek-R1 7B (deepseek-r1)](https://ollama.com/library/deepseek-r1) | DeepSeek | LLM de razonamiento (destilado) | Local (Ollama) | 7B; 4.7 GB en disco | ~8 GB RAM | Gratis, open-weight | Matemáticas y lógica paso a paso en equipo modesto |
| 6 | Razonamiento | [gpt-oss-20b](https://developers.openai.com/cookbook/articles/gpt-oss/run-locally-ollama) | OpenAI | LLM de razonamiento open-weight (MoE) | Local (Ollama, LM Studio) | 21B totales / 3.6B activos; ~13 GB; contexto 131K; cuantización MXFP4 | ≥16 GB VRAM o memoria unificada | Gratis, open-weight (Apache 2.0) | Razonamiento y uso de herramientas en local con GPU media/alta |
| 7 | Razonamiento | [Claude Opus 5.5](https://platform.claude.com/docs/en/about-claude/pricing) | Anthropic | LLM propietario de razonamiento | Cloud (API) | No publicado; contexto 1M | No aplica | USD 4 entrada / 20 salida por 1M tokens | Problemas complejos, agentes de larga duración |
| 8 | Razonamiento | [Gemini 3.1 Pro (preview)](https://ai.google.dev/gemini-api/docs/pricing) | Google | LLM multimodal de razonamiento | Cloud (API) | No publicado; contexto ≥1M (verificar) | No aplica | USD 2/12 por 1M tokens (≤200K); USD 4/18 (>200K); sin capa gratuita | Razonamiento multimodal y documentos largos |
| 9 | Desarrollo de software | [Qwen2.5-Coder 7B (qwen2.5-coder:7b)](https://github.com/QwenLM/Qwen2.5-Coder) | Alibaba (Qwen) | Modelo de código | Local (Ollama, LM Studio) | 7.6B; contexto 32K por defecto (hasta 128K con YaRN) | ~8 GB RAM / ~6 GB VRAM | Gratis, open-weight (Apache 2.0) | Modelo 'local coding' viable en equipo de estudiante (Comp. 2 y 3) |
| 10 | Desarrollo de software | [Qwen3-Coder 30B (qwen3-coder:30b)](https://ollama.com/library/qwen3-coder) | Alibaba (Qwen) | Modelo de código (MoE) | Local (Ollama) | 30.5B totales / 3.3B activos; ~19 GB Q4_K_M; contexto 256K | 24 GB VRAM o Mac de 32 GB | Gratis, open-weight (Apache 2.0) | Coding local de alta calidad si hay GPU grande |
| 11 | Desarrollo de software | [GPT-5.3-Codex](https://developers.openai.com/api/docs/pricing) | OpenAI | Modelo de código propietario | Cloud (API, Codex) | No publicado | No aplica | USD 1.75 entrada / 14 salida por 1M tokens | Modelo 'cloud coding' del Comp. 3 (vía Codex) |
| 12 | Visión / multimodal | [Qwen3.6 27B (qwen3.6:27b)](https://ollama.com/library/qwen3.6/tags) | Alibaba (Qwen) | VLM / multimodal (texto + imagen) | Local (Ollama) | 27B; 18 GB; contexto 256K | 24 GB VRAM o Mac de 32 GB | Gratis, open-weight | Análisis de imágenes y capturas en local con privacidad |
| 13 | Visión / multimodal | [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/pricing) | Google | Multimodal propietario | Cloud (API) | No publicado; contexto: verificar | No aplica | Capa gratuita; pago: USD 0.75/3.75 por 1M hasta 31/12/2026 (luego 1.50/7.50) | Multimodal cloud barato; prototipos con imágenes/video |
| 14 | Voz (STT) | [Whisper large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) | OpenAI | Speech-to-Text | Local (Python/transformers) y cloud vía terceros | ~809M parámetros | ~1.8 GB VRAM en FP16; funciona en CPU | Gratis, open-weight | Transcripción local de audio en español |
| 15 | Voz (STT) | [gpt-transcribe](https://developers.openai.com/api/docs/pricing) | OpenAI | Speech-to-Text propietario | Cloud (API) | No publicado | No aplica | ~USD 0.0045 por minuto | Transcripción cloud sin hardware propio |
| 16 | Voz (TTS) | [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | hexgrad | Text-to-Speech | Local (Python) | 82M parámetros | CPU suficiente | Gratis, open-weight (Apache 2.0) | Síntesis de voz local ligera (soporte parcial de español) |
| 17 | Voz (TTS) | [Gemini 3.1 Flash TTS (preview)](https://ai.google.dev/gemini-api/docs/pricing) | Google | Text-to-Speech propietario | Cloud (API) | No publicado | No aplica | Capa gratuita; pago: USD 1 texto entrada / 20 audio salida por 1M tokens | Voz controlable en la nube |
| 18 | Embeddings | [nomic-embed-text](https://ollama.com/library/nomic-embed-text) | Nomic AI | Embeddings de texto | Local (Ollama) | 137M; 274 MB; contexto 8192 (Ollama carga 2048 por defecto) | CPU suficiente | Gratis, open-weight (Apache 2.0) | Búsqueda semántica / RAG local |
| 19 | Embeddings | [Qwen3-Embedding (0.6B / 4B / 8B)](https://ollama.com/library/qwen3-embedding) | Alibaba (Qwen) | Embeddings multilingües (100+ idiomas, incluye código) | Local (Ollama) | 0.6B a 8B según variante | 0.6B: CPU; 8B: GPU recomendada | Gratis, open-weight | RAG multilingüe y búsqueda de código |
| 20 | Embeddings | [text-embedding-3-small](https://www.cloudzero.com/blog/openai-pricing/) | OpenAI | Embeddings propietario | Cloud (API) | No publicado | No aplica | ~USD 0.02 por 1M tokens | Embeddings cloud muy baratos a gran escala |

**Notas de lectura.** "No publicado" significa que el proveedor no revela el número de parámetros de sus modelos cerrados, que es lo normal en modelos propietarios. En los modelos locales, el hardware indicado es aproximado para la cuantización por defecto (normalmente Q4) y un contexto moderado. Ampliar la ventana de contexto aumenta el consumo de memoria, y Ollama carga por defecto un contexto mucho menor que el máximo del modelo, así que hay que configurarlo con `num_ctx`.

## 3. Guía de selección por restricción

| Situación | Modelo sugerido | Razón |
|---|---|---|
| Portátil con 8 GB de RAM y sin GPU | Gemma 4 E2B, Qwen2.5-Coder 7B, DeepSeek-R1 7B | Caben en memoria con cuantización Q4; serán lentos, pero funcionan |
| Portátil con 16 GB de RAM | Gemma 4 E4B (general) + Qwen2.5-Coder 7B (código) | Buen equilibrio; cubren el Componente 2 completo |
| GPU de 24 GB o Mac de 32 GB | Qwen3-Coder 30B, Qwen3.6 27B, gpt-oss-20b | Calidad cercana a modelos cloud sin enviar datos afuera |
| Datos sensibles (privacidad) | Cualquier modelo local | Los datos nunca salen del equipo |
| Presupuesto cero y sin hardware | Capa gratuita de Gemini Flash | Única opción cloud gratuita con límites de uso |
| Máxima calidad en programación | GPT-5.3-Codex, Claude Opus 5.5 | Mejor desempeño, pero con costo por token y dependencia de internet |
| Transcribir audio | Whisper large-v3-turbo (local) o gpt-transcribe (cloud) | Whisper corre incluso en CPU; la opción cloud evita instalar nada |
| Búsqueda semántica / RAG | nomic-embed-text (local) o text-embedding-3-small (cloud) | Ambos son muy livianos o muy baratos |

## 4. Conclusión: ¿qué modelo usar para cada problema y por qué?

No existe un "mejor modelo" universal: la elección depende de cinco variables que tiran en direcciones distintas.

**Tarea.** Un modelo especializado de tamaño medio suele superar a un generalista del mismo tamaño en su dominio. Por eso, para el Componente 3 conviene comparar un generalista (Gemma 4) contra un especialista en código (Qwen2.5-Coder o Qwen3-Coder) del mismo orden de tamaño. Los embeddings y los modelos de voz no compiten con los LLM: resuelven otro tipo de problema.

**Recursos.** El hardware disponible es el primer filtro en local. La regla práctica es que, con Q4, cada mil millones de parámetros ocupa aproximadamente 0.6 GB, más el espacio de la ventana de contexto. Los modelos MoE (Qwen3-Coder 30B, gpt-oss-20b, Gemma 4 26B) activan solo una fracción de sus parámetros por token, lo que los hace rápidos, pero igual necesitan tener todos los pesos cargados en memoria.

**Privacidad.** Si los datos no pueden salir de la organización, la respuesta es local y open-weight, aunque se sacrifique algo de calidad.

**Costo.** Los modelos locales no cobran por token, pero consumen hardware y electricidad. Los modelos cloud cobran por uso: los tokens de salida cuestan de 5 a 8 veces más que los de entrada, y los modelos de razonamiento generan tokens de "pensamiento" que también se facturan como salida.

**Modalidad.** Si el problema incluye imágenes, audio o video, hay que filtrar por modelos multimodales o especializados (VLM, STT o TTS) antes de comparar la calidad.

**Decisión del equipo para el laboratorio.** El equipo de ejecución principal tiene un AMD Ryzen 7 7735HS, 19.7 GB de RAM utilizables y GPU AMD Radeon integrada (sin GPU dedicada), por lo que los modelos se ejecutan principalmente en CPU. Por eso se eligió la siguiente configuración:

- **Generalista local:** Gemma 4 E4B, con Gemma 4 E2B como respaldo si E4B resulta lento en CPU.
- **Código local:** Qwen2.5-Coder 7B. Es un modelo especializado en código, liviano (~4.7 GB en Q4) y reciente, que funciona en CPU con la RAM disponible y admite hasta 128K de contexto.
- **Cloud coding (Componente 3):** GPT-5.3-Codex vía Codex, o Gemini Flash en su capa gratuita si no hay presupuesto.

Modelos como Qwen3-Coder 30B o Qwen3.6 27B se descartaron porque requieren 24 GB de VRAM o 32 GB de memoria unificada.

## 5. Advertencias

El ecosistema cambia cada pocas semanas. Durante esta investigación, por ejemplo, OpenAI ya listaba GPT-6 como su familia principal y Google cambiaba el precio de Gemini Flash a partir de enero de 2027. Antes de entregar, cada integrante debe abrir las fuentes de la columna "Fuente" y confirmar los valores. Los campos marcados como "verificar" no tenían un dato oficial accesible al momento de la consulta.
