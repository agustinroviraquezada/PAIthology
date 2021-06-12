import random
from matplotlib import pyplot as plt
import numpy as np
from record import Record
from tile import Tile


class TileGenerator:
    def __init__(self, frame, tile_size, num_tiles):
        self.tile_size = tile_size
        self.num_tiles = num_tiles
        self.frame = frame
        self.image_frame = np.array(frame.frame)
        self.mitotic_coordinates = frame.records
        self.centroid_limits = self.get_centroid_limits()
        self.possible_negative_centroids = self.get_possible_negative_centroids()
        self.possible_positive_centroids = self.get_possible_positive_centroids()
        
    def get_possible_negative_centroids(self):
        # ATTENTION, Label.xlsx ARE WITH THE COORDINATES TRANSPOSED. THIS HAS BEEN CHANGED TO THAT
        return [coords for coords in zip(*np.where(self.frame.frame_mask == 0)) if self.check_record_presence_in_boundaries(Record(*reversed(coords), 0), self.centroid_limits)]
    
    def get_possible_positive_centroids(self):
        # ATTENTION, Label.xlsx ARE WITH THE COORDINATES TRANSPOSED. THIS HAS BEEN CHANGED TO THAT
        return [coords for coords in zip(*np.where(self.frame.frame_mask == 1)) if self.check_record_presence_in_boundaries(Record(*reversed(coords), 1), self.centroid_limits)]
        
    def get_random_negative_tile_centroid(self):
        return random.choice(self.possible_negative_centroids)
        
    def get_random_positive_tile_centroid(self):
        return random.choice(self.possible_positive_centroids)
    
    def get_centroid_limits(self):
        limits_random_centroid_x = (
            int(self.tile_size/2), # min limit
            int(frame.frame.shape[0] - self.tile_size/2)  # max limit
        )

        limits_random_centroid_y = (
            int(self.tile_size/2), # min limit
            int(frame.frame.shape[1] - self.tile_size/2)  # max limit
        )

        return limits_random_centroid_x, limits_random_centroid_y
    
    def get_boundaries_tile(self, centroid):
        return tuple(
            (int(centroid_coord - self.tile_size/2), int(centroid_coord + self.tile_size/2)) for centroid_coord in centroid
        )
    
    def check_record_presence_in_boundaries(self, record, boundaries):
        return (boundaries[0][0] <= record.x <= boundaries[0][1]) and \
               (boundaries[1][0] <= record.y <= boundaries[1][1])
    
    def frame_record_to_tile_record(self, x_min_tile : int, y_min_tile : int, record: Record) -> Record:
        x_tile = record.x - x_min_tile
        y_tile = record.y - y_min_tile    
        return Record(x_tile, y_tile, record.confidence)
    
    def generate_real_negative_tiles(self):
        negative_tiles_centroids = [self.get_random_negative_tile_centroid() for _ in range(self.num_tiles)]
        boundaries_negative_tiles = [self.get_boundaries_tile(cent) for cent in negative_tiles_centroids]
        negative_tiles_images = [self.image_frame[boundaries[0][0]:boundaries[0][1],
            boundaries[1][0]:boundaries[1][1]] for boundaries in boundaries_negative_tiles]
        negative_tiles_records = [
            [self.frame_record_to_tile_record(boundaries[0][0], boundaries[1][0], record) 
                 for record in self.mitotic_coordinates
                 if self.check_record_presence_in_boundaries(record, boundaries)
            ]
            for boundaries in boundaries_negative_tiles
        ]
        return [Tile(image, records) for image, records in zip(negative_tiles_images, negative_tiles_records)]
    
    def generate_real_positive_tiles(self):
        # Get centroids for tiles
        try:
            positive_tiles_centroids = [self.get_random_positive_tile_centroid() for _ in range(self.num_tiles)]
        except IndexError:
            print(self.possible_positive_centroids)
            print(self.centroid_limits)
        print(self.mitotic_coordinates[0].__dict__)
        
        # Get tiles' boundaries
        boundaries_positive_tiles = [self.get_boundaries_tile(cent) for cent in positive_tiles_centroids]
        print(boundaries_positive_tiles)
        
        for boundaries in boundaries_positive_tiles:
            for record in self.mitotic_coordinates:
                print(self.check_record_presence_in_boundaries(record, boundaries))
        
        # Get tiles' images
        positive_tiles_images = [self.image_frame[boundaries[0][0]:boundaries[0][1],
            boundaries[1][0]:boundaries[1][1]] for boundaries in boundaries_positive_tiles]
        
        # Get records in tiles
        positive_tiles_records = [
            [self.frame_record_to_tile_record(boundaries[0][0], boundaries[1][0], record) 
                 for record in self.mitotic_coordinates
                 if self.check_record_presence_in_boundaries(record, boundaries)
            ]
            for boundaries in boundaries_positive_tiles
        ]
        
        print(positive_tiles_records)
        
        # Show tiles within frame
        mask = np.zeros(self.frame.frame.shape[:2], np.uint8)
        for boundaries in boundaries_positive_tiles:
            mask[boundaries[0][0]:boundaries[0][1],
            boundaries[1][0]:boundaries[1][1]] = 1
        plt.imshow(cv2.bitwise_and(self.frame.frame,self.frame.frame,mask = mask))
        
        # Return tiles
        return [Tile(image, records) for image, records in zip(positive_tiles_images, positive_tiles_records)]