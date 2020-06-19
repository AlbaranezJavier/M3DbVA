# [<img src="https://static.dwcdn.net/css/flag-icons/flags/4x3/es.svg" alt="es" height="30" align="right"/>](docs/Guia_del_sistema_de_comunicacion.md)
# 3D Modeling based on Artificial Vision
A tool designed to generate simplified 3D environments from real images, with real-time processing and maintaining the most widespread environments in the fields of artificial intelligence and 3D graphics generation. It also provides the necessary complements to establish a generic communication between Python and Unity.

<p align="center">
  <img src="docs/Images/githubgif.gif" alt="example input output gif" width="600" />
</p>

## :bulb:Motivation
This is my end-of-degree project in Video Game Development and Design at the Rey Juan Carlos University, which together with my TFG tutor, we found interesting for the study of the problems that arise when capturing a real environment in its 3D virtual expression and its application in automatic learning systems, especially reinforcement learning algorithms.

This has been a great first personal step in addressing problems related to Artificial Intelligence, a sector in which I hope to direct my academic development. 

## :checkered_flag:Objective
The present project must provide the developers with a tool that allows them to model a real environment in a virtual simplification of free access and that is easy to adapt to other types of projects, also respecting the usual development environments in the fields of artificial intelligence and graphic representation.

## :factory:Design
To achieve the main objective, the problem is subdivided into 3 parts:
### Visual information processing
The starting point is the RGB and depth images, using deep neural networks specialized in the classification and location of entities in an image, which, as input data receive the RGB image and as output, produce an array with the detected entities. The depth map is then used to obtain distance information and estimated orientation. Finally, it is necessary to debug the information obtained and reduce to a minimum the errors that could exist due to overlaps between entities.
### Communication between environments:
This process is carried out on the client (visual information processing) and on the server (graphic representation). On the client side, the relevant data of each entity is selected: the class it belongs to, its width and height in pixels, the coordinate (x,y) of its central pixel, the distance it is from the camera and the estimated rotation. In the server, these data are translated again in order to operate with them and make the last calculations necessary for their graphic representation.
### Graphical representation:
It is in charge of translating the above information into a rectangular prism and placing it in a 3D space. To do this, the last calculations are made to obtain the vectors of three coordinates (x, y, z) that allow to locate each entity in the environment and its scale, the estimated rotation on the "y-axis" is applied and finally, a color is applied depending on the class detected.

## :bar_chart:Results
The following table shows the accuracy, calculated with the average deviation, of the program when positioning, scaling and rotating the rectangular prisms that represent the entities contained in the processed images. The position is described with a 2 coordinate vector (x, z), the scaling with a 3 coordinate vector (x, y, z) and the rotation on the axis.
| **Experiment** | **Position (m)** | **Scale** | **Rotation (degrees)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | ±0.012, ±0.042 | nd, ±0.077, nd | nd |
| **2** | ±0.007, ±0.014 | ±0.007, ±0.017, nd | nd |
| **3** | ±0.002, ±0.012 | ±0.008, ±0.005, nd | ±1.248 |
| **4** | ±0.006, ±0.011 | ±0.017, ±0.009, nd | ±0.015 |
| **5** | ±0.011, ±0.045 | nd, ±0.041, nd | nd |
| **Average deviation** | **±0.008, ±0.025** | **±0.011, ±0.03, nd** | **±0.631** |

Tabla de exactitud, calculada con el error medio.
| **Experiment** | **Position (m)** | **Scale** | **Rotation (degrees)** |
|:-------:|:------:|:-------------:|:-------:|
| **1** | 1.11, 0.53 | nd, 0.38, nd | nd |
| **2** | 0.45, 1.25 | 0.72, 0.29, 0.18 | nd |
| **3** | 0.41, 0.82 | 0.30, 0.24, 0.16 | 27.51 |
| **4** | nd, 3.41 | 1.33, 0.47, 0.18 | 0.34 |
| **5** | 1.06, 0.40 | nd, 0.52, nd | nd |
| **Mean** | **0.75, 1.28** | **0.78, 0.38, 0.17** | **13.92** |

Tabla de rendimiento de los algoritmos empleados (medidas en segundos).
| **Experiment** | **Yolo** | **Positioning** | **Orientation** | **Occlusion** | **Sum** |
|:-------:|:------:|:-------------:|:-------:|:-------------:|:-------:|
| **1** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **2** | 0.181012 | 0.004479 | 0.005126 | 0.000092 | 0.190504 |
| **3** | 0.189242 | 0.003446 | 0.000046 | 0.000019 | 0.195398 |
| **4** | 0.244766 | 0.008196 | 0.004057 | 0.000166 | 0.257959 |
| **5** | 0.187091 | 0.005373 | 0.006858 | 0.000044 | 0.195654 |
| **6** | 0.201137 | 0.005176 | 0.011905 | 0.000116 | 0.215897 |
| **Mean** | **0.198748** | **0.004852** | **0.004673** | **0.000076** | **0.208468** |

## :memo:Prerequisites
### Nvidia Graphics (tested on 1000 and 2000 series)
 - CUDA 10.1
 - cuDNN 7.6.5
### Virtual environment for Python
 - Numpy
 - Scikit-learn
 - Matplotlib
 - Absl-py
 - Opencv-python
 - Tensorflow 2.1

## :bookmark_tabs:Guides
 - [Generic use of the communication system](docs/Communication_System_Guide.md)
 - [Generation of environments](docs/Environment_generation_guide.md)

## :raised_hands:References
 - [Implementation of YoloV3 with TensorFlow 2, author Zihao Zhang (zzh8829)](https://github.com/zzh8829/yolov3-tf2)
 - [RANSAC algorithm, from Scikit-Learn library](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html)
