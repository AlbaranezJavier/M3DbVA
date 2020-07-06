import numpy as np
import cv2

'''
Tool designed to process YOLO information
'''
def get_objects(img, imgDepths, boxes, scores, classes, nums, class_names, maxx, maxy):
    '''
    It returns the relevant information of the objects detected at the scene in a list.
    Receives rgb image (img) and depth map image (imgDepths)
    It receives the rectangles that form and delimit each object (boxes)
    You receive the certainty that that object is of the predicted class (scores)
    Receive the predicted classes (int classes)
    Receives the number of detected objects (nums)
    It receives the name of the possible classes (class_names)
    Receives the resolution in x(maxx) and y (maxy)
    Returns a list of objects, where each object = [class, px, py, wx, hy, average distance, points of the pattern,
        upper left limit of the rectangle, lower right limit of the rectangle, rotation]
    '''
    # Data obtained by Yolo
    boxes, objectness, classes, nums = boxes[0], scores[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    listObjects = []
    for i in range(nums):
        # Delimitation of the object in a rectangle
        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)

        # Center of the object and its width
        centerx = (x1y1[0] + x2y2[0]) // 2
        centery = (x1y1[1] + x2y2[1]) // 2
        wx = x2y2[0] - x1y1[0]
        hy = x2y2[1] - x1y1[1]

        # Depth patterns
        classname = class_names[int(classes[i])].replace(" ", "_")
        patternDepths, meanDepth = get_pattern_depth(imgDepths, centerx, centery, wx, hy, maxx, maxy, classname)

        # Adds the detected object to the object list
        listObjects.append([classname, centerx, centery, wx, hy, meanDepth, patternDepths, x1y1, x2y2, 0])
    return listObjects

'''
Tools used to treat the depth of the relevant points in the detected objects.
'''
def get_pattern_depth(depths, centerx, centery, wx, hy, maxx, maxy, classname):
    '''
    Returns the average depth of the patterns and a list of the depths of each pattern.
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
    Execute a pattern depending on the class you stay in.
    '''
    if classname == 'person':
        return person_pattern(centerx, centery, maxx, maxy, wx, hy)
    elif classname == 'car':
        return car_pattern(centerx, centery, maxx, maxy, wx, hy)
    else:
        return default_pattern(centerx, centery, maxx, maxy, wx, hy)

'''
Point patterns that will be used to locate the object of the detected class.
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