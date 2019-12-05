import time

import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(4)
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)


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
    n = len(l)
    points = [(l[i], l[(i + 1) % n]) for i in range(n)]
    for point in points:
        draw_line(*point)


def get_square_vertices(x, y, size=50):
    s = size / 2
    return [[x + s, y + s],
            [x + s, y - s],
            [x - s, y - s],
            [x - s, y + s]]


def translate(l, tx, ty):
    points = []
    for point in l:
        x, y = point

        points.append((x + tx, y + ty))
    return points
    # l2 = [tuple(((a + tx, b + ty) for a, b in point)) for point in l]
    # print(l2)


def scale(l, sx, sy, rx=0, ry=0):
    l = translate(l, -rx, -ry)
    points = []
    for point in l:
        x, y = point
        res = np.dot(get_scaling_matrix(sx, sy), get_point_matrix(x, y))
        points.append((res[0][0], res[1][0]))
    return translate(points, rx, ry)


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


def rotate(points, theta, rx=0, ry=0):
    theta = np.pi * theta / 180

    points = translate(points, -rx, -ry)
    nl = []
    for point in points:
        x, y = point
        B = np.array([[x], [y], [1]])
        B = np.dot(get_rot_matrix(theta), B)
        # x1 = x * np.cos(theta) - y * np.sin(theta)
        # y1 = x * np.sin(theta) + y * np.cos(theta)
        nl.append((B[0][0], B[1][0]))
    return translate(nl, rx, ry)


def disp():
    pass
    # poly(l)
    # print(l)
    # poly(4, l)
    # draw_line((500, 500), (0, 0))
    # glFlush()


def mouse(btn, state, x, y):
    global l
    # print(btn, state, x, y)
    y = 500 - y
    if btn == 0 and state == 1:
        poly(get_square_vertices(x, y))
        move_till_collide(x, y, 1, -2)
        # l = rotate(l, 10)
        # poly(l)


def refresh():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


def fall_down(x, y):
    while y >= 25:
        y -= 5
        poly(get_square_vertices(x, y))
        time.sleep(0.001)
        refresh()


def move_till_collide(x, y, tx, ty):
    for _ in range(1000):
        if x < 25 or x > 475:
            tx = -tx
        if y < 25 or y > 475:
            ty = -ty
        poly(get_square_vertices(x, y))
        time.sleep(0.01)
        refresh()
        x += tx
        y += ty
    fall_down(x, y)


def har(*args):
    print(args)

def keys(btn, x, y):
    global l
    if btn == 'a':
        l = translate(l, -10, 0)
    if btn == 'd':
        l = translate(l, 10, 0)
    if btn == 's':
        l = translate(l, 0, -10)
    if btn == 'w':
        l = translate(l, 0, 10)
    if btn == 'r':
        l = rotate(l, 10)
    if btn == 'v':
        l = scale(l, 2, 2)
    poly(l)
    print(l)


def main():
    global l
    l = [(0, 0), (100, 0), (100, 100), (0, 100)]
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'On Day')
    init()
    glutDisplayFunc(disp)
    glutKeyboardFunc(keys)
    glutMouseFunc(mouse)
    glutMainLoop()


main()
