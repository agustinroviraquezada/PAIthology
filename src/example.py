# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import cv2
from src.Frames import Frame
import os
import random

random_seed = np.random.seed(12)
random.seed = 12

TILE_SIZE = 256
NUM_TILES = 100
## Partimos de la imagen y las coordenadas en las que hay una celula mitotica
path_image = "C:\\Users\\pasto\\projects\\ai_saturdays_proyecto\\A17_01Cb.tiff"
path_annotations = "C:\\Users\\pasto\\projects\\ai_saturdays_proyecto"

os.makedirs(path_annotations,exist_ok=True)
os.makedirs(os.path.join(path_annotations,'annotations'),exist_ok=True)
os.makedirs(os.path.join(path_annotations,'images'),exist_ok=True)

cells = [[400,400,1.0]]

frame = Frame(path=path_image,cells=cells,tile_size=TILE_SIZE,num_tiles=NUM_TILES,path_annotations=path_annotations)
frame.create_mask()
frame.get_records()
frame.get_all_tiles()
frame.create_annotations()