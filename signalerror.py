#!/usr/bin/env python
import colorsys
import itertools
import math
import random
import subprocess

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import gif
from pyfrax.common import base_dir

class Canvas3DShaded(Canvas):
    
    def shade(self, z, c):
        W = self.image.shape[0]
        return tuple(color * min(W, max(0, W - z)) / W for color in c)

FRAMES = 32
FACES = 16
FRAMES_PER_FACE = 8
ROTATION = .1
SIZE = 250
BORDER = 20

for frame in xrange(FRAMES):
    if frame % FRAMES_PER_FACE == 0:
        abstractshit = Model() 
        for face in xrange(FACES):
            corners = [
                tuple(random.randint(BORDER, SIZE - BORDER) for _ in xrange(3))
                for _ in xrange(3)
            ]
            color = tuple(int(n * 256) for n in colorsys.hsv_to_rgb(random.random(), 1, 1))
            abstractshit.face(*corners + [color])
    abstractshit.rotate((SIZE / 2, SIZE / 2, SIZE / 2), (0, ROTATION, 0))
    canvas = Canvas3DShaded(SIZE, SIZE)
    canvas.import_model(abstractshit)
    canvas.write('abstractshit.%s' % str(frame).zfill(3))
    print str(frame).zfill(3)

for frame in xrange(FRAMES):
    proc = subprocess.Popen(((
        'convert ' + base_dir + 'texture/stripes-250.png -negate -write MPR:mask '
        '+delete ' + base_dir + 'render/abstractshit.%s.png '
        '-mask MPR:mask ' + base_dir + 'render/abstractshit.%s.png '
        '-composite +mask ' + base_dir + 'render/signalerror.%s.png') % (
            str(frame).zfill(3),
            str((frame + 1) % FRAMES).zfill(3),
            str(frame).zfill(3),
        )).split(' '))
    proc.wait()
    print str(frame).zfill(3)

gif('signalerror')
