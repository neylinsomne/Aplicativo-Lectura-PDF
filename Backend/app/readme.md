![ETL pasajes](https://i.ibb.co/G29XycQ)


Después del ETL vamos a ver el proceso de conexión entre Backend y Frontend

-Qué hace cada archivo y cada Carpeta?

--Carpeta BD:
Se encarga de manejar todos los procesos que conllevan a la base postgres, desde la creación del modelo de cada tabla, hasta la inserción de estos datos.
-conectar.py:
contiene las URI y la conexión en si que se da con

-insertar_datos.py:
se encarga de cargar desde un df y la session (que se obtiene desde el archivo conectar)

-Lectura.py:
Se encarga de leer desde las imagenes hasta los archivos pdf en si

-Pipeline.py:
El corazón de este proyecto en si se encarga de procesar la información obtenida desde lectura.py, tomando el procesamiento de imagen
