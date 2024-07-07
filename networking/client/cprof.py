import numpy as np
from dt_apriltags import Detector
import cv2
import PySpin
import time
from mapping import *
import cProfile
import pstats
import csv 
from utils import SERIAL, HOST, PORT, TIMEOUT

"""
Cam 1 22139585 Sanjit Sir's Office
Cam 2 22139594 AGX Saket Sir's Office
Cam 3 22139582 AGX Middle Camera 
Cam 4 22139568 AGX LCS Lab 1
Cam 5 22139572 AGX Discussion Room
Cam 6 22139569 Next to LCS Lab 2
"""

HEIGTH = 1080
WIDTH = 1440
CHANNELS = 3
FILENAME = 'output.csv'
FIELDS = ['ID', 'X', 'Y', 'Time'] 
THRESHOLD = 45

INTRINSIC = np.load('intrinsics.npz') # Load Intrinsics
matr = INTRINSIC['mtx']

fx = matr[0][0]
fy = matr[1][1]
cx = matr[0][2]
cy = matr[1][2]

k1, k2, p1, p2, k3 = INTRINSIC['dist'][0]

def steady_state(fireFly, detector):
    im = fireFly.GetNextImage()
    image_converted = im.Convert(PySpin.PixelFormat_BGR8)
    im.Release()

    rectified_img = image_converted.GetData().reshape(HEIGTH, WIDTH, CHANNELS)
    rectified_img = cv2.cvtColor(rectified_img, cv2.COLOR_BGR2GRAY) # AprilTags Detection Requires Grayscale Frame
    rectified_img = np.where((255 - rectified_img) < THRESHOLD,255,rectified_img+THRESHOLD)  # Thresholding to Improve Detectability 

    result = detector.detect(rectified_img) # Detect Tag
    detection_time = time.time() # Assuming all tags are detected at same time

    rows = []
    if len(result) < 1:
        row = np.array([], dtype=np.float32)

    else:
        for i in range(len(result)):
            row = np.array([-1, -1, -1], dtype=np.float32)
            row[0] = result[i].tag_id
            row[1] = result[i].center[0]
            row[2] = result[i].center[1]

            id, x, y = row
            x = (x-cx)/fx
            y = (y-cy)/fy
            x0, y0 = x, y

            for _ in range(3):
                r2 = x ** 2 + y ** 2
                k_inv = 1 / (1 + k1 * r2 + k2 * r2**2 + k3 * r2**3)
                delta_x = 2 * p1 * x*y + p2 * (r2 + 2 * x**2)
                delta_y = p1 * (r2 + 2 * y**2) + 2 * p2 * x*y
                x = (x0 - delta_x) * k_inv
                y = (y0 - delta_y) * k_inv

            row = np.array([id, x * fx + cx, y * fy + cy, detection_time])
            row = mapToImage(row)
            row = row.tolist()
            row.append(detection_time)
            rows.append(row)

    rows = np.array(rows, dtype='<u2')
    return rows

def create_detector():
    detector = Detector(families='tag36h11',
                        nthreads=4,
                        quad_decimate=2.0,
                        quad_sigma=0.3,
                        refine_edges=1,
                        decode_sharpening=0.6,
                        debug=0)
    return detector

def main():
    # Acquire and Turn ON Camera
    system = PySpin.System.GetInstance()
    fireFly_list = system.GetCameras()
    fireFly = fireFly_list.GetBySerial(SERIAL)
    
    fireFly.Init()
    fireFly.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
    fireFly.BeginAcquisition()   

    profiler = cProfile.Profile()
    profiler.enable()

    detector = create_detector() # Create AprilTag Detector Object

    with open(FILENAME, 'w') as csvfile:  # Create CSV file to record Tags
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(FIELDS) 

    # Begin Recording
    try:
        for i in range(1000):
            rows = steady_state(fireFly, detector) 

            for row in rows:
                with open(FILENAME, 'a') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row)

    finally:
        profiler.disable()
        profile_filename = "profile_results.prof"
        profiler.dump_stats(profile_filename)
        
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        # stats.sort_stats('cumulative')

        # Print the profiling results to the console
        stats.print_stats()

        fireFly.EndAcquisition()


if __name__ == '__main__':
    main()
    