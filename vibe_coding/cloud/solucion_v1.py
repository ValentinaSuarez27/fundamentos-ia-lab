#!/usr/bin/env python3
"""
Consulta la API pública de Open-Meteo para obtener las temperaturas máximas y
mínimas diarias de Manizales (Colombia) de los últimos 30 días, valida la
respuesta, calcula estadísticas de la temperatura máxima y genera una gráfica.

Dependencias: requests, pandas, matplotlib
    pip install requests pandas matplotlib
"""

import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")  # Backend sin ventana: permite guardar la imagen en cualquier entorno
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import requests

# --------------------------------------------------------------------------
# Configuración
# --------------------------------------------------------------------------
URL_API = "https://api.open-meteo.com/v1/forecast"
LATITUD = 5.07
LONGITUD = -75.52
ZONA_HORARIA = "America/Bogota"
DIAS = 30
TIEMPO_ESPERA_S = 15
ARCHIVO_GRAFICA = "temperatura_manizales.png"

CLAVE_FECHAS = "time"
CLAVE_MAX = "temperature_2m_max"
CLAVE_MIN = "temperature_2m_min"


class ErrorDatosClima(Exception):
    """Error propio para problemas de conexión o de validación de datos."""


# --------------------------------------------------------------------------
# 1. Consulta a la API
# --------------------------------------------------------------------------
def obtener_datos(latitud=LATITUD, longitud=LONGITUD, dias=DIAS,
                  zona_horaria=ZONA_HORARIA, timeout=TIEMPO_ESPERA_S):
    """
    Consulta Open-Meteo y devuelve el JSON de la respuesta.

    Se piden `dias` días pasados más el día actual; el día actual se descarta
    después (ver `construir_dataframe`) porque todavía está incompleto.

    Args:
        latitud (float): Latitud del lugar.
        longitud (float): Longitud del lugar.
        dias (int): Número de días pasados a solicitar.
        zona_horaria (str): Zona horaria IANA para agrupar los días.
        timeout (float): Segundos máximos de espera de la petición.

    Returns:
        dict: Contenido JSON de la respuesta.

    Raises:
        ErrorDatosClima: Si hay error de conexión, tiempo de espera agotado,
            código HTTP distinto de 200 o un cuerpo que no es JSON.
    """
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": f"{CLAVE_MAX},{CLAVE_MIN}",
        "timezone": zona_horaria,
        "past_days": dias,
        "forecast_days": 1,
    }

    try:
        respuesta = requests.get(URL_API, params=parametros, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ErrorDatosClima(
            f"La API no respondió en {timeout} segundos. "
            "Inténtalo de nuevo más tarde."
        ) from None
    except requests.exceptions.ConnectionError:
        raise ErrorDatosClima(
            "No se pudo conectar con la API de Open-Meteo. "
            "Revisa tu conexión a internet."
        ) from None
    except requests.exceptions.RequestException as error:
        raise ErrorDatosClima(f"Error inesperado en la petición: {error}") from None

    if respuesta.status_code != 200:
        detalle = ""
        try:
            detalle = respuesta.json().get("reason", "")
        except ValueError:
            pass
        raise ErrorDatosClima(
            f"La API devolvió el código HTTP {respuesta.status_code}"
            + (f": {detalle}" if detalle else ".")
        )

    try:
        return respuesta.json()
    except ValueError:
        raise ErrorDatosClima("La respuesta de la API no es un JSON válido.") from None


# --------------------------------------------------------------------------
# 2. Validación
# --------------------------------------------------------------------------
def validar_datos(datos):
    """
    Verifica que el JSON tenga la estructura y el contenido esperados.

    Comprueba que exista la clave "daily" con las listas de fechas,
    temperaturas máximas y mínimas; que las tres listas tengan la misma
    longitud (y no estén vacías) y que no contengan valores nulos.

    Args:
        datos (dict): JSON devuelto por la API.

    Raises:
        ErrorDatosClima: Si alguna validación falla.
    """
    if not isinstance(datos, dict):
        raise ErrorDatosClima("La respuesta no tiene formato de objeto JSON.")

    if "daily" not in datos or not isinstance(datos["daily"], dict):
        raise ErrorDatosClima('Falta la clave "daily" en la respuesta.')

    diario = datos["daily"]
    for clave in (CLAVE_FECHAS, CLAVE_MAX, CLAVE_MIN):
        if clave not in diario:
            raise ErrorDatosClima(f'Falta la clave "daily.{clave}" en la respuesta.')
        if not isinstance(diario[clave], list):
            raise ErrorDatosClima(f'"daily.{clave}" no es una lista.')

    longitudes = {clave: len(diario[clave]) for clave in (CLAVE_FECHAS, CLAVE_MAX, CLAVE_MIN)}
    if len(set(longitudes.values())) != 1:
        raise ErrorDatosClima(f"Las listas tienen longitudes distintas: {longitudes}")
    if longitudes[CLAVE_FECHAS] == 0:
        raise ErrorDatosClima("La respuesta no contiene datos diarios.")

    for clave in (CLAVE_FECHAS, CLAVE_MAX, CLAVE_MIN):
        nulos = [diario[CLAVE_FECHAS][i] for i, v in enumerate(diario[clave]) if v is None]
        if nulos:
            raise ErrorDatosClima(
                f'Hay {len(nulos)} valor(es) nulo(s) en "daily.{clave}" '
                f"(fechas: {', '.join(map(str, nulos))})."
            )


# --------------------------------------------------------------------------
# Transformación
# --------------------------------------------------------------------------
def construir_dataframe(datos, dias=DIAS, zona_horaria=ZONA_HORARIA, hoy=None):
    """
    Convierte el JSON validado en un DataFrame con los últimos `dias` días
    completos (excluye el día actual y cualquier fecha futura).

    Args:
        datos (dict): JSON ya validado.
        dias (int): Número de días a conservar.
        zona_horaria (str): Zona horaria usada para determinar "hoy".
        hoy (datetime.date | None): Fecha de referencia (útil para pruebas).

    Returns:
        pandas.DataFrame: Columnas "fecha", "t_max" y "t_min", ordenado por fecha.
    """
    diario = datos["daily"]
    df = pd.DataFrame({
        "fecha": pd.to_datetime(diario[CLAVE_FECHAS]),
        "t_max": pd.to_numeric(diario[CLAVE_MAX]),
        "t_min": pd.to_numeric(diario[CLAVE_MIN]),
    }).sort_values("fecha")

    if hoy is None:
        hoy = datetime.now(ZoneInfo(zona_horaria)).date()

    df = df[df["fecha"].dt.date < hoy].tail(dias).reset_index(drop=True)

    if df.empty:
        raise ErrorDatosClima("No quedaron días completos después de filtrar.")
    return df


# --------------------------------------------------------------------------
# 3. Estadísticas
# --------------------------------------------------------------------------
def calcular_estadisticas(df):
    """
    Calcula estadísticas descriptivas de la temperatura máxima.

    La desviación estándar es la muestral (ddof=1), el valor por defecto de pandas.
    Si el mínimo o el máximo se repite, se reportan todas las fechas.

    Args:
        df (pandas.DataFrame): DataFrame con las columnas "fecha" y "t_max".

    Returns:
        dict: media, minimo, maximo, desviacion, fechas_minimo, fechas_maximo, n_dias.
    """
    serie = df["t_max"]
    minimo = serie.min()
    maximo = serie.max()
    return {
        "n_dias": int(serie.count()),
        "media": float(serie.mean()),
        "minimo": float(minimo),
        "maximo": float(maximo),
        "desviacion": float(serie.std()) if serie.count() > 1 else 0.0,
        "fechas_minimo": df.loc[serie == minimo, "fecha"].dt.strftime("%Y-%m-%d").tolist(),
        "fechas_maximo": df.loc[serie == maximo, "fecha"].dt.strftime("%Y-%m-%d").tolist(),
    }


def mostrar_resultados(estadisticas, df):
    """
    Imprime en consola un resumen ordenado de las estadísticas.

    Args:
        estadisticas (dict): Resultado de `calcular_estadisticas`.
        df (pandas.DataFrame): Datos usados, para mostrar el período.
    """
    inicio = df["fecha"].min().strftime("%Y-%m-%d")
    fin = df["fecha"].max().strftime("%Y-%m-%d")
    linea = "=" * 52

    print(linea)
    print(" TEMPERATURA MÁXIMA DIARIA — MANIZALES, COLOMBIA")
    print(linea)
    print(f" Período            : {inicio} a {fin} ({estadisticas['n_dias']} días)")
    print(f" Media              : {estadisticas['media']:6.2f} °C")
    print(f" Desviación estándar: {estadisticas['desviacion']:6.2f} °C")
    print(f" Mínimo             : {estadisticas['minimo']:6.2f} °C  "
          f"({', '.join(estadisticas['fechas_minimo'])})")
    print(f" Máximo             : {estadisticas['maximo']:6.2f} °C  "
          f"({', '.join(estadisticas['fechas_maximo'])})")
    print(linea)


# --------------------------------------------------------------------------
# 4. Gráfica
# --------------------------------------------------------------------------
def generar_grafica(df, archivo=ARCHIVO_GRAFICA):
    """
    Genera una gráfica de líneas con las temperaturas máxima y mínima por fecha
    y la guarda como imagen PNG.

    Args:
        df (pandas.DataFrame): DataFrame con "fecha", "t_max" y "t_min".
        archivo (str): Ruta del archivo de salida.

    Returns:
        str: Ruta del archivo guardado.
    """
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(df["fecha"], df["t_max"], marker="o", color="#d62728", label="Temperatura máxima")
    ax.plot(df["fecha"], df["t_min"], marker="o", color="#1f77b4", label="Temperatura mínima")
    ax.fill_between(df["fecha"], df["t_min"], df["t_max"], color="gray", alpha=0.12)

    ax.set_title(
        f"Temperatura diaria en Manizales, Colombia "
        f"({df['fecha'].min():%d/%m/%Y} – {df['fecha'].max():%d/%m/%Y})"
    )
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    fig.autofmt_xdate()
    fig.tight_layout()

    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------
def main():
    """Ejecuta el flujo completo: consulta, validación, estadísticas y gráfica."""
    try:
        print("Consultando la API de Open-Meteo...")
        datos = obtener_datos()
        validar_datos(datos)
        df = construir_dataframe(datos)
    except ErrorDatosClima as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    estadisticas = calcular_estadisticas(df)
    mostrar_resultados(estadisticas, df)

    try:
        archivo = generar_grafica(df)
    except OSError as error:
        print(f"ERROR: no se pudo guardar la gráfica: {error}", file=sys.stderr)
        return 1

    print(f"Gráfica guardada en: {archivo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
