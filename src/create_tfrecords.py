import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import ast
import glob
from src.Frames import *

path_discards_images = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\discards\\images'
path_discards_annotations = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\discards\\annotations'
path_tiles = 'X:\\projects\\PAIthology\\src\\/processed_data\\dataset\\images'
path_tiles_annotations = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\annotations'

output_dir = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord'
os.makedirs(output_dir,exist_ok=True)






!python X:\\projects\\PAIthology\\src\\/create_pascal_tfrecord_xml.py --image_dir=X:\\projects\\PAIthology\\src\\/processed_data\\dataset\\images --annotations_dir=X:\\projects\\PAIthology\\src\\processed_data\\dataset\\annotations --output_path=X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord

X:\projects\PAIthology\src\create_pascal_tfrecord_xml.py --image_dir=X:\projects\PAIthology\src\processed_data\dataset\images --annotations_dir=X:\projects\PAIthology\src\processed_data\dataset\annotations --output_path=X:\projects\PAIthology\src\processed_data\dataset\tfrecord

X:/projects/PAIthology/src/create_pascal_tfrecord_xml.py --image_dir=X:/projects/PAIthology/src/processed_data/dataset/images --annotations_dir=X:/projects/PAIthology/src/processed_data/dataset/annotations --output_path=X:/projects/PAIthology/src/processed_data/dataset/tfrecord











