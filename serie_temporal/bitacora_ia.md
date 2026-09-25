# Bitácora de uso de IA: Componente 4

> El laboratorio exige "documentar cómo fue utilizada la IA durante el desarrollo y qué decisiones fueron tomadas por el equipo". **Revisar y ajustar con nuestras propias palabras**: en la sustentación debemos poder explicar cada fila.

**Herramienta de IA usada:** Claude Opus 5.5 (claude.ai), como asistente de programación.
**Por qué:** en el Componente 3 fue el único de los tres modelos evaluados que resolvió el problema de Open-Meteo en una sola iteración, sin intervención humana (Gemma y Qwen no lo resolvieron en 5 iteraciones).

**Forma de trabajo:** un módulo a la vez. La IA generaba el código; el equipo lo leía, lo ejecutaba en su computador, revisaba el resultado y decidía si lo aceptaba. Ningún módulo se integró sin ejecutarse antes.

| # | Fecha y hora | Herramienta | Qué se le pidió (resumen) | Qué entregó | ¿Se ejecutó? Resultado | Decisión del equipo |
|---|---|---|---|---|---|---|
| 1 | 25/09/2026 (10:04) | Claude Opus 5.5 | Módulo para consultar la API histórica de Open-Meteo con manejo de errores | `api_client.py` | ✅ 992 registros (01/01/2024 – 18/09/2026) | Aceptado. Se entendió por qué la fecha final es hoy − 7 días (el archivo histórico llega con retraso). |
| 2 | 25/09/2026 (10:08) | Claude Opus 5.5 | Módulo para convertir el JSON en DataFrame y validar tipos, fechas, duplicados, orden y faltantes | `preprocessing.py` | ✅ 992 registros válidos, 0 faltantes, 0 duplicados, en orden | Aceptado. Se decidió interpolar solo si falta ≤ 5 % de los datos; con más, se detiene el programa. |
| 3 | 25/09/2026 (10:26) | Claude Opus 5.5 | Baselines (persistencia y media móvil de 7 días) y regresión lineal con 7 rezagos, sin fuga de datos | `model.py` | ✅ Ecuación: y(t) = 1.950 + 0.546·y(t−1) + … | Aceptado. Se verificó que todos los pronósticos usan solo días anteriores (`shift`). |
| 4 | 25/09/2026 (10:34) | Claude Opus 5.5 | División temporal, MAE, RMSE y gráficas | `evaluation.py` | ✅ (probado a través de `app.py`) | Aceptado. Se eligieron los últimos 60 días como prueba. |
| 5 | 25/09/2026 (10:34) | Claude Opus 5.5 | Aplicación principal que une todo el flujo | `app.py` | ✅ Flujo completo; 2 gráficas y 2 CSV generados | Aceptado. |

## Incidentes y problemas resueltos

- **`pip` no reconocido** en el segundo computador: se resolvió usando `python -m pip`.
- **La carpeta del proyecto desapareció** al mover archivos en el Explorador: se volvió a crear.
- **Windows bloqueó las DLL de pandas** ("Una directiva de Control de aplicaciones bloqueó este archivo"). La causa era el Control inteligente de aplicaciones de Windows 11. Se desactivó con autorización del dueño del equipo (el cambio es permanente).

## Decisiones tomadas por el equipo (no por la IA)

- **API elegida y por qué:** Open-Meteo Historical Weather. Es gratuita, no requiere clave, está dentro de las opciones "meteorológicas" permitidas por el laboratorio y ya la conocíamos del Componente 3.
- **Variable y lugar:** temperatura media diaria de Manizales (lat 5.07, lon −75.52).
- **Período de datos:** del 01/01/2024 hasta hoy − 7 días (992 días), suficiente para entrenar y evaluar.
- **Tamaño del conjunto de prueba y por qué:** los últimos 60 días (≈ 6 % de la serie): cerca de dos meses de días recientes para evaluar, dejando 932 para entrenar. La división respeta el orden temporal.
- **Baselines elegidos:** persistencia ("mañana igual que hoy") y media móvil de 7 días.
- **Modelo elegido y por qué:** regresión lineal con 7 rezagos. Es simple, interpretable (cada coeficiente dice cuánto pesa cada día anterior) y adecuada para el nivel del curso.
- **Manejo de faltantes:** interpolación lineal solo si faltan ≤ 5 % de los datos.
- **Errores de la IA detectados y cómo se corrigieron:** ninguno en el código. Los problemas fueron del entorno (ver Incidentes).

## Resultados finales (período de prueba: 21/07/2026 – 18/09/2026, 60 días)

| Método | MAE (°C) | RMSE (°C) |
|---|---|---|
| Regresión lineal (7 rezagos) | 0.666 | 0.828 |
| Persistencia | 0.680 | 0.849 |
| Media móvil 7 días | 0.777 | 0.994 |

**Interpretación del modelo:** el día anterior es el que más pesa (coeficiente 0.546). Los coeficientes suman 0.871 < 1, así que el modelo "tira" los pronósticos hacia el promedio histórico: 1.950 / (1 − 0.871) ≈ 15.1 °C, casi igual a la media real de la serie (15.16 °C).

**Conclusión:** la regresión lineal obtuvo el menor error, pero solo mejoró el MAE un 2.1 % frente a la persistencia (0.014 °C). Con 60 días de prueba esa diferencia es muy pequeña para afirmar que el modelo es realmente mejor: en la práctica, **igualó al baseline**. La media móvil fue la peor porque reacciona tarde a los cambios. La temperatura de Manizales es muy estable (desviación de 0.94 °C) y depende sobre todo del día anterior. Los modelos basados solo en días pasados no pueden anticipar cambios bruscos (por ejemplo, el salto a 18.0 °C del 17/09). Para mejorar habría que agregar otras variables (humedad, nubosidad, precipitación) o usar modelos de series temporales más avanzados.
