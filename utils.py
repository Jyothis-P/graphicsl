import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


def draw_line(p1, p2):
    glBegin(GL_POINTS)
    x1, y1 = p1
    x2, y2 = p2

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    steps = dx if dx > dy else dy

    xi = (x2 - x1) / steps
    yi = (y2 - y1) / steps

    for _ in range(int(steps)):
        glVertex2f(x1, y1)
        x1 += xi
        y1 += yi
    glEnd()
    glFlush()


def poly(l):
    glClear(GL_COLOR_BUFFER_BIT)  # so that previous polygons are removed
    n = len(l)
    points = [[l[i], l[(i + 1) % n]] for i in range(n)]
    for point in points:
        draw_line(*point)


def draw_circle(xc, yc, r=10):
    glBegin(GL_POINTS)

    p = 3.0 - 2.0 * r
    x, y = r, 0.0

    while x > y:
        y += 1
        if p <= 0:
            p += 4.0 * y - 6.0
        else:
            x -= 1.0
            p += 4.0 * y - 4.0 * x + 10.0
        glVertex2f(-x + xc, y + yc)
        glVertex2f(-x + xc, -y + yc)
        glVertex2f(x + xc, y + yc)
        glVertex2f(x + xc, -y + yc)
        glVertex2f(y + yc, -x + xc)
        glVertex2f(-y + yc, -x + xc)
        glVertex2f(y + yc, x + xc)
        glVertex2f(-y + yc, x + xc)
    glEnd()
    glFlush()


# Might not work as intended
def get_mid_point(points):
    x_max = y_max = 0
    x_min = y_min = points[0]
    for point in points:
        if point[0] > x_max:
            x_max = point[0]
        if point[1] > y_max:
            y_max = point[1]
        if point[0] < x_min:
            x_min = point[0]
        if point[1] < y_min:
            y_min = point[1]
    x = (x_max - x_min) / 2
    y = (y_max - y_min) / 2
    return x, y


def get_square_vertices(x, y, size=50):
    s = size / 2
    return [[x + s, y + s],
            [x + s, y - s],
            [x - s, y - s],
            [x - s, y + s]]


def get_rot_matrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])


def get_point_matrix(x, y):
    return np.array([[x], [y], [1]])


def get_translation_matrix(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])


def get_scaling_matrix(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def translate(l, tx, ty):
    t_mat = get_translation_matrix(tx, ty)
    for point in l:
        p_mat = get_point_matrix(*point)
        res = np.dot(t_mat, p_mat)
        point[0] = res[0][0]
        point[1] = res[1][0]
    return l


def rotate(points, theta, rx=0, ry=0):
    theta = np.pi * theta / 180
    points = translate(points, -rx, -ry)
    rot_mat = get_rot_matrix(theta)
    for point in points:
        p_mat = get_point_matrix(*point)
        res = np.dot(rot_mat, p_mat)
        point[0] = res[0][0]
        point[1] = res[1][0]
    return translate(points, rx, ry)


def scale(points, sx, sy, rx=0, ry=0):
    points = translate(points, -rx, -ry)
    scale_mat = get_scaling_matrix(sx, sy)
    for point in points:
        p_mat = get_point_matrix(*point)
        res = np.dot(scale_mat, p_mat)
        point[0] = res[0][0]
        point[1] = res[1][0]
    return translate(points, rx, ry)
