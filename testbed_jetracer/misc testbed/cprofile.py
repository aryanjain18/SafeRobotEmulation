import pandas as pd
import numpy as np
from dt_apriltags import Detector
import cv2
import pickle
from scipy import ndimage
import os
import sys
from PIL import Image
import PySpin
import socket
import time
import csv
import cProfile
import pstats

"""
Cam 1 22139585 132.168.31.209 Sanjit Sir's Office
Cam 2 22139594 AGX Saket Sir's Office
Cam 3 22139582 AGX Middle Camera 
Cam 4 22139568 AGX LCS Lab 1
Cam 5 22139572 AGX Discussion Room
Cam 6 22139569 192.168.20.204 Next to LCS Lab 2
"""

fields = ['ID', 'X', 'Y']
filename = "points.csv"
height = 1080
width = 1440
channels = 3


def steady_state(fireFly, intrinsic, detector):
    print("Steady State - Stage 5: Frame Acquisition")
    im = fireFly.GetNextImage()  # Get Frame
    image_converted = im.Convert(PySpin.PixelFormat_BGR8)
    print("Steady State - Stage 5: Frame Acquisition Complete")

    print("Steady State - Stage 6: Image Preprocessing")
    rectified_img = image_converted.GetData().reshape(height, width, channels)
    rectified_img = cv2.undistort(rectified_img, intrinsic['mtx'], intrinsic['dist'],
                                  None)  # Rectify Image using Intrisics

    gray = increase_brightness(rectified_img)  # Color Correction to Improve Detectability
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)  # AprilTags Detection Requires Grayscale Frame
    print("Steady State - Stage 6: Image Preprocessed")

    print("Steady State - Stage 7: April Tag Detection")
    result = detector.detect(gray)  # Detect Tag
    detection_time = time.time()  # Assuming all tags are detected at same time
    im.Release()
    print("Steady State - Stage 7: April Tag Detected")

    print("Steady State - Stage 8: Writing to CSV")
    # Store Detected Data for writing to CSV
    rows = []
    for i in range(len(result)):
        row = []
        row.append(result[i].tag_id)
        row.append(result[i].center[0])
        row.append(result[i].center[1])
        row.append(detection_time)
        rows.append(row)

    # Writing to CSV file
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    print("Steady State - Stage 7: Writing to CSV Completed")

    return result


def increase_brightness(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def create_detector():
    detector = Detector(families='tag36h11',
                        nthreads=1,
                        quad_decimate=1.0,
                        quad_sigma=0.0,
                        refine_edges=1,
                        decode_sharpening=0.5,
                        debug=0)
    return detector


def main():
    # Acquire and Turn ON Camera
    print("Stage 1: Acquisition Begin")
    serial = '22139585'  # Refer to Comments in the beginning and Select Serial ID

    system = PySpin.System.GetInstance()
    fireFly_list = system.GetCameras()
    fireFly = fireFly_list.GetBySerial(serial)

    fireFly.Init()
    fireFly.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
    fireFly.BeginAcquisition()
    print("Stage 1: Acquisition Completed")

    # Load Intrinsics
    print("Stage 2: Load Intrinsics")
    intrinsics = np.load('intrinsics.npz')
    print("Stage 2: Loaded Intrinsics")

    # Create AprilTag Detector Object
    print("Stage 3: Create Detector")
    detector = create_detector()
    print("Stage 3: Created Detector")

    # Create CSV file to record Tags
    print("Stage 4: Create CSV File")
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
    print("Stage 4: Created CSV File")

    # Start profiling
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        # Begin Recording
        for i in range(10):
            print("Iteration: ", i + 1)
            steady_state(fireFly, intrinsics, detector)

    finally:
        # Stop profiling
        profiler.disable()

        # Save the profile results to a file
        profile_filename = "profile_results.prof"
        profiler.dump_stats(profile_filename)

        # Create a pstats object to print the profiling results
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumulative')

        # Print the profiling results to the console
        stats.print_stats()



        # fireFly.EndAcquisition()

if __name__ == '__main__':
    main()