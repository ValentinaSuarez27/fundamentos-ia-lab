"""
evaluation.py - División temporal, métricas (MAE y RMSE) y gráficas.

Responsabilidad de este módulo (fase de PRUEBAS / EVALUACIÓN):
    1. Separar entrenamiento y prueba respetando el orden temporal
       (los últimos N días son la prueba; nunca se mezclan ni se barajan).
    2. Calcular MAE y RMSE de cada método en el período de prueba.
    3. Generar las gráficas: serie completa y real vs. predicción.

Métricas:
    MAE  = promedio de |real - pronóstico|               (error típico, en °C)
    RMSE = raíz del promedio de (real - pronóstico)^2   (penaliza más los errores grandes, en °C)
"""
import matplotlib

matplotlib.use("Agg")  # guardar imágenes sin abrir ventanas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

DIAS_PRUEBA = 60


def dividir_temporal(serie, dias_prueba=DIAS_PRUEBA):
    """
    Devuelve la fecha de corte: desde ella empieza el período de prueba.

    Todo lo anterior a la fecha de corte es entrenamiento. No se baraja nada.

    Args:
        serie (pandas.Series): Serie indexada por fecha, en orden.
        dias_prueba (int): Número de días finales reservados para prueba.

    Returns:
        pandas.Timestamp: Primera fecha del período de prueba.
    """
    if dias_prueba >= len(serie):
        raise ValueError("El período de prueba no puede ser mayor que la serie.")
    return serie.index[-dias_prueba]


def calcular_metricas(real, pronosticos):
    """
    Calcula MAE y RMSE de cada método en las fechas donde hay valor real y pronóstico.

    Args:
        real (pandas.Series): Valores reales del período de prueba.
        pronosticos (dict[str, pandas.Series]): Nombre del método -> pronósticos.

    Returns:
        pandas.DataFrame: Una fila por método, columnas MAE y RMSE, ordenado de mejor a peor MAE.
    """
    filas = []
    for nombre, pronostico in pronosticos.items():
        pares = pd.concat([real, pronostico], axis=1, join="inner").dropna()
        y, y_hat = pares.iloc[:, 0], pares.iloc[:, 1]
        filas.append({
            "Método": nombre,
            "MAE (°C)": mean_absolute_error(y, y_hat),
            "RMSE (°C)": float(np.sqrt(mean_squared_error(y, y_hat))),
            "Días evaluados": len(pares),
        })
    return pd.DataFrame(filas).sort_values("MAE (°C)").reset_index(drop=True)


def grafica_serie_completa(serie, fecha_corte, archivo="grafica_serie_completa.png"):
    """Grafica la serie histórica completa y sombrea el período de prueba."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(serie.index, serie.values, color="#1f77b4", linewidth=1, label="Temperatura media diaria")
    ax.plot(serie.rolling(30, center=True).mean(), color="#ff7f0e", linewidth=2, label="Promedio móvil 30 días (tendencia)")
    ax.axvspan(fecha_corte, serie.index[-1], color="gray", alpha=0.2, label="Período de prueba")
    ax.set_title(f"Temperatura media diaria en Manizales ({serie.index[0]:%d/%m/%Y} – {serie.index[-1]:%d/%m/%Y})")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo


def grafica_real_vs_prediccion(real, pronosticos, archivo="grafica_real_vs_prediccion.png"):
    """Grafica el período de prueba: valores reales frente a cada pronóstico."""
    estilos = {
        "Persistencia": dict(color="#2ca02c", linestyle="--"),
        "Media móvil 7 días": dict(color="#9467bd", linestyle=":"),
        "Regresión lineal (7 rezagos)": dict(color="#d62728", linestyle="-"),
    }
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(real.index, real.values, color="black", marker="o", markersize=3, linewidth=1.5, label="Real")
    for nombre, pronostico in pronosticos.items():
        ax.plot(pronostico.index, pronostico.values, linewidth=1.5, label=nombre,
                **estilos.get(nombre, {}))
    ax.set_title(f"Real vs. pronóstico a un día – período de prueba ({len(real)} días)")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo
