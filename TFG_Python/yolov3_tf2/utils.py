from absl import logging
import numpy as np
import tensorflow as tf
import cv2
import statistics
from sklearn import linear_model
from math import atan, degrees

YOLOV3_LAYER_LIST = [
    'yolo_darknet',
    'yolo_conv_0',
    'yolo_output_0',
    'yolo_conv_1',
    'yolo_output_1',
    'yolo_conv_2',
    'yolo_output_2',
]

YOLOV3_TINY_LAYER_LIST = [
    'yolo_darknet',
    'yolo_conv_0',
    'yolo_output_0',
    'yolo_conv_1',
    'yolo_output_1',
]


def load_darknet_weights(model, weights_file, tiny=False):
    wf = open(weights_file, 'rb')
    major, minor, revision, seen, _ = np.fromfile(wf, dtype=np.int32, count=5)

    if tiny:
        layers = YOLOV3_TINY_LAYER_LIST
    else:
        layers = YOLOV3_LAYER_LIST

    for layer_name in layers:
        sub_model = model.get_layer(layer_name)
        for i, layer in enumerate(sub_model.layers):
            if not layer.name.startswith('conv2d'):
                continue
            batch_norm = None
            if i + 1 < len(sub_model.layers) and \
                    sub_model.layers[i + 1].name.startswith('batch_norm'):
                batch_norm = sub_model.layers[i + 1]

            logging.info("{}/{} {}".format(
                sub_model.name, layer.name, 'bn' if batch_norm else 'bias'))

            filters = layer.filters
            size = layer.kernel_size[0]
            in_dim = layer.input_shape[-1]

            if batch_norm is None:
                conv_bias = np.fromfile(wf, dtype=np.float32, count=filters)
            else:
                # darknet [beta, gamma, mean, variance]
                bn_weights = np.fromfile(
                    wf, dtype=np.float32, count=4 * filters)
                # tf [gamma, beta, mean, variance]
                bn_weights = bn_weights.reshape((4, filters))[[1, 0, 2, 3]]

            # darknet shape (out_dim, in_dim, height, width)
            conv_shape = (filters, in_dim, size, size)
            conv_weights = np.fromfile(
                wf, dtype=np.float32, count=np.product(conv_shape))
            # tf shape (height, width, in_dim, out_dim)
            conv_weights = conv_weights.reshape(
                conv_shape).transpose([2, 3, 1, 0])

            if batch_norm is None:
                layer.set_weights([conv_weights, conv_bias])
            else:
                layer.set_weights([conv_weights])
                batch_norm.set_weights(bn_weights)

    assert len(wf.read()) == 0, 'failed to read all data'
    wf.close()


def broadcast_iou(box_1, box_2):
    # box_1: (..., (x1, y1, x2, y2))
    # box_2: (N, (x1, y1, x2, y2))

    # broadcast boxes
    box_1 = tf.expand_dims(box_1, -2)
    box_2 = tf.expand_dims(box_2, 0)
    # new_shape: (..., N, (x1, y1, x2, y2))
    new_shape = tf.broadcast_dynamic_shape(tf.shape(box_1), tf.shape(box_2))
    box_1 = tf.broadcast_to(box_1, new_shape)
    box_2 = tf.broadcast_to(box_2, new_shape)

    int_w = tf.maximum(tf.minimum(box_1[..., 2], box_2[..., 2]) -
                       tf.maximum(box_1[..., 0], box_2[..., 0]), 0)
    int_h = tf.maximum(tf.minimum(box_1[..., 3], box_2[..., 3]) -
                       tf.maximum(box_1[..., 1], box_2[..., 1]), 0)
    int_area = int_w * int_h
    box_1_area = (box_1[..., 2] - box_1[..., 0]) * \
        (box_1[..., 3] - box_1[..., 1])
    box_2_area = (box_2[..., 2] - box_2[..., 0]) * \
        (box_2[..., 3] - box_2[..., 1])
    return int_area / (box_1_area + box_2_area - int_area)


