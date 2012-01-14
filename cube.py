#!/usr/bin/env python
import itertools
import pyfrax

class canvas_3d_mod(pyfrax.canvas_3d):
    def shade(self, x, y, z, c):
        return ''.join([chr(int(ord(b) / float(z))) for b in c])

cube = canvas_3d_mod(2000, 2000, 'k')

for corner in itertools.product(range(100, 1800, 300), repeat=2):
    
    for horizontal_edge in (corner[1], corner[1] + 200):
        for depth in (1, 1.2):
            for point_x in xrange(corner[0], corner[0] + 200):
                cube.point(point_x, horizontal_edge, depth, '\xff')

    for vertical_edge in (corner[0], corner[0] + 200):
        for depth in (1, 1.2):
            for point_y in xrange(corner[1], corner[1] + 200):
                cube.point(vertical_edge, point_y, depth, '\xff')

    for side_ud in (corner[1], corner[1] + 200):
        for side_lr in (corner[0], corner[0] + 200):
            for point_z in xrange(1000, 1200):
                cube.point(side_lr, side_ud, point_z / 1000., '\xff')

cube.write("cube.raw")
