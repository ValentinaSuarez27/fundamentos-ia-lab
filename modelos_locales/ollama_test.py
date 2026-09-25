"""
ollama_test.py - Consumo de un modelo local mediante la API REST de Ollama.

Arquitectura (Componente 2):
    MODELO (qwen2.5-coder:7b) -> OLLAMA (runtime/servidor) -> API LOCAL (http://localhost:11434)
    -> APLICACIÓN PYTHON (este programa)

Requisitos:
    - Ollama en ejecución (http://localhost:11434 debe responder "Ollama is running").
    - El modelo descargado:  ollama pull qwen2.5-coder:7b
    - Librería requests:     pip install requests

Uso:
    python ollama_test.py
    python ollama_test.py gemma4:e4b          (para probar otro modelo)
"""
import sys
import time

import requests

URL_BASE = "http://localhost:11434"
MODELO = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder:7b"
PROMPT = (
    "Escribe una función en Python llamada media_movil(valores, ventana) que reciba "
    "una lista de números y un entero, y devuelva la media móvil simple. Incluye un ejemplo de uso."
)


def verificar_servidor() -> None:
    """Comprueba que el servidor de Ollama esté activo antes de enviar la consulta."""
    try:
        r = requests.get(URL_BASE, timeout=5)
        print(f"[OK] Servidor: {r.text.strip()}")
    except requests.exceptions.ConnectionError:
        sys.exit("[ERROR] No hay conexión con Ollama. Ábrelo o ejecuta 'ollama serve' y vuelve a intentar.")


def consultar_modelo(prompt: str) -> dict:
    """Envía un mensaje al endpoint /api/chat y devuelve la respuesta JSON."""
    payload = {
        "model": MODELO,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,                     # respuesta completa en un solo JSON
        "options": {"temperature": 0.2},     # temperatura baja: salida más estable para código
    }
    respuesta = requests.post(f"{URL_BASE}/api/chat", json=payload, timeout=600)
    if respuesta.status_code == 404:
        sys.exit(f"[ERROR] El modelo '{MODELO}' no está descargado. Ejecuta: ollama pull {MODELO}")
    respuesta.raise_for_status()
    return respuesta.json()


def main() -> None:
    print("=" * 60)
    print(f"Prueba de API local de Ollama | Modelo: {MODELO}")
    print("=" * 60)
    verificar_servidor()

    print(f"\n[PROMPT]\n{PROMPT}\n")
    print("Esperando respuesta del modelo (puede tardar en CPU)...\n")

    inicio = time.perf_counter()
    datos = consultar_modelo(PROMPT)
    duracion_cliente = time.perf_counter() - inicio

    print("[RESPUESTA DEL MODELO]")
    print(datos["message"]["content"])

    # Ollama reporta los tiempos en nanosegundos
    ns = 1e9
    tokens_salida = datos.get("eval_count", 0)
    tiempo_generacion = datos.get("eval_duration", 0) / ns
    print("\n" + "=" * 60)
    print("[MÉTRICAS]")
    print(f"Tiempo medido por Python:     {duracion_cliente:.2f} s")
    print(f"Tiempo total (Ollama):        {datos.get('total_duration', 0) / ns:.2f} s")
    print(f"Tiempo de carga del modelo:   {datos.get('load_duration', 0) / ns:.2f} s")
    print(f"Tokens de entrada:            {datos.get('prompt_eval_count', 0)}")
    print(f"Tokens generados:             {tokens_salida}")
    if tiempo_generacion > 0:
        print(f"Velocidad de generación:      {tokens_salida / tiempo_generacion:.2f} tokens/s")
    print("=" * 60)


if __name__ == "__main__":
    main()
