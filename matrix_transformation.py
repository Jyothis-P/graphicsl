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
    glClear(GL_COLOR_BUFFER_BIT)  # so that previous polygons are removed
    n = len(l)
    points = [[l[i], l[(i + 1) % n]] for i in range(n)]
    for point in points:
        draw_line(*point)


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


def disp():
    poly(l)


def keys(btn, x, y):
    global l
    if btn == b'+':
        l = scale(l, 1.5, 1.5)
    if btn == b'-':
        l = scale(l, 1 / 1.5, 1 / 1.5)
    poly(l)


def arrow_keys(btn, x, y):
    global l
    if btn == GLUT_KEY_LEFT:
        l = translate(l, -10, 0)
    if btn == GLUT_KEY_DOWN:
        l = translate(l, 0, -10)
    if btn == GLUT_KEY_UP:
        l = translate(l, 0, 10)
    if btn == GLUT_KEY_RIGHT:
        l = translate(l, 10, 0)

    poly(l)


def main():
    global l
    l = [[0, 0], [100, 0], [100, 100], [0, 100]]
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Matrix Transformation')
    init()
    glutDisplayFunc(disp)
    glutSpecialFunc(arrow_keys)
    glutKeyboardFunc(keys)
    glutMainLoop()


main()
