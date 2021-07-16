import pygame
import pygame_menu
import math
import sys
from random import randint
from psutil import cpu_percent

from ray_class import Ray   # importing classes
from wall_class import Wall
from player_class import Player

pygame.init()

map_width, map_height = 150, 150    # dimensions of mini-map
width, height = 1000, 600       # dimensions of program output window
walk_speed = 1.5
rotation_speed = 3.5
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Ray Casting/Rendering by Adam Watney for Arkwright Engineering Scholarship")

background = (0, 0, 0)
is_high_contrast = False
frame_rate = 30
player_fov = 45


def get_wall_colour(is_hc, shade):
    if is_hc:   # if in high contrast mode
        return shade, 0, shade
    else:
        return shade, shade, shade


def change_colour(_, colour_type):
    global background, is_high_contrast
    if colour_type == 0:
        background = (0, 0, 0)
        is_high_contrast = False
    elif colour_type == 1:
        background = (0, 255, 0)
        is_high_contrast = True


def change_speed(_, speed):
    global walk_speed, rotation_speed
    walk_speed = speed
    rotation_speed = walk_speed * 2.2


def change_FOV(_, fov):
    global player_fov
    player_fov = fov


def gen_rays(player):
    for i in range(int(-player.num_rays / 2), int(player.num_rays / 2)):
        # create rays by parsing in the starting position and the angle of each ray
        player.rays.append(Ray(player.x, player.y, i * (player.FOV / player.num_rays)))


# convert a value that is between 0 & old_range to a new value between 0 & new_range
def translate(value, old_range, new_range):
    percentage = value / old_range
    new_value = percentage * new_range
    return new_value


def render(player, walls):
    screen.fill(background)  # clear screen
    ren_width = width / player.num_rays  # width of each vertical pixel on screen

    for index, ray in enumerate(player.rays):
        ray.update(player.x, player.y, ray.angle)
        record = math.inf
        intersection = None
        for wall in walls:
            ray.intersect(wall)
            if ray.hits_wall:
                pt = (ray.x4, ray.y4)
                dist = math.hypot(pt[0] - player.x, pt[1] - player.y) # distance between point of intersection and player

                if dist < record:
                    record = dist
                    intersection = pt

        if intersection:
            # set ray end point to be point of intersection
            ray.x4, ray.y4 = intersection[0], intersection[1]
            # calculate darkness of pixel (length of diagonal of the map is the maximum possible ray length)
            b = 255 - translate(record, math.hypot(map_width, map_height), 255)
            # calculate half of height of vertical pixel
            h = height/2 - translate(record, math.hypot(map_width, map_height), height/2)
            # draw top half
            pygame.draw.rect(screen, get_wall_colour(is_high_contrast, b), (index * ren_width, int(height/2 - h), ren_width, h+1))
            # draw bottom half
            pygame.draw.rect(screen, get_wall_colour(is_high_contrast, b), (index * ren_width, int(height/2), ren_width, h))

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, map_width, map_height))  # add black background to the map
    for ray in player.rays:
        ray_start, ray_end = ray.get_coords()
        pygame.draw.line(screen, (255, 100, 100), ray_start, ray_end, 1)


def start_game():
    # generate walls
    walls = []
    for i in range(4):  # create 4 random walls
        walls.append(Wall(randint(0, map_width), randint(0, map_height), randint(0, map_width), randint(0, map_height)))
    walls.append(Wall(map_width, 0, map_width, map_height, 2, (255, 255, 255)))     # edges of screen
    walls.append(Wall(0, map_height, map_width, map_height, 2, (255, 255, 255)))
    walls.append(Wall(0, 0, 0, map_height, 2, (255, 255, 255)))
    walls.append(Wall(0, 0, map_width, 0, 2, (255, 255, 255)))

    player = Player(map_width / 2, map_height / 2)
    player.FOV = player_fov
    gen_rays(player)
    render(player, walls)

    show_cpu_usage = pygame.USEREVENT
    pygame.time.set_timer(show_cpu_usage, 5000)    # check CPU usage every 5 seconds

    global frame_rate
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == show_cpu_usage:
                usage = cpu_percent()
                print(f"CPU Usage: {usage}%")    # show CPU usage
                # alter frame rate if cpu usage is too high
                if usage >= 2:
                    frame_rate = 15
                    print("Frame rate reduced for better performance")
                else:
                    frame_rate = 30

        pk = pygame.key.get_pressed()
        if pk[pygame.K_a]:
            player.rotate(-rotation_speed)     # rotate the player left

        elif pk[pygame.K_d]:
            player.rotate(rotation_speed)

        if pk[pygame.K_w]:
            player.move(walk_speed, map_width, map_height)

        elif pk[pygame.K_s]:
            player.move(-walk_speed, map_width, map_height)

        render(player, walls)

        # render the randomised walls
        for wall in walls:
            wall_start, wall_end, wall_width, wall_colour = wall.get_details()
            pygame.draw.line(screen, wall_colour, wall_start, wall_end, wall_width)

        pygame.display.flip()   # render the screen
        clock.tick(frame_rate)    # set frame rate of game (in FPS)


menu = pygame_menu.Menu("Render Rays Menu", 500, 320, theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Start', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.selector('Speed: ', [('Default', 1.5), ('Slow', 1), ('Fast', 3)], onchange=change_speed)
menu.add.selector('Colour Mode: ', [('Normal', 0), ('High Contrast', 1)], onchange=change_colour)
menu.add.selector('FOV: ', [('Normal', 45), ('Narrow', 30), ('Wide', 90)], onchange=change_FOV)

menu.mainloop(screen)
