import pandas as pd    
import numpy as np
from dt_apriltags import Detector
import cv2
import PySpin
import time
import csv 
from utils import SERIAL


def capture_video(fireFly, intrinsic, detector):

    while(True):
        height = 1080
        width = 1440
        channels= 3
        im= fireFly.GetNextImage()
        image_converted = im.Convert(PySpin.PixelFormat_BGR8)
        rectified_img   = image_converted.GetData().reshape(height, width, channels)
        rectified_img   = cv2.undistort(rectified_img, intrinsic['mtx'], intrinsic['dist'], None)
        gray = increase_brightness(rectified_img)
        gray            = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("image.png", gray)
        

def Function_That_Does_It_All(fireFly, intrinsic, detector):

    height = 1080
    width = 1440
    channels= 3
    im= fireFly.GetNextImage()
    image_converted = im.Convert(PySpin.PixelFormat_BGR8)
    rectified_img   = image_converted.GetData().reshape(height, width, channels)
    rectified_img   = cv2.undistort(rectified_img, intrinsic['mtx'], intrinsic['dist'], None)
    gray = increase_brightness(rectified_img)
    gray            = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("image.png", gray)

    result = detector.detect(gray)
    im.Release()
    
    rows = []

    for i in range(len(result)):
        row = []
        row.append(result[i].tag_id)
        row.append(result[i].center[0])
        row.append(result[i].center[1])
        rows.append(row)

    # field names 
    fields = ['ID', 'X', 'Y'] 

    # name of csv file 
    filename = "points.csv"
        
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)

    return result

def increase_brightness(img, value=40):
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

def display_tag_id(tag, rectified_img):
    print(f"Tag ID: {tag.tag_id}.")
    cv2.putText(rectified_img, str(tag.tag_id),
                org=(tag.corners[0, 0].astype(int)+10,
                     tag.corners[0, 1].astype(int)+10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                thickness=2,
                color=(100, 100, 255))
    return tag.tag_id


def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)


def display_tag_corners(tag, rectified_img):
    corners= np.array(((tag.corners[0]),(tag.corners[1]),(tag.corners[2]),(tag.corners[3])))
    print(f"Corner Co-ordinates in pixels: {corners}")
    return corners

def display_tag_center(tag, rectified_img):
    center = np.array((int(tag.center[0]), int(tag.center[1])))
    #print(f"Center Co-ordinates in pixels: {center}")
    #rectified_img = cv2.circle(rectified_img, center, 2, (0, 0, 255), -1)
    return center

def main():
# Depends on the camera you are using. To know the Serial number, run the example 'Acquisition.py', the number would appear on your terminal.
    serial= SERIAL

    system = PySpin.System.GetInstance()
    fireFly_list = system.GetCameras()

    fireFly = fireFly_list.GetBySerial(serial)
    
    #Load the corresponding intrinsic calibration matrix file
    intrinsics = np.load('/home/jetson/testbed/aruco_capture/intrinsics.npz')

    fireFly.Init()
    fireFly.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
    fireFly.BeginAcquisition()    

    begin_time= time.time()

    detector = create_detector()

    # while time.time()-begin_time<30:
    Function_That_Does_It_All(fireFly, intrinsics, detector)   
    # capture_video(fireFly, intrinsics, detector)   

    fireFly.EndAcquisition()


if __name__ == '__main__':
    main()