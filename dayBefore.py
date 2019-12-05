from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


def init():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glClearColor(1.0, 1.0, 0.0, 1.0)
    # glPointSize(4)
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)


def dda_draw(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)

    xinc = dx / float(step)
    yinc = dy / float(step)

    x, y = x1, y1

    for i in range(int(step)):
        glVertex2f(x, y)
        x += xinc
        y += yinc


def my_dda(p1, p2):
    x1, x2 = p1


def draw_polygon():
    l = []
    p = []
    for i in range(len(l) - 1):
        p.append((l[i], l[(i + 1) % len(l)]))

def plot():
    glBegin(GL_POINTS)
    dda_draw((0, 0), (100, 100))
    glEnd()
    glFlush()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Day before the exam')
    init()
    glutDisplayFunc(plot)
    glutMainLoop()


main()