def draw_outputs(img, outputs, class_names, isprint=False):
    boxes, objectness, classes, nums = outputs
    boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    for i in range(nums):
        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)
        img = cv2.putText(img, '{} {:.4f}'.format(
            class_names[int(classes[i])], objectness[i]),
            x1y1, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        if isprint:
            print(f'center point x:{int((x1y1[0] + x2y2[0]) / 2)}, y:{int((x1y1[1] + x2y2[1]) / 2)}, class:{class_names[int(classes[i])]}')
    return img

def outputs_2_send(img, path, outputs, class_names, focal_depth, isprint=False):
    boxes, objectness, classes, nums = outputs
    boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    msg=""
    depths = cv2.imread(path)
    for i in range(nums):
        # class
        cn = class_names[int(classes[i])]
        des = 0.20 if cn == 'car' else 0.05

        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        # widths
        wx = x2y2[0] - x1y1[0]
        wy = x2y2[1] - x1y1[1]

        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)
        ox = (x1y1[0] + x2y2[0]) // 2
        oy = (x1y1[1] + x2y2[1]) // 2
        img = cv2.circle(img, (ox, oy), 2, (255, 0, 0))
        depth = [int(depths[oy, ox][0])]
        desx = wx * des
        desy = wy * des
        oxl = int(ox - desx) if ox - desx >= 0 else 0
        oyu = int(oy + desy) if oy + desy < 720 else 719
        oxr = int(ox + desx) if ox + desx < 1280 else 1279
        oyd = int(oy - desy) if oy - desy >= 0 else 0
        dotPatternList = [(oxl, oyu), (oxr, oyu), (oxl, oyd), (oxr, oyd)]
        for (x, y) in dotPatternList:
            img = cv2.circle(img, (x, y), 2, (0, 0, 255))
            depth.append(int(depths[y, x][0]))
        # depth
        depth = statistics.mean(depth)
        ox -= wh[0] // 2
        oy -= wh[1] // 2
        oz = focal_depth

        msg += f'{cn} {ox} {oy} {oz} {depth} {wx} {wy},' if depth != float('inf') else f'empty'

    if isprint:
        print("Msg: " + msg)
    if msg=='':
        msg += "empty"
    else:
        msg = msg[:len(msg)-1]
    return msg

def getOrientation(X, y):
    for elem in y:
        count = 0
        for eachelem in y:
            if elem == eachelem:
                count+=1
        if count >2:
            return 0
    ransac = linear_model.RANSACRegressor()
    ransac.fit(X, y)

    line_X = np.array([X.min(), X.max()])[:, np.newaxis]
    line_y_ransac = ransac.predict(line_X)
    a = X.item(4) - X.item(0)
    b = line_y_ransac[1] - line_y_ransac[0]
    if b == 0:
        return 0
    else:
        return degrees(atan(a / b))

def getCorrectDepth(depth):
    return 255-depth;

def improveOcclusion(img, objs, lag, size, indx1y1, indx2y2):
    '''Si todos los puntos de un objeto estan ocluidos por otros no lo pinta'''
    objs[0][4] = objs[0][lag][0]
    for x in range(0, size):
        img = cv2.circle(img, (objs[0][x+lag][1], objs[0][x+lag][2]), 2, (0, 0, 255))
    list = [objs[0]] # objetos ya colocados
    rot = getOrientation(
        np.array([[objs[0][5][1]], [objs[0][6][1]], [objs[0][7][1]], [objs[0][8][1]], [objs[0][9][1]]]),
        np.array([getCorrectDepth(objs[0][5][0]), getCorrectDepth(objs[0][6][0]), getCorrectDepth(objs[0][7][0]), getCorrectDepth(objs[0][8][0]), getCorrectDepth(objs[0][9][0])]))
    msg = f'{objs[0][0]} {objs[0][1]} {objs[0][2]} {objs[0][3]} {objs[0][4]} {objs[0][10]} {objs[0][11]} {rot*-1},'
    for x in range(1, len(objs)): # para los objetos que contienen la escena
        is_correct = [False, 0]
        while is_correct[1] < size and not is_correct[0]:
            if not isPointInOtherObj(objs[x][is_correct[1]+lag], list, indx1y1, indx2y2):
                is_correct[0] = True
                depht_mean = 0
                divisor = size - is_correct[1]
                while is_correct[1] < size:
                    depht_mean += objs[x][is_correct[1]+lag][0]
                    img = cv2.circle(img, (objs[x][is_correct[1]+lag][1], objs[x][is_correct[1]+lag][2]), 2, (0, 0, 255))
                    is_correct[1] += 1
                objs[x][4] = depht_mean/divisor
                rot = getOrientation(np.array([[objs[x][5][1]], [objs[x][6][1]], [objs[x][7][1]], [objs[x][8][1]], [objs[x][9][1]]]),
                                     np.array([objs[x][5][0], objs[x][6][0], objs[x][7][0], objs[x][8][0], objs[x][9][0]]))
                msg += f'{objs[x][0]} {objs[x][1]} {objs[x][2]} {objs[x][3]} {objs[x][4]} {objs[x][10]} {objs[x][11]} {rot},'
            is_correct[1] += 1
        list.append(objs[x])
    return msg

