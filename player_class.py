import math


class Player:
    def __init__(self, x, y):
        self.FOV = 45       # field of view in degrees
        self.num_rays = 100
        self.speed = 1
        self.x = x
        self.y = y
        self.rays = []
        self.direction = 0      # in degrees
        self.dir_vector = [math.cos(math.radians(self.direction)),
                           math.sin(math.radians(self.direction))]

    def move(self, dire, map_width, map_height):
        self.x += self.dir_vector[0] * self.speed * dire     # dire means forward or backward (1=forward or -1=backward)
        self.y += self.dir_vector[1] * self.speed * dire

        # stop the player when it hits the outer walls
        if self.x > map_width - 1:
            self.x = map_width - 1
        elif self.x < 1:
            self.x = 1
        if self.y > map_height - 1:
            self.y = map_height - 1
        elif self.y < 1:
            self.y = 1

    def rotate(self, angle):
        # update directions of the rays
        for ray in self.rays:
            ray.angle += angle
            ray.update(ray.x3, ray.y3, ray.angle)
        # set the direction of player to the direction of the middle ray
        self.direction = self.rays[int(len(self.rays) / 2)].angle
        # update direction vector of player
        self.dir_vector[0] = math.cos(math.radians(self.direction))
        self.dir_vector[1] = math.sin(math.radians(self.direction))
