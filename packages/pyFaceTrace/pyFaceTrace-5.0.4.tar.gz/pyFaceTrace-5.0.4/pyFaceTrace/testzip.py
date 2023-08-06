#!/usr/bin/env python
# coding: utf-8
import sys,dlib
import numpy as np
#pip install scikit-image
from skimage import io
import cv2
import os
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from os.path import dirname
import requests
import bz2#bz2file pypi
import zipfile

destination='train.zip'
folder='train'
with zipfile.ZipFile(destination, mode='r') as myzip:
    for file in myzip.namelist():
        print("extract "+file)
        myzip.extract(file,folder)