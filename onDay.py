import numpy
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


def init():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)
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


def poly(n, l):
    points = [(l[i], l[(i + 1) % 4]) for i in range(n)]
    for point in points:
        draw_line(*point)


def translate(l, tx, ty):
    points = []
    for point in l:
        x, y = point
        points.append((x + tx, y + ty))
    return points
    # l2 = [tuple(((a + tx, b + ty) for a, b in point)) for point in l]
    # print(l2)


def scale(l, sx, sy, rx, ry):
    l = translate(l, -rx, -ry)
    points = []
    for point in l:
        x, y = point
        points.append((x * sx, y * sy))
    return translate(points, rx, ry)


def rotate(points, theta, rx, ry):
    points = translate(points, -rx, -ry)
    theta = numpy.pi*theta/180
    nl = []
    for point in points:
        x,y = point
        x1 = x*numpy.cos(theta) - y*numpy.sin(theta)
        y1 = x*numpy.sin(theta) + y*numpy.cos(theta)
        nl.append((x1, y1))
    return translate(nl, rx, ry)



def disp():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    poly(len(l), l)
    print(l)
    # poly(4, l)
    # draw_line((500, 500), (0, 0))
    glFlush()


def mouse(btn, state, x, y):
    global l
    print(btn, state, x, y)
    y = 500 - y
    if btn == 0 and state == 1:
        # l = scale(l, 2, 2, 10, 10)
        # l = rotate(l, 20, 0, 0)
        l = translate(l, 10, 10)
        poly(len(l), l)


def main():
    global l
    l = [(0, 0), (100, 0), (100, 100), (0, 100)]
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1920, 1080)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'On Day')
    init()
    glutDisplayFunc(disp)
    glutMouseFunc(mouse)
    glutMainLoop()


main()
