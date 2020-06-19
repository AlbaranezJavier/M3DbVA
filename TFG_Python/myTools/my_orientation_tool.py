import numpy as np
import cv2
from sklearn import linear_model
from math import degrees, atan

'''
Tools to estimate the orientation of the detected object
'''
def add_orientations(img, imgDepths, listObjects):
    '''
    It sets an estimated orientation for the cars found on the list.
    Receives the list of objects (listObjects)
    Get the image of the depth map (imgDepths)
    '''
    for object in listObjects:
        if object[0] == 'car':
            patternsX, patternsY = car_orientation(object[7][0], object[2], object[3], object[4], 20, imgDepths, img)
            if is_correct_for_ransac(patternsY):
                # The RANSAC algorithm is trained
                ransac = linear_model.RANSACRegressor()
                ransac.fit(patternsX, patternsY)
                # The predominant line in the point cloud is obtained
                line_X = np.array([patternsX.min(), patternsX.max()])[:, np.newaxis]
                line_y_ransac = ransac.predict(line_X)
                # The angle formed by the camera and the detected object is calculated
                a = (line_y_ransac[1] - line_y_ransac[0]) * -1
                b = patternsX.max() - patternsX.min()
                object[9] = int(degrees(atan(a / b)))

'''
Point patterns that will be used to estimate the rotation of the object of the detected class.
'''
def car_orientation(x1, centery, wx, hy, numPoints, imgDepths, img):
    '''
    It receives the necessary parameters for locating points within the limits of the object, the number of points to be detected
    and the image of the depth map.
    Returning two lists of numpy, one with the values corresponding to the x-axis (positions across the object)
    and another with those corresponding to the y axis (depths of the point consulted).
    Note: when referring to "y-axis", it refers to the coordinate axis shown in a 2D graphic, but the
    depths correspond to the z axis in a 3D system.
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
    Check that this vector is correct for the RANSAC algorithm.
    Returns false if more than half the values are equal, true if not.
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