#!/usr/bin/env python
import math
import random

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import gif
from pyfrax.colors.rgb import *

class CanvasLinearShading(Canvas):
    def shade(self, p, c):
        return tuple(color * min(256, max(0, 256 - p[2])) / 256 for color in c)

blood = []
for b in xrange(64):
    blood.append((b / 2, random.random() * math.pi * 2))
blood_base = Model()
blood_base.face((250, 250, 0), (246, 240, 0), (254, 240, 0), RED)

for frame in xrange(32):
    lines = Model()
    for l in xrange(8):
        center = random.randrange(215, 285)
        width = random.randrange(5, 20)
        d = random.randrange(1, 50)
        top, bottom = center - width / 2, center + width / 2
        lines.quad((-50, top, d), (500 - top, top, d), (500 - bottom, bottom, d), (-50, bottom, d), WHITE)
        lines.quad((550, 500 - top, d), (top, 500 - top, d), (bottom, 500 - bottom, d), (550, 500 - bottom, d), WHITE)

    all_blood = Model()
    for b in blood:
        if -8 < frame - b[0] < 8:
            d = frame - b[0] + 8
        elif frame - b[0] > 24:
            d = frame - b[0] - 24
        elif frame - b[0] < -24:
            d = frame - b[0] + 40
        else:
            continue
        intensity = (8 - abs(8 - d)) / 8.
        blood_model = Model(blood_base)
        blood_model.translate((0, -8 * d, 0))
        blood_model.rotate((250, 250, 0), (0, 0, b[1]))
        all_blood.append(blood_model[0][:-1] + ({'a': intensity, 'aa': False},))
    
    
    canvas = Canvas()
    canvas.import_model(lines)
    canvas.import_model(all_blood)
    canvas.write('stab.%s' % str(frame).zfill(2))

#gif('stab')
