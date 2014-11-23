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
ROWS = 10
COLS = 10
RADIUS = 10

particles = []

class Thing(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def alt(p):
    return 1 if (p.x + p.y) % 2 else -1

for point in product(xrange(ROWS + 5), xrange(COLS + 5)):
    particles.append(Thing(
        p=Thing(x=point[0], y=point[1]),
        x=WIDTH * (point[0] - 2) / ROWS,
        y=HEIGHT * (point[1] - 2 + (.5 if point[0] % 2 else 0)) / COLS,
        z=random() * WIDTH / 5,
    ))

for point in product(xrange(ROWS + 5), xrange(COLS + 5)):
    p = [p for p in particles if p.p.x == point[0] and p.p.y == point[1]][0]
    other = [o for o in particles if o.p.x == point[0] + alt(p.p) * 2 and o.p.y == point[1]]
    if other:
        p.z2 = other[0].z
    else:
        p.z2 = p.z

for frame in xrange(FRAMES):
    f = float(frame) / FRAMES
    m = Model()
    
    for pair in combinations(particles, 2):
        newpair = []
        for i, p in enumerate(pair):
            x = p.x + (f * WIDTH / ROWS) * 2 * alt(p.p)
            y = p.y
            z = p.z * (1 - f) + p.z2 * f
            newpair.append(Thing(x=x, y=y, z=z))
        # Convenience
        n = newpair
        d = ((n[0].x - n[1].x) ** 2 + (n[0].y - n[1].y) ** 2 + (n[0].z - n[1].z) ** 2) ** .5
        brightness = min(255, max(0, 255 - (d * 4)))
        c = (min(255, brightness * 2), 0, brightness * 2 - 255)
        if not c[0]:
            continue
        #m.point((particle[0] + RADIUS * math.sin(theta + particle[2]),
        #         particle[1] + RADIUS * math.cos(theta + particle[2]),
        #         p * 10), WHITE)
        m.line((n[0].x, n[0].y, n[0].z), (n[1].x, n[1].y, n[1].z), c)
    
    canvas = Canvas(WIDTH, HEIGHT)
    canvas.vp = (WIDTH / 2, HEIGHT / 8)
    canvas.import_model(m)
    canvas.write('brokenmesh.%s' % str(frame).zfill(3))
    print frame

gif('brokenmesh')
