import cv2

'''
Herramientas destinadas a solucionar las oclusiones entre objetos y estimar sus posiciones con mayor precisión.
'''
def solve_occlusion(img, listObjects):
    '''
    Mejora la preción de la distancia de los objetos, descartando los puntos ocluidos por otros más cercanos. Pinta los
    puntos que se han tenido en cuenta para determinar su distancia en la imagen de entrada.
    Recibe una imagen rgb.
    Recibe una lista de objetos.
    Devuelve un string, siendo el mensaje generado para el servidor.
    '''
    # Se ordena la lista por medias de profundidad
    listObjects.sort(key=sort_by_mean_depth, reverse=True)

    # El elemento más cercano es añadido tanto a la lista de oclusores como al mensaje directamente
    occluders = [listObjects[0]]
    for counter in range(len(listObjects[0][6])):
        img = cv2.circle(img, (listObjects[0][6][counter][1], listObjects[0][6][counter][2]), 2, (0, 0, 255))
    msg = f'{listObjects[0][0]} {listObjects[0][1]} {listObjects[0][2]} {listObjects[0][3]} {listObjects[0][4]} {listObjects[0][5]} {listObjects[0][9]},'

    # Empezando a comprobar si los objetos oclusores están tapando los puntos de los patrones de los objetos más lejanos
    for x in range(1, len(listObjects)):
        meanDividerCounter = 0
        depht_mean = 0
        patternSize = len(listObjects[x][6])
        # Se obtiene la media de los puntos no ocluidos por otros objetos
        for counter in range(patternSize):
            # Si el punto no está en el máximo rango de visión y no es ocluido
            if listObjects[x][5] != 255 and not is_occluded(listObjects[x][6][counter], occluders):
                depht_mean += listObjects[x][6][counter][0]
                img = cv2.circle(img, (listObjects[x][6][counter][1], listObjects[x][6][counter][2]), 2, (0, 0, 255))
                meanDividerCounter += 1
        if meanDividerCounter > 0: # Si contiene algun punto sin ocluir
            # Se guarda la nueva media para ese objeto, se añade al mensaje y se agrega a la lista de oclusores
            listObjects[x][5] = depht_mean / meanDividerCounter
            msg += f'{listObjects[x][0]} {listObjects[x][1]} {listObjects[x][2]} {listObjects[x][3]} {listObjects[x][4]} {listObjects[x][5]} {listObjects[x][9]},'
        occluders.append(listObjects[x]) # Se agrega como oclusor siempre, pues puede ocluir a otros igualmente
    return msg

def solve_occlusion(img, listObjects):
    '''
    Mejora la preción de la distancia de los objetos, descartando los puntos ocluidos por otros más cercanos. Pinta los
    puntos que se han tenido en cuenta para determinar su distancia en la imagen de entrada.
    Recibe una imagen rgb.
    Recibe una lista de objetos.
    Devuelve un string, siendo el mensaje generado para el servidor.
    '''
    # Se ordena la lista por medias de profundidad
    listObjects.sort(key=sort_by_mean_depth, reverse=True)

    # El elemento más cercano es añadido tanto a la lista de oclusores como al mensaje directamente
    occluders = [listObjects[0]]
    for counter in range(len(listObjects[0][6])):
        img = cv2.circle(img, (listObjects[0][6][counter][1], listObjects[0][6][counter][2]), 2, (0, 0, 255))
    msg = f'{listObjects[0][0]} {listObjects[0][1]} {listObjects[0][2]} {listObjects[0][3]} {listObjects[0][4]} {listObjects[0][5]} {listObjects[0][9]},'

    # Empezando a comprobar si los objetos oclusores están tapando los puntos de los patrones de los objetos más lejanos
    for x in range(1, len(listObjects)):
        meanDividerCounter = 0
        depht_mean = 0
        patternSize = len(listObjects[x][6])
        # Se obtiene la media de los puntos no ocluidos por otros objetos
        for counter in range(patternSize):
            # Si el punto no está en el máximo rango de visión y no es ocluido
            if listObjects[x][5] != 255 and not is_occluded(listObjects[x][6][counter], occluders):
                depht_mean += listObjects[x][6][counter][0]
                img = cv2.circle(img, (listObjects[x][6][counter][1], listObjects[x][6][counter][2]), 2, (0, 0, 255))
                meanDividerCounter += 1
        if meanDividerCounter > 0: # Si contiene algun punto sin ocluir
            # Se guarda la nueva media para ese objeto, se añade al mensaje y se agrega a la lista de oclusores
            listObjects[x][5] = depht_mean / meanDividerCounter
            msg += f'{listObjects[x][0]} {listObjects[x][1]} {listObjects[x][2]} {listObjects[x][3]} {listObjects[x][4]} {listObjects[x][5]} {listObjects[x][9]},'
        occluders.append(listObjects[x]) # Se agrega como oclusor siempre, pues puede ocluir a otros igualmente
    return msg

def sort_by_mean_depth(val):
    # En la posición 5 se encuentran los puntos del patrón, con sus profundidades
    return val[5]

def is_occluded(point, occluders):
    '''
    Detecta si un punto se encuentra dentro de los límites establecidos por los objetos pertenecientes a una lista.
    Recibe el punto = [meanDepth, px, py] = point
    Recibe una lista de oclusores, donde el oclusor = [clase, px, py, wx, wy, meanDepth, patternDepths, x1y1, x2y2] = occluder
    Devuelve True si es ocluido, False si esta libre de oclusión.
    '''
    for occluder in occluders:
        if occluder[7][0] <= point[1] <= occluder[8][0] and occluder[7][1] <= point[2] <= occluder[8][1]:
            return True
    return False