# Image Stitching Project

This project aims to develop an image stitching algorithm that can combine multiple images into a single panoramic image.
The code right now work for the current infrastructure containing of 6 images, this can be easily extended for multiple images.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

Image stitching is the process of combining multiple images with overlapping regions to create a single panoramic image. This project provides an algorithm that can automatically detect and stitch together images to create a seamless panorama.

## Directory Content
- `lidar_preprocessed`: This directory contains another directory with the same name containing all the pcd files.
- `new_rectified_data` : The folder contains other 4 folders.
    - `masks`: The folder containt the masks for the 6 camera images.
    -  `rectified`: The folder contains the rectified images captured from the 6 cameras.
    - `rectified_ar`: The folder contains the rectified images having aruco captured from the 6 cameras.
    - `rectified_csv`: The folder contains the csv file of the camera frame cordinate in the respective images.



## Installation
To use this project, you need to have the required dependencies installed, follow the steps below to set it up.

- Create a virtual environment using the command `python3 -m venv env`.
- Activate the virtual environment using the command `source env/bin/activate`.
- Install the following required python libraries using the commad `pip install -r reqirements.txt`.

## Usage
- Activate the virtual environment using the command `source env/bin/activate`.
- Open the `ransac.ipynb` and run through the cells to generate the lidar frame cordinates. The cordinates will get save to the `intersection.txt`.
- Open the `stitching.ipynb` and run through the cells to genenrate the sticthed image.


## Contact

If you encounter any issues or have any questions, please feel free to contact the following individuals:
- Vishwesh Vhavle (vishwesh20156@iiitd.ac.in)
- Jatin Sharma (jatin20563@iiitd.ac.in)
