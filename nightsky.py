#!/usr/bin/env python
import math
from random import random

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.gray import *

FRAMES = 32
WIDTH = 500
HEIGHT = 500
STARS = 25
PS = 1 # 1 for gray, 3 for rgb

star = Model()
star.lines(((-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)), WHITE)

sky = []

for frame in xrange(FRAMES):
    globe = Model()
    for _ in xrange(STARS):
        new_star = Model(star)
        new_star.rotate((0, 0, WIDTH / 2), (
            (random() * 2 - 1) * math.pi / 4,
            (random() * 2 - 1) * math.pi / 4,
            (random() * 2 - 1) * math.pi / 4,
        ))
        globe.extend(new_star)
    globe.rotate((0, 0, WIDTH / 2), (math.pi, 0, 0))
    sky.append(globe)


for frame in xrange(FRAMES):
    
    output = Model()

    for neighbor in xrange(frame - FRAMES / 4, frame + FRAMES / 4):
        globe = Model(sky[neighbor % FRAMES])
        dist = float(frame - neighbor)
        globe.rotate((0, 0, WIDTH / 2), (-dist / 50, 0, -dist / 500))
        c = (FRAMES / 4. - abs(dist)) * 4 / FRAMES * 255
        color = (int(c),) * PS
        for star in globe:
            args = list(star[1])
            args[-1] = color
            output.append((star[0], tuple(args), star[2]))
    
    output.translate((WIDTH / 2, WIDTH / 2, -WIDTH))

    canvas = Canvas(WIDTH, HEIGHT, 'gray')
    canvas.import_model(output)
    canvas.write('nightsky.%s' % str(frame).zfill(3))
    print frame

gif('nightsky')
