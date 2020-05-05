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

