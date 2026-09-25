# Registro del Componente 3: Vibe Coding

**Equipo:** Laura Valentina Suarez · Daniela Garcia · Mariana Otalvaro · **Equipo de cómputo:** Ryzen 7 7735HS, 19.7 GB RAM, sin GPU dedicada · **Fecha:** 23/09/2026 · **Entorno:** Python 3.14.7, requests 2.34.2, pandas 3.0.6, matplotlib 3.11.2

## Modelos comparados

| Rol | Modelo | Entorno |
|---|---|---|
| Local generalista | gemma4:e4b | Ollama (chat interactivo) |
| Local de código | qwen2.5-coder:7b | Ollama (chat interactivo) |
| Cloud coding | Claude Opus 5.5 | claude.ai (web), chat incógnito (sin memoria), búsqueda web desactivada |

---

## Bitácora: Local generalista (gemma4:e4b)

| Iteración | Hora | Qué se envió | Resultado de la ejecución | Archivo |
|---|---|---|---|---|
| 1 | 4:48 p. m. (respuesta en 6 min 3 s; 3174 tokens; 8.89 tok/s) | Prompt estándar | ❌ `404 Client Error: Not Found` para `https://api.open-meteo.com/v1/forecast_historical`. El programa capturó el error y terminó con un mensaje claro ("No se pudo procesar ningún dato"), sin fallar abruptamente. | solucion_v1.py |
| 2 | 5:06 – 5:10 p. m. (3 min 23 s; 919 tokens; 7.93 tok/s) | Mensaje de corrección con el error 404 | ⚠️ **Respuesta cortada:** el código se interrumpe en `response = requests.get(API_URL, params=params, timeout=15)`, así que no se puede ejecutar. Gemma cambió la URL a `https://api.open-meteo.com/v1/historical` y afirmó que "la API cambió su estructura". | (no ejecutable) |
| 3 | 5:15 – 5:22 p. m. (7 min 2 s; 2588 tokens; 8.29 tok/s) | Configuración: `/set parameter num_ctx 16384`. Mensaje: "Tu respuesta anterior se cortó... Devuélveme el código completo corregido." | ❌ De nuevo `404 Client Error: Not Found` para `https://api.open-meteo.com/v1/historical?...&start_date=2026-08-25&end_date=2026-09-23&timezone=America%2FBogota`. El manejo de errores volvió a funcionar. | solucion_v3.py |
| 4 | Inicio 5:31 p. m. del 23/09 (21 min 0 s; 3217 tokens; 2.94 tok/s) | Mensaje de corrección con el error 404 de `/v1/historical` | ❌ `SyntaxError: unterminated f-string literal (detected at line 88)`. El programa ni siquiera arranca. | solucion_v4.py |
| 5 | Inicio 1:45 p. m. del 24/09 (8 min 40 s; 2529 tokens; 7.03 tok/s) | Mensaje de corrección con el `SyntaxError` | ❌ La sintaxis quedó corregida y el programa se ejecuta, pero vuelve el `404 Not Found` de `/v1/historical` (mismo error que en la iteración 3). Mensaje de error más detallado. | solucion_v5.py |

**Análisis de la iteración 1:**
- El error se debe a que Gemma **inventó un endpoint que no existe** (`/v1/forecast_historical`), un caso de alucinación. Open-Meteo no tiene esa ruta.
- Aspecto positivo: el manejo de errores funcionó. El `HTTPError` se capturó y se mostró el código 404 con un mensaje legible.
- Otras observaciones de la revisión del código (no enviadas al modelo; se evalúan en el checklist final): usa `forecast_days=30` (días *futuros*, no los últimos 30 días) y `timezone="UTC"` en lugar de `America/Bogota`, como pedía el enunciado.

**Análisis de la iteración 2:**
- **Causa del corte: se llenó la ventana de contexto.** Ollama cargó el modelo con 4096 tokens de contexto. El prompt de esta iteración ocupó 3177 tokens (todo el historial: prompt, razonamiento y el código anterior) y la respuesta 919: 3177 + 919 = **4096 exactamente**. El modelo se quedó sin espacio y la respuesta se cortó. Es una evidencia práctica del concepto de *ventana de contexto* del mapa mental.
- Gemma justificó el cambio de URL con una explicación inventada ("la API cambió su estructura") y propuso otro endpoint, `/v1/historical`, que tampoco corresponde a la documentación de Open-Meteo (se confirmará al ejecutar).
- Mantuvo `forecast_days` y `timezone="UTC"`.

