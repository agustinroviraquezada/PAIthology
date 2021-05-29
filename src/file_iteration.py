from src.Class_PatchGenerator import PatchGenerator
from PIL import Image
import os
import pandas as pd
from pathlib import Path

path_image = Path("C:/Users/pasto/projects/ai_saturdays_proyecto/A14").glob('**/*.jpg')
path_label = Path("C:/Users/pasto/projects/ai_saturdays_proyecto/A14").glob('**/*.xlsx')

for image in path_image:

    image_string = str(image)
    label_string = str(image).rsplit('.', 1)[0]

    tile_size = 256
    num_tiles = 100

    labels = pd.read_excel(label_string + ".xlsx", header=None)

    if labels.empty:
        patch = PatchGenerator(image_string, tile_size, num_tiles, None)
        patch_not_mitotic_cell = patch.create_patches(both_sides=False)

    else:
        for i in range(labels[0].size):
            for j in range(num_tiles):
                x_mitotic = labels[1][i]
                y_mitotic = labels[0][i]

                patch = PatchGenerator(image_string, tile_size, num_tiles, (x_mitotic, y_mitotic))

                original_image_coordinates, patch_with_mitotic_cell, \
                patch_not_mitotic_cell = patch.create_patches(both_sides=True)

                #x1[i][0][0], x2[i][0][1], y1[i][1][0], y2[i][1][1]
                if ((x_mitotic - tile_size < original_image_coordinates[j][0][0] < x_mitotic + tile_size) or \
                        (y_mitotic - tile_size < original_image_coordinates[j][0][1] < y_mitotic + tile_size)) and \
                        ((x_mitotic - tile_size < original_image_coordinates[j][1][0] < x_mitotic + tile_size) or \
                        (y_mitotic - tile_size < original_image_coordinates[j][1][1] < y_mitotic + tile_size)):

                    del patch_with_mitotic_cell[i]




