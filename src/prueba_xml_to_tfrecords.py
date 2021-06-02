import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import ast
import glob

sys.path.append('/content/drive/MyDrive/pAItologos/src/01_GIT/PAIthology/src')
from Frames import Frame

TILE_SIZE = 256
NUM_TILES = 10

path_labels = '/content/drive/MyDrive/pAItologos/src/01_GIT/PAIthology/src/Labels.xlsx'
path_annotations = '/content/drive/MyDrive/pAItologos/processed_data/dataset'
path_images = '/content/drive/MyDrive/pAItologos/raw_data/'
os.makedirs(path_annotations,exist_ok=True)
os.makedirs(os.path.join(path_annotations,'annotations'),exist_ok=True)
os.makedirs(os.path.join(path_annotations,'images'),exist_ok=True)

labels = pd.read_excel(path_labels,dtype={"MPoint":object})
labels_mitosis = labels[labels['Mitosis']==True]

for i,row in labels_mitosis.iterrows():
    filename = f'{row["Combinacion"]}.tiff'
    path_image = glob.glob(os.path.join(path_images,'*','x40', filename))
    if os.path.exists(path_image[0]):
        print(filename)
        cells = row["MPoint"]
        cells = ast.literal_eval(cells)
        frame = Frame(path=path_image[0],cells=cells,tile_size=TILE_SIZE,num_tiles=NUM_TILES,path_annotations=path_annotations)
        frame.get_records()
        frame.create_mask()
        frame.get_all_tiles()
        frame.create_annotations()

import shutil

path_discards_images = '/content/drive/MyDrive/pAItologos/processed_data/dataset/discards/images'
path_dicards_annotations = '/content/drive/MyDrive/pAItologos/processed_data/dataset/discards/annotations'
path_tiles = '/content/drive/MyDrive/pAItologos/processed_data/dataset/images'
path_tiles_annotations = '/content/drive/MyDrive/pAItologos/processed_data/dataset/annotations'
os.makedirs('/content/drive/MyDrive/pAItologos/processed_data/dataset/discards/', exist_ok=True)
os.makedirs(path_discards_images, exist_ok=True)
os.makedirs(path_dicards_annotations, exist_ok=True)
imgs = os.listdir(path_tiles)
for img in imgs:
    image = cv2.imread(os.path.join(path_tiles, img))
    if image.shape != (256, 256, 3):
        print(img)
        shutil.move(os.path.join(path_tiles, img), os.path.join(path_discards_images, img))
        shutil.move(os.path.join(path_tiles_annotations, img.replace('jpg', 'xml')),
                    os.path.join(path_dicards_annotations, img.replace('jpg', 'xml')))


#output_dir = '/content/drive/MyDrive/pAItologos/processed_data/dataset/tfrecord'
#os.makedirs(output_dir,exist_ok=True)

#sys.path.append('/content/drive/MyDrive/pAItologos/src/01_GIT/automl/efficientdet/')
#%cd /content/drive/MyDrive/pAItologos/processed_data/dataset/
#!python /content/drive/MyDrive/pAItologos/src/01_GIT/automl/efficientdet/dataset/create_pascal_tfrecord_xml.py --image_dir=/content/drive/MyDrive/pAItologos/processed_data/dataset/images --annotations_dir=/content/drive/MyDrive/pAItologos/processed_data/dataset/annotations --output_path=/content/drive/MyDrive/pAItologos/processed_data/dataset/tfrecord

output_model = '/content/drive/MyDrive/pAItologos/processed_data/dataset/output'
os.makedirs(output_model, exist_ok=True)

