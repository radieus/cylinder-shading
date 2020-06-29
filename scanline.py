from pygame import Color

class Filler:

    def __init__(self, screen):
        self.screen = screen

    def set_pixel(self, x, y):
        r, g, b = 255, 0, 0
        self.screen.set_at((x, y), Color(r, g, b))

    def scan_line(self, points):
        # print(points)
        t_ps = [points[i] for i in range(len(points))]
        t_ps.sort(key=lambda p: p[1])
        A = t_ps[0]
        B = t_ps[1]
        C = t_ps[2]

        dy1 = B[1] - A[1]
        dx1 = B[0] - A[0]

        dy2 = C[1] - A[1]
        dx2 = C[0] - A[0]

        dax_step = dbx_step = 0

        if dy1:
            dax_step = dx1 / abs(dy1)
        if dy2:
            dbx_step = dx2 / abs(dy2)
        if dy1:
            i = A[1]
            while i <= B[1]:
                ax = A[0] + (i - A[1]) * dax_step
                bx = A[0] + (i - A[1]) * dbx_step

                if ax > bx:
                    # swap values to ensure going from smaller to larger
                    ax, bx = bx, ax

                # step in the texture
                j = int(ax)
                while j < bx:
                    self.set_pixel(j, i)
                    j += 1
                # iterate loop
                i += 1

        dy1 = C[1] - B[1]
        dx1 = C[0] - B[0]

        if dy1:
            dax_step = dx1 / abs(dy1)
        if dy2:
            dbx_step = dx2 / abs(dy2)
        if dy1:
            i = B[1]
            while i <= C[1]:
                ax = B[0] + (i - B[1]) * dax_step
                bx = A[0] + (i - A[1]) * dbx_step
                if ax > bx:
                    # swap values to ensure going from smaller to larger
                    ax, bx = bx, ax

                j = int(ax)
                while j < bx:
                    self.set_pixel(j, i)
                    j += 1
                # iterate loop
                i += 1