#!/usr/bin/env python
import itertools, math, random
from pyfrax.canvas import *
from pyfrax.model import *

class CanvasShaded(Canvas):
    def shade(self, p, c):
        return tuple(max(0, min(255, b - int(p[2] / 8))) for b in c)

windows = Model()
for x, y in itertools.product(xrange(5, 50, 15), repeat=2):
    windows.lines([(x, y, 0), (x + 10, y, 0), (x + 10, y + 10, 0), (x, y + 10, 0)], (127,))

buildings = Model()

sides = [(0, 0), (50, 0), (50, 50), (0, 50)]

print "Generating buildings..."
for x, z in itertools.product(xrange(-475, 1000, 100), xrange(25, 500, 100)):
    y = 500
    height = random.randrange(450, 100, -45)
    # Base square
    buildings.lines([(x, y, z), (x + 50, y, z), (x + 50, y, z + 50), (x, y, z + 50)], (255,))
    # "Road"
    buildings.lines([(x - 16, y, z - 16), (x + 66, y, z - 16), (x + 66, y, z + 66), (x - 16, y, z + 66)], (63,))
    # Top square
    buildings.lines([(x, height, z), (x + 50, height, z), (x + 50, height, z + 50), (x, height, z + 50)], (255,))
    # Vertical lines
    for side, (dx, dz) in enumerate(sides):
        buildings.line((x + dx, y, z + dz), (x + dx, height, z + dz), (255,))
        # Windows
        for y_ in xrange(height, y - 5, 45):
            windows_ = Model(windows)
            windows_.translate((x + dx, y_, z + dz))
            windows_.rotate((x + dx, 0, z + dz), (0, math.pi / 2 * side, 0))
            buildings.extend(windows_)
    # Black interior
    interior = Model()
    interior.face((x + 1, y - 1, z + 1), (x + 1, height + 1, z + 1), (x + 49, height + 1, z + 1), (0,))
    interior.face((x + 1, y - 1, z + 1), (x + 49, y - 1, z + 1), (x + 49, height + 1, z + 1), (0,))
    for i in xrange(4):
        buildings.extend(interior)
        if i < 3:
            interior.rotate((x + 25, 0, z + 25), (0, math.pi / 2, 0))

#print "Rotating buildings..."
#buildings.rotate((250, 0, 1000), (0, .075, 0))

print "Writing to canvas..."
canvas = CanvasShaded(500, 500, "gray")
canvas.import_model(buildings)
print "Writing to file..."
canvas.write("city")
