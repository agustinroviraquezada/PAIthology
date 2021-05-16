class Tile:
    def __init__(self, centroid_x: int, centroid_y: int, height: int, width: int):
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y
        self.height = height
        self.width = width

class Record:
    def __init__(self, x: int, y: int, confidence: float):
        self.x = x
        self.y = y
        self.confidence = confidence
    

def get_cell_coordinates_in_tile(tile: Tile, record: Record) -> Record:
    x_tile = record.x - tile.centroid_x + tile.width
    y_tile = record.y - tile.centroid_y + tile.height

    return Record(x_tile, y_tile, record.confidence)

