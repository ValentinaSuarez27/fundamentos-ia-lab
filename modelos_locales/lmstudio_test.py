"""
lmstudio_test.py - Consumo de un modelo local mediante la API de LM Studio
(compatible con el formato de OpenAI).

Arquitectura (Componente 2):
    MODELO (Qwen2.5-Coder-7B-Instruct) -> LM STUDIO (runtime/servidor) -> API LOCAL (http://localhost:1234/v1)
    -> APLICACIÓN PYTHON (este programa)

Requisitos:
    - LM Studio abierto, con el modelo cargado y el servidor local iniciado (pestaña Developer).
    - Librería requests:  pip install requests

Uso:
    python lmstudio_test.py
"""
import sys
import time

import requests

URL_BASE = "http://localhost:1234/v1"
PROMPT = (
    "Escribe una función en Python llamada media_movil(valores, ventana) que reciba "
    "una lista de números y un entero, y devuelva la media móvil simple. Incluye un ejemplo de uso."
)


def obtener_modelo() -> str:
    """Consulta /v1/models para saber qué modelo está disponible en el servidor."""
    try:
        r = requests.get(f"{URL_BASE}/models", timeout=5)
    except requests.exceptions.ConnectionError:
        sys.exit("[ERROR] No hay conexión con LM Studio. Inicia el servidor en la pestaña Developer (puerto 1234).")
    r.raise_for_status()
    modelos = [m["id"] for m in r.json().get("data", [])]
    if not modelos:
        sys.exit("[ERROR] El servidor está activo pero no hay modelos disponibles. Carga uno en LM Studio.")
    print(f"[OK] Modelos disponibles: {modelos}")
    # Se prefiere el modelo de código si está en la lista
    for m in modelos:
        if "qwen2.5-coder" in m.lower():
            return m
    return modelos[0]


def consultar_modelo(modelo: str, prompt: str) -> dict:
    """Envía un mensaje al endpoint /v1/chat/completions (formato OpenAI)."""
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "stream": False,
    }
    respuesta = requests.post(f"{URL_BASE}/chat/completions", json=payload, timeout=600)
    respuesta.raise_for_status()
    return respuesta.json()


def main() -> None:
    print("=" * 60)
    print("Prueba de API local de LM Studio")
    print("=" * 60)
    modelo = obtener_modelo()
    print(f"[MODELO USADO] {modelo}")

    print(f"\n[PROMPT]\n{PROMPT}\n")
    print("Esperando respuesta del modelo...\n")

    inicio = time.perf_counter()
    datos = consultar_modelo(modelo, PROMPT)
    duracion = time.perf_counter() - inicio

    print("[RESPUESTA DEL MODELO]")
    print(datos["choices"][0]["message"]["content"])

    uso = datos.get("usage", {})
    tokens_salida = uso.get("completion_tokens", 0)
    print("\n" + "=" * 60)
    print("[MÉTRICAS]")
    print(f"Tiempo total medido por Python: {duracion:.2f} s")
    print(f"Tokens de entrada:              {uso.get('prompt_tokens', 0)}")
    print(f"Tokens generados:               {tokens_salida}")
    if duracion > 0 and tokens_salida:
        print(f"Velocidad aproximada:           {tokens_salida / duracion:.2f} tokens/s (incluye tiempo al primer token)")
    print("=" * 60)


if __name__ == "__main__":
    main()