def isPointInOtherObj(p, objs, ind1, ind2):
    for obj in objs:
        x1y1, x2y2 = obj[ind1], obj[ind2]
        if x1y1[0] <= p[1] <= x2y2[0] and x1y1[1] <= p[2] <= x2y2[1]:
            return True
    return False

def sortDepth(val):
    return val[4]

def depht_outputs(img, path, outputs, class_names, focal_depth):
    boxes, objectness, classes, nums = outputs
    boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    depths = cv2.imread(path)
    listObj = []
    for i in range(nums):
        # class
        cn = class_names[int(classes[i])]
        des = 0.20 if cn == 'car' else 0.05

        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        # widths
        wx = x2y2[0] - x1y1[0]
        wy = x2y2[1] - x1y1[1]

        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)
        ox = (x1y1[0] + x2y2[0]) // 2
        oy = (x1y1[1] + x2y2[1]) // 2
        # img = cv2.circle(img, (ox, oy), 2, (255, 0, 0))
        depth = [[int(depths[oy, ox][0]), ox, oy]]
        desx = wx * des
        desy = wy * des
        oxl = int(ox - desx) if ox - desx >= 0 else 0
        oyu = int(oy + desy) if oy + desy < 720 else 719
        oxr = int(ox + desx) if ox + desx < 1280 else 1279
        oyd = int(oy - desy) if oy - desy >= 0 else 0
        dotPatternList = [(oxl, oyu), (oxr, oyu), (oxl, oyd), (oxr, oyd)]
        for (x, y) in dotPatternList:
            # img = cv2.circle(img, (x, y), 2, (0, 0, 255))
            depth.append([int(depths[y, x][0]), x, y])
        # depth
        depthMean = (depth[0][0] + depth[1][0] + depth[2][0] + depth[3][0] + depth[4][0])/5
        ox -= wh[0] // 2
        oy -= wh[1] // 2
        oz = focal_depth
        depth.sort(reverse=True)
        listObj.append([cn, ox, oy, oz, depthMean, depth[0], depth[1], depth[2], depth[3], depth[4], wx, wy, x1y1, x2y2])
    if len(listObj) > 0:
        listObj.sort(key=sortDepth, reverse=True)
        msg = improveOcclusion(img, listObj, 5, 5, 12, 13)
    else:
        msg = 'empty'
    return msg

def draw_labels(x, y, class_names):
    img = x.numpy()
    boxes, classes = tf.split(y, (4, 1), axis=-1)
    classes = classes[..., 0]
    wh = np.flip(img.shape[0:2])
    for i in range(len(boxes)):
        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
        img = cv2.rectangle(img, x1y1, x2y2, (255, 0, 0), 2)
        img = cv2.putText(img, class_names[classes[i]],
                          x1y1, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                          1, (0, 0, 255), 2)
    return img


def freeze_all(model, frozen=True):
    model.trainable = not frozen
    if isinstance(model, tf.keras.Model):
        for l in model.layers:
            freeze_all(l, frozen)
