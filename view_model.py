#!/usr/bin/env python
import sys
import pyfrax

class canvas_3d_mod(pyfrax.canvas_3d):
    def shade(self, x, y, z, c):
        return (x, y, z, ''.join([chr(int(ord(b) / (1 + float(z)) ** .1)) for b in c]))

model = pyfrax.model_3d(from_file=sys.argv[1])
x_range, y_range = [v[0] for v in model.points], [v[1] for v in model.points]
x_min, y_min = int(min(x_range)), int(min(y_range))
x_max, y_max = int(max(x_range)), int(max(y_range))
x_off, y_off = (x_max - x_min) / 2 - x_min, (y_max - y_min) / 2 - y_min

canvas = canvas_3d_mod(2 * (x_max - x_min), 2 * (y_max - y_min), "gray")

for point in model.points:
    canvas.point(point[0] + x_off, point[1] + y_off, point[2], '\xff')

canvas.write("/home/fraxtil/root/pyfrax/model/%s.png" % sys.argv[1])