**Análisis de la iteración 3 (código recibido):**
- Con el contexto ampliado, la respuesta llegó completa: 3771 tokens de entrada + 2588 de salida = 6359, dentro de los 16384 disponibles.
- Mejoras respecto a v1: calcula un rango de fechas (`start_date`/`end_date` = hoy − 29 días a hoy), usa `timezone="America/Bogota"`, cierra la figura con `plt.close()` e incluye las 3 pruebas sugeridas como comentario al final.
- Mantiene la URL `https://api.open-meteo.com/v1/historical`, que al ejecutarse también devolvió 404: la "corrección" de la iteración 2 era otra alucinación. Los parámetros de fecha y zona horaria sí se construyeron bien, como muestra la URL del error.

**Análisis de la iteración 4 (código recibido):**
- Gemma **no cambió la URL** (`/v1/historical`) ni los nombres de las variables. Atribuyó el 404 a "la combinación de parámetros" y agregó un mensaje especial para el error 404 que dice que "es posible que haya un cambio en la estructura de la API". Es decir, cambió cómo se *reporta* el error en lugar de *resolverlo*.
- **Alucinación sobre la fecha:** afirmó que las fechas de 2026 indican "un entorno que simula o está forzando un día futuro". El modelo cree que 2026 es el futuro por su fecha de corte de entrenamiento, aunque las fechas eran correctas (el día real de la prueba). Es un ejemplo de por qué el conocimiento de un modelo está limitado a sus datos de entrenamiento.
- En su razonamiento consideró "cambiar a otro proveedor de clima" si esto fallaba de nuevo.
- **Nuevo error de sintaxis:** en la línea 88 un texto `f"..."` quedó partido en dos líneas (`...no reconoce la combinación de parámetros` / `(Lat/Lon/Fechas/Parametros).")`), lo que en Python es un error de sintaxis.
  - **Nota de verificación posterior:** con Qwen (iteración 5) se comprobó que Ollama puede partir líneas largas al mostrarlas en la terminal (*word wrap*), y que ese corte se copia junto con el código. En el caso de Gemma la línea parecía caber en el ancho de la terminal y el propio modelo "reconoció" el error y lo corrigió en la iteración 5, pero **no se puede descartar por completo** que el corte haya sido un artefacto de la visualización. Por eso esta regresión se considera **probable, pero no confirmada**.
- **Rendimiento:** 3217 tokens a solo 2.94 tok/s (frente a ~8-9 en iteraciones anteriores), 21 minutos en total. La caída probablemente se debe a que el computador se suspendió o pasó a modo de ahorro de energía durante la generación, ya que la respuesta se revisó al día siguiente (confirmar con el equipo). El contexto acumulado llegó a 6165 tokens de entrada.

**Análisis de la iteración 5 (código recibido):**
- Corrigió el error de sintaxis dividiendo el mensaje en varios `print` independientes.
- Mantiene sin cambios la URL `/v1/historical` y los nombres de variables `temperature_max`/`temperature_min`.
- En su razonamiento reconstruyó "de memoria" la línea que había fallado, con una versión distinta a la que realmente había generado, lo que muestra que no revisa con exactitud su propio código anterior.
- El contexto acumulado llegó a 8500 tokens de entrada (más de 2 veces la ventana original de 4096).

**Intervenciones humanas:** ninguna en el código. **Intervención de configuración:** en la iteración 3 se amplió la ventana de contexto de Ollama de 4096 a 16384 tokens (`/set parameter num_ctx 16384`), porque la respuesta de la iteración 2 se cortó al llenarse el contexto. (Incidente operativo sin efecto en la evaluación: el código se pegó por error en PowerShell en lugar del Bloc de notas; no cuenta como iteración.)

### Resultado final de Gemma: ❌ NO RESUELTO en 5 iteraciones

**Resumen de las iteraciones:**

| Iteración | Error principal | ¿Avanzó? |
|---|---|---|
| 1 | 404: endpoint inventado `/v1/forecast_historical` | — |
| 2 | Respuesta cortada por la ventana de contexto (4096 tokens) | No ejecutable |
| 3 | 404: otro endpoint inventado `/v1/historical` | Sí: fechas y zona horaria correctas |
| 4 | `SyntaxError` (probable regresión del modelo; posible artefacto del *word wrap* de Ollama) | No |
| 5 | 404 igual que en la iteración 3 | Solo corrigió la sintaxis |

**Totales:** 5 iteraciones · ~46 min de generación (6:03 + 3:23 + 7:02 + 21:00 + 8:40; la iteración 4 se alargó por la suspensión del equipo) · 12 427 tokens generados.

