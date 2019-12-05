import time

import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils import *

g = 9.8
t_start = 0


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(2)
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)


def disp():
    draw_circle(50, 50, 10)


def mouse(btn, state, x, y):
    global t_start
    if btn == 0 and state == 1:
        t_start = time.time()
        kick(50, 50, 45, 20)


def kick(x, y, theta, u):
    theta *= np.pi/180
    tot_time = 2 * u * np.sin(theta) / g
    print(tot_time)
    t0 = time.time()
    t = 0
    while t < tot_time:
        t = time.time() - t0
        x_inc = u * np.cos(theta) + t + x
        y_inc = u * np.sin((theta)) - g * t ** 2 + y
        print(x_inc, y_inc)
        poly(get_square_vertices(x_inc, y_inc))
        time.sleep(0.1)



def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Projectile Motion')
    init()
    glutDisplayFunc(disp)
    glutMouseFunc(mouse)
    glutMainLoop()


main()
