from math import cos, sin, tan, pi
import numpy as np
import pygame
from PIL import Image
from pygame.locals import *
from cylinder import Cylinder
from sys import exit

width = 1024
height = 1024
pygame.init()
pygame.display.set_caption('cylinder-shading')
screen = pygame.display.set_mode((width, height))
CLOCK = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# projection setup
theta = pi / 2
S = 1 / tan(theta / 2)
near = 0.1
far = 100.0

# projection matrix (https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/building-basic-perspective-projection-matrix)
M = np.array([
    [S, 0, 0, 0],
    [0, S, 0, 0],
    [0, 0, -far / (far - near), -1],
    [0, 0, (-far * near) / (far - near), 0]
])

# scaling matrix
S = np.array([
    [1000, 0, 0, 0],
    [0, 1000, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

def draw_triangle(x1, y1, x2, y2, x3, y3):
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x1, y1), (x2, y2), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x2, y2), (x3, y3), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x3, y3), (x1, y1), 1)

cyl = Cylinder()

# translation matrix
T = np.eye(4)
T[3, 1] = -cyl.get_center_y()

T2 = np.eye(4)
T2[3, 1] = cyl.get_center_y()
T2[3, 2] = 5

# camera
camera = np.zeros(3)

def cross_product(v, w):
    vec = np.zeros(4)
    vec[0] = v[1] * w[2] - v[2] * w[1]
    vec[1] = v[2] * w[0] - v[0] * w[2]
    vec[2] = v[0] * w[1] - v[1] * w[0]
    return vec

# function which draws 3D triangles on screen and applies rotation
def rotate(dx, dy, dz):
    R_xn = np.array([
        [1, 0, 0, 0],
        [0, cos(dx), sin(dx), 0],
        [0, -sin(dx), cos(dx), 0],
        [0, 0, 0, 1]])

    R_yn = np.array([
        [cos(dy), 0, -sin(dy), 0],
        [0, 1, 0, 0],
        [sin(dy), 0, cos(dy), 0],
        [0, 0, 0, 1]])

    R_zn = np.array([
        [cos(dz), -sin(dz), 0, 0],
        [sin(dz), cos(dz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    # set rotation and translation matrix
    master_matrix = np.eye(4).dot(T).dot(R_yn).dot(R_xn).dot(R_zn).dot(T2)

    for triangle in cyl.tris:
        points = triangle.get_points()

        for i in range(3):
            points[i] = points[i].dot(master_matrix)
            
        # https://math.stackexchange.com/questions/305642/how-to-find-surface-normal-of-a-triangle
        normal = cross_product(points[1] - points[0], points[2] - points[0])

        # visibility of triangles
        normal = normal / np.sqrt(np.sum(normal ** 2))
        if normal[0] * (points[0][0] - camera[0]) + \
            normal[1] * (points[0][1] - camera[1]) + \
            normal[2] * (points[0][2] - camera[2]) < 0:

            shift = np.array([1, 0.5, 0, 0])
            for i in range(3): # projection, normalize (by z) and shift
                points[i] = (points[i].dot(M) / points[i][2] + shift) / 2
                points[i] = points[i].dot(S)

            draw_triangle(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1])

rotate(0, 0, pi)

pygame.display.flip()

angle_x = angle_y = 0
angle_z = pi
delta_ang = pi / 120
left = right = up = down = z_key = a_key = False
redraw = False
on = True

while on:
    for event in pygame.event.get():
        if event.type == QUIT:
            on = False
            pygame.display.quit()
            pygame.quit()
            break

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True
            if event.key == K_a:
                a_key = True
            if event.key == K_z:
                z_key = True
            if event.key == K_s:
                T2[3, 2] -= 1
                redraw = True
            if event.key == K_x:
                T2[3, 2] += 1
                redraw = True

        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_RIGHT:
                right = False
            if event.key == K_a:
                a_key = False
            if event.key == K_z:
                z_key = False

    if up:
        angle_x += delta_ang
    elif down:
        angle_x -= delta_ang
    if left:
        angle_y -= delta_ang
    elif right:
        angle_y += delta_ang
    if a_key:
        angle_z += delta_ang
    elif z_key:
        angle_z -= delta_ang

    if left or right or up or down or a_key or z_key or redraw:
        screen.fill((0, 0, 0))
        rotate(angle_x, angle_y, angle_z)
        pygame.display.flip()
        redraw = False
    CLOCK.tick(120)

exit(0)
