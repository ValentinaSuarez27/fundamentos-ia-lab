# ============================================================
# Código generado por qwen2.5-coder:7b (Ollama) para la consulta C2
# Transcrito sin modificaciones desde la respuesta del modelo.
# ============================================================
def media_movil(valores, ventana):
    if ventana > len(valores):
        raise ValueError("El tamaño de la ventana debe ser menor o igual a la longitud de la lista de valores")
    medias_móviles = []
    for i in range(len(valores) - ventana + 1):
        media = sum(valores[i:i + ventana]) / ventana
        medias_móviles.append(media)
    return medias_móviles

# Ejemplo de uso:
valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ventana = 3
print(media_movil(valores, ventana))


# ============================================================
# PRUEBAS AGREGADAS POR EL EQUIPO (verificación humana)
# ============================================================
print("\n========== PRUEBAS DEL EQUIPO ==========")
casos = [
    ("Caso normal ventas, ventana 3", [10.0, 12.0, 15.0, 11.0, 9.0, 14.0, 16.0], 3),
    ("Lista más corta que la ventana", [1, 2], 3),
    ("Ventana = 0", [1, 2, 3, 4], 0),
    ("Ventana negativa (-2)", [1, 2, 3, 4], -2),
]
for nombre, valores, ventana in casos:
    try:
        print(f"{nombre}: {media_movil(valores, ventana)}")
    except Exception as e:
        print(f"{nombre}: {type(e).__name__} -> {e}")
