"""
api_client.py - Consulta de datos históricos a la API pública de Open-Meteo.

Responsabilidad de este módulo (fase de ANÁLISIS / IMPLEMENTACIÓN):
    Conectarse a la API, manejar los errores de red y devolver el JSON.
    No transforma ni valida el contenido: eso lo hace preprocessing.py.

API usada: Open-Meteo Historical Weather (gratuita, sin clave para uso no comercial).
Documentación: https://open-meteo.com/en/docs/historical-weather-api
"""
from datetime import date, timedelta

import requests

# --- Configuración ---
URL_API = "https://archive-api.open-meteo.com/v1/archive"
LATITUD = 5.07          # Manizales, Colombia
LONGITUD = -75.52
ZONA_HORARIA = "America/Bogota"
VARIABLE = "temperature_2m_mean"   # temperatura media diaria a 2 m del suelo (°C)
FECHA_INICIO = "2024-01-01"
DIAS_RETRASO_ARCHIVO = 7           # el archivo histórico se actualiza con algunos días de retraso
TIEMPO_ESPERA_S = 30


class ErrorAPI(Exception):
    """Error propio para problemas de conexión o respuestas inválidas de la API."""


def fecha_fin_por_defecto():
    """Devuelve la fecha de fin segura: hoy menos unos días, porque el archivo no tiene los días más recientes."""
    return (date.today() - timedelta(days=DIAS_RETRASO_ARCHIVO)).isoformat()


def obtener_datos_historicos(fecha_inicio=FECHA_INICIO, fecha_fin=None,
                             latitud=LATITUD, longitud=LONGITUD,
                             variable=VARIABLE, timeout=TIEMPO_ESPERA_S):
    """
    Consulta la API de Open-Meteo y devuelve la respuesta JSON como diccionario.

    Args:
        fecha_inicio (str): Fecha inicial en formato AAAA-MM-DD.
        fecha_fin (str | None): Fecha final en formato AAAA-MM-DD. Si es None,
            se usa hoy menos DIAS_RETRASO_ARCHIVO días.
        latitud (float): Latitud del lugar.
        longitud (float): Longitud del lugar.
        variable (str): Variable diaria a consultar.
        timeout (float): Segundos máximos de espera.

    Returns:
        dict: JSON de la respuesta (incluye la clave "daily").

    Raises:
        ErrorAPI: Si no hay conexión, se agota el tiempo, el código HTTP no es 200
            o la respuesta no es un JSON válido.
    """
    if fecha_fin is None:
        fecha_fin = fecha_fin_por_defecto()

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "daily": variable,
        "timezone": ZONA_HORARIA,
    }

    try:
        respuesta = requests.get(URL_API, params=parametros, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ErrorAPI(f"La API no respondió en {timeout} segundos.") from None
    except requests.exceptions.ConnectionError:
        raise ErrorAPI("No se pudo conectar con la API. Revisa tu conexión a internet.") from None
    except requests.exceptions.RequestException as error:
        raise ErrorAPI(f"Error inesperado en la petición: {error}") from None

    if respuesta.status_code != 200:
        # Open-Meteo explica el motivo del error en la clave "reason"
        try:
            motivo = respuesta.json().get("reason", "")
        except ValueError:
            motivo = ""
        raise ErrorAPI(f"La API devolvió el código HTTP {respuesta.status_code}. {motivo}".strip())

    try:
        return respuesta.json()
    except ValueError:
        raise ErrorAPI("La respuesta de la API no es un JSON válido.") from None


if __name__ == "__main__":
    # Prueba rápida del módulo: python api_client.py
    print("Consultando Open-Meteo...")
    try:
        datos = obtener_datos_historicos()
    except ErrorAPI as error:
        print(f"ERROR: {error}")
    else:
        fechas = datos["daily"]["time"]
        valores = datos["daily"][VARIABLE]
        print(f"Registros recibidos: {len(fechas)}")
        print(f"Primer dato: {fechas[0]} -> {valores[0]} °C")
        print(f"Último dato: {fechas[-1]} -> {valores[-1]} °C")
