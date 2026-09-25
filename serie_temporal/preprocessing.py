"""
preprocessing.py - Conversión del JSON de la API en una serie temporal validada.

Responsabilidad de este módulo (fase de ANÁLISIS / IMPLEMENTACIÓN):
    1. Convertir la respuesta JSON en un DataFrame de pandas.
    2. Validar: estructura, tipos de datos, fechas, valores faltantes,
       duplicados y orden temporal.
    3. Dejar la serie lista para modelar (una fila por día, sin huecos).

Decisión del equipo sobre valores faltantes: si faltan pocos datos (máximo el
5 %), se rellenan por interpolación lineal entre los días vecinos y se informa
cuántos se rellenaron. Si faltan más, se detiene el programa, porque rellenar
demasiado inventaría la serie.
"""
import pandas as pd

VARIABLE = "temperature_2m_mean"
MAX_PORCENTAJE_FALTANTES = 5.0


class ErrorDatos(Exception):
    """Error propio para datos con estructura o contenido inválido."""


def json_a_dataframe(datos, variable=VARIABLE):
    """
    Convierte el JSON de Open-Meteo en un DataFrame con columnas "fecha" y "temperatura".

    Args:
        datos (dict): Respuesta JSON de la API.
        variable (str): Nombre de la variable diaria dentro de "daily".

    Returns:
        pandas.DataFrame: Columnas "fecha" (datetime) y "temperatura" (float).

    Raises:
        ErrorDatos: Si faltan claves o las listas no tienen la misma longitud.
    """
    if not isinstance(datos, dict) or "daily" not in datos:
        raise ErrorDatos('La respuesta no contiene la clave "daily".')

    diario = datos["daily"]
    for clave in ("time", variable):
        if clave not in diario:
            raise ErrorDatos(f'Falta la clave "daily.{clave}".')

    if len(diario["time"]) != len(diario[variable]):
        raise ErrorDatos(
            f"Longitudes distintas: {len(diario['time'])} fechas y "
            f"{len(diario[variable])} valores."
        )
    if len(diario["time"]) == 0:
        raise ErrorDatos("La respuesta no contiene datos.")

    return pd.DataFrame({"fecha": diario["time"], "temperatura": diario[variable]})


def validar_y_limpiar(df):
    """
    Valida tipos, fechas, duplicados, orden y faltantes, y deja una serie diaria continua.

    Args:
        df (pandas.DataFrame): Salida de `json_a_dataframe`.

    Returns:
        tuple: (serie limpia como DataFrame indexado por fecha, informe de validación como dict)

    Raises:
        ErrorDatos: Si hay fechas inválidas, valores no numéricos o demasiados faltantes.
    """
    informe = {"registros_recibidos": len(df)}

    # 1. Tipos de datos: fechas y números
    fechas = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    if fechas.isna().any():
        raise ErrorDatos(f"Hay {int(fechas.isna().sum())} fecha(s) con formato inválido.")
    valores = pd.to_numeric(df["temperatura"], errors="coerce")
    no_numericos = int(valores.isna().sum() - df["temperatura"].isna().sum())
    if no_numericos > 0:
        raise ErrorDatos(f"Hay {no_numericos} valor(es) de temperatura que no son números.")
    df = pd.DataFrame({"fecha": fechas, "temperatura": valores})

    # 2. Duplicados: una sola medición por día
    duplicados = int(df["fecha"].duplicated().sum())
    informe["fechas_duplicadas_eliminadas"] = duplicados
    df = df.drop_duplicates(subset="fecha", keep="first")

    # 3. Orden temporal
    informe["estaba_ordenada"] = bool(df["fecha"].is_monotonic_increasing)
    df = df.sort_values("fecha").set_index("fecha")

    # 4. Días faltantes en el calendario (se agregan como NaN)
    calendario = pd.date_range(df.index.min(), df.index.max(), freq="D")
    informe["dias_ausentes_en_calendario"] = len(calendario) - len(df)
    df = df.reindex(calendario)
    df.index.name = "fecha"

    # 5. Valores faltantes
    faltantes = int(df["temperatura"].isna().sum())
    porcentaje = 100 * faltantes / len(df)
    informe["valores_faltantes"] = faltantes
    informe["porcentaje_faltantes"] = round(porcentaje, 2)
    if porcentaje > MAX_PORCENTAJE_FALTANTES:
        raise ErrorDatos(
            f"Faltan {faltantes} valores ({porcentaje:.1f} %), más del "
            f"{MAX_PORCENTAJE_FALTANTES} % permitido."
        )
    if faltantes > 0:
        df["temperatura"] = df["temperatura"].interpolate(method="linear").bfill().ffill()
    informe["valores_interpolados"] = faltantes

    # 6. Rango físico razonable para Manizales (control de calidad)
    fuera_rango = int(((df["temperatura"] < -5) | (df["temperatura"] > 40)).sum())
    informe["valores_fuera_de_rango"] = fuera_rango
    if fuera_rango > 0:
        raise ErrorDatos(f"Hay {fuera_rango} temperatura(s) fuera del rango físico esperado (-5 a 40 °C).")

    informe["registros_finales"] = len(df)
    informe["fecha_inicio"] = df.index.min().strftime("%Y-%m-%d")
    informe["fecha_fin"] = df.index.max().strftime("%Y-%m-%d")
    return df, informe


def preparar_serie(datos):
    """Ejecuta la conversión y la validación completas. Devuelve (serie, informe)."""
    return validar_y_limpiar(json_a_dataframe(datos))


def imprimir_informe(informe):
    """Muestra en consola el informe de validación de forma ordenada."""
    print("---------- Informe de validación ----------")
    etiquetas = {
        "registros_recibidos": "Registros recibidos",
        "fechas_duplicadas_eliminadas": "Fechas duplicadas eliminadas",
        "estaba_ordenada": "¿Venía en orden temporal?",
        "dias_ausentes_en_calendario": "Días ausentes en el calendario",
        "valores_faltantes": "Valores faltantes (nulos)",
        "porcentaje_faltantes": "Porcentaje de faltantes (%)",
        "valores_interpolados": "Valores rellenados por interpolación",
        "valores_fuera_de_rango": "Valores fuera de rango físico",
        "registros_finales": "Registros finales",
        "fecha_inicio": "Fecha de inicio",
        "fecha_fin": "Fecha de fin",
    }
    for clave, etiqueta in etiquetas.items():
        print(f"{etiqueta:<38}: {informe[clave]}")
    print("-------------------------------------------")


if __name__ == "__main__":
    # Prueba rápida del módulo: python preprocessing.py
    from api_client import obtener_datos_historicos, ErrorAPI

    try:
        serie, informe = preparar_serie(obtener_datos_historicos())
    except (ErrorAPI, ErrorDatos) as error:
        print(f"ERROR: {error}")
    else:
        imprimir_informe(informe)
        print("\nPrimeras filas:")
        print(serie.head())
        print("\nResumen estadístico:")
        print(serie["temperatura"].describe().round(2))
