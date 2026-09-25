# Componente 4: Reto integrador (Vibe Coding + API + Series Temporales)

Aplicación en Python que descarga la temperatura media diaria de **Manizales** desde la API pública **Open-Meteo**, valida la serie, compara dos baselines con una regresión lineal y evalúa los pronósticos con **MAE** y **RMSE**.

```
API → JSON → PYTHON/PANDAS → PREPARACIÓN → SERIE TEMPORAL → MODELO → PREDICCIÓN → MAE/RMSE → GRÁFICAS
```

## Cómo ejecutarlo

Desde la raíz del proyecto (`fundamentos-ia-lab`):

```bash
python -m pip install -r requirements.txt
cd serie_temporal
python app.py
```

Requiere conexión a internet. No necesita claves de API.

## Módulos (fase de diseño)

| Archivo | Responsabilidad |
|---|---|
| `api_client.py` | Consulta la API y maneja errores de conexión, tiempo de espera y HTTP |
| `preprocessing.py` | JSON → DataFrame; valida tipos, fechas, duplicados, orden y faltantes |
| `model.py` | Baselines (persistencia, media móvil de 7 días) y regresión lineal con 7 rezagos |
| `evaluation.py` | División temporal, MAE, RMSE y gráficas |
| `app.py` | Orquesta el flujo completo |

Cada módulo, salvo `evaluation.py`, se puede probar por separado con `python <archivo>.py`.

## Relación con el ciclo de vida del software

| Fase | Qué se hizo |
|---|---|
| **Requisitos** | Pronosticar la temperatura media del día siguiente en Manizales, mostrar la serie, comparar real vs. predicción y reportar MAE/RMSE. |
| **Análisis** | API Open-Meteo Historical (`archive-api.open-meteo.com/v1/archive`), variable `temperature_2m_mean`; el archivo llega con unos días de retraso. |
| **Diseño** | Cinco módulos con una responsabilidad cada uno; pronóstico a un paso; división temporal sin barajar. |
| **Implementación** | Código generado con apoyo de IA (Claude Opus 5.5), revisado y ejecutado por el equipo (ver `bitacora_ia.md`). |
| **Pruebas** | Ejecución de cada módulo, verificación de que no hay fuga de datos y comparación contra baselines. |
| **Despliegue** | Ejecución local con `python app.py`; dependencias fijadas en `requirements.txt`. |
| **Mantenimiento** | Parámetros configurables al inicio de cada módulo (lugar, fechas, días de prueba, rezagos). |

## Resultados (ejecución del 25/09/2026)

- Datos: 992 días (01/01/2024 – 18/09/2026), sin faltantes ni duplicados.
- Entrenamiento: 932 días · Prueba: 60 días (21/07/2026 – 18/09/2026).

| Método | MAE (°C) | RMSE (°C) |
|---|---|---|
| Regresión lineal (7 rezagos) | 0.666 | 0.828 |
| Persistencia | 0.680 | 0.849 |
| Media móvil 7 días | 0.777 | 0.994 |

La regresión fue la mejor, pero solo un 2.1 % por debajo de la persistencia. En la práctica igualó al baseline (ver la conclusión en `bitacora_ia.md`).

## Archivos que genera

- `grafica_serie_completa.png`: serie histórica con tendencia y período de prueba sombreado.
- `grafica_real_vs_prediccion.png`: valores reales frente a los tres pronósticos en el período de prueba.
- `resultados_metricas.csv` y `predicciones_prueba.csv`.

> Nota: los resultados cambian ligeramente en cada ejecución porque la API agrega los días más recientes.
