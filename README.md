# Modelado 3D basado en Visión Artificial
Herramienta destinada a la generación de entornos 3D simplificados a partir de imágenes reales, en tiempo real y manteniendo los entornos más extendidos en los ámbitos de inteligencia artificial y generación de gráficos 3D. Además, se proporcionan los complementos necesarios para establecer una comunicación genérica entre Python y Unity.

## Motivación
Se trata de mi proyecto de fin de carrera en Desarrollo y Diseño de Videojuegos en la Univerdidad Rey Juan Carlos, que junto mi tutor de TFG, vimos interesante para el estudio de los problemas surgidos a la hora de plasmar un entorno real en su expersión virtual 3D y su aplicación en sistemas de aprendizaje automático, en especial algoritmos de aprendizaje por refuerzo.

Este ha sido un gran primer paso personal a la hora de abordar problemas relacionados con la Inteligencia Artificial, sector en el que espero dirigir mi desarrollo académico. 

## Objetivo
El presente proyecto debe dotar a los desarrolladores de una herramienta que les permita modelar un entorno real en una simplificación virtual de libre acceso y que sea sencillo adaptarlo a otro tipo de proyectos. Respetando además, los entornos de desarrollo habituales en los campos de inteligencia artificial y representación gráfica.

## Diseño
Para conseguir el objetivo principal, se subdivide el problema en 3 partes:
### Procesado de información visual:
Se parte de las imágenes RGB y de profundidad, empleando redes neuronales profundas especializadas en la clasificación y localización de entidades en una imagen, las cuales, como dato de entrada reciben la imagen RGB y como salida, producen un array con las entidades detectadas. A continuación, se utiliza el mapa de profundidad para obtener información de distancia y la orientación estimada. Por último, es necesario depurar la información obtenida y reducir al mínimo los errores que pudieran existir por solapamientos entre entidades.
### Comunicación entre entornos:
Este proceso se realiza en el cliente (procesado de información visual) y en el servidor (representación gráfica). En el lado del cliente, se seleccionan los datos relevantes de cada entidad: la clase a la que pertenece, su ancho y alto en píxeles, la coordenada (x,y) de su píxel central, la distancia a la que se encuentra de la cámara y la rotación estimada. En el servidor, se traducen estos datos de nuevo para poder operar con ellos y realizar los últimos cálculos necesarios para su representación gráfica.
### Representación gráfica:
Es la encargada de traducir la información anterior en un prisma rectángular y ubicarlo en un espacio 3D. Para ello, se realizan los últimos cálculos para obtener los vectores de tres coordenadas (x, y, z) que permita ubicar cada entidad en el entorno y su escala, se aplica la rotación estimada en el "eje y" y por último, se aplica un color dependiendo de la clase detectada.

## Resultados
La siguiente tabla muestra la precisión, calculada con la desviación media, del programa a la hora de posicionar, escalar y rotar los prismas rectangulares que representan las entidades contenidas en las imágenes procesadas. La posición se describe con un vector de 2 coordenadas (x, z), la escala con un vector de 3 coordenadas (x, y, z) y la rotación en el eje.
| **Experimento** | **Posición (m)** | **Escala** | **Rotación (grados)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | ±0.012, ±0.042 | nd, ±0.077, nd | nd |
| **2** | ±0.007, ±0.014 | ±0.007, ±0.017, nd | nd |
| **3** | ±0.002, ±0.012 | ±0.008, ±0.005, nd | ±1.248 |
| **4** | ±0.006, ±0.011 | ±0.017, ±0.009, nd | ±0.015 |
| **5** | ±0.011, ±0.045 | nd, ±0.041, nd | nd |
| **Desviación media** | **±0.008, ±0.025** | **±0.011, ±0.03, nd** | **±0.631** |

Tabla de exactitud, calculada con el error medio.
| **Experimento** | **Posición (m)** | **Escala** | **Rotación (grados)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | 1.11, 0.53 | nd, 0.38, nd | nd |
| **2** | 0.45, 1.25 | 0.72, 0.29, 0.18 | nd |
| **3** | 0.41, 0.82 | 0.30, 0.24, 0.16 | 27.51 |
| **4** | nd, 3.41 | 1.33, 0.47, 0.18 | 0.34 |
| **5** | 1.06, 0.40 | nd, 0.52, nd | nd |
| **Media** | **0.75, 1.28** | **0.78, 0.38, 0.17** | **13.92** |

Tabla de rendimiento de los algoritmos empleados (medidas en segundos).
| **Experimento** | **Yolo** | **Posicionamiento** | **Orientación** | **Oclusión** | **Suma** |
|:-------:|:------:|:-------------:|:-------:|:-------------:|:-------:|
| **1** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **2** | 0.181012 | 0.004479 | 0.005126 | 0.000092 | 0.190504 |
| **3** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **4** | 0.244766 | 0.008196 | 0.004057 | 0.000166 | 0.257959 |
| **5** | 0.187091 | 0.005373 | 0.006858 | 0.000044 | 0.195654 |
| **6** | 0.201137 | 0.005176 | 0.011905 | 0.000116 | 0.215897 |
| **Media** | **0.198748** | **0.004852** | **0.004673** | **0.000076** | **0.208468** |

## Guías:
 - [Uso genérico del sistema de comunicación](docs/Guia_del_sistema_de_comunicacion.md)
 - [Generación de entornos](Guia_para_la_generación_de_entornos.md)

## Referencias
 - [Implementación de YoloV3 con TensorFlow 2, autor Zihao Zhang (zzh8829)](https://github.com/zzh8829/yolov3-tf2)

