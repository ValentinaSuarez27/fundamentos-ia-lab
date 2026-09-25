# Componente 3: Vibe Coding. Problema y protocolo de comparación

## 1. Origen del problema

El docente no asignó un enunciado específico, así que el equipo tomó como base el ejemplo que da el propio laboratorio: *"consumir una API pública, validar la respuesta, calcular estadísticas básicas y generar una visualización"*. El mismo problema y el mismo prompt se usan con los tres modelos.

## 2. Enunciado del problema

Construir un programa en Python que:

1. Consulte la API pública **Open-Meteo** (no requiere clave) y obtenga la **temperatura máxima y mínima diaria de Manizales, Colombia, de los últimos 30 días**.
2. **Valide la respuesta:** código HTTP, estructura del JSON, que las listas tengan la misma longitud y que no haya valores faltantes, y maneje errores de conexión con mensajes claros.
3. Calcule **estadísticas básicas** de la temperatura máxima: media, mínimo, máximo, desviación estándar y las fechas en que ocurrieron el mínimo y el máximo.
4. Genere una **gráfica de línea** con ambas series (máxima y mínima), con título, etiquetas de ejes y leyenda, y la guarde como archivo PNG.

## 3. Prompt estándar (idéntico para los tres modelos)

Copiar y pegar **exactamente** este texto como primer mensaje en cada modelo:

```
Escribe un programa completo en Python 3 que haga lo siguiente:

1. Consulte la API pública de Open-Meteo (no requiere clave) para obtener la temperatura máxima y mínima diaria de Manizales, Colombia (latitud 5.07, longitud -75.52), de los últimos 30 días, usando la zona horaria America/Bogota.
2. Valide la respuesta: código HTTP, que el JSON tenga las claves esperadas, que las listas de fechas y temperaturas tengan la misma longitud y que no haya valores nulos. Maneja errores de conexión y tiempo de espera con mensajes claros.
3. Calcule para la temperatura máxima: media, mínimo, máximo, desviación estándar y las fechas en que ocurrieron el mínimo y el máximo. Muestra los resultados en consola de forma ordenada.
4. Genere una gráfica de línea con la temperatura máxima y mínima por fecha, con título, etiquetas en los ejes y leyenda, y guárdala como "temperatura_manizales.png".

Requisitos: usa las librerías requests, pandas y matplotlib. Organiza el código en funciones con docstrings y un bloque if __name__ == "__main__". Al final, sugiere al menos 3 pruebas para verificar que el programa funciona correctamente.
```

## 4. Protocolo de iteración (igual para los tres modelos)

1. Enviar el prompt estándar y **registrar la hora de inicio**.
2. Copiar el código a `vibe_coding/<modelo>/solucion_v1.py` **sin modificarlo** y ejecutarlo.
3. Si hay un error o el resultado no cumple el enunciado, enviar al modelo el siguiente mensaje de corrección, con el error copiado literalmente:

   ```
   Al ejecutar el código obtuve este resultado/error:
   <pegar aquí el error o describir qué no cumple>
   Corrígelo y devuélveme el código completo.
   ```

4. Guardar cada versión como `solucion_v2.py`, `solucion_v3.py`, etc. Cada envío de corrección cuenta como **una iteración**.
5. **Máximo 5 iteraciones.** Si después de 5 no funciona, se registra como "no resuelto por el modelo" y se describe la intervención humana necesaria.
6. La versión final que funcione se guarda también como `solucion_final.py`, y se **registra la hora de finalización**.
7. **Intervención humana:** cualquier cambio que el equipo haga al código a mano, sin pedírselo al modelo, se anota en el registro. Lo ideal es no hacer ninguno y pedirle todo al modelo.

## 5. Criterios de aceptación (checklist de verificación)

Una solución se considera **correcta** si cumple todo lo siguiente:

- [ ] Se ejecuta con `python solucion.py` sin errores.
- [ ] Obtiene datos reales de Open-Meteo para Manizales (coordenadas 5.07, -75.52).
- [ ] Trae aproximadamente 30 días de datos (máximas y mínimas).
- [ ] Valida el código HTTP y la estructura del JSON.
- [ ] Maneja el error de conexión con un mensaje claro (**prueba:** desconectar el wifi y ejecutar).
- [ ] Calcula media, mínimo, máximo y desviación estándar de la temperatura máxima.
- [ ] Muestra las fechas del mínimo y del máximo.
- [ ] Guarda `temperatura_manizales.png` con ambas series, título, ejes y leyenda.
- [ ] Usa funciones con docstrings y `if __name__ == "__main__"`.
- [ ] Sugiere al menos 3 pruebas.
