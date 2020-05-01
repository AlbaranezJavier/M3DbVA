import numpy as np
import cv2

'''
Herramienta destinada procesar la información de YOLO
'''
def get_objects(img, imgDepths, boxes, scores, classes, nums, class_names, maxx, maxy):
    '''
    Devuelve la información relevante de los objetos detectados en la escena en una lista.
    Recibe imagen rgb (img) y la imagen del mapa de profundidades (imgDepths)
    Recibe los rectangulos que conforman y delimitan a cada objeto (boxes)
    Recibe la certeza de que ese objeto sea de la clase predicha (scores)
    Recibe las clases predichas (int classes)
    Recibe el número de objetos detectados (nums)
    Recibe el nombre de las clases posibles (class_names)
    Recibe la resolución en x(maxx) y en y (maxy)
    Devuelve una lista de objetos, donde cada objeto = [clase, px, py, wx, hy, distancia media, puntos del patrón,
        límite superior izquierda del rectángulo, límite inferior derecha del rectángulo, rotación]
    '''
    # Datos obtenidos por Yolo
    boxes, objectness, classes, nums = boxes[0], scores[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    listObjects = []
    for i in range(nums):
        # Delimitación del objeto en un rectángulo
        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)

        # Centro del objeto y su ancho
        centerx = (x1y1[0] + x2y2[0]) // 2
        centery = (x1y1[1] + x2y2[1]) // 2
        wx = x2y2[0] - x1y1[0]
        hy = x2y2[1] - x1y1[1]

        # Patrones de profundidad
        classname = class_names[int(classes[i])].replace(" ", "_")
        patternDepths, meanDepth = get_pattern_depth(imgDepths, centerx, centery, wx, hy, maxx, maxy, classname)

        # Sistema de referencia modificado al centro de la imagen (posición de la cámara)
        centerx -= wh[0] // 2
        centery -= wh[1] // 2

        # Agrega el objeto detectado a la lista de objetos
        listObjects.append([classname, centerx, centery, wx, hy, meanDepth, patternDepths, x1y1, x2y2, 0])
    return listObjects

'''
Herramientas empleadas en tratar la profundidad de los puntos relevantes en los objetos detectados.
'''
def get_pattern_depth(depths, centerx, centery, wx, hy, maxx, maxy, classname):
    '''
    Devuelve la profundidad media de los patrones y una lista con las profundidades de cada patrón.
    '''
    depth = []
    dotPatternList = calculate_by_class(centerx, centery, maxx, maxy, wx, hy, classname)
    divisor = 0
    depthMean = 0
    for x, y in dotPatternList:
        depth.append([int(depths[y, x][0]), x, y])
        depthMean += int(depths[y, x][0])
        divisor += 1
    # depth
    depthMean /= divisor
    return depth, depthMean

def calculate_by_class(centerx, centery, maxx, maxy, wx, hy, classname):
    '''
    Ejecuta un patrón dependiendo de la clase a la que permanezca.
    '''
    if classname == 'person':
        return person_pattern(centerx, centery, maxx, maxy, wx, hy)
    elif classname == 'car':
        return car_pattern(centerx, centery, maxx, maxy, wx, hy)
    else:
        return default_pattern(centerx, centery, maxx, maxy, wx, hy)

'''
Patrones de puntos que se usarán para ubicar al objeto de la clase detectada.
'''
def person_pattern(centerx, centery, maxx, maxy, wx, hy):
    desx = wx * 0.1
    desy = hy * 0.1
    centerxl = int(centerx - desx) if centerx - desx >= 0 else 0
    centeryu = int(centery + desy) if centery + desy < maxy else maxy-1
    centerxr = int(centerx + desx) if centerx + desx < maxx else maxx-1
    centeryd = int(centery - desy) if centery - desy >= 0 else 0
    return [(centerx, centery), (centerxl, centeryu), (centerxr, centeryu), (centerxl, centeryd), (centerxr, centeryd)]

def car_pattern(centerx, centery, maxx, maxy, wx, hy):
    desx1 = wx * 0.15
    desx2 = wx * 0.3
    desy = hy * 0.2
    centerxll = int(centerx - desx2) if centerx - desx2 >= 0 else 0
    centerxl = int(centerx - desx1) if centerx - desx1 >= 0 else 0
    centerxr = int(centerx + desx1) if centerx + desx1 < maxx else maxx-1
    centerxrr = int(centerx + desx2) if centerx + desx2 < maxx else maxx-1
    centeryd = int(centery + desy) if centery + desy < maxy else maxy - 1
    return [(centerxll, centery), (centerxl, centeryd), (centerx, centery), (centerxr, centeryd), (centerxrr, centery)]

def default_pattern(centerx, centery, maxx, maxy, wx, hy):
    desx = wx * 0.2
    desy = hy * 0.2
    centerxl = int(centerx - desx) if centerx - desx >= 0 else 0
    centeryu = int(centery + desy) if centery + desy < maxy else maxy - 1
    centerxr = int(centerx + desx) if centerx + desx < maxx else maxx - 1
    centeryd = int(centery - desy) if centery - desy >= 0 else 0
    return [(centerx, centery), (centerxl, centeryu), (centerxr, centeryu), (centerxl, centeryd), (centerxr, centeryd)]