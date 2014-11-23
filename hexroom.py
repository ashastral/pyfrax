#!/usr/bin/env python
import math
import random

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

FRAMES = 16
WIDTH = 500
HEIGHT = 500
HEXAGONS = 12

class CanvasLinearShading(Canvas):
    def shade(self, z, c):
        M = 500
        return tuple(color * min(M, max(0, M - z)) / M for color in c)

hexagon = Model()
hexagon.lines(((.25, 0, 0), (.75, 0, 0), (1, 5/12., 0), (.75, 5/6., 0), (.25, 5/6., 0), (0, 5/12., 0)), RED)
hexagon.scale(WIDTH / HEXAGONS)
#hexagon.rotate((.5, 0, 0), (math.pi / 4, 0, 0))


for frame in xrange(6, FRAMES):
    hexagons = Model()

    for x in xrange(-1 - HEXAGONS / 2, 3 * HEXAGONS / 2 + 1):
        x += frame / float(FRAMES)
        for z in xrange(-1, HEXAGONS + 1):
            z -= frame / float(FRAMES)
            hexagon2 = Model(hexagon)
            hexagon2.translate((x * (WIDTH / HEXAGONS), (z + (x % 2) / 2.) * (WIDTH / HEXAGONS), 10 * math.sin(x * 2. / HEXAGONS * math.pi)))
            hexagons.extend(hexagon2)

    hexagons.rotate((WIDTH / 2, HEIGHT / 2, 0), (math.pi / 2, 0, 0))
    hexagons.translate((0, -HEIGHT / 2, WIDTH / 2))

    hexagons2 = Model(hexagons)
    hexagons2.rotate((WIDTH / 2, HEIGHT / 2, 0), (0, 0, math.pi))

    canvas = CanvasLinearShading()
    canvas.import_model(hexagons)
    del hexagons
    canvas.import_model(hexagons2)
    del hexagons2

#    lightning = Model()
#    corner = (random.randrange(WIDTH * 3 / 5.), random.randrange(300))
#    top = (corner[0] + random.randrange(WIDTH * 2 / 5.), corner[1] + random.randrange(200))
#    for h in xrange(5):
#        bottom = (corner[0] + random.randrange(WIDTH * 2 / 5.), corner[1] + random.randrange(200))
#        lightning.line(
#            (top[0], h * HEIGHT / 5, top[1]),
#            (bottom[0], (h + 1) * HEIGHT / 5, bottom[1]),
#            WHITE
#        )
#        top = bottom
#        corner = (random.randrange(WIDTH * 3 / 5.), random.randrange(300))
#
#    canvas.import_model(lightning)

    canvas.write('hexroom.%s' % str(frame).zfill(3))

gif('hexroom')