**Causa raíz que el modelo nunca identificó:** usó endpoints inexistentes (`/v1/forecast_historical` y `/v1/historical`) y nombres de variables inexistentes (`temperature_max`, `temperature_min`; los reales son `temperature_2m_max` y `temperature_2m_min`). En lugar de corregir la causa, atribuyó el error a "cambios en la API" y a fechas "futuras".

**Intervención humana necesaria para que funcione** (`solucion_final_intervencion_humana.py`, cambios marcados con `# INTERVENCIÓN HUMANA`):
1. `API_URL`: `https://api.open-meteo.com/v1/historical` → `https://api.open-meteo.com/v1/forecast`
2. Parámetro `daily`: `temperature_max,temperature_min` → `temperature_2m_max,temperature_2m_min`
3. Claves del DataFrame: `['temperature_max']` / `['temperature_min']` → `['temperature_2m_max']` / `['temperature_2m_min']`

**Resultado con la intervención (24/09/2026):** ✅ el programa funcionó de principio a fin.
```
✅ Datos obtenidos y validados correctamente.
Temperatura Media:    21.18 °C
Temperatura Mínima:   18.80 °C (Ocurrió el 2026-09-11)
Temperatura Máxima:   24.00 °C (Ocurrió el 2026-09-08)
Desviación Estándar:   1.31 °C
✅ Gráfico guardado exitosamente como 'temperatura_manizales.png'
```
**Conclusión:** la estructura, los cálculos, la gráfica y el manejo de errores que generó Gemma eran correctos. El problema estaba **solo en el conocimiento de la API** (endpoint y nombres de variables), y bastaron 3 cambios humanos puntuales. Esto muestra que el modelo sabe *programar* la solución, pero no *conoce* con precisión la API externa y no puede consultarla.

**Checklist de aceptación (sobre `solucion_v5.py`):**
- [ ] Se ejecuta sin errores: se ejecuta sin fallar, pero no cumple su objetivo (no obtiene datos).
- [ ] Obtiene datos reales de Open-Meteo: ❌ (404).
- [ ] ~30 días de datos: ❌ (no aplica sin datos). El rango de fechas sí se calcula bien.
- [~] Valida código HTTP y estructura del JSON: parcial. Valida HTTP y la clave `daily`, pero **no** valida que las listas tengan la misma longitud ni que no haya nulos (requisito del enunciado).
- [x] Maneja error de conexión con mensaje claro: ✅ **probado con el wifi desconectado**: mostró "🚨 Error de Conexión: No se pudo conectar con la API. Verifique su red." y terminó ordenadamente.
- [~] Media, mínimo, máximo y desviación estándar: ❌ en v5 (sin datos); ✅ funcionan con la intervención humana.
- [~] Fechas del mínimo y del máximo: ❌ en v5; ✅ con la intervención humana.
- [~] Gráfica PNG con título, ejes y leyenda: ❌ en v5; ✅ generada con la intervención humana (`temperatura_manizales.png`).
- [x] Funciones con docstrings y `if __name__ == "__main__"`: ✅
- [~] Sugiere al menos 3 pruebas: ✅ en v1 y v3 (pytest con mocks); ❌ la versión 5 las eliminó.

**Aspectos positivos:** código bien estructurado y documentado, manejo de errores robusto (el programa nunca se "cayó" por errores de red o HTTP), corrección progresiva de fechas y zona horaria.
**Aspectos negativos:** alucinaciones repetidas sobre la API, justificaciones inventadas, una regresión (SyntaxError), razonamiento muy lento (~8 tok/s con miles de tokens de *thinking*) y sensibilidad a la ventana de contexto.

---

## Bitácora: Local de código (qwen2.5-coder:7b)

**Condición inicial:** a diferencia de Gemma, desde el inicio se configuró `/set parameter num_ctx 16384`, para evitar el corte de respuestas por la ventana de contexto observado con Gemma.

| Iteración | Hora | Qué se envió | Resultado de la ejecución | Archivo |
|---|---|---|---|---|
| 1 | 2:53 p. m. del 24/09 (3 min 46 s; 1670 tokens; 7.89 tok/s) | Prompt estándar | ❌ `Error general: Error al obtener datos: 400` (Bad Request). El programa no se cayó, pero el mensaje no explica la causa. | solucion_v1.py |

| 2 | 3:01 p. m. (4 min 49 s; 1777 tokens; 6.19 tok/s) | Mensaje de corrección con el error 400 | ❌ `400 {"error":true,"reason":"Parameter 'start_date' is out of allowed range from 2026-06-23 to 2026-10-09"}`. El mensaje detallado revela la causa exacta. | solucion_v2.py |

