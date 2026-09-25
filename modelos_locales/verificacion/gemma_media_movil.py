# ============================================================
# Código generado por gemma4:e4b (Ollama) para la consulta C2
# Transcrito sin modificaciones desde la respuesta del modelo.
# ============================================================
from typing import List

def media_movil(valores: List[float], ventana: int) -> List[float]:
    """
    Calcula la Media Móvil Simple (SMA) de una serie de valores.

    Args:
        valores: La lista de números (la serie temporal).
        ventana: El tamaño de la ventana o período de cálculo.

    Returns:
        Una lista de floats que contiene la media móvil en cada paso.
    Raises:
        ValueError: Si la ventana no es un entero positivo.
    """
    # 1. Validación de entradas
    if not isinstance(ventana, int) or ventana <= 0:
        raise ValueError("La ventana debe ser un entero positivo.")

    if len(valores) < ventana:
        # Si la lista es más corta que la ventana, no se puede calcular.
        print("Advertencia: La lista es más corta que el tamaño de la ventana.")
        return []

    media_movil_result = []

    # 2. Lógica de cálculo
    # El bucle va hasta el índice que permite formar la última ventana completa.
    for i in range(len(valores) - ventana + 1):
        # Se extrae la porción (la ventana) de datos actual.
        ventana_actual = valores[i : i + ventana]

        # Se calcula el promedio de la ventana.
        media = sum(ventana_actual) / ventana
        media_movil_result.append(media)

    return media_movil_result

# ==================================================
# EJEMPLO DE USO
# ==================================================

# 1. Datos de ejemplo (simulando ventas diarias)
ventas_diarias = [10.0, 12.0, 15.0, 11.0, 9.0, 14.0, 16.0]

# 2. Definir el tamaño de la ventana (usaremos 3 días)
periodo_ventana = 3

print("--------------------------------------------------")
print(f"Serie Original (Ventas): {ventas_diarias}")
print(f"Periodo de cálculo (Ventana): {periodo_ventana} días")

try:
    # 3. Llamar a la función
    sma_result = media_movil(ventas_diarias, periodo_ventana)

    print("\nMedia Móvil Simple Calculada:")
    # Imprimir resultados formateados
    print(f"El resultado muestra el promedio de los siguientes periodos:")

    # Se imprime una tabla de fácil lectura
    for i, media in enumerate(sma_result):
        # Determinar qué período cubre este cálculo
        inicio = i
        fin = i + periodo_ventana - 1
        print(f"  Paso {i+1}: Promedio de [Día {inicio+1} a Día {fin+1}] = {media:.2f}")

except ValueError as e:
    print(f"\nError al ejecutar la función: {e}")


# ============================================================
# PRUEBAS AGREGADAS POR EL EQUIPO (verificación humana)
# ============================================================
print("\n========== PRUEBAS DEL EQUIPO ==========")
casos = [
    ("Caso normal [1..10], ventana 3", list(range(1, 11)), 3),
    ("Lista más corta que la ventana", [1, 2], 3),
    ("Ventana = 0", [1, 2, 3, 4], 0),
    ("Ventana negativa (-2)", [1, 2, 3, 4], -2),
]
for nombre, valores, ventana in casos:
    try:
        print(f"{nombre}: {media_movil(valores, ventana)}")
    except Exception as e:
        print(f"{nombre}: {type(e).__name__} -> {e}")
