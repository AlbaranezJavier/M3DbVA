import time, cv2, os
from absl import app, flags, logging
from absl.flags import FLAGS
import tensorflow as tf
from yolov3_tf2.models import (YoloV3, YoloV3Tiny)
from yolov3_tf2.dataset import transform_images
import myTools.my_orientation_tool as orientationT
import myTools.my_yolo_tool as yoloT
import myTools.my_occlusion_tool as occlusionT
from myTools.my_client import bind2server
import time as t

'''
Detect video wo r, does not apply the rotations to the entities.
wo = without
r = rotación
'''

# Parameters
flags.DEFINE_string('classes', './data/coco.names', 'path to classes file')
flags.DEFINE_string('weights', './checkpoints/yolov3-320.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_integer('fps_record', 30, 'fps it was recorded')
flags.DEFINE_string('image', './data/exp1/', 'path to input image')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')
flags.DEFINE_integer('x_resolution', 1280, 'image resolution x')
flags.DEFINE_integer('y_resolution', 720, 'image resolution y')

def main(_argv):
    # Preparing the gpu for use
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    # Choice of model, NN, used by Yolo. Load of weights and classes used.
    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights).expect_partial()
    logging.info('weights loaded')

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    logging.info('classes loaded')

    # Link is established with the server
    mySocket = bind2server()

    # Image processing
    try:
        ind = 0
        t_timelose = 0
        while os.path.exists(f'{FLAGS.image}/RGB/{ind}.jpg'):
            time_step = t.time()
            # Preparation of the images to be processed
            img_raw = tf.image.decode_image(open(f'{FLAGS.image}/RGB/{ind}.jpg', 'rb').read(), channels=3)
            img = tf.expand_dims(img_raw, 0)
            img = transform_images(img, FLAGS.size)
            imgDepths = cv2.imread(f'{FLAGS.image}/depths/{ind}.jpg')

            t1 = time.time()
            # Yolo results for the processed image
            boxes, scores, classes, nums = yolo(img)
            img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)

            # Information processing
            listObjects = yoloT.get_objects(img, imgDepths, boxes, scores, classes, nums, class_names,
                                            FLAGS.x_resolution, FLAGS.y_resolution)
            if len(listObjects) > 0:
                msg = occlusionT.solve_occlusion(img, listObjects)
            else:
                msg = 'empty'
            t2 = time.time()
            logging.info('time: {}'.format(t2 - t1))

            # Sending the message
            mySocket.sendall(msg.encode())

            # Painting of the image processed by yolo
            cv2.imshow('output', img)
            if cv2.waitKey(1) == ord('q'):
                break

            # Wait for the message from the server, to process the following image
            mySocket.recv(1024)

            time_step = t.time() - time_step
            f_step = FLAGS.fps_record * time_step
            i_step = int(f_step)
            t_timelose += f_step - i_step
            i_timelose = int(t_timelose)
            t_timelose -= i_timelose
            ind += i_step + i_timelose
        mySocket.close()
    finally:
        mySocket.close()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

