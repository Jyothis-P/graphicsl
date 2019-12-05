from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time

import numpy as np


def init():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPointSize(4)
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

    for i in np.arange(step):
        glVertex2f(x, y)
        x += xinc
        y += yinc


def delay(s):
    t = time.time()
    while(time.time() - t) < s:
        print('a')

def refresh():
    print(time.time())
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)
    # dda_draw(p1, p2)
    glVertex2f(0, 100)
    glVertex2f(500, 100)
    glEnd()




def draw_square(x,y):
    size = 50
    glBegin(GL_LINES)
    # dda_draw(p1, p2)
    glVertex2f(x-size/2, y-size/2)
    glVertex2f(x+size/2, y-size/2)
    glVertex2f(x+size/2, y-size/2)
    glVertex2f(x+size/2, y+size/2)
    glVertex2f(x+size/2, y+size/2)
    glVertex2f(x-size/2, y+size/2)
    glVertex2f(x-size/2, y+size/2)
    glEnd()
    glFlush()


def draw_point(x,y):
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()
    glFlush()

def draw_train(x, y):
    draw_square(x-25, y)
    draw_square(x-75, y)
    draw_square(x-125, y)
    draw_square(x-175, y)


def plot():
    glBegin(GL_POINTS)
    # dda_draw(p1, p2)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glEnd()
    glFlush()

    for x in range(100, 300):
        refresh()
        draw_train(x, 200)
        time.sleep(0.05)
        # delay(0.1)
    # draw_point(100, 200)


def main():
    global p1, p2
    # p1 = (int(i) for i in
    #       input('Enter first point (comma separated): ').split(','))
    # p2 = (int(i) for i in
    #       input('Enter second point (comma separated): ').split(','))
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b'lines')
    init()
    glutDisplayFunc(plot)
    glutMainLoop()


if __name__ == '__main__':
    main()
