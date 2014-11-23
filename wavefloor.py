#!/usr/bin/env python
from pyfrax.model import *
from pyfrax.canvas import *
from pyfrax import rendertools
import math

W = 500
H = 500
F = 32

class CanvasLinearShading(Canvas):
    
    def shade(self, z, c):
        M = 1000
        return tuple(color * min(M, max(0, M - z)) / M for color in c)

for frame in xrange(1, F-1): # temporary, already generated other frames
    # build matrix
    matrix = []
    for x in xrange(-1 * W, 2 * W + W / 10, W / 10):
        matrix.append([])
        for z in xrange(-H / 10, H * 2, H / 10):
            y = H - 10 * math.sin((x + z) * 10. / W + frame * 2 * math.pi / F)
            matrix[-1].append((x, y, z))
    # build grid model
    grid = Model()
    for ix, rx in enumerate(matrix):
        for iz, rz in enumerate(rx):
            try:
                grid.line(rz, matrix[ix][iz + 1], (ix * 8, iz * 8, 255))
            except IndexError: pass
            try:
                grid.line(rz, matrix[ix + 1][iz], (ix * 8, iz * 8, 255))
            except IndexError: pass
    # draw to canvas
    canvas = CanvasLinearShading(W, H, 'rgb')
    canvas.import_model(grid)
    canvas.write('wavefloor.%s' % str(frame).zfill(3))
    print "===== %s =====" % str(frame).zfill(3)

rendertools.gif('wavefloor')
