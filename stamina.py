#!/usr/bin/env python
import math
from random import random, randrange

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

FRAMES = 32
WIDTH = 500
HEIGHT = 500
TRIANGLES = FRAMES
TSIZE = 80.

triangles = []

triangles = [{
    'x': randrange(WIDTH),
    'y': randrange(HEIGHT),
    'r': random() * math.pi * 2,
} for _ in xrange(TRIANGLES)]

def mktriangle(x, y, t, tframe):
    triangle = Model()
    outer = -2 * TSIZE
    inner = -2 * TSIZE * frame / FRAMES
    z = WIDTH * (1 - (2. * ((frame + t) % FRAMES) / FRAMES))
    print outer, inner, z
    for angle_index in xrange(3):
        angle = angle_index * math.pi * 2 / 3
        next_angle = (angle_index+1) * math.pi * 2 / 3
        triangle.quad(
            (x + math.sin(angle) * outer, y + math.cos(angle) * outer, z),
            (x + math.sin(angle) * inner, y + math.cos(angle) * inner, z),
            (x + math.sin(next_angle) * inner, y + math.cos(next_angle) * inner, z),
            (x + math.sin(next_angle) * outer, y + math.cos(next_angle) * outer, z),
            WHITE
        )
    return triangle

#####
for frame in [31]:#xrange(FRAMES):
    canvas = Canvas(WIDTH, HEIGHT, 'rgb')
    canvas.import_model(mktriangle(x=HEIGHT/2, y=WIDTH/2, t=0, tframe=frame))
    canvas.write('triangle_test.%s' % str(frame).zfill(2))
gif('triangle_test')
exit()
#####

for frame in xrange(FRAMES):
    for t, triangle in enumerate(triangles):
        x, y = triangle['x'], triangle['y']
        # WIDTH to -WIDTH
        z = WIDTH * (1 - (2 * ((frame + t) % FRAMES) / FRAMES))

gif('stamina')
