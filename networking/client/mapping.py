
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

h_lcslab2 = np.array([[-3.16795466e-04,  2.98499279e-03, -9.35009464e-01],
       [ 2.84907527e-03,  1.88839689e-04,  2.15272393e+00],
       [-3.38293645e-05, -2.77805840e-05,  1.04152687e+00]])

m_lcslab2 = np.array([[1.95966597e-01, 9.27052776e-01, 1.06510010e+03],
        [9.80912115e-01, 3.01898760e-01, 1.75274109e+03],
        [1.19739141e-04, 1.40672025e-04, 1.00000000e+00]])

K_matrix = np.array([[200, 0, 1500],
                    [0, 200, 2500],
                    [0, 0, 1]])

WIDTH = 4000
HEIGHT = 4000

ROTATION = 85

HORIZONTAL_FLIP = np.array([[-1, 0, WIDTH],
                            [0, 1, 0],
                            [0, 0, 1]])

def mapToImage(point):

    hom_point = np.array([point[1], point[2], 1]).reshape((-1, 1))

    image_point = m_lcslab2 @ hom_point
    image_point /= image_point[2]

    rotation_matrix = cv.getRotationMatrix2D((WIDTH/2, HEIGHT/2), ROTATION, 1)
    image_point = rotation_matrix @ image_point

    image_point = np.array([image_point[0], image_point[1], [1]])
    image_point = HORIZONTAL_FLIP @ image_point
    
    image_point = np.array([point[0], image_point[0][0], image_point[1][0]], dtype=np.float32)
    return image_point
