# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import cv2
from Frames import Frame
import os

TILE_SIZE = 256
NUM_TILES = 10
## Partimos de la imagen y las coordenadas en las que hay una celula mitotica
path_image = 'C:\\Users\\maria\\Desktop\\mitosis\\images\\A17_00Db.tiff'
path_annotations = 'C:\\Users\\maria\\Desktop\\mitosis\\annotations'
os.makedirs(path_annotations,exist_ok=True)
os.makedirs(os.path.join(path_annotations,'annotations'),exist_ok=True)
os.makedirs(os.path.join(path_annotations,'images'),exist_ok=True)
cells = [[400,400,1.0]]

frame = Frame(path=path_image,cells=cells,tile_size=TILE_SIZE,num_tiles=NUM_TILES,path_annotations=path_annotations)
frame.get_records()
frame.get_all_tiles()
frame.create_annotations()