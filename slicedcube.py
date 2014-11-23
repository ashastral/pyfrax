#!/usr/bin/env python
import itertools
import math
import shutil

import modeltools
import rendertools
from pyfrax.canvas import *
from model import *
from common import *

class CanvasLinearShading(Canvas):
    def shade(self, p, c):
        return tuple(color * min(500, max(0, 500 - p[2])) / 500 for color in c)

for frame in xrange(32):
    i = 16 * (1 - math.cos(frame / 32. * math.pi))
    corner = model_3d()
    # edges
    corner.line((i, 0, 0), (32, 0, 0), (255,))
    corner.line((0, i, 0), (0, 32, 0), (255,))
    corner.line((0, 0, i), (0, 0, 32), (255,))
    # cut off part of corner
    corner.lines(((i, 0, 0), (0, i, 0), (0, 0, i)), (255,))
    
    corner2 = model_3d(data=corner.data[:])
    corner.reflect((32, None, None))
    corner2.data.extend(corner.data)
    
    corner = model_3d(data=corner2.data[:])
    corner2.reflect((None, 32, None))
    corner.data.extend(corner2.data)

    cube = model_3d(data=corner.data[:])
    corner.reflect((None, None, 32))
    cube.data.extend(corner.data)
    
    cube.data = modeltools.scale(cube.data, .25)
    cube.translate((122, 122, 0))
    canvas = CanvasLinearShading(500, 500, "gray")
    canvas.import_model(cube)
    canvas.write("slicedcube.%s" % str(frame).zfill(2))
    shutil.copy(base_dir + "render/slicedcube.%s.png" % str(frame).zfill(2),
                base_dir + "render/slicedcube.%s.png" % str(95 - frame))
    print frame

for frame in xrange(32, 64):
    i = math.pi / 4 * (1 - math.cos((frame - 32) / 32. * math.pi))
    cube_copy = model_3d(data=cube.data[:])
    cube_copy.rotate((250, 250, 128), (i, 0, 0))
    canvas = CanvasLinearShading(500, 500, "gray")
    canvas.import_model(cube_copy)
    canvas.write("slicedcube.%s" % str(frame).zfill(2))
    print frame

rendertools.gif("slicedcube")
