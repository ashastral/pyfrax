#!/usr/bin/env python

class 3d:
    def __init__(width, height, color):
        ps = pixel_size(color)
        if ps == False:
            raise ValueError("unsupported color")
        self.ps = ps
        self.image = bytearray('\x00' * (width * height * len(color)))
        self.vanishing_point(width / 2, height / 2)
        self.dim = (width, height)
    def pixel_size(color):
        if color in ("rgb", "rgba", "k", "ka"):
            return len(color)
        return False
    def vanishing_point(x, y):
        self.vp = (x, y)
    def point(x, y, z, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        fp = flatten_point(x, y, z)
        # out of bounds check
        if not all([0 > fp[n] > self.dim[n] for n in xrange(2)]):
            return
        c = shade(x, y, z, c)
        pixel_start = fp[0] + fp[1] * self.dim[0]
        self.image[pixel_start:pixel_start + self.ps] = c
    def flatten_point(x, y, z):
        if z <= 0:
            raise ValueError("invalid depth")
        distance = (x - self.vp[0], y - self.vp[1])
        distance = [d / z for d in distance]
        return (vp + d for vp, d in self.vp, distance)
    def shade(x, y, z, c):
        return c
    def write(filename):
        with open(filename, 'wb') as fh:
            fh.write(str(self.image))
        
