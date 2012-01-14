#!/usr/bin/env python

class canvas_3d:
    def __init__(self, width, height, color):
        ps = self.pixel_size(color)
        if ps == False:
            raise ValueError("unsupported color")
        self.ps = ps
        self.image = bytearray('\x00' * (width * height * len(color)))
        self.vanishing_point(width / 2, height / 2)
        self.dim = (width, height)
    def pixel_size(self, color):
        if color in ("rgb", "rgba", "k", "ka"):
            return len(color)
        return False
    def vanishing_point(self, x, y):
        self.vp = (x, y)
    def point(self, x, y, z, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        fp = self.flatten_point(x, y, z)
        # out of bounds check
        if not all([0 < fp[n] < self.dim[n] for n in xrange(2)]):
            return
        c = self.shade(x, y, z, c)
        pixel_start = int(fp[0]) + int(fp[1]) * self.dim[0]
        self.image[pixel_start:pixel_start + self.ps] = c
    def line(self, start, end, c, res):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        distance = [end[n] - start[n] for n in xrange(3)]
        for offset in xrange(res):
            x, y, z = [start[n] + distance[n] * (offset / float(res)) for n in xrange(3)]
            self.point(x, y, z, c)
    def flatten_point(self, x, y, z):
        if z <= 0:
            raise ValueError("invalid depth")
        distance = (x - self.vp[0], y - self.vp[1])
        distance = [d / z for d in distance]
        return [vp + d for vp, d in zip(self.vp, distance)]
    def shade(self, x, y, z, c):
        return c
    def write(self, filename):
        with open(filename, 'wb') as fh:
            fh.write(str(self.image))
        
