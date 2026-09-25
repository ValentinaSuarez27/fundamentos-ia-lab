"""
model.py - Baselines y modelo predictivo para la serie de temperatura diaria.

Responsabilidad de este módulo (fase de DISEÑO / IMPLEMENTACIÓN):
    Generar predicciones "a un paso": para cada día t se predice la temperatura
    usando SOLO los valores de días anteriores (t-1, t-2, ...). Así se evita la
    fuga de datos (usar información del futuro para predecir el pasado).

Métodos:
    - Baseline 1, persistencia: "mañana será igual que hoy" -> y_hat(t) = y(t-1)
    - Baseline 2, media móvil: promedio de los 7 días anteriores
    - Modelo: regresión lineal con los 7 rezagos (y(t-1) ... y(t-7)) como variables
"""
import pandas as pd
from sklearn.linear_model import LinearRegression

N_REZAGOS = 7
VENTANA_MEDIA_MOVIL = 7


def pronostico_persistencia(serie):
    """
    Baseline de persistencia: el pronóstico de cada día es el valor del día anterior.

    Args:
        serie (pandas.Series): Temperatura diaria indexada por fecha.

    Returns:
        pandas.Series: Pronóstico para cada fecha (el primer día queda vacío).
    """
    return serie.shift(1).rename("persistencia")


def pronostico_media_movil(serie, ventana=VENTANA_MEDIA_MOVIL):
    """
    Baseline de media móvil: promedio de los `ventana` días ANTERIORES.

    Se aplica shift(1) antes de promediar para no incluir el día que se predice.

    Args:
        serie (pandas.Series): Temperatura diaria indexada por fecha.
        ventana (int): Número de días anteriores a promediar.

    Returns:
        pandas.Series: Pronóstico para cada fecha.
    """
    return serie.shift(1).rolling(window=ventana).mean().rename(f"media_movil_{ventana}d")


def crear_rezagos(serie, n_rezagos=N_REZAGOS):
    """
    Construye la tabla de variables para la regresión: una columna por rezago.

    Ejemplo: la columna "rezago_1" del día t contiene la temperatura del día t-1.

    Args:
        serie (pandas.Series): Temperatura diaria indexada por fecha.
        n_rezagos (int): Número de días anteriores a usar.

    Returns:
        pandas.DataFrame: Columnas rezago_1 ... rezago_n y "objetivo" (el valor del día t),
        sin las primeras filas que no tienen rezagos completos.
    """
    tabla = pd.DataFrame({f"rezago_{k}": serie.shift(k) for k in range(1, n_rezagos + 1)})
    tabla["objetivo"] = serie
    return tabla.dropna()


def entrenar_regresion(tabla_entrenamiento):
    """
    Entrena una regresión lineal con los rezagos del período de entrenamiento.

    Args:
        tabla_entrenamiento (pandas.DataFrame): Salida de `crear_rezagos`, SOLO con fechas de entrenamiento.

    Returns:
        sklearn.linear_model.LinearRegression: Modelo entrenado.
    """
    X = tabla_entrenamiento.drop(columns="objetivo")
    y = tabla_entrenamiento["objetivo"]
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo


def pronostico_regresion(modelo, tabla):
    """
    Genera el pronóstico a un paso para las filas de `tabla`.

    Args:
        modelo (LinearRegression): Modelo ya entrenado.
        tabla (pandas.DataFrame): Salida de `crear_rezagos` para las fechas a predecir.

    Returns:
        pandas.Series: Pronóstico indexado por fecha.
    """
    X = tabla.drop(columns="objetivo")
    return pd.Series(modelo.predict(X), index=tabla.index, name="regresion_lineal")


def describir_modelo(modelo):
    """Devuelve un texto con la ecuación del modelo (coeficientes de cada rezago)."""
    partes = [f"{coef:+.3f}·y(t-{k})" for k, coef in enumerate(modelo.coef_, start=1)]
    return f"y_hat(t) = {modelo.intercept_:.3f} " + " ".join(partes)


if __name__ == "__main__":
    # Prueba rápida del módulo: python model.py
    # (La división y las métricas definitivas están en evaluation.py)
    from api_client import obtener_datos_historicos
    from preprocessing import preparar_serie

    serie = preparar_serie(obtener_datos_historicos())[0]["temperatura"]
    corte = serie.index[-60]  # los últimos 60 días quedan para prueba

    tabla = crear_rezagos(serie)
    modelo = entrenar_regresion(tabla[tabla.index < corte])
    print("Ecuación del modelo:")
    print(describir_modelo(modelo))

    comparacion = pd.concat([
        serie.rename("real"),
        pronostico_persistencia(serie),
        pronostico_media_movil(serie),
        pronostico_regresion(modelo, tabla[tabla.index >= corte]),
    ], axis=1).loc[corte:].round(2)
    print("\nÚltimos 5 días de prueba (real vs. pronósticos):")
    print(comparacion.tail())
