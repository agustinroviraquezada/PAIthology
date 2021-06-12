# This could be a namedtuple
class Record:
    """Class which gathers information of the position and confidence of a cell."""
    def __init__(self, y: int, x: int, confidence: float):
        # ATTENTION, Label.xlsx ARE WITH THE COORDINATES TRANSPOSED. THIS HAS BEEN CHANGED TO THAT

        self.x = x
        self.y = y
        self.confidence = confidence
        
    def generate_bndbox(self):
        bndbox_size = 30
        return (
            int(self.x - bndbox_size/2), int(self.x + bndbox_size/2),
            int(self.y - bndbox_size/2), int(self.y + bndbox_size/2)
        )