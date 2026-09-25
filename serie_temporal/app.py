"""
app.py - Aplicación principal del Componente 4 (reto integrador).

Flujo completo:
    API -> JSON -> PYTHON/PANDAS -> PREPARACIÓN -> SERIE TEMPORAL -> MODELO
        -> PREDICCIÓN -> MAE/RMSE -> GRÁFICAS

Uso (desde la carpeta serie_temporal):
    python app.py

Salidas:
    - Informe de validación, ecuación del modelo y tabla de métricas en consola.
    - grafica_serie_completa.png y grafica_real_vs_prediccion.png
    - resultados_metricas.csv y predicciones_prueba.csv
"""
import sys

import pandas as pd

from api_client import ErrorAPI, obtener_datos_historicos
from evaluation import (DIAS_PRUEBA, calcular_metricas, dividir_temporal,
                        grafica_real_vs_prediccion, grafica_serie_completa)
from model import (crear_rezagos, describir_modelo, entrenar_regresion,
                   pronostico_media_movil, pronostico_persistencia,
                   pronostico_regresion)
from preprocessing import ErrorDatos, imprimir_informe, preparar_serie


def main():
    """Ejecuta el flujo completo y devuelve 0 si todo sale bien, o 1 si hay un error."""
    linea = "=" * 60
    print(linea)
    print(" PRONÓSTICO DE TEMPERATURA MEDIA DIARIA - MANIZALES")
    print(linea)

    # 1. API -> JSON
    print("\n[1/5] Consultando la API de Open-Meteo...")
    try:
        datos = obtener_datos_historicos()
    except ErrorAPI as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    # 2. JSON -> DataFrame validado (serie temporal)
    print("[2/5] Validando y preparando la serie temporal...")
    try:
        df, informe = preparar_serie(datos)
    except ErrorDatos as error:
        print(f"ERROR en los datos: {error}", file=sys.stderr)
        return 1
    serie = df["temperatura"]
    imprimir_informe(informe)

    # 3. División temporal (sin mezclar el orden)
    fecha_corte = dividir_temporal(serie, DIAS_PRUEBA)
    print(f"\n[3/5] División temporal:")
    print(f"  Entrenamiento: {serie.index[0]:%Y-%m-%d} a "
          f"{serie.index[serie.index < fecha_corte][-1]:%Y-%m-%d} "
          f"({int((serie.index < fecha_corte).sum())} días)")
    print(f"  Prueba       : {fecha_corte:%Y-%m-%d} a {serie.index[-1]:%Y-%m-%d} ({DIAS_PRUEBA} días)")

    # 4. Modelos: baselines + regresión entrenada SOLO con el período de entrenamiento
    print("\n[4/5] Entrenando el modelo y generando pronósticos...")
    tabla = crear_rezagos(serie)
    modelo = entrenar_regresion(tabla[tabla.index < fecha_corte])
    print(f"  Ecuación: {describir_modelo(modelo)}")

    real = serie.loc[fecha_corte:]
    pronosticos = {
        "Persistencia": pronostico_persistencia(serie).loc[fecha_corte:],
        "Media móvil 7 días": pronostico_media_movil(serie).loc[fecha_corte:],
        "Regresión lineal (7 rezagos)": pronostico_regresion(modelo, tabla[tabla.index >= fecha_corte]),
    }

    # 5. Evaluación: métricas y gráficas
    print("\n[5/5] Evaluando en el período de prueba...")
    metricas = calcular_metricas(real, pronosticos)
    print("\n" + metricas.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    mejor = metricas.iloc[0]
    mae_persistencia = metricas.loc[metricas["Método"] == "Persistencia", "MAE (°C)"].iloc[0]
    mejora = 100 * (mae_persistencia - mejor["MAE (°C)"]) / mae_persistencia
    print(f"\nMejor método por MAE: {mejor['Método']} ({mejor['MAE (°C)']:.3f} °C).")
    if mejor["Método"] != "Persistencia":
        print(f"Reduce el MAE un {mejora:.1f} % frente al baseline de persistencia.")
    else:
        print("Ningún método superó al baseline de persistencia.")

    metricas.to_csv("resultados_metricas.csv", index=False, encoding="utf-8-sig")
    pd.concat([real.rename("Real"), *pronosticos.values()], axis=1).round(3).to_csv(
        "predicciones_prueba.csv", encoding="utf-8-sig")
    g1 = grafica_serie_completa(serie, fecha_corte)
    g2 = grafica_real_vs_prediccion(real, pronosticos)
    print(f"\nArchivos generados: {g1}, {g2}, resultados_metricas.csv, predicciones_prueba.csv")
    print(linea)
    return 0


if __name__ == "__main__":
    sys.exit(main())
