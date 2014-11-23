#!/usr/bin/env python
import itertools
import math
import random

import numpy

from pyfrax.model import Model
from pyfrax.canvas import Canvas
from pyfrax.colors.rgb import *
from pyfrax.rendertools import *

WIDTH = 500
HEIGHT = 500

class CanvasCutoff(Canvas):
    def line(self, start, end, c, a=1.0):
        choice = random.randrange(50)
        if choice == 0:
            end = (1000, start[1], start[2])
        if choice == 1:
            end = (-500, start[1], start[2])
        if choice == 2:
            start = (1000, end[1], end[2])
        if choice == 3:
            start = (-500, end[1], end[2])
        super(CanvasCutoff, self).line(start, end, c, a)
    def pixel(self, z, fp, c, a):
        if 250 < z <= 300:
            a *= (300 - z) / 50.
        elif z > 300:
            return
        super(CanvasCutoff, self).pixel(z, fp, c, a)

cube_face = Model()
#cube_face.quad(
#    (100, 100, 100),
#    (100, 400, 100),
#    (400, 400, 100),
#    (400, 100, 100),
#    BLACK
#)
for i in xrange(6):
    cube_face.line(
        (75, 125 + 50 * i, 75),
        (425, 125 + 50 * i, 75),
        WHITE
    )
for i in xrange(6):
    cube_face.line(
        (125 + 50 * i, 75, 75),
        (125 + 50 * i, 425, 75),
        WHITE
    )

cube = Model(cube_face)

rotations = (
    (0, math.pi / 2, 0),
    (0, math.pi, 0),
    (0, 3 * math.pi / 2, 0),
    (math.pi / 2, 0, 0),
    (3 * math.pi / 2, 0, 0)
)
for rotation in rotations:
    cube_face_rotated = Model(cube_face)
    cube_face_rotated.rotate((250, 250, 250), rotation)
    cube.extend(cube_face_rotated)

del cube_face, cube_face_rotated

cube.rotate((250, 250, 250), (math.pi / 4, math.pi / 4, 0))

for frame in xrange(32):
    # generate background
    bg = numpy.zeros((WIDTH, HEIGHT, 3), dtype='uint8')
    l = random.randrange(WIDTH / 2, WIDTH)
    i = 0
    bgcolor = [[0, 0, 0], [random.randrange(64)] * 3]
    whichcolor = 0
    for x, y in itertools.product(xrange(WIDTH), xrange(HEIGHT)):
        bg[x][y] = bgcolor[whichcolor]
        i += 1
        if i == l:
            whichcolor = 1 - whichcolor
            i = 0
    cube_rotated = Model(cube)
    cube_rotated.rotate((250, 250, 250), (0, frame * math.pi / 32, 0))
    canvas = CanvasCutoff(WIDTH, HEIGHT)
    canvas.background(bg)
    canvas.import_model(cube_rotated)
    canvas.write("wired.%s" % str(frame).zfill(2))
    print str(frame).zfill(2)
    del canvas

del cube_rotated, cube

gif("wired")
