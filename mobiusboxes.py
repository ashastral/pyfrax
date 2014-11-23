#!/usr/bin/env python
import itertools

from pyfrax import rendertools
from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.colors.gray import *

box = Model()

box.line((0, 0, 0), (0, 0, 1), WHITE)
box.line((0, 0, 0), (0, 1, 0), WHITE)
box.line((0, 0, 0), (1, 0, 0), WHITE)

box.line((1, 1, 1), (1, 1, 0), WHITE)
box.line((1, 1, 1), (1, 0, 1), WHITE)
box.line((1, 1, 1), (0, 1, 1), WHITE)

box.line((1, 0, 0), (1, 0, 1), WHITE)
box.line((1, 0, 0), (1, 1, 0), WHITE)

box.line((0, 1, 0), (1, 1, 0), WHITE)
box.line((0, 1, 0), (0, 1, 1), WHITE)

box.line((0, 0, 1), (1, 0, 1), WHITE)
box.line((0, 0, 1), (0, 1, 1), WHITE)

box.scale(25)

d = {'x': 0, 'y': 0, 'z': 0}

for frame in xrange(48):
    c = Canvas(125, 125, 'gray')

    d['x'] = 37.5 * (math.sin(frame / 16. * math.pi / 2) if frame < 16 else 1.0)
    d['y'] = 37.5 * (0.0 if frame < 16 else (math.sin((frame - 16) / 16. * math.pi / 2) if frame < 32 else 1.0))
    d['z'] = 37.5 * (0.0 if frame < 32 else (math.sin((frame - 32) / 16. * math.pi / 2) if frame < 48 else 1.0))

    for (x, y, z) in itertools.product((-1, 0, 1), repeat=3):
        newbox = Model(box)
        newbox.translate((50 + d['x'] * x, 50 + d['y'] * y, 37.5 + d['z'] * z))
        c.import_model(newbox)

    c.write('mobiusboxes.%s' % str(frame).zfill(2))
    print frame

rendertools.gif('mobiusboxes')
