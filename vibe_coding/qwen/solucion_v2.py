import requests
import pandas as pd
import matplotlib.pyplot as plt

# Constantes
URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = "5.07"
LONGITUDE = "-75.52"
TIME_ZONE = "America/Bogota"
DAYS = "30"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "timezone": TIME_ZONE,
    "daily": "temperature_2m_max,temperature_2m_min",
    "start_date": "2023-04-01",
    "end_date": "2023-04-30"
}

def obtener_datos_clima():
    """
    Obtiene los datos climáticos de Manizales usando la API de Open-Meteo.

    Returns:
        dict: Datos de temperatura máxima y mínima diaria.
    """
    response = requests.get(URL, params=PARAMS)
    if response.status_code != 200:
        raise Exception(f"Error al obtener datos: {response.status_code} {response.text}")

    datos = response.json()
    if not all(clave in datos for clave in ["daily", "time", "temperature_2m_max", "temperature_2m_min"]):
        raise Exception("Respuesta JSON no contiene las claves esperadas")

    datos_clima = {
        "fecha": datos["daily"]["time"],
        "maxima": datos["daily"]["temperature_2m_max"],
        "minima": datos["daily"]["temperature_2m_min"]
    }

    if len(datos_clima["fecha"]) != len(datos_clima["maxima"]) or len(datos_clima["maxima"]) != len(datos_clima["minima"]):
        raise Exception("Las listas de fechas y temperaturas no tienen la misma longitud")

    if None in datos_clima["maxima"] or None in datos_clima["minima"]:
        raise Exception("Hay valores nulos en los datos de temperatura")

    return datos_clima

def calcular_estadisticas(temperaturas):
    """
    Calcula estadísticas básicas para una lista de temperaturas.

    Args:
        temperaturas (list): Lista de temperaturas.

    Returns:
        tuple: Media, mínimo, máximo, desviación estándar.
    """
    media = sum(temperaturas) / len(temperaturas)
    minimo = min(temperaturas)
    maximo = max(temperaturas)
    desviacion_estandar = (sum((x - media) ** 2 for x in temperaturas) / len(temperaturas)) ** 0.5
    return media, minimo, maximo, desviacion_estandar

def graficar_temperaturas(fechas, maxima, minima):
    """
    Genera una gráfica de línea con la temperatura máxima y mínima por fecha.

    Args:
        fechas (list): Lista de fechas.
        maxima (list): Lista de temperaturas máximas.
        minima (list): Lista de temperaturas mínimas.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, maxima, label="Temperatura Máxima", marker="o")
    plt.plot(fechas, minima, label="Temperatura Mínima", marker="x")
    plt.title("Temperatura Máxima y Mínima diaria de Manizales")
    plt.xlabel("Fecha")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("temperatura_manizales.png")

def main():
    try:
        datos_clima = obtener_datos_clima()
        maxima = datos_clima["maxima"]
        minima = datos_clima["minima"]

        media_maxima, minimo_maxima, maximo_maxima, desviacion_maxima = calcular_estadisticas(maxima)
        media_minima, minimo_minima, maximo_minima, desviacion_minima = calcular_estadisticas(minima)

        print(f"Estadísticas de Temperatura Máxima:")
        print(f"Media: {media_maxima:.2f} °C")
        print(f"Mínimo: {minimo_maxima:.2f} °C")
        print(f"Máximo: {maximo_maxima:.2f} °C")
        print(f"Desviación Estándar: {desviacion_maxima:.2f} °C")
        print(f"Fecha del Mínimo: {datos_clima['fecha'][maxima.index(minimo_maxima)]}")
        print(f"Fecha del Máximo: {datos_clima['fecha'][maxima.index(maximo_maxima)]}")

        print("\nEstadísticas de Temperatura Mínima:")
        print(f"Media: {media_minima:.2f} °C")
        print(f"Mínimo: {minimo_minima:.2f} °C")
        print(f"Máximo: {maximo_minima:.2f} °C")
        print(f"Desviación Estándar: {desviacion_minima:.2f} °C")
        print(f"Fecha del Mínimo: {datos_clima['fecha'][minima.index(minimo_minima)]}")
        print(f"Fecha del Máximo: {datos_clima['fecha'][minima.index(maximo_minima)]}")

        graficar_temperaturas(datos_clima["fecha"], maxima, minima)
        print("\nGráfica guardada como 'temperatura_manizales.png'")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Error de tiempo de espera: {e}")
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    main()