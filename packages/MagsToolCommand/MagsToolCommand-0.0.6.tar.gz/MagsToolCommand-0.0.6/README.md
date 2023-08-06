# MagsMLTool

[![Build Status](https://img.icons8.com/color/2x/python.png?branch=master)]()

MagsMLTool is a Python Application that uses various libraries to process a PDF file.

The script converts the PDF to images, extracts frames from each image, and then applies object detection models to each frame to detect if the image is incorrectly oriented or contains explicit content. 

Additionally, the script detects and crops any faces present in the images, and checks if they are clipped. 

Finally, the results are written to an Excel file and HTML file.


## Features

- Detecting Explicit Images in Pdf files
- Detecting Wrong Direction Image in Pdf files
- Detecting Clipped Face Image in Pdf files



## Technical

MagsMLTool uses a number of open source projects to work properly:

The script imports the following libraries:

- os.path: provides a way of interacting with the file system
- ssl: provides access to SSL certificates
- sys: provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
- time: provides various time-related functions
- datetime: provides classes for working with dates and times
- random: provides functions for generating random numbers
- numpy: provides support for arrays and mathematical operations on arrays
- tensorflow: an open source platform for machine learning
- xlsxwriter: a Python module for creating Excel XLSX files
- PIL: a Python Imaging Library that adds image processing capabilities to Python interpreter
- pdf2image: a Python module that converts PDF pages to JPEG format
- six: a Python module that helps in writing code that is compatible with both Python 2 and Python 3
- retinaface: a Python module for face detection
- cv2: a Python module for computer vision
- torch: a Python module for machine learning
...
## Installation

MagsMLTool requires [Python](https://www.python.org/) v3.7 to run.

Create virtual environment python and active it.

```sh
cd magstoolnewversion
python3 -m venv venv 
source venv/bin/active
```

Install Libraries

```sh
cd magstoolnewversion
python3 -m install ultralytics
python3 -m pip install -r requirements.txt
python3 -m pip install retina-face
cd yolov5
python3 -m install -r requirements.txt
```

## Run

```sh
cd magstoolnewversion
python3 BatchCheck.py [Put your PDF folder here]
```
## Docker
- https://hub.docker.com/r/hien240891/magstool

