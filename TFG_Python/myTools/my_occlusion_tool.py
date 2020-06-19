import cv2

'''
Tools for solving occlusions between objects and estimating their positions more accurately
'''
def solve_occlusion(img, listObjects):
    '''
    It improves the precision of the distance of the objects, discarding the points occluded by other closer ones. Paints the
    points that have been taken into account to determine their distance in the input image.
    It receive an rgb image.
    It receive a list of objects.
    Returns a string, being the message generated for the server.
    '''
    # The list is sorted by average depth
    listObjects.sort(key=sort_by_mean_depth, reverse=True)

    # The nearest element is added to both the list of occluders and the message directly
    occluders = [listObjects[0]]
    for counter in range(len(listObjects[0][6])):
        img = cv2.circle(img, (listObjects[0][6][counter][1], listObjects[0][6][counter][2]), 2, (0, 0, 255))
    msg = f'{listObjects[0][0]} {listObjects[0][1]} {listObjects[0][2]} {listObjects[0][3]} {listObjects[0][4]} {listObjects[0][5]} {listObjects[0][9]},'

    # Starting to check if the occlusive objects are covering the points of the patterns of the farthest objects
    for x in range(1, len(listObjects)):
        meanDividerCounter = 0
        depht_mean = 0
        patternSize = len(listObjects[x][6])
        # You get the average of the points not occluded by other objects
        for counter in range(patternSize):
            # If the point is not in the maximum range of vision and is not occluded
            if listObjects[x][5] != 255 and not is_occluded(listObjects[x][6][counter], occluders):
                depht_mean += listObjects[x][6][counter][0]
                img = cv2.circle(img, (listObjects[x][6][counter][1], listObjects[x][6][counter][2]), 2, (0, 0, 255))
                meanDividerCounter += 1
        if meanDividerCounter > 0: # If it contains any unoccluded points
            # The new media for that object is saved, added to the message and added to the list of occluders
            listObjects[x][5] = depht_mean / meanDividerCounter
            msg += f'{listObjects[x][0]} {listObjects[x][1]} {listObjects[x][2]} {listObjects[x][3]} {listObjects[x][4]} {listObjects[x][5]} {listObjects[x][9]},'
        occluders.append(listObjects[x]) # It is always added as an occluder, as it can occlude others as well
    return msg

def solve_occlusion(img, listObjects):
    '''
    It improves the precision of the distance of the objects, discarding the points occluded by other closer ones. Paints the
    points that have been taken into account to determine their distance in the input image.
    It receive an rgb image.
    It receive a list of objects.
    Returns a string, being the message generated for the server.
    '''
    # The list is sorted by average depth
    listObjects.sort(key=sort_by_mean_depth, reverse=True)

    # The nearest element is added to both the list of occluders and the message directly
    occluders = [listObjects[0]]
    for counter in range(len(listObjects[0][6])):
        img = cv2.circle(img, (listObjects[0][6][counter][1], listObjects[0][6][counter][2]), 2, (0, 0, 255))
    msg = f'{listObjects[0][0]} {listObjects[0][1]} {listObjects[0][2]} {listObjects[0][3]} {listObjects[0][4]} {listObjects[0][5]} {listObjects[0][9]},'

    # Starting to check if the occlusive objects are covering the points of the patterns of the farthest objects
    for x in range(1, len(listObjects)):
        meanDividerCounter = 0
        depht_mean = 0
        patternSize = len(listObjects[x][6])
        # You get the average of the points not occluded by other objects
        for counter in range(patternSize):
            # If the point is not in the maximum range of vision and is not occluded
            if listObjects[x][5] != 255 and not is_occluded(listObjects[x][6][counter], occluders):
                depht_mean += listObjects[x][6][counter][0]
                img = cv2.circle(img, (listObjects[x][6][counter][1], listObjects[x][6][counter][2]), 2, (0, 0, 255))
                meanDividerCounter += 1
        if meanDividerCounter > 0: # If it contains any unoccluded points
            # The new media for that object is saved, added to the message and added to the list of occluders
            listObjects[x][5] = depht_mean / meanDividerCounter
            msg += f'{listObjects[x][0]} {listObjects[x][1]} {listObjects[x][2]} {listObjects[x][3]} {listObjects[x][4]} {listObjects[x][5]} {listObjects[x][9]},'
        occluders.append(listObjects[x]) # It is always added as an occluder, as it can occlude others as well
    return msg

def sort_by_mean_depth(val):
    # In position 5 are the points of the pattern, with their depths
    return val[5]

def is_occluded(point, occluders):
    '''
    Detects if a point is within the limits set by the objects belonging to a list.
    It receives the point = [meanDepth, px, py] = point
    It receive a list of occluders, where the occluder = [class, px, py, wx, wy, meanDepth, patternDepths, x1y1, x2y2] = occluder
    Returns True if occluded, False if free of occlusion.
    '''
    for occluder in occluders:
        if occluder[7][0] <= point[1] <= occluder[8][0] and occluder[7][1] <= point[2] <= occluder[8][1]:
            return True
    return False