| 3 | 3:11 p. m. (5 min 6 s; 1726 tokens; 5.71 tok/s) | Mensaje de corrección con el error 400 detallado (`start_date` fuera de rango) | ❌ `Error general: Respuesta JSON no contiene las claves esperadas`. La API **sí respondió 200** (pasó la validación HTTP); el fallo es el error latente de validación de claves presente desde la versión 1. | solucion_v3.py |

| 4 | 3:37 p. m. (7 min 32 s; 1706 tokens; 3.93 tok/s) | Mensaje de corrección con el error de claves | ❌ Mismo error: `Respuesta JSON no contiene las claves esperadas` | solucion_v4.py |
| 5 | 3:46 p. m. (10 min 3 s; 1866 tokens; 3.14 tok/s) | Mensaje de corrección + "El error persiste igual que en la versión anterior" | ⚠️ Primero `SyntaxError` por el ajuste de línea de la terminal al copiar (ver análisis). Con las líneas restauradas: ❌ `Respuesta JSON no contiene las claves esperadas` (mismo error de las iteraciones 3 y 4). | solucion_v5.py |

**Análisis de la iteración 1 (Qwen):**
- ✅ Usó desde el inicio el **endpoint real** (`https://api.open-meteo.com/v1/forecast`) y los **nombres reales de las variables** (`temperature_2m_max`, `temperature_2m_min`), lo que Gemma nunca logró en 5 iteraciones.
- ❌ **Causa del 400:** las fechas están escritas a mano y fijas (`start_date: 2023-04-01`, `end_date: 2023-04-30`) en lugar de calcular "los últimos 30 días". El endpoint `/forecast` no ofrece datos de 2023, por eso la API rechaza la solicitud. Además, no cumple el enunciado ("últimos 30 días").
- Otras observaciones de la revisión del código (no enviadas al modelo):
  - La validación de claves busca `time` y `temperature_2m_max` en el nivel superior del JSON, pero están dentro de `daily`. Aunque la API respondiera bien, esta validación fallaría (error latente).
  - No usa `timeout` en `requests.get`, así que el `except Timeout` nunca se activa. Además está después de `except RequestException`, que ya lo captura (código inalcanzable).
  - Importa `pandas` pero no lo usa (el enunciado lo pedía).
  - La desviación estándar es poblacional (÷N), mientras que pandas usa la muestral (÷N−1) por defecto.
  - Las pruebas sugeridas tienen errores conceptuales: una zona horaria inválida no produce un error de *tiempo de espera*.

**Análisis de la iteración 2 (Qwen, código recibido):**
- Único cambio real: el mensaje de error ahora incluye el texto de la respuesta de la API (`{response.status_code} {response.text}`), lo que permitirá ver *por qué* la API rechaza la solicitud.
- **No corrigió la causa:** las fechas siguen fijas en abril de 2023. Planteó hipótesis genéricas (formato de latitud, zona horaria) sin identificar el problema.
- El resto del código (incluidas las pruebas sugeridas y la explicación) es idéntico a la versión 1.

**Análisis de la iteración 3 (Qwen, código recibido):**
- ❌ **"Corrección" por copia literal del mensaje de error:** en vez de calcular los últimos 30 días a partir de la fecha actual, copió el rango permitido que mencionaba el error como constantes fijas (`ALLOWED_START_DATE = "2026-06-23"`, `ALLOWED_END_DATE = "2026-10-09"`). Esto pide ~109 días, incluye **fechas futuras** (pronóstico hasta el 9 de octubre, no datos históricos) y dejará de funcionar en cuanto el rango permitido de la API cambie. No cumple el enunciado ("últimos 30 días").
- Importó `datetime` y `timedelta`, pero no los usa.
- Mejora de diseño: `obtener_datos_clima` ahora recibe las fechas como parámetros.
- Eliminó la sección de pruebas sugeridas.
- La validación de claves en el nivel superior del JSON sigue igual (error latente).

**Análisis de la iteración 4 (Qwen, código recibido):**
- ❌ **Cambio cosmético, sin corrección real:** lo único que cambió fue extraer la lista de claves a una variable (`expected_keys = [...]`). La lógica es idéntica: sigue buscando `time`, `temperature_2m_max` y `temperature_2m_min` en el nivel superior del JSON y no dentro de `daily`. Atribuyó el error a "un cambio en la estructura de la respuesta de la API" en lugar de revisar su propio código (mismo patrón que Gemma).
- **Rendimiento en descenso:** la velocidad bajó a 3.93 tok/s (desde 7.89 en la iteración 1) a medida que crecía el contexto acumulado (5746 tokens de entrada).

