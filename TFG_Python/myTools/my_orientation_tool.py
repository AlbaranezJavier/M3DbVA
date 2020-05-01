import numpy as np
import cv2
from sklearn import linear_model
from math import degrees, atan

'''
Herramientas destinadas a estimar la orientación del objeto detectado
'''
def add_orientations(img, imgDepths, listObjects):
    '''
    Establece una orientación estimada para los coches encontrados en la lista.
    Recibe la lista de objetos (listObjects)
    Recibe la imagen del mapa de profundidades (imgDepths)
    '''
    for object in listObjects:
        if object[0] == 'car':
            patternsX, patternsY = car_orientation(object[7][0], object[2], object[3], object[4], 20, imgDepths, img)
            if is_correct_for_ransac(patternsY):
                # Se entrena al algoritmo RANSAC
                ransac = linear_model.RANSACRegressor()
                ransac.fit(patternsX, patternsY)
                # Se obtiene la recta predominante en la nube de puntos
                line_X = np.array([patternsX.min(), patternsX.max()])[:, np.newaxis]
                line_y_ransac = ransac.predict(line_X)
                # Se calcula el ángulo formado por la cámara y el objeto detectado
                a = (line_y_ransac[1] - line_y_ransac[0]) * -1
                b = patternsX.max() - patternsX.min()
                object[9] = int(degrees(atan(a / b)))

'''
Patrones de puntos que se usarán para estimar la rotación del objeto de la clase detectada.
'''
def car_orientation(x1, centery, wx, hy, numPoints, imgDepths, img):
    '''
    Recibe los parámetros necesarios por ubicar puntos dentro de los límites del objeto, el número de puntos a detectar
    y la imagen del mapa de profundidad.
    Devolviendo dos listas de numpy, una con los valores correspondientes al eje x (posiciones a lo ancho del objeto)
    y otra con los correspondientes al eje y (profundidades del punto consultado).
    Nota: cuando se refiere a "eje y" se hace referencia al eje de coordenadas representado en una gráfica 2D, pero las
    profundidades corresponden al eje z en un sistema 3D.
    '''
    half = numPoints//2
    _centery = centery + len(imgDepths) // 2
    patternX = []
    patternY = []
    desCentery = int(hy * 0.2 + _centery)
    step = wx / (numPoints//2+1)
    x = x1 + step
    for _ in range(half):
        patternX.append([int(x)])
        patternY.append(255 - imgDepths[_centery, int(x)][0])
        img = cv2.circle(img, (int(x), _centery), 2, (0, 255, 0))
        x += step
    x = x1 + step * 1.5
    for _ in range(half, numPoints):
        patternX.append([int(x)])
        patternY.append(255 - imgDepths[desCentery, int(x)][0])
        img = cv2.circle(img, (int(x), desCentery), 2, (0, 255, 0))
        x += step
    return np.array(patternX), np.array(patternY)

def is_correct_for_ransac(patternsY):
    '''
    Comprueba que este vector sea correcto para el algoritmo RANSAC.
    Devuelve false si más de la mitad de los valores son iguales, true en caso contrario.
    '''
    dict = {}
    max = 1
    for elem in patternsY:
        if elem not in dict:
            dict.update({elem: 1})
        else:
            dict[elem] += 1
            if dict[elem] > max:
                max = dict[elem]
    return False if max > len(patternsY)//2 else True