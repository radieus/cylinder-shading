import numpy as np
from math import cos, sin, tan, pi

class Triangle:
    # class consist of 3 vertices V = (p,n,t) p - point (x,y,z,1)
    def __init__(self, p1, p2, p3):
        self.verts = [p1, p2, p3]

    def draw(self):
        pass

    def get_points(self):
        return [self.verts[0][0], self.verts[1][0], self.verts[2][0]]

    def __repr__(self):
        return str(self.verts)

class Cylinder:
    def __init__(self):
        self.h = 2
        r = 1 
        n = 30

        # points on the bottom and the top of the cylinder
        p = [None] * (4 * n + 2)

        # points on top
        p_top = [np.array([0, self.h, 0, 1])] + [np.array([r * cos(2 * pi * i / n), self.h, r * sin(2 * pi * i / n), 1]) for i in range(n)]
        p[0:n + 1] = p_top
        # normal vector top
        n_top = [np.array([0, 1, 0, 0]) for _ in range(n + 1)]

        # points on bottom
        p_bot = [np.array([r * cos(2 * pi * i / n), 0, r * sin(2 * pi * i / n), 1]) for i in range(n)] + [np.array([0, 0, 0, 1])]
        p[(3 * n + 1):(4 * n + 2)] = p_bot
        # normal vector bottom
        n_bot = [np.array([0, -1, 0, 0]) for _ in range(n + 1)]

        # sides
        p_sides = [np.array(p[i - n]) for i in range(n + 1, 2 * n + 1)] + [np.array(p[i + n]) for i in range(2 * n + 1, 3 * n + 1)]
        p[(n + 1):3 * n + 1] = p_sides
        # sides norm
        n_sides = [np.array([p[i][0] / r, 0, p[i][2] / r, 0]) for i in range(n + 1, 3 * n + 1)]

        norms = n_top + n_sides + n_bot
        self.points = p

        # create vertices
        verts = []
        for i in range(4 * n + 2):
            verts += [(p[i], norms[i])]

        top_tri = [Triangle(verts[0], verts[i + 2], verts[i + 1]) for i in range(n - 1)] + [
            Triangle(verts[0], verts[1], verts[n])]
        bot_tri = [Triangle(verts[4 * n + 1], verts[i + 1], verts[i + 2]) for i in range(3 * n, 4 * n - 1)] + [
            Triangle(verts[4 * n + 1], verts[4 * n], verts[3 * n + 1])]

        # side triangles n, ... ,3n-1
        side_tri = [Triangle(verts[i + 1], verts[i + 2], verts[i + 1 + n]) for i in range(n, 2 * n - 1)] + \
                   [Triangle(verts[2 * n], verts[n + 1], verts[3 * n])] + \
                   [Triangle(verts[i + 1], verts[i + 2 - n], verts[i + 2]) for i in range(2 * n, 3 * n - 1)] + \
                   [Triangle(verts[3 * n], verts[n + 1], verts[2 * n + 1])]
        self.tris = bot_tri + top_tri + side_tri

    def get_center_y(self):
        return self.h / 2