**Análisis de la iteración 5 (Qwen, código recibido):**
- Agregó validaciones nuevas (que los valores sean listas) y reorganizó la validación de longitudes y nulos, esta vez leyendo correctamente dentro de `datos["daily"]`. Sin embargo, **dejó intacta la línea que causa el error** (la búsqueda de `time` y `temperature_2m_*` en el nivel superior del JSON).
- **SyntaxError por artefacto de copia, no del modelo:** las líneas 44 y 47 del archivo quedaron partidas (`... or not` / `isinstance(...)` y `... !=` / `len(...)`). Las dos líneas originales miden más de 150 caracteres, justo el ancho con el que Ollama ajusta el texto en la terminal (*word wrap*), y la continuación aparece sin sangría, en la columna 0. Todo indica que el corte lo introdujo la visualización de Ollama al copiar desde la terminal, no el modelo. Por eso se restauraron las dos líneas uniéndolas (sin cambiar ningún carácter del código) y se volvió a ejecutar. Para evitarlo, Ollama permite desactivar el ajuste con `/set nowordwrap`.
- La velocidad siguió bajando (3.14 tok/s) con 7511 tokens de contexto acumulado.

### Resultado final de Qwen: ❌ NO RESUELTO en 5 iteraciones

**Resumen de las iteraciones:**

| Iteración | Error principal | ¿Avanzó? |
|---|---|---|
| 1 | 400: fechas fijas de abril de 2023 | Endpoint y variables **correctos** desde el inicio |
| 2 | 400 (ahora con detalle: `start_date` fuera de rango) | Sí: mejor mensaje de error |
| 3 | Validación de claves mal hecha | Sí: la API ya respondió 200, pero con fechas copiadas del error |
| 4 | Mismo error de claves | No: cambio cosmético |
| 5 | Mismo error de claves | No: agregó validaciones, pero no corrigió la línea que falla |

**Totales:** 5 iteraciones · ~31 min de generación (3:46 + 4:49 + 5:06 + 7:32 + 10:03) · 8745 tokens generados.

**Causa raíz que el modelo nunca identificó:** su propia validación busca `time`, `temperature_2m_max` y `temperature_2m_min` en el nivel superior del JSON, cuando están dentro de `daily`. En tres iteraciones seguidas atribuyó el problema a "un cambio en la estructura de la API".

**Intervenciones humanas:** ninguna en la lógica del código. **Restauración de formato:** en `solucion_v5.py` se unieron dos líneas partidas por el ajuste de línea de la terminal (sin cambiar ningún carácter).

**Intervención humana necesaria para que funcione** (`solucion_final_intervencion_humana.py`, cambios marcados con `# INTERVENCIÓN HUMANA`):
1. Validación de claves: buscar `time`, `temperature_2m_max` y `temperature_2m_min` **dentro de** `datos["daily"]`.
2. Fechas: reemplazar las constantes fijas por el cálculo de los últimos 30 días (`datetime.now()` − 29 días), como pide el enunciado.

**Resultado con la intervención (24/09/2026):** ✅ el programa funcionó de principio a fin.
```
Estadísticas de Temperatura Máxima:        Estadísticas de Temperatura Mínima:
Media: 21.25 °C                             Media: 12.99 °C
Mínimo: 18.80 °C (2026-09-11)               Mínimo: 11.60 °C (2026-09-08)
Máximo: 24.00 °C (2026-09-08)               Máximo: 13.90 °C (2026-09-14)
Desviación Estándar: 1.23 °C                Desviación Estándar: 0.58 °C
Gráfica guardada como 'temperatura_manizales.png'
```
**Comparación con el resultado de Gemma con intervención** (mismo día, mismos 30 días): el mínimo, el máximo y sus fechas coinciden exactamente (18.80 °C el 11/09 y 24.00 °C el 08/09), lo que valida ambos programas. Las diferencias en la media (21.18 frente a 21.25 °C) y en la desviación estándar (1.31 frente a 1.23 °C) se explican probablemente por dos motivos: (1) el valor del día actual es un pronóstico que la API actualiza durante el día y las ejecuciones se hicieron a horas distintas, y (2) Gemma usa la desviación estándar **muestral** de pandas (÷N−1), mientras que Qwen calcula la **poblacional** (÷N).

**Conclusión:** bastaron 2 cambios humanos. Qwen conocía la API, pero no detectó el error lógico de su propia validación ni calculó las fechas dinámicamente. Como valor agregado, calculó también las estadísticas de la temperatura mínima (no pedidas).

