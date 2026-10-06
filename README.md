# BigData

# Proyecto: Análisis de Sensores Industriales

## Objetivo
El objetivo de este proyecto es analizar un conjunto de mediciones de temperatura y vibración provenientes de sensores instalados en maquinaria de cuatro plantas industriales. El script principal procesa esta información para calcular métricas clave (como promedios por planta y temperaturas máximas) y extrae un reporte con las alertas de sobrecalentamiento cuando la temperatura supera el umbral de 85 °C.

## Descripción de los datos
El análisis utiliza el archivo `sensores_industriales.csv`, el cual contiene 100,000 registros con las siguientes columnas:
* `id_registro`: Identificador único de la medición.
* `fecha_hora`: Fecha y hora exacta de la lectura.
* `id_sensor`: Identificador del dispositivo.
* `planta`: Ubicación del sensor (Planta 1 a 4).
* `temperatura_c`: Lectura de temperatura en grados Celsius.
* `vibracion_mm_s`: Lectura de vibración en milímetros por segundo.

**Nota importante:** Todos los datos contenidos en el archivo CSV son mediciones **simuladas** y se utilizan exclusivamente con fines didácticos para este ejercicio.

## Requisitos previos
Este proyecto utiliza un entorno virtual de Python y requiere la instalación de librerías externas declaradas en el archivo `requirements.txt` (principalmente `pandas` para el manejo y análisis eficiente del CSV).

## Comandos para instalar y ejecutar el proyecto

Sigue estos pasos en tu terminal para reproducir el proyecto en tu máquina local:

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   git clone <[text](https://github.com/Mordzet/BigData.git)>
   cd proyecto_sensores