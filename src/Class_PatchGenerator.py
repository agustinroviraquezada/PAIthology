import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.datasets import load_sample_image
from matplotlib.patches import Rectangle
import random

#Hello darkness my old friend,



class PatchGenerator():
    def __init__(self, image, tile_size, num_tiles, mitotic_coordinates):
        self.tile_size = tile_size
        self.num_tiles = num_tiles
        self.image = np.asarray(Image.open(image))
        self.mitotic_coordinates = mitotic_coordinates

    def generate_negative_patches(self, image, tile_size, num_tiles, mitotic_coordinates):
        """Generates random tiles that do NOT contain the mitotic coordinates. We pick x1 and y1
        randomly within the range of the whole image.
        We then randomly choose x2 and y2 if the patch does not contain the mitotic coordinates,
        we discard it otherwise"""
        y_image, x_image, _ = image.shape

        coord_x1 = []
        coord_y1 = []
        coord_x2 = []
        coord_y2 = []

        choice = [tile_size, -tile_size]

        i = 0
        while i < num_tiles:
            #choose x1 and y1 within the whole image
            x_choice = np.random.randint(0, x_image, 1)
            y_choice = np.random.randint(0, y_image, 1)

            if mitotic_coordinates is None:

                x2_candidate = x_choice + (random.choice(choice))
                y2_candidate = y_choice + (random.choice(choice))

                coord_x2.append(x2_candidate)
                coord_y2.append(y2_candidate)

                coord_x1.append(x_choice)
                coord_y1.append(y_choice)
                i += 1
            #generate random x2 and y2 candidates, we then choose the ones that do
            # not contain the mitotic coordinates
            else:
                x_mitotic, y_mitotic = mitotic_coordinates
                x2_candidate = x_choice + (random.choice(choice))
                y2_candidate = y_choice + (random.choice(choice))

                if (0 < x2_candidate < x_image) \
                    and (0 < y2_candidate < y_image) \
                    and (x2_candidate not in range(x_mitotic-tile_size, x_mitotic+tile_size)) \
                    and (y2_candidate not in range(y_mitotic-tile_size, y_mitotic+tile_size)):

                    coord_x1.append(x_choice)
                    coord_y1.append(y_choice)

                    coord_x2.append(x2_candidate)
                    coord_y2.append(y2_candidate)
                    i += 1

        return coord_x1, coord_x2, coord_y1, coord_y2

    def generate_positive_patches(self, image, tile_size, num_tiles, mitotic_coordinates):
        """Generates random tiles that contain the mitotic coordinates. We pick x1 and y1
        randomly within the range of the mitotic coordinates, given a tile size. We then randomly choose
        x2 and y2 if the patch contains the mitotic coordinates, we discard it otherwise"""
        y_image, x_image, _ = image.shape
        x_mitotic, y_mitotic = mitotic_coordinates

        coord_x1 = []
        coord_y1 = []
        coord_x2 = []
        coord_y2 = []

        choice = [tile_size, -tile_size]

        i = 0

        while i < num_tiles:
            #we get x1,y1 randomly within the range of the tile size, centered on the mitotic coordinates
            x_choice = np.random.randint(x_mitotic - tile_size, x_mitotic + tile_size, 1)
            y_choice = np.random.randint(y_mitotic - tile_size, y_mitotic + tile_size, 1)

            #We generate x2 and y2 candidates, and we check if the mitotic coordinates are contained in the patch
            x2_candidate = x_choice + (random.choice(choice))
            y2_candidate = y_choice + (random.choice(choice))

            if ((x_mitotic - tile_size < x_choice < x_mitotic + tile_size) or \
                (y_mitotic - tile_size < y_choice < y_mitotic + tile_size))and \
                ((x_mitotic - tile_size < x2_candidate < x_mitotic + tile_size) or \
                (y_mitotic - tile_size < y2_candidate < y_mitotic + tile_size)):

                coord_x1.append(x_choice)
                coord_y1.append(y_choice)

                coord_x2.append(x2_candidate)
                coord_y2.append(y2_candidate)
                i += 1

        return coord_x1, coord_x2, coord_y1, coord_y2

    def create_patches(self, both_sides=True):
        """calls both functions for generating positive and negative patches and stores the images in
        two separate lists (lists of numpy arrays)"""
        if both_sides == True:
            pos_x1_coord, pos_x2_coord, pos_y1_coord, \
            pos_y2_coord = self.generate_positive_patches(self.image, self.tile_size, self.num_tiles, self.mitotic_coordinates)

            neg_x1_coord, neg_x2_coord, neg_y1_coord, \
            neg_y2_coord = self.generate_negative_patches(self.image, self.tile_size, self.num_tiles, self.mitotic_coordinates)


            patch_with_mitotic_cell = []
            patch_not_mitotic_cell = []
            original_image_coordinates = []

            for i in range(self.num_tiles):
                x1_mitotic = int(min(pos_x1_coord[i], pos_x2_coord[i]))
                x2_mitotic = int(max(pos_x1_coord[i], pos_x2_coord[i]))
                y1_mitotic = int(min(pos_y1_coord[i], pos_y2_coord[i]))
                y2_mitotic = int(max(pos_y1_coord[i], pos_y2_coord[i]))

                individual_mitotic_patch = self.image[x1_mitotic:x2_mitotic, y1_mitotic:y2_mitotic, :]
                patch_with_mitotic_cell.append(individual_mitotic_patch)

                original_image_coordinates.append([[x1_mitotic, x2_mitotic], [y1_mitotic, y2_mitotic]])

                x1_not_mitotic = int(min(neg_x1_coord[i], neg_x2_coord[i]))
                x2_not_mitotic = int(max(neg_x1_coord[i], neg_x2_coord[i]))
                y1_not_mitotic = int(min(neg_y1_coord[i], neg_y2_coord[i]))
                y2_not_mitotic = int(max(neg_y1_coord[i], neg_y2_coord[i]))

                individual_not_mitotic_patch = self.image[x1_not_mitotic:x2_not_mitotic, y1_not_mitotic:y2_not_mitotic, :]
                patch_not_mitotic_cell.append(individual_not_mitotic_patch)

            #output: list of numpy arrays
            return original_image_coordinates, patch_with_mitotic_cell, patch_not_mitotic_cell

        else:
            neg_x1_coord, neg_x2_coord, \
            neg_y1_coord, neg_y2_coord = self.generate_negative_patches(self.image, self.tile_size, self.num_tiles,
                                                          self.mitotic_coordinates)
            patch_not_mitotic_cell = []

            for i in range(self.num_tiles):
                x1_not_mitotic = int(min(neg_x1_coord[i], neg_x2_coord[i]))
                x2_not_mitotic = int(max(neg_x1_coord[i], neg_x2_coord[i]))
                y1_not_mitotic = int(min(neg_y1_coord[i], neg_y2_coord[i]))
                y2_not_mitotic = int(max(neg_y1_coord[i], neg_y2_coord[i]))

                individual_not_mitotic_patch = self.image[x1_not_mitotic:x2_not_mitotic,
                                               y1_not_mitotic:y2_not_mitotic, :]

                patch_not_mitotic_cell.append(individual_not_mitotic_patch)

            # output: list of numpy arrays
            return patch_not_mitotic_cell




if __name__ == "__main__":
    #PatchGenerator()
    cell = "A14_02Aa_mitosis.jpg"

    tile_size = 256
    num_tiles = 100
    mitotic_coordinates = (865, 651)

    patch = PatchGenerator(cell, tile_size, num_tiles, mitotic_coordinates)

    original_image_coordinates, patch_with_mitotic_cell, patch_not_mitotic_cell = patch.create_patches()
    print(original_image_coordinates[0])
    #mitotic_cell = Image.fromarray(patch_with_mitotic_cell[0])
    #print(patch_with_mitotic_cell[0].shape)
    #mitotic_cell.show()