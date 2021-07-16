class Wall:
    def __init__(self, x1, y1, x2, y2, thickness=1, colour=(200, 200, 200)):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.thickness = thickness
        self.colour = colour

    def get_details(self):
        return (self.x1, self.y1), (self.x2, self.y2), self.thickness, self.colour
