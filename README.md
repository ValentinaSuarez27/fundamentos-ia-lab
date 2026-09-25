# Laboratorio: Fundamentos de IA y Desarrollo de Software Aumentado

**Curso:** Fundamentos de Inteligencia Artificial, Ingeniería de Sistemas
**Equipo:** Laura Valentina Suarez · Daniela Garcia · Mariana Otalvaro


Laboratorio en 5 componentes: fundamentos de IA, cartografía de modelos, ejecución de modelos locales, comparación de modelos para programar (*vibe coding*) y una aplicación de series temporales con datos reales.

## Estructura del repositorio

```
fundamentos-ia-lab/
├── README.md                  ← este archivo
├── requirements.txt           ← dependencias con versiones fijas
├── .env.example               ← plantilla de variables de entorno (no se usan claves)
├── mapa_mental/               ← Componente 0
├── cartografia_modelos/       ← Componente 1
├── modelos_locales/           ← Componente 2
├── vibe_coding/               ← Componente 3
├── serie_temporal/            ← Componente 4
└── evidence/                  ← capturas y registros, separados por componente
    ├── componente2/
    ├── componente3/
    └── componente4/
```

## Componentes

| # | Componente | Peso | Entregables principales |
|---|---|---|---|
| 0 | Mapa mental de fundamentos | 15 % | `mapa_mental/Componente0_Mapa_Mental.pdf` (mapa + fichas de 34 conceptos) y `.png` |
| 1 | Cartografía del ecosistema de modelos | 20 % | `cartografia_modelos/modelos.csv` (20 modelos, 6 categorías, con fuentes) y `cartografia_modelos.md` (guía de selección y conclusión) |
| 2 | Modelos locales: Ollama + LM Studio | 20 % | `modelos_locales/registro_tecnico.md`, `ollama_test.py`, `lmstudio_test.py`, `verificacion/` |
| 3 | Vibe Coding: comparación de 3 modelos | 20 % | `vibe_coding/comparativo.md` (bitácoras, tabla comparativa y reflexión), `problema_y_prompt.md`, código de cada modelo en `gemma/`, `qwen/` y `cloud/` |
| 4 | Reto integrador: API + series temporales | 25 % | `serie_temporal/` (5 módulos, `README.md`, `bitacora_ia.md`, gráficas y métricas) |

## Instalación

Requiere **Python 3.14** (probado con 3.14.7 en Windows 11).

```bash
python -m pip install -r requirements.txt
```

Para el Componente 2 se necesitan además **Ollama** (0.34.2) y **LM Studio** (0.4.24), con los modelos `gemma4:e4b` y `qwen2.5-coder:7b` descargados.

## Cómo ejecutar

| Componente | Comando (desde la carpeta indicada) | Requisito |
|---|---|---|
| 2 | `python ollama_test.py` en `modelos_locales/` | Ollama abierto |
| 2 | `python lmstudio_test.py` en `modelos_locales/` | Servidor de LM Studio activo (puerto 1234) |
| 3 | `python solucion_v1.py` en `vibe_coding/cloud/` (o cualquier versión de `gemma/` y `qwen/`) | Internet |
| 4 | `python app.py` en `serie_temporal/` | Internet |

## Resultados destacados

- **Componente 2:** con el mismo modelo (Qwen2.5-Coder 7B, Q4_K_M), LM Studio fue ~30 % más rápido que Ollama en este equipo (~9.0 frente a ~7.3 tokens/s) por usar la GPU integrada. Se verificó la cadena modelo → runtime → API local → aplicación Python.
- **Componente 3:** con el mismo prompt, Gemma 4 E4B y Qwen2.5-Coder 7B (locales) no resolvieron el problema en 5 iteraciones: alucinaron endpoints o no detectaron un error en su propio código. Claude Opus 5.5 (cloud) lo resolvió en 1 iteración. Al comparar resultados se descubrió un empate en la temperatura máxima que solo el modelo cloud reportó.
- **Componente 4:** la regresión lineal con 7 rezagos obtuvo MAE = 0.666 °C frente a 0.680 °C de la persistencia (2.1 % de mejora), es decir, prácticamente igualó al baseline.

## Entorno de pruebas

Windows 11 · AMD Ryzen 7 7735HS (8 núcleos) · 19.7 GB de RAM · GPU integrada AMD Radeon (sin GPU dedicada).

## Evidencias

Las capturas y los registros están en `evidence/`, separados por componente. La lista de capturas del Componente 3 y el significado de cada una están en `evidence/componente3/evidencias_componente3.md`. Las conversaciones completas con los modelos del Componente 3 están en los archivos `*_conversacion_completa.txt`.

## Uso de IA

Todo el código generado por IA se ejecutó y verificó antes de aceptarlo. El proceso está documentado en `modelos_locales/registro_tecnico.md`, `vibe_coding/comparativo.md` y `serie_temporal/bitacora_ia.md`. No se incluyen claves ni credenciales en el repositorio.
