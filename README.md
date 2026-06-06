# Taller 4: Pipeline de Datos - Art Institute of Chicago
**Autor:** Iván Durango

## Descripción
Este proyecto implementa un flujo ETL completo, entonces el xtrae datos paginados de la API pública del Art Institute of Chicago, los almacena en crudo en MongoDB local, y utiliza Pandas/Seaborn en Jupyter Notebook para realizar limpieza, análisis exploratorio y visualización de datos.

## Ejecución
1. Encender MongoDB local (`brew services start mongodb-community@7.0`).
2. Ejecutar `python ingesta.py` para poblar la base de datos.
3. Ejecutar las celdas de `analisis.ipynb` para ver los resultados.