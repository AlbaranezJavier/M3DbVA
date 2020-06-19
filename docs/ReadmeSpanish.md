# [<img src="https://static.dwcdn.net/css/flag-icons/flags/4x3/gb.svg" alt="gb" height="30" align="right"/>](../README.md)
# Modelado 3D basado en Visi�n Artificial
Herramienta destinada a la generaci�n de entornos 3D simplificados a partir de im�genes reales, con un procesamiento en tiempo real y manteniendo los entornos m�s extendidos en los �mbitos de inteligencia artificial y generaci�n de gr�ficos 3D. Adem�s, se proporcionan los complementos necesarios para establecer una comunicaci�n gen�rica entre Python y Unity.

<p align="center">
  <img src="docs/Images/githubgif.gif" alt="example input output gif" width="600" />
</p>

## :bulb:Motivaci�n
Se trata de mi proyecto de fin de carrera en Desarrollo y Dise�o de Videojuegos en la Univerdidad Rey Juan Carlos, que junto a mi tutor de TFG, vimos interesante para el estudio de los problemas surgidos a la hora de plasmar un entorno real en su expresi�n virtual 3D y su aplicaci�n en sistemas de aprendizaje autom�tico, en especial algoritmos de aprendizaje por refuerzo.

Este ha sido un gran primer paso personal a la hora de abordar problemas relacionados con la Inteligencia Artificial, sector en el que espero dirigir mi desarrollo acad�mico. 

## :checkered_flag:Objetivo
El presente proyecto debe dotar a los desarrolladores de una herramienta que les permita modelar un entorno real en una simplificaci�n virtual de libre acceso y que sea sencillo adaptarlo a otro tipo de proyectos, respetando adem�s, los entornos de desarrollo habituales en los campos de inteligencia artificial y representaci�n gr�fica.

## :factory:Dise�o
Para conseguir el objetivo principal, se subdivide el problema en 3 partes:
### Procesado de informaci�n visual:
Se parte de las im�genes RGB y de profundidad, empleando redes neuronales profundas especializadas en la clasificaci�n y localizaci�n de entidades en una imagen, las cuales, como dato de entrada reciben la imagen RGB y como salida, producen un array con las entidades detectadas. A continuaci�n, se utiliza el mapa de profundidad para obtener informaci�n de distancia y la orientaci�n estimada. Por �ltimo, es necesario depurar la informaci�n obtenida y reducir al m�nimo los errores que pudieran existir por solapamientos entre entidades.
### Comunicaci�n entre entornos:
Este proceso se realiza en el cliente (procesado de informaci�n visual) y en el servidor (representaci�n gr�fica). En el lado del cliente, se seleccionan los datos relevantes de cada entidad: la clase a la que pertenece, su ancho y alto en p�xeles, la coordenada (x,y) de su p�xel central, la distancia a la que se encuentra de la c�mara y la rotaci�n estimada. En el servidor, se traducen estos datos de nuevo para poder operar con ellos y realizar los �ltimos c�lculos necesarios para su representaci�n gr�fica.
### Representaci�n gr�fica:
Es la encargada de traducir la informaci�n anterior en un prisma rect�ngular y ubicarlo en un espacio 3D. Para ello, se realizan los �ltimos c�lculos para obtener los vectores de tres coordenadas (x, y, z) que permita ubicar cada entidad en el entorno y su escala, se aplica la rotaci�n estimada en el "eje y" y por �ltimo, se aplica un color dependiendo de la clase detectada.

## :bar_chart:Resultados
La siguiente tabla muestra la precisi�n, calculada con la desviaci�n media, del programa a la hora de posicionar, escalar y rotar los prismas rectangulares que representan las entidades contenidas en las im�genes procesadas. La posici�n se describe con un vector de 2 coordenadas (x, z), la escala con un vector de 3 coordenadas (x, y, z) y la rotaci�n en el eje.
| **Experimento** | **Posici�n (m)** | **Escala** | **Rotaci�n (grados)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | �0.012, �0.042 | nd, �0.077, nd | nd |
| **2** | �0.007, �0.014 | �0.007, �0.017, nd | nd |
| **3** | �0.002, �0.012 | �0.008, �0.005, nd | �1.248 |
| **4** | �0.006, �0.011 | �0.017, �0.009, nd | �0.015 |
| **5** | �0.011, �0.045 | nd, �0.041, nd | nd |
| **Desviaci�n media** | **�0.008, �0.025** | **�0.011, �0.03, nd** | **�0.631** |

Tabla de exactitud, calculada con el error medio.
| **Experimento** | **Posici�n (m)** | **Escala** | **Rotaci�n (grados)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | 1.11, 0.53 | nd, 0.38, nd | nd |
| **2** | 0.45, 1.25 | 0.72, 0.29, 0.18 | nd |
| **3** | 0.41, 0.82 | 0.30, 0.24, 0.16 | 27.51 |
| **4** | nd, 3.41 | 1.33, 0.47, 0.18 | 0.34 |
| **5** | 1.06, 0.40 | nd, 0.52, nd | nd |
| **Media** | **0.75, 1.28** | **0.78, 0.38, 0.17** | **13.92** |

Tabla de rendimiento de los algoritmos empleados (medidas en segundos).
| **Experimento** | **Yolo** | **Posicionamiento** | **Orientaci�n** | **Oclusi�n** | **Suma** |
|:-------:|:------:|:-------------:|:-------:|:-------------:|:-------:|
| **1** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **2** | 0.181012 | 0.004479 | 0.005126 | 0.000092 | 0.190504 |
| **3** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **4** | 0.244766 | 0.008196 | 0.004057 | 0.000166 | 0.257959 |
| **5** | 0.187091 | 0.005373 | 0.006858 | 0.000044 | 0.195654 |
| **6** | 0.201137 | 0.005176 | 0.011905 | 0.000116 | 0.215897 |
| **Media** | **0.198748** | **0.004852** | **0.004673** | **0.000076** | **0.208468** |

## :memo:Requisitos previos
### Gr�ficas Nvidia (provado en series 1000 y 2000)
 - CUDA 10.1
 - cuDNN 7.6.5
### Entorno virtual para Python
 - Numpy
 - Scikit-learn
 - Matplotlib
 - Absl-py
 - Opencv-python
 - Tensorflow 2.1

## :bookmark_tabs:Gu�as
 - [Uso gen�rico del sistema de comunicaci�n](docs/Guia_del_sistema_de_comunicacion.md)
 - [Generaci�n de entornos](docs/Guia_para_la_generacion_de_entornos.md)

## :raised_hands:Referencias
 - [Implementaci�n de YoloV3 con TensorFlow 2, autor Zihao Zhang (zzh8829)](https://github.com/zzh8829/yolov3-tf2)
 - [Algoritmo RANSAC, de la librer�a de Scikit-Learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html)