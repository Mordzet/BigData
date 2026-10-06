# Informe: Parte II. Aplicación al caso de Big Data

### 5. Las 5 V aplicadas al proyecto

| V | Relación con el sistema | Ejemplo concreto | Origen |
|---|---|---|---|
| **Volumen** | Tamaño y cantidad de datos a almacenar. | Escalar de un archivo de 4.4 MiB a generar Terabytes de historial continuo. | Futura ampliación |
| **Velocidad** | Ritmo al que se generan y procesan los datos. | Recibir lecturas de cada sensor una vez por segundo en lugar de una vez por minuto. | Futura ampliación |
| **Variedad** | Diferentes formatos de datos ingeridos. | Procesar en un mismo sistema CSV (tabla), JSON, imágenes de máquinas y reportes (texto libre). | Futura ampliación |
| **Veracidad** | Nivel de confianza y limpieza de los datos. | Identificar si un registro de 105 °C es una falla real de la máquina o un error del propio sensor. | Aparece en el CSV |
| **Valor** | Información útil extraída para el negocio. | Descubrir qué planta concentra la mayor cantidad de alertas para priorizar mantenimientos. | Aparece en el CSV |

### 6. Tipos de datos y procesamiento tradicional

**Clasificación de datos:**
* **Estructurados:** El CSV de sensores.
* **Semiestructurados:** Un mensaje JSON enviado por un sensor.
* **No estructurados:** Una fotografía de una máquina; El texto libre de un reporte de mantenimiento.

**Justificación y limitaciones:**
Un archivo con 100,000 registros y un peso de 4.4 MiB no es Big Data porque puede ser cargado y procesado completamente en la memoria RAM de una computadora personal estándar en fracciones de segundo utilizando herramientas tradicionales (como Pandas o Excel). 
Al aumentar la escala a millones de mediciones, aparecerán limitaciones de hardware: la memoria RAM será insuficiente para cargar el dataset completo, el disco duro presentará cuellos de botella en velocidad de escritura (I/O) y un solo procesador no podrá iterar los datos a tiempo, obligando a migrar a sistemas distribuidos.

### 7. Batch y Streaming

* **Procesamiento realizado (Batch):** El programa ejecuta un procesamiento por lotes (Batch). Esto se justifica porque analiza un conjunto de datos histórico, finito y en reposo (el archivo CSV) de una sola vez, de principio a fin.
* **Enfoque para alerta en segundos (Streaming):** Utilizaría procesamiento en *Streaming* (flujo continuo). Al requerir una alerta casi en tiempo real (baja latencia) ante una condición crítica (>85 °C), el sistema debe analizar cada evento en el momento exacto en que ingresa a la red.
* **Enfoque para resumen al terminar el día (Batch):** Utilizaría procesamiento *Batch*. Dado que el resultado solo se necesita al cierre de la jornada, hay una alta tolerancia al tiempo de respuesta y los datos diarios ya estarán acumulados en una base de datos listos para procesarse juntos.

### 8. Lambda y Kappa

**Escenario A: Combinar historial por lotes con mediciones recientes.**
* **Arquitectura:** Lambda.
* **Justificación:** Es ideal porque mantiene una "Capa Batch" robusta para recalcular el histórico completo con alta precisión, y simultáneamente usa una "Capa Speed" (Streaming) para dar acceso a los datos críticos en tiempo real. Ambas vistas se unen en la capa de servicio.

```text
[ Datos ] ---> [ Capa Batch (Historial) ] ------\
     \                                           +---> [ Capa de Servicio ] ---> Consultas
      \--> [ Capa Speed (Streaming/Reciente) ] -/
```

**Escenario B: Sola lógica de eventos y reprocesamiento.**
* **Arquitectura:** Kappa.
* **Justificación:** Trata todo (histórico y reciente) como un flujo continuo de eventos (Stream). Al mantener una única base de código de procesamiento, simplifica drásticamente la infraestructura. Si se necesita reprocesar datos del pasado, simplemente se vuelve a reproducir el flujo de eventos retenido bajo la misma lógica.

```text
[ Datos ] ---> [ Sistema Ingesta/Retención (ej. Kafka) ] ---> [ Capa Stream ] ---> [ Capa Servicio ] ---> Consultas
```

### 9. Analítica descriptiva, predictiva y prescriptiva

* **Descriptiva:** 
  1. La Planta_3 es la instalación que presenta la mayor cantidad de alertas de temperatura, registrando exactamente 1,777 lecturas por encima del umbral de 85 °C[cite: 13].
  2. El total general de alertas de sobrecalentamiento asciende a 6,954 eventos combinando las cuatro instalaciones (Planta_3: 1777, Planta_1: 1737, Planta_4: 1732, Planta_2: 1708)[cite: 13].
* **Predictiva:** 
  * *Pregunta:* ¿Cuál es la probabilidad de que una máquina en la Planta_3 sufra un fallo mecánico crítico en las próximas 48 horas tras registrar lecturas sostenidas superiores a 95 °C? 
  * *Datos adicionales:* Se necesitaría el registro histórico de averías mecánicas, la antigüedad y ciclo de vida de los componentes, y la bitácora de turnos u horarios de carga de producción.
* **Prescriptiva:** 
  * *Acción propuesta:* Implementar un sistema de control automatizado que reduzca temporalmente la velocidad de operación o active sistemas de refrigeración auxiliares en la máquina en cuanto el sensor reporte 85 °C.
  * *Información a revisar:* Antes de decidir, la gerencia debe contrastar el costo operativo de reducir la velocidad de producción contra el impacto económico que representaría detener la planta por completo debido a una falla catastrófica del equipo.