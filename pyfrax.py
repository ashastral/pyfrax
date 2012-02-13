#!/usr/bin/env python
import array, cPickle, gzip, itertools, math, subprocess

class canvas_3d:
    def __init__(self, width, height, color):
        self.color = color
        self.ps = {"rgb": 3, "rgba": 4, "gray": 1}[color]
        self.image = bytearray('\x00' * (width * height * self.ps))
        self.zbuffer = array.array("f", [float("inf")] * (width * height))
        self.vanishing_point(width / 2, height / 2)
        self.dim = (width, height)
    def vanishing_point(self, x, y):
        self.vp = (x, y)
    def point(self, x, y, z, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        fp = self.flatten_point(x, y, z)
        # out of bounds check
        if not all([0 < fp[n] < self.dim[n] for n in xrange(2)]):
            return
        pixel = int(fp[0]) + int(fp[1]) * self.dim[0]
        if self.zbuffer[pixel] < z:
            return
        x, y, z, c = self.shade(x, y, z, c)
        byte_start = pixel * self.ps
        self.image[byte_start:byte_start + self.ps] = c
        self.zbuffer[pixel] = z
    def line(self, start, end, c, res):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        distance = [end[n] - start[n] for n in xrange(3)]
        for offset in xrange(res):
            x, y, z = [start[n] + distance[n] * (offset / float(res)) for n in xrange(3)]
            self.point(x, y, z, c)
#    def flatten_point(self, x, y, z):
#        if z <= 0:
#            raise ValueError("invalid depth")
#        distance = (x - self.vp[0], y - self.vp[1])
#        distance = [d / z for d in distance]
#        return [vp + d for vp, d in zip(self.vp, distance)]
    def flatten_point(self, x, y, z):
        distance = (x - self.vp[0], y - self.vp[1])
        distance = [d / (1 + float(z) / self.dim[0]) for d in distance]
        return [vp + d for vp, d in zip(self.vp, distance)]
    def shade(self, x, y, z, c):
        return (x, y, z, c)
    def write(self, filename, raw=False, resize="100%"):
        if raw:
            with open(filename, 'wb') as fh:
                fh.write(str(self.image))
            return
        proc = subprocess.Popen(['convert', '-depth', '8', '-resize', resize,
                                 '-size', '%sx%s' % tuple(self.dim), '%s:-' % self.color,
                                 'png:' + filename], stdin=subprocess.PIPE)
        proc.communicate(str(self.image))
        proc.wait()        

class model_common:
    def __init__(self, points=None, from_file=None):
        if points is None and from_file is None:
            self.points = []
        elif from_file:
            fh = gzip.GzipFile(from_file, "rb")
            self.points = cPickle.load(fh)
        else:
            self.points = points
    def write(self, filename):
        fh = gzip.GzipFile(filename, "wb")
        cPickle.dump(self.points, fh)
        fh.close()
    
class model_3d(model_common):
    def point(self, x, y, z):
        self.points.append((x, y, z))
    def line(self, start, end, res):
        distance = [end[n] - start[n] for n in xrange(3)]
        for offset in xrange(res):
            x, y, z = [start[n] + distance[n] * (offset / float(res)) for n in xrange(3)]
            self.point(x, y, z)
    def rotate(self, center, amounts):
        points = []
        for point in self.points:
            deltas = list(itertools.imap(lambda x, y: x - y, point, center))
            # WOW this needs some explanation
            # a[0] is the axis we're rotating - 0 for x, 1 for y, or 2 for z.
            # The following indices of 'a' just reference the axes that will need to be manipulated.
            # The formula being used here is really just this:
            # x' = x cos(theta) - y sin(theta); y' = x sin(theta) + y cos(theta)
            # Except serially applied to all three axes.
            for a in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
                deltas[a[1]], deltas[a[2]] = deltas[a[1]] * math.cos(amounts[a[0]]) - deltas[a[2]] * math.sin(amounts[a[0]]), deltas[a[1]] * math.sin(amounts[a[0]]) + deltas[a[2]] * math.cos(amounts[a[0]])
            points.append(tuple(itertools.imap(lambda x, y: x + y, center, deltas)))
        self.points = points

class model_2d(model_common):
    def point(self, x, y):
        self.points.append((x, y))
    def line(self, start, end, res):
        distance = [end[n] - start[n] for n in xrange(2)]
        for offset in xrange(res):
            x, y = [start[n] + distance[n] * (offset / float(res)) for n in xrange(2)]
            self.point(x, y)
