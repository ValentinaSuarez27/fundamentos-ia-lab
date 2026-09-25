import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import numpy as np
from typing import Optional, Tuple, Dict, Any

# --- Constantes Globales ---
MANIZALES_LAT = 5.07
MANIZALES_LON = -75.52
API_URL = "https://api.open-meteo.com/v1/forecast_historical"
DIAS_A_CONSULTAR = 30
HORA_LOCAL = "America/Bogota"

def fetch_historical_weather_data(lat: float, lon: float, days: int) -> Optional[pd.DataFrame]:
    """
    Consulta la API de Open-Meteo para obtener datos históricos de temperatura.

    Args:
        lat: Latitud del punto de interés.
        lon: Longitud del punto de interés.
        days: Número de días históricos a consultar.

    Returns:
        Un DataFrame de pandas con las columnas de temperatura, o None si falla la consulta.
    """
    print(f"🔍 Conectando a Open-Meteo para Manizales ({days} días)...")

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_max,temperature_min",
        "forecast_days": days,
        "timezone": "UTC" # Usamos UTC y ajustamos las fechas en pandas
    }

    try:
        # Se usa un timeout de 15 segundos para manejar cortes de conexión
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status() # Lanza excepción para códigos 4xx/5xx

        data: Dict[str, Any] = response.json()

        # 2. Validación de la respuesta
        if not data.get('daily'):
            print("❌ Error de validación: La API no devolvió datos diarios.")
            return None

        try:
            # Crear DataFrame
            df = pd.DataFrame({
                'date': pd.to_datetime(data['daily']['time']),
                'temp_max': data['daily']['temperature_max'],
                'temp_min': data['daily']['temperature_min']
            })

            # Ajustar la zona horaria a America/Bogota
            df['date'] = pd.to_datetime(df['date']).dt.tz_convert('America/Bogota')

            print("✅ Datos obtenidos y validados correctamente.")
            return df

        except KeyError as e:
            print(f"❌ Error de estructura de JSON: Falta la clave esperada {e}.")
            return None
        except Exception as e:
            print(f"❌ Error al procesar el DataFrame: {e}")
            return None

    except requests.exceptions.Timeout:
        print("🚨 Error de Conexión: Tiempo de espera excedido. Revise su conexión a internet.")
        return None
    except requests.exceptions.ConnectionError:
        print("🚨 Error de Conexión: No se pudo conectar con la API. Verifique su red.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"🚨 Error HTTP: Falló la solicitud API. Código: {e.response.status_code}. Mensaje: {e}")
        return None

def calculate_statistics(df: pd.DataFrame) -> Tuple[float, float, float, float, str, str]:
    """
    Calcula estadísticas descriptivas para la temperatura máxima.

    Args:
        df: DataFrame que contiene la temperatura máxima.

    Returns:
        Tuple de resultados estadísticos y fechas de extremos.
    """
    temp_max = df['temp_max']

    # 3. Cálculo de estadísticas
    media = temp_max.mean()
    min_val = temp_max.min()
    max_val = temp_max.max()
    std_dev = temp_max.std()

    # Encontrar fechas de mínimo y máximo
    date_min = df.loc[temp_max.idxmin(), 'date'].strftime('%Y-%m-%d')
    date_max = df.loc[temp_max.idxmax(), 'date'].strftime('%Y-%m-%d')

    return media, min_val, max_val, std_dev, date_min, date_max

def generate_plot(df: pd.DataFrame) -> None:
    """
    Genera y guarda una gráfica de línea de las temperaturas.

    Args:
        df: DataFrame que contiene la temperatura (fecha, temp_max, temp_min).
    """
    print("\n📊 Generando gráfico...")

    # 4. Generar la gráfica
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['temp_max'], label='Máxima (°C)', marker='o', linestyle='-')
    plt.plot(df['date'], df['temp_min'], label='Mínima (°C)', marker='o', linestyle='-')

    plt.title(f'Temperatura Diaria en Manizales, Colombia ({DIAS_A_CONSULTAR} días)')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Mejorar la rotación de etiquetas de la fecha
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Ajusta el layout para que no se corten etiquetas

    # Guardar la figura
    nombre_archivo = "temperatura_manizales.png"
    plt.savefig(nombre_archivo)
    print(f"✅ Gráfico guardado exitosamente como '{nombre_archivo}'")

def main():
    """
    Función principal que orquesta la descarga, análisis y visualización de datos.
    """
    # 1. Consulta y Validación de datos
    weather_df = fetch_historical_weather_data(MANIZALES_LAT, MANIZALES_LON, DIAS_A_CONSULTAR)

    if weather_df is None or weather_df.empty:
        print("\n🛑 No se pudo procesar ningún dato. Terminando ejecución.")
        return

    # 3. Cálculo de Estadísticas
    media, minimo, maximo, std_dev, date_min, date_max = calculate_statistics(weather_df)

    # Mostrar resultados de forma ordenada
    print("\n===================================================")
    print("📈 ESTADÍSTICAS DE TEMPERATURA MÁXIMA (Últimos 30 días)")
    print("===================================================")
    print(f"🌡️  Temperatura Media:          {media:.2f} °C")
    print(f"📉  Temperatura Mínima:        {minimo:.2f} °C (Ocurrió el {date_min})")
    print(f"📈  Temperatura Máxima:        {maximo:.2f} °C (Ocurrió el {date_max})")
    print(f"🌪️  Desviación Estándar:        {std_dev:.2f} °C")
    print("===================================================")

    # 4. Generar y guardar la gráfica
    generate_plot(weather_df)

if __name__ == "__main__":
    # Asegurarse de que matplotlib pueda crear la gráfica
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un error inesperado: {e}")
        print("Asegúrese de tener todas las librerías instaladas: pip install requests pandas matplotlib")