**Checklist de aceptación (sobre `solucion_v5.py`):**
- [ ] Se ejecuta sin errores: se ejecuta sin fallar, pero no cumple su objetivo (rechaza los datos por su propia validación).
- [~] Obtiene datos reales de Open-Meteo: la API **sí responde 200** con datos reales, pero el programa los descarta.
- [ ] ~30 días de datos: ❌ usa un rango fijo de ~109 días (23/06 al 09/10/2026) copiado del mensaje de error, que incluye días futuros.
- [~] Valida código HTTP y estructura del JSON: HTTP ✅; tipos de lista, longitudes iguales y nulos ✅ (bien implementados en v5); validación de claves ❌ (errónea).
- [~] Maneja error de conexión con mensaje claro: **probado con el wifi desconectado**. El error se captura y el programa no se cae, pero el mensaje muestra el texto técnico completo de la excepción (`HTTPSConnectionPool(...) NameResolutionError ... getaddrinfo failed`), poco claro para un usuario. Además, no usa `timeout`, así que el manejo de tiempo de espera nunca se activa.
- [~] Media, mínimo, máximo y desviación estándar: ❌ en v5 (sin datos); ✅ con la intervención humana (sin pandas; desviación poblacional ÷N).
- [~] Fechas del mínimo y del máximo: ❌ en v5; ✅ con la intervención humana.
- [~] Gráfica PNG con título, ejes y leyenda: ❌ en v5; ✅ generada con la intervención humana.
- [~] Funciones con docstrings y `if __name__ == "__main__"`: ✅, excepto `main()`, que no tiene docstring.
- [ ] Sugiere al menos 3 pruebas: en v1 y v2 sí (con errores conceptuales); las eliminó desde la v3.
- [ ] Usa pandas (requisito): ❌ lo importa pero no lo usa.

**Aspectos positivos:** encontró el endpoint y las variables reales de la API desde el primer intento, respuestas mucho más rápidas que Gemma (sin razonamiento previo), validaciones de longitud y nulos bien implementadas al final.
**Aspectos negativos:** no calculó las fechas dinámicamente (primero fijas en 2023, luego copiadas del error), no detectó el error de su propia validación en 3 iteraciones, cambios cosméticos en lugar de correcciones, no usó pandas y la velocidad cayó de 7.9 a 3.1 tok/s a medida que crecía el contexto.

---

## Bitácora: Cloud coding (Claude Opus 5.5)

**Condiciones:** chat incógnito en claude.ai (no usa la memoria ni el historial de conversaciones, así que no conoce este laboratorio), búsqueda web desactivada. El modelo tenía disponible su entorno de ejecución de código (sin acceso a internet), que usó para probar su propio programa con datos simulados antes de entregarlo.

| Iteración | Hora | Qué se envió | Resultado de la ejecución | Archivo |
|---|---|---|---|---|
| 1 | 4:15 – ~4:17 p. m. del 24/09 (~2 min; hora de fin aproximada) | Prompt estándar | ✅ **Funcionó a la primera.** Período 2026-08-25 a 2026-09-23 (30 días completos); media 21.26 °C; desviación 1.25 °C; mínimo 18.80 °C (2026-09-11); máximo 24.00 °C (**2026-09-08 y 2026-09-17**); gráfica guardada. | solucion_v1.py |

**Análisis de la iteración 1 (respuesta recibida):**
- Entregó el programa como archivo `.py` descargable (sin riesgo de líneas partidas al copiar).
- **Autoverificación:** antes de responder, probó el programa con datos simulados en su entorno de ejecución (estadísticas, gráfica, detección de nulos y manejo del tiempo de espera). Aclaró de forma explícita que **no pudo llamar a la API real** por falta de internet, en lugar de afirmar que funcionaba.
- **Decisiones de diseño explicadas:** endpoint `/v1/forecast` con `past_days=30` y `forecast_days=1`, descartando el día actual (incompleto en Bogotá) para conservar 30 días completos; desviación estándar muestral (`ddof=1`) con la alternativa poblacional indicada; manejo de empates en mínimo/máximo; excepción propia `ErrorDatosClima` y código de salida 1 en caso de error.
- **Pruebas sugeridas:** 5 pruebas concretas con `pytest` y `unittest.mock` (caso feliz, validación de estructura, errores de red, gráfica e integración real), frente a las 3 pedidas.

### Resultado final del modelo cloud: ✅ RESUELTO en 1 iteración, sin intervención humana

