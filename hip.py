#!/usr/bin/env python
from itertools import combinations, product
import math
from random import random, triangular

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

FRAMES = 24
WIDTH = 350
HEIGHT = 350
ROWRANGE = (-10, 20)
LAYERRANGE = (0, 15)
ROWS = ROWRANGE[1] - ROWRANGE[0]
LAYERS = LAYERRANGE[1] - LAYERRANGE[0]
RADIUS = 10

vertices = []

class Canvas3DShaded(Canvas):
    def shade(self, z, c):
        W = 1.5 * self.image.shape[0]
        return tuple(color * min(W, max(0, W - z)) / W for color in c)


class Thing(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

for l in xrange(*LAYERRANGE):
    layer = []
    for r in xrange(*ROWRANGE):
        layer.append(Thing(
            p=Thing(x=r, y=l),
            x=WIDTH * r / 10,
            y=HEIGHT + HEIGHT * math.sin(float(r) / ROWS * math.pi) / 5 + random() * HEIGHT / 10,
            z=HEIGHT * l / 10,
        ))
    vertices.append(layer)

mrange = Model()
for l in xrange(LAYERS - 1):
    for r in xrange(ROWS - 1):
        vs = [vertices[l][r], vertices[l][r + 1], vertices[l + 1][r + 1], vertices[l + 1][r]]
        for v in xrange(len(vs) - 1):
            mrange.line((vs[v].x, vs[v].y, vs[v].z),
                        (vs[v+1].x, vs[v+1].y, vs[v+1].z),
                        WHITE)

c = Canvas3DShaded(WIDTH, HEIGHT)
c.import_model(mrange)
c.write('mrange')
