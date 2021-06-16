class Tile:
    """Class of all sub-frames and the specific position of mitotic cells in them."""
    def __init__(self, image, records=None):
        self.image = image
        self.records = records or []
    
    def update_records(self,record):
        self.records += [record]