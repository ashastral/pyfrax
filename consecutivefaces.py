#!/usr/bin/env python
from pyfrax.canvas import Canvas
from pyfrax.colors.rgb import *

class CanvasLinearShading(Canvas):
    def shade(self, p, c):
        return tuple(color * min(500, max(0, 500 - p[2])) / 500 for color in c)
#    def flatten_point(self, p):
#        distance = (p[0] - self.vp[0], p[1] - self.vp[1])
#        distance = [d * (500 - float(p[2])) / 500 for d in distance]
#        return (self.vp[0] + distance[0], self.vp[1] + distance[1])

c = CanvasLinearShading()

#c.face((29, 225, 101), (29, 201, 107), (329, 274, 398), WHITE)
#c.face((-21, 201, 107), (279, 274, 398), (329, 274, 398), GRAY)
#c.line((329, 274, 410), (-21, 201, 107), LIGHTGRAY)

#c.quad((100, 200, 0), (100, 300, 0), (400, 300, 500), (400, 200, 500), WHITE)
#c.quad((100, 100, 250), (100, 300, 250), (300, 300, 250), (300, 100, 250), WHITE)

c.face((100, 100, 0), (100, 400, 0), (400, 250, 32767), WHITE)
c.face((400, 100, 0), (400, 400, 0), (400, 250, 1024), WHITE)
#c.face((200, 300, 100), (300, 300, 100), (250, 400, 100), WHITE)

c.write('test_rect')
