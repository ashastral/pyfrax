#!/usr/bin/env python
import math
from random import choice, triangular

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

FRAMES = 32
WIDTH = 500
HEIGHT = 500
STARS_PER_FRAME = 5

stars = []

for frame in xrange(FRAMES):
    f = []
    for star in xrange(STARS_PER_FRAME):
        f.append((
            triangular(0, WIDTH),
            triangular(0, HEIGHT),
            choice((-1, 1))
        ))
    stars.append(f)

night_background = load_texture('night2.jpg')

for frame in xrange(FRAMES):
    sky = Model()
    
    for neighbor in xrange(frame - FRAMES / 4, frame + FRAMES / 4):
        neighbor_stars = stars[neighbor % FRAMES]
        dist = frame - neighbor
        c = (FRAMES / 4. - abs(dist)) * 4 / FRAMES * 255
        color = (int(c),) * 3
        for star in neighbor_stars:
            # there's no particular reason to use math.pi here; I just wanted
            # any irrational number to keep the pixels interesting
            new_point = (
                star[0] + dist * math.pi / 2 * star[2],
                star[1] + dist * math.pi / 2 * star[2],
                0
            )
            sky.point(new_point, color)

    canvas = Canvas(WIDTH, HEIGHT)
    canvas.background(night_background)
    canvas.import_model(sky)
    canvas.write('starrybyte.%s' % str(frame).zfill(3))
    print frame

gif('starrybyte')
