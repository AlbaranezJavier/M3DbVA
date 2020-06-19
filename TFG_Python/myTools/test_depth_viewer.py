'''
Script, viewing the depth images
'''
import cv2, os

def print_depth(fps, path, pathOutput):
    '''
    Paints the images in the specified directory, skipping as many images as there are established (fps)
    '''
    ind = 0
    cv2.imshow('output', cv2.imread(f'{path}{ind}.jpg', cv2.IMREAD_COLOR))
    cv2.waitKey(0)
    while os.path.exists(f'{path}{ind}.jpg'):
        img = cv2.imread(f'{path}{ind}.jpg', cv2.IMREAD_COLOR)
        if ind == -5:
            cv2.imwrite(pathOutput, img)
        cv2.imshow('output', img)
        if cv2.waitKey(25) == ord('q'):
            break
        ind+=fps

if __name__ == '__main__':
    path = "../data/exp6/depths/"
    pathOutput = "../data/clima1260.jpg"
    fps = 5
    print_depth(fps, path, pathOutput)