# ============================================================
# Código generado por Qwen2.5-Coder-7B-Instruct (LM Studio) para la consulta C2
# Transcrito sin modificaciones desde la respuesta del modelo.
# ============================================================
def media_movil(valores, ventana):
    if len(valores) < ventana:
        raise ValueError("La lista debe tener al menos tantos elementos como el tamaño de la ventana.")

    medias = []
    for i in range(len(valores)-ventana+1):
        subconjunto = valores[i:i+ventana]
        media = sum(subconjunto)/len(subconjunto)
        medias.append(media)

    return medias

# Ejemplo de uso:
valores = [1, 2, 3, 4, 5, 6, 7, 8, 9]
ventana = 3

print(media_movil(valores, ventana))
# Output: [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]


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
