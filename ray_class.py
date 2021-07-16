import math


class Ray:
    def __init__(self, x3, y3, angle):
        self.angle = angle
        self.dir_vector = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
        self.x3 = x3    # x3 and y3 are always the origin of the light ray
        self.y3 = y3
        self.x4 = self.x3 + self.dir_vector[0]      # calculate new position
        self.y4 = self.y3 + self.dir_vector[1]
        self.hits_wall = False

    def update(self, x3, y3, angle):
        if angle > 180:
            angle = angle - 360
        elif angle < -180:
            angle = angle + 360
        self.angle = angle
        self.x3 = x3  # set new origin
        self.y3 = y3
        self.dir_vector = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
        self.x4 = self.x3 + self.dir_vector[0]
        self.y4 = self.y3 + self.dir_vector[1]
        self.hits_wall = False

    def intersect(self, wall):
        # do all the maths to calculate coordinate of intersection with wall
        den = (wall.x1 - wall.x2) * (self.y3 - self.y4) - (wall.y1 - wall.y2) * (self.x3 - self.x4)  # denominator
        if den == 0:
            return

        t = ((wall.x1 - self.x3) * (self.y3 - self.y4) - (wall.y1 - self.y3) * (self.x3 - self.x4)) / den
        u = -((wall.x1 - wall.x2) * (wall.y1 - self.y3) - (wall.y1 - wall.y2) * (wall.x1 - self.x3)) / den

        if 0 <= t <= 1 and u >= 0:
            self.x4 = wall.x1 + t * (wall.x2 - wall.x1)
            self.y4 = wall.y1 + t * (wall.y2 - wall.y1)
            self.hits_wall = True

    def get_coords(self):
        return (self.x3, self.y3), (self.x4, self.y4)
