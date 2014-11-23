#!/usr/bin/env python
import math

from pyfrax.model import Model
from pyfrax.canvas import Canvas
from pyfrax import rendertools
from pyfrax.colors.rgb import *

def white(cel):
    return all(r == 255 for r in cel)

tex = rendertools.load_texture('bro.png')
bro = Model()

lines = 0
points = 0

for y, col in enumerate(tex):
    for x, row in enumerate(col):
        if y == len(tex) - 1 and x == len(col) - 1: continue
        if not white(row):
            try:
                if white(tex[y - 1][x]) or white(tex[y + 1][x]) or \
                        white(tex[y][x - 1]) or white(tex[y][x + 1]):
                    lines += 1
                    bro.line((x, y, 0), (x, y, 50), tuple(row))
                else:
                    points += 1
                    bro.point((x, y, 0), tuple(row))
                    #bro.point((x, y, 50), tuple(row))
            except IndexError:
                lines += 1
                bro.line((x, y, 0), (x, y, 50), tuple(row))

bro.translate((15, 15, 10))

step = Model()
step.lines(((0, 50, 0), (0, 0, 0), (50, 0, 0), (50, 0, 250), (0, 0, 250), (0, 50, 250)), GRAY)
step.line((0, 0, 0), (0, 0, 250), GRAY)

stairs = Model(step)

for i in xrange(10):
    step.translate((50, -50, 0))
    stairs.extend(step)

stairs.translate((-100, 450, 50))

FRAMES = 32

for F in xrange(FRAMES):
    bro2 = Model(bro)
    bro2.rotate((95, 95, 125), (0, 0, -F * math.pi * 2 / FRAMES))
    bro2.rotate((95, 95, 125), (math.pi / 8, math.pi / 8, 0))

    stairs2 = Model(stairs)
    stairs2.translate((F * 100. / FRAMES, -F * 100. / FRAMES, 0))
    stairs2.rotate((125, 225, 75), (math.pi / 4, math.pi / 4, 0))

    canvas = Canvas(250, 250, 'rgb', alpha_buffer=16)
    canvas.background(rendertools.load_texture('white.jpg'))
    canvas.import_model(bro2)
    canvas.import_model(stairs2)
    canvas.write('fallingin5d.%s' % str(F).zfill(3))
    print F

rendertools.gif('fallingin5d')
