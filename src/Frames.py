import numpy as np
import os
from PIL import Image
import cv2
import random
from xml_tools import create_base_xml, create_object_xml
from record import Record
from tile_generator import TileGenerator


class Frame:
    """Class containg all the information gathered of an specific frame and its
    mitotic and not mitotic tiles."""
    def __init__(self, path, cells, tile_size, num_tiles=10, path_annotations=None):
        self.path = path
        self.filename = os.path.basename(path)
        self.frame = cv2.imread(path)
        self.tile_size = tile_size
        self.num_tiles = num_tiles
        self.cells = cells
        self.tiles_mitosis = []
        self.tiles_not_mitosis = []
        self.records = []
        self.path_annotations = path_annotations
        self.frame_mask = []
        self.frame_mask_per_record = []
        
    def get_records(self):
        self.records = [Record(*cell) for cell in self.cells]
        print(f'Got records for {self.filename}')   
        
    def create_mask(self):
        '''Generate a mask of ones around the mitosis point'''
        mask = np.zeros(self.frame.shape[:2], np.uint8)
        for record in self.records:
            mask_per_record = np.zeros(self.frame.shape[:2], np.uint8)
            # This could use floor and ceiling to also work with odd tile sizes
            # This could use floor and ceiling to also work with odd tile sizes
            mask[max(int(record.x-(self.tile_size/2)), 0):min(int(record.x+(self.tile_size/2)), self.frame.shape[0]),
                 max(int(record.y-(self.tile_size/2)), 0):min(int(record.y+(self.tile_size/2)), self.frame.shape[1])] = 1
            
            mask_per_record[int(record.x-(self.tile_size/2)):int(record.x+(self.tile_size/2)),
                 int(record.y-(self.tile_size/2)):int(record.y+(self.tile_size/2))] = 1
            
            self.frame_mask_per_record.append(mask_per_record)
        self.frame_mask = mask
        print(f'Generated mask for {self.filename}')

    def get_all_tiles(self):
        tile_generator = TileGenerator(self, self.tile_size, self.num_tiles)
        self.tiles_mitosis = tile_generator.generate_real_positive_tiles()
        self.tiles_not_mitosis = tile_generator.generate_real_negative_tiles()
        
    def create_annotations(self):
        delta = 15
        count = 0 # enum
        for tile_mitosis in self.tiles_mitosis:
            tile_filename_base = f"{self.filename.replace('.tiff','')}_mitosis_{count}"
            tree = create_base_xml(self.path, tile_mitosis, f"{tile_filename_base}.jpg")
            
            tree.write(os.path.join(self.path_annotations,'annotations',f"{tile_filename_base}.xml"))
            cv2.imwrite(os.path.join(self.path_annotations,'images',f"{tile_filename_base}.jpg"), tile_mitosis.image)
            count += 1
        count = 0
        for tile_not_mitosis in self.tiles_not_mitosis:
            tile_filename_base = f"{self.filename.replace('.tiff','')}_not_mitosis_{count}"
            tree = create_base_xml(self.path, tile_not_mitosis, f"{tile_filename_base}.jpg")
            
            tree.write(os.path.join(self.path_annotations,'annotations',f"{tile_filename_base}.xml"))
            cv2.imwrite(os.path.join(self.path_annotations,'images',f"{tile_filename_base}.jpg"), tile_not_mitosis.image)
            count += 1


