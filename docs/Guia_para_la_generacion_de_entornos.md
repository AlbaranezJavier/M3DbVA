# Guía para la generación de entornos
En esta guía se enumeran los pasos necesarios para hacer uso de la herramienta desarrollada en este proyecto.

1. En el entorno virtual de Python (versión 3.7) es necesario tener instalados los siguientes módulos: Tensorflow 2.1, opencv-python, absl-py, matplotlib, skikit-learn y numpy.
2. Abrir el proyecto llamado TFG_Python y configurar el intérprete con el entorno virtual anterior.
3. Descargar los pesos de la red neuronal preentrenada de [Yolo](https://pjreddie.com/darknet/yolo/), llamada YOLOv3-320 (YOLOv3-tiny es opcional), en Repositorio/TFG_Python/data, renombrando el archivo a yolov3-320.
4. En el directorio Repositorio/TFB_Python/ se ejecuta el fichero "convert.py", encar-gado de traducir los pesos al formato que el programa necesita y guardarlos en la carpeta llamada "checkpoints".
5. Después, se debe instalar la versión 2019.2.17f1 con Unity Hub o desde el [archivo](https://unity3d.com/get-unity/download/archive) para poder abrir el proyecto de Unity que se encuentra en Repositorio/TFG_Unity.
6. Se puede elegir entre dos versiones ("server y server_floor", ambos en la carpeta "Scenes" de "Assets"), siendo "server_floor" una modificación de "server" que genera un suelo sobre el que se ubican los modelos.
7. Comprobar la dirección IPv4 del equipo (ejecutar en la consola del sistema el comando "ipconfig" en Widnows o "ifconfig" en Linux/Max) y copiar en el apartado "Ip_address" del servidor.
8. Al pulsar el botón play de Unity, se levanta el servidor y queda a la espera de la conexión del entorno de Python, donde ejecutando "detect_video.py" comienza el proceso de generación de modelos. Los resultados se aprecian en el entorno de Unity, mientras que el de Python genera otra ventana donde se puede apreciar las imágenes que se están procesando en ese momento. 

## Documentación
En el entorno de Python se pueden encontrar 4 versiones distintas para el procesado de vídeos: "detect_video.py" aplica todos los algoritmos expuestos, "detect_video_wo_gl.py", "detect_video_wo_gl.py", "detect_video_wo_gl_r.py" y "detect_video_wo_r.py". Las 3 últimas versiones son modificaciones de la primera, donde "gl" significa que no ajusta el ratio de fotogramas y "r" que no estima la orientación de los modelos. Mientras que la versión de "detect.py" únicamente aplica Yolo a una imagen, guardando el resultado en el lugar y con el nombre especificados.

En el entorno de Unity podemos encontrar los siguientes parámetros ajustables para los ficheros "Factory, Factory_floor y Server":

- "Min Distance y Max Distance" determinan el rango de distancia en el que se pueden encontrar los objetos de la simulación.
- "Field Of View Vertical / Horizontal" y la resolución, son los parámetros de la cámara implicada en la grabación.
- Port es el puerto donde el servidor escuchará las peticiones del cliente.

El entorno de Python dispone de los siguientes parámetros:

- "weights" determina el directorio donde se encuentran los pesos de la red neuronal.
- "output" es el directorio de almacenamiento.
- "tiny" es una variable de tipo boolean. Si su valor es verdadero se empleará la versión "yolov3-tiny" en la ejecución.
- "classes" directorio donde se encuentra un fichero con las clases a detectar por Yolo.
- "size" tamaño al que se reescalan las imágenes de entrada.
- "image" especifica el lugar donde se encuentra la imagen o las imágenes a procesar, dependiendo de la versión del programa ejecutada.
- "fps_record" son los fotogramas por segundo a los que se ha realizado el vídeo.
- "x_resolution e y_resolution" es la resolución de las imágenes a procesar.
