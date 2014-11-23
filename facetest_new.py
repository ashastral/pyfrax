#!/usr/bin/env python
import itertools
import math
import shutil

from pyfrax.canvas import *
from model import *
from common import *

class Canvas3DShaded(Canvas3D):
    def shade(self, p, c):
        return tuple(color * min(500, max(0, 500 - p[2])) / 500 for color in c)

canvas = Canvas3DShaded()
canvas.line((0, 400, 0), (100, 400, 0), (255, 255, 255))
canvas.line((0, 300, 100), (100, 300, 100), (255, 255, 255))
canvas.line((0, 200, 200), (100, 200, 200), (255, 255, 255))
canvas.line((0, 100, 300), (100, 100, 300), (255, 255, 255))
canvas.face(((100, 400, 0), (400, 400, 100), (250, 100, 300)), (255, 255, 255))
canvas.write('facetest_new')