**Hallazgo al comparar con los modelos locales:**
- El mínimo coincide con Gemma y Qwen (18.80 °C el 11/09), lo que valida los tres programas.
- **Empate en el máximo:** la temperatura de 24.00 °C se repitió el **08/09 y el 17/09**. El modelo cloud mostró ambas fechas porque manejó los empates a propósito. Gemma (`idxmax`) y Qwen (`list.index`) solo mostraron la primera (08/09), aunque el 17/09 también estaba dentro de su período. Sus programas daban un resultado **incompleto sin que se notara**.
- La media (21.26 °C) difiere ligeramente de la de Gemma y Qwen porque el período es distinto: el modelo cloud excluye el día actual (incompleto) y usa del 25/08 al 23/09, mientras que los locales con intervención usaron del 26/08 al 24/09 e incluyeron el día en curso.

**Revisión del código (verificada por el equipo):**
- Usa `timeout=15` y captura por separado `Timeout`, `ConnectionError` y `RequestException`, cada uno con su mensaje claro. Es el único de los tres modelos cuyo manejo de tiempo de espera realmente funciona.
- Usa pandas (como pedía el enunciado) para construir, ordenar y filtrar el DataFrame y para las estadísticas.
- Usa `zoneinfo` para determinar el "hoy" en la zona de Bogotá y `matplotlib.use("Agg")` para que la gráfica se guarde sin abrir ventanas.
- Diseño testeable: las funciones reciben parámetros con valores por defecto, y `construir_dataframe` acepta una fecha `hoy` fija para pruebas.

**Intervenciones humanas:** ninguna.

**Métricas de rendimiento:** la interfaz web de claude.ai no muestra tokens, velocidad ni duración de la respuesta (a diferencia de `ollama run --verbose`). Solo se registró la hora de inicio (4:15 p. m.) y la hora aproximada de fin (~4:17 p. m.), es decir, unos 2 minutos para la respuesta completa, incluida su autoverificación. Es una diferencia práctica entre usar un modelo local (métricas completas y control del hardware) y un servicio cloud (métricas ocultas; el cómputo ocurre en los servidores del proveedor).

**Checklist de aceptación (sobre `solucion_v1.py`):**
- [x] Se ejecuta sin errores: ✅
- [x] Obtiene datos reales de Open-Meteo para Manizales: ✅
- [x] ~30 días de datos: ✅ exactamente 30 días completos (25/08 al 23/09), excluyendo el día actual incompleto.
- [x] Valida código HTTP y estructura del JSON: ✅ verificado en el código. `validar_datos` comprueba que sea un objeto JSON, la clave `daily` y las tres listas dentro de ella, su tipo, longitudes iguales, que no estén vacías y los nulos (indicando en qué fechas). Además, en un error HTTP muestra el motivo (`reason`) que devuelve la API.
- [x] Maneja error de conexión con mensaje claro: ✅ **probado con el wifi desconectado**: "ERROR: No se pudo conectar con la API de Open-Meteo. Revisa tu conexión a internet." (mensaje claro, sin texto técnico).
- [x] Media, mínimo, máximo y desviación estándar: ✅ (desviación muestral, `ddof=1`).
- [x] Fechas del mínimo y del máximo: ✅ incluye **todas** las fechas en caso de empate (detectó que el máximo se repitió el 08/09 y el 17/09).
- [x] Gráfica PNG: ✅ generada, con título (incluye el rango de fechas), etiquetas de ejes, leyenda, área sombreada entre máxima y mínima, fechas formateadas y `dpi=150`.
- [x] Funciones con docstrings y `if __name__ == "__main__"`: ✅ verificado. Las 7 funciones y la clase de error tienen docstring (con Args, Returns y Raises), más un docstring del módulo con las dependencias. `main()` devuelve un código de salida usado con `sys.exit(main())`.
- [x] Sugiere al menos 3 pruebas: ✅ sugirió 5, con `pytest` y `unittest.mock`.

**Intervenciones humanas:**

**Checklist de aceptación:**

---

## Tabla comparativa (formato del laboratorio)

