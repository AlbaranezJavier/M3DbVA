import cv2, os
from absl import logging
import time as t

def disparity_map(img, fps):
    '''
    Cálcula el mapa de disparidad de dos imágenes
    '''
    ind = 0
    # t_timelose = 0

    while os.path.exists(f'{image}/Left/{ind}.jpg'):
        t1 = t.time()
        imgL = cv2.imread(f'{image}/Left/{ind}.jpg', 0)
        imgR = cv2.imread(f'{image}/Right/{ind}.jpg', 0)

        stereo = cv2.StereoBM_create()
        # stereo = cv2.StereoSGBM_create()
        disparity = stereo.compute(imgL, imgR)
        disparity = disparity / disparity.max()
        cv2.imshow('output', disparity)
        t2 = t.time()
        logging.info('time: {}'.format(t2 - t1))

        # cv2.imwrite(f'{FLAGS.image}/Depths/{ind}.jpg', disparity)
        if cv2.waitKey(1) == ord('q'):
            break

        ind += 1
        # ind += FLAGS.frames
        # time_step = t.time() - time_step
        # f_step = FLAGS.fps_record * time_step
        # i_step = int(f_step)
        # t_timelose += f_step - i_step
        # i_timelose = int(t_timelose)
        # t_timelose -= i_timelose
        # ind += i_step + i_timelose

if __name__ == '__main__':
    image = '../data/1_RGB/'
    fps = 1
    disparity_map(image, fps)
