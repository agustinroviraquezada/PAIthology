import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import ast
import glob
from src.Frames_v2 import Frame

TILE_SIZE = 224
NUM_TILES = 1

#path_labels = "X:\\projects\\PAIthology\\src\\Labels.xlsx"

path_labels = "C:\\Users\\pasto\\projects\\PAIthology\\src\\Labels_2.xlsx"

#path_images = "X:\\projects\\PAIthology\\src\\raw_data"
#path_annotations = "X:\\projects\\PAIthology\\src\\processed_data\\dataset"

path_images = "C:\\Users\\pasto\\projects\\PAIthology\\raw_data"
path_annotations = "C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset"

os.makedirs(path_annotations,exist_ok=True)
os.makedirs(os.path.join(path_annotations,'annotations'),exist_ok=True)
os.makedirs(os.path.join(path_annotations,'images'),exist_ok=True)

labels = pd.read_excel(path_labels,dtype={"MPoint":object})
labels_mitosis = labels[labels['Mitosis']==True].reset_index()
labels_mitosis = labels[(labels['Mitosis']==True)].reset_index()
labels_mitosis = labels_mitosis[(labels_mitosis['SubImage']==1)].reset_index()

complete_annotations = pd.DataFrame()

for i, row in labels_mitosis.iterrows():
    filename = f'{row["Combinacion"]}.tiff'
    a = os.path.join(path_images,'*','x40', filename)
    path_image = glob.glob(os.path.join(path_images,'*','x40', filename))
    if os.path.exists(path_image[0]):
        print(i)
        print(filename)
        cells = row["MPoint"]
        cells = ast.literal_eval(cells)
        #for i in range(len(cells)):
        frame = Frame(path=path_image[0],cells=cells,tile_size=TILE_SIZE,num_tiles=NUM_TILES,path_annotations=path_annotations)
        frame.get_records() #peta en el primer frame con subimages
        frame.create_mask()
        frame.get_all_tiles()
        frame.create_annotations()

        df = frame.csv_annotations()

        complete_annotations = complete_annotations.append(df, ignore_index=True)
        #complete_annotations.to_csv(os.path.join(path_annotations, "annotations.csv"))


complete_annotations.to_csv(os.path.join(path_annotations, "annotations.csv"), header=False)


import shutil

"""path_discards_images = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\discards\\images'
path_discards_annotations = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\discards\\annotations'
path_tiles = 'X:\\projects\\PAIthology\\src\\/processed_data\\dataset\\images'
path_tiles_annotations = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\annotations'
os.makedirs('X:\\projects\\PAIthology\\src\\processed_data\\dataset\\discards\\', exist_ok=True)"""

path_discards_images = 'C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset\\discards\\images'
path_discards_annotations = 'C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset\\discards\\annotations'
path_tiles = 'C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset\\images'
path_tiles_annotations = 'C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset\\annotations'
os.makedirs('C:\\Users\\pasto\\projects\\PAIthology\\processed_data\\dataset\\discards\\', exist_ok=True)


os.makedirs(path_discards_images, exist_ok=True)
os.makedirs(path_discards_annotations, exist_ok=True)
imgs = os.listdir(path_tiles)

for img in imgs:
    image = cv2.imread(os.path.join(path_tiles, img))
    if image.shape != (TILE_SIZE, TILE_SIZE, 3):
        print(img)
        shutil.move(os.path.join(path_tiles, img), os.path.join(path_discards_images, img))
        shutil.move(os.path.join(path_tiles_annotations, img.replace('jpg', 'xml')),
                    os.path.join(path_discards_annotations, img.replace('jpg', 'xml')))


#output_dir = 'X:\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord'
output_dir = 'C:\\Users\\pasto\\projects\\PAIthology\\src\\processed_data\\dataset\\tfrecord'
os.makedirs(output_dir,exist_ok=True)

#sys.path.append('/content/drive/MyDrive/pAItologos/src/01_GIT/automl/efficientdet/')
#%cd /content/drive/MyDrive/pAItologos/processed_data/dataset/
#!python /content/drive/MyDrive/pAItologos/src/01_GIT/automl/efficientdet/dataset/create_pascal_tfrecord_xml.py --image_dir=/content/drive/MyDrive/pAItologos/processed_data/dataset/images --annotations_dir=/content/drive/MyDrive/pAItologos/processed_data/dataset/annotations --output_path=/content/drive/MyDrive/pAItologos/processed_data/dataset/tfrecord

output_model = '/content/drive/MyDrive/pAItologos/processed_data/dataset/output'
os.makedirs(output_model, exist_ok=True)

