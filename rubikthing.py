#!/usr/bin/env python
from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.colors.rgb import *

cube = Model()
# front
cube.quad((0, 0, 0), (0, 100, 0), (100, 100, 0), (100, 0, 0), WHITE, aa=False, shaded=False)
# back
cube.quad((0, 0, 100), (0, 100, 100), (100, 100, 100), (100, 0, 100), WHITE, aa=False, shaded=False)
# left
cube.quad((0, 0, 0), (0, 0, 100), (0, 100, 100), (0, 100, 0), WHITE, aa=False, shaded=False)
# right
cube.quad((100, 0, 0), (100, 0, 100), (100, 100, 100), (100, 100, 0), WHITE, aa=False, shaded=False)
# top
cube.quad((0, 0, 0), (100, 0, 0), (100, 0, 100), (0, 0, 100), WHITE, aa=False, shaded=False)
# bottom
cube.quad((0, 100, 0), (100, 100, 0), (100, 100, 100), (0, 100, 100), WHITE, aa=False, shaded=False)

frames = 64

for frame in xrange(64):
    cubes = Model()
    for corner in itertools.product((0, 100), repeat=3):
        corner_cube = Model(cube)
        corner_cube.translate(corner)
        if frame < frames / 2:
            f = frame
            corner_cube.rotate((100, 100, 100), (0, math.pi / 2 * math.sin(math.pi * (f - 16) / 32) * ((50 - corner[1]) / 50.), 0))
        else:
            f = frame - 32
            corner_cube.rotate((100, 100, 100), (math.pi / 2 * math.sin(math.pi * (f - 16) / 32) * ((50 - corner[0]) / 50.), 0, 0))
        cubes.extend(corner_cube)
    cubes.translate((150, 150, 50))
    c = Canvas()
    c.vp = (250 + 100 * math.sin(math.pi * 2 * frame / frames), 250 + 100 * math.cos(math.pi * 2 * frame / frames))
    c.import_model(cubes)
    c.write('rubikthing.%s' % str(frame).zfill(3))
    print frame
