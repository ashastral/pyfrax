#!/usr/bin/env python
import math

from pyfrax.canvas import Canvas
from pyfrax.model import Model
from pyfrax.colors.rgb import *
from pyfrax.render import gif

class CanvasLighting(Canvas):
    def face(self, p1, p2, p3, c, a=1.0, aa=True):
        v1 = tuple(a - b for a, b in zip(p2, p1))
        v2 = tuple(a - b for a, b in zip(p3, p1))
        norm = [v1[1]*v2[2] - v1[2]*v2[1],
                v1[2]*v2[0] - v1[0]*v2[2],
                v1[0]*v2[1] - v1[1]*v2[0]]
        cmul = math.atan2(abs(norm[2]), abs(norm[1])) / math.pi
        c2 = tuple(int(round((cmul + .5) * cc)) for cc in c)
        super(CanvasLighting, self).face(p1, p2, p3, c2, a, aa)

#leftmost stroke
l = Model()
for z in (0, 0.5):
    l.quad((1, 3, z), (2, 3, z), (4, 5, z), (3, 5, z), WHITE)
    l.quad((3, 5, z), (4, 5, z), (3, 6, z), (2, 6, z), WHITE)

l.quad((1, 3, 0), (2, 3, 0), (2, 3, .5), (1, 3, .5), WHITE, aa=False)
l.quad((2, 3, 0), (4, 5, 0), (4, 5, .5), (2, 3, .5), WHITE, aa=False)
l.quad((4, 5, 0), (3, 6, 0), (3, 6, .5), (4, 5, .5), WHITE, aa=False)
l.quad((3, 6, 0), (2, 6, 0), (2, 6, .5), (3, 6, .5), WHITE, aa=False)
l.quad((2, 6, 0), (3, 5, 0), (3, 5, .5), (2, 6, .5), WHITE, aa=False)
l.quad((3, 5, 0), (1, 3, 0), (1, 3, .5), (3, 5, .5), WHITE, aa=False)

# middle stroke
m = Model()
for z in (0, 0.5):
    m.quad((0, 0, z), (1, 0, z), (7, 6, z), (6, 6, z), WHITE)

m.quad((0, 0, 0), (1, 0, 0), (1, 0, .5), (0, 0, .5), WHITE, aa=False)
m.quad((1, 0, 0), (7, 6, 0), (7, 6, .5), (1, 0, .5), WHITE, aa=False)
m.quad((7, 6, 0), (6, 6, 0), (6, 6, .5), (7, 6, .5), WHITE, aa=False)
m.quad((6, 6, 0), (0, 0, 0), (0, 0, .5), (6, 6, .5), WHITE, aa=False)

# right stroke
r = Model()
for z in (0, 0.5):
    r.quad((2, 0, z), (3, 0, z), (9, 6, z), (8, 6, z), WHITE)
    r.quad((8, 0, z), (9, 0, z), (6, 3, z), (5.5, 2.5, z), WHITE)

r.quad((2, 0, 0), (3, 0, 0), (3, 0, .5), (2, 0, .5), WHITE, aa=False)
r.quad((3, 0, 0), (5.5, 2.5, 0), (5.5, 2.5, .5), (3, 0, .5), WHITE, aa=False)
r.quad((5.5, 2.5, 0), (8, 0, 0), (8, 0, .5), (5.5, 2.5, .5), WHITE, aa=False)
r.quad((8, 0, 0), (9, 0, 0), (9, 0, .5), (8, 0, .5), WHITE, aa=False)
r.quad((9, 0, 0), (6, 3, 0), (6, 3, .5), (9, 0, .5), WHITE, aa=False)
r.quad((6, 3, 0), (9, 6, 0), (9, 6, .5), (6, 3, .5), WHITE, aa=False)
r.quad((9, 6, 0), (8, 6, 0), (8, 6, .5), (9, 6, .5), WHITE, aa=False)
r.quad((8, 6, 0), (2, 0, 0), (2, 0, .5), (8, 6, .5), WHITE, aa=False)

for model in (l, m, r):
    model.scale(50)
    model.translate((25, 100, 0))

for frame in xrange(50):
    offset = 1 - math.sin(frame * math.pi / 100.)
    l2 = Model(l)
    l2.translate(((offset ** 2) * -200, 0, 237.5))
    m2 = Model(m)
    m2.translate((0, 0, 237.5))
    r2 = Model(r)
    r2.translate(((offset ** 2) * 200, 0, 237.5))
    x = Model(l2 + m2 + r2)
    x.rotate((250, 250, 250), (math.pi * offset / 2, 0, 0))
    x.translate((frame * .8 - 50, 0, 0))
    C = CanvasLighting()
    C.import_model(x)
    C.write('ident.%s' % str(frame).zfill(3))
    print frame

gif('ident')