| Criterio | Local general (gemma4:e4b, Ollama) | Local coding (qwen2.5-coder:7b, Ollama) | Cloud coding (Claude Opus 5.5) |
|---|---|---|---|
| **Código ejecutable** | Se ejecuta sin fallar, pero **nunca obtuvo datos** (404) en 5 versiones | Se ejecuta sin fallar, pero **nunca procesó datos** (su propia validación los rechazaba) en 5 versiones | ✅ **Funcionó a la primera** |
| **Errores encontrados** | Endpoints inventados (`/forecast_historical`, `/historical`), nombres de variables incorrectos, días futuros y zona UTC en v1, respuesta cortada por la ventana de contexto, SyntaxError en v4 (probable), no maneja empates | Fechas fijas (2023, luego copiadas del error), validación de claves errónea, sin `timeout`, pandas sin usar, mensaje de error de red técnico, no maneja empates | Ninguno detectado |
| **Iteraciones necesarias** | 5 (no resuelto) | 5 (no resuelto) | 1 |
| **Tiempo hasta solución** | No resuelto; ~46 min de generación acumulada (~12 400 tokens) | No resuelto; ~31 min de generación acumulada (~8 700 tokens) | Resuelto en una sola respuesta: ~2 min (4:15 – ~4:17 p. m.) |
| **Calidad/claridad del código** | Buena estructura (funciones, type hints, manejo de errores por tipo); lógica de cálculo y gráfica correctas | Estructura simple; cálculos a mano sin pandas; excepciones genéricas; código repetido para máximas y mínimas | Diseño cuidadoso: excepción propia, código de salida, empates, exclusión del día incompleto, decisiones justificadas |
| **Documentación** | Docstrings completos y explicación del flujo | Docstrings en casi todas las funciones (falta en `main`) | Docstring del módulo y de todas las funciones (Args/Returns/Raises), comentarios por sección y decisiones de diseño explicadas en la respuesta |
| **Pruebas sugeridas/generadas** | 3 pruebas con pytest y mocks (v1 y v3); eliminadas en v5 | 3 pruebas en v1–v2, con errores conceptuales; eliminadas desde v3 | 5 pruebas concretas con pytest y mocks; además **se autoverificó** con datos simulados antes de entregar |
| **Intervención humana necesaria** | 3 cambios (endpoint y nombres de variables), más ampliar `num_ctx` a 16384 | 2 cambios (validación de claves y cálculo de fechas) | Ninguna |

**Ciclo de trabajo:** PROBLEMA → PROMPT → MODELO → CÓDIGO → EJECUCIÓN → ERROR/RESULTADO → CORRECCIÓN → SOLUCIÓN

## Reflexión técnica: ¿qué cambió al usar modelos diferentes?

**1. Conocer vs. programar.** Los tres modelos sabían *programar* la solución: estructura en funciones, cálculos, gráfica y manejo de errores. La diferencia estuvo en el **conocimiento preciso de la API externa**. Gemma nunca dio con el endpoint real y lo inventó dos veces; Qwen lo conocía desde el inicio; el modelo cloud lo usó correctamente, con parámetros avanzados (`past_days`, `forecast_days`). Con 2 o 3 cambios humanos puntuales, el código de los modelos locales funcionó: su debilidad no era la lógica, sino datos concretos que "alucinaron".

**2. Corregir vs. aparentar corregir.** Ante un error, los modelos locales tendieron a culpar a factores externos ("la API cambió su estructura", "las fechas son futuras") en lugar de revisar su propio código. Hicieron cambios cosméticos (mover una lista a una variable, reformular mensajes) o parches superficiales (copiar las fechas del mensaje de error). Ninguno identificó la causa raíz en 5 iteraciones.

**3. El tamaño y los recursos importan.** Los modelos locales (4B efectivos y 7.6B parámetros) corrieron en CPU a 3-10 tokens/s, y su velocidad se degradó a medida que crecía el contexto (Qwen pasó de 7.9 a 3.1 tok/s). Gemma sufrió un corte por la ventana de contexto de 4096 tokens y dedicó miles de tokens a razonar en inglés. El modelo cloud, mucho más grande y ejecutado en servidores del proveedor, resolvió el problema en una sola respuesta. A cambio, no ofrece métricas de rendimiento, requiere internet y cuenta de pago, y los datos salen del equipo.

**4. La verificación humana es indispensable.** El hallazgo más importante surgió al **comparar los resultados**: el máximo de 24.00 °C ocurrió dos veces (08/09 y 17/09). Los programas de Gemma y Qwen, aun con la intervención humana, solo reportaban la primera fecha. Parecían funcionar, pero daban un resultado incompleto. Solo el modelo cloud anticipó los empates. Además, detalles como la desviación estándar muestral frente a la poblacional o incluir o no el día actual cambian los resultados y deben ser decisiones conscientes del equipo, no del modelo.

**5. Recomendación.** Para prototipos privados o sin internet, un modelo local de código como Qwen2.5-Coder es útil si un humano revisa y corrige el código, especialmente todo lo que dependa de conocimiento externo (APIs, versiones de librerías). Para tareas que exigen precisión en APIs y diseño robusto, el modelo cloud fue claramente superior. En todos los casos, el código generado por IA debe **ejecutarse, probarse con casos límite y contrastarse** antes de aceptarse.
