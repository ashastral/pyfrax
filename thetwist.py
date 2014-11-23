#!/usr/bin/env python
import math
import random

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

FRAMES = 32
WIDTH = 500
HEIGHT = 500
SECTIONS = 12
RADIUS = 40
TWISTS = 2
PADDING = 2

def xyz(s, l, scale):
    f = float(frame) / FRAMES
    theta = l + float(s * TWISTS) / SECTIONS - f / 3
    theta *= math.pi / 2
    pulse = math.sin(float(s * TWISTS) / SECTIONS + f * math.pi * 2)
    return ((float(s) - float(frame * 2) / FRAMES) * WIDTH / SECTIONS,
            HEIGHT / 2 + RADIUS * math.sin(theta) * pulse * scale,
            RADIUS + RADIUS * math.cos(theta) * pulse * scale)

for frame in xrange(FRAMES):
    tube = Model()

    for s in xrange(-PADDING, SECTIONS + 1 + PADDING):
        for l in xrange(4):
            tube.line(xyz(s, l, 1), xyz(s + 1, l, 1), AQUA)
            tube.line(xyz(s, l, 1.5), xyz(s, l + 1, 1.5), (0, 128, 255))

    tube.rotate((WIDTH / 2, HEIGHT / 2, 0), (0, 0, -math.pi / 12))

    canvas = Canvas(WIDTH, HEIGHT)
    canvas.import_model(tube)
    canvas.write('thetwist.%s' % str(frame).zfill(3))
    print frame

gif('thetwist')
