import itertools
import math
import subprocess
import sys
import time

import numpy

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from __init__ import *

__all__ = ['Canvas']

class Canvas(object):
    def __init__(self, width=500, height=500, colorspace='rgb', alpha_buffer=4):
        self.color = colorspace
        # we generally don't care what each channel represents, just how many there are
        self.ps = 3 if colorspace == 'rgb' else 1
        self.image = numpy.zeros((width, height, alpha_buffer, self.ps + 1), dtype='uint8')
        self.zbuffer = numpy.zeros((width, height, alpha_buffer), dtype='int16')
        self.zbuffer.fill(32767)
        self.bg = numpy.zeros((width, height, self.ps), dtype='uint8')
        self.vp = (width / 2, height / 2)
        self._facelines = set()
        self._already_drawn = None
        self.negative_z = False
    # optimized version
    def flatten_point(self, p):
        return (self.vp[0] + (p[0] - self.vp[0]) / (1 + float(p[2]) / self.image.shape[0]),
                self.vp[1] + (p[1] - self.vp[1]) / (1 + float(p[2]) / self.image.shape[0]))
    # readable version
#    def flatten_point(self, p):
#        distance = (p[0] - self.vp[0], p[1] - self.vp[1])
#        distance = [d / (1 + float(p[2]) / self.image.shape[0]) for d in distance]
#        return (self.vp[0] + distance[0], self.vp[1] + distance[1])
    def shade(self, z, c):
        return c
    def float_to_uint8(self, f):
        return min(255, max(0, int(f * 256)))
    def blend_colors(self, top, bottom):
        # special cases
        if top[-1] == 255 or bottom[-1] == 0:
            return top
        elif top[-1] == 0:
            return bottom
        # alpha blending
        alphas = (top[-1] / 255., bottom[-1] / 255.)
        weights = (alphas[0], (1 - alphas[0]) * alphas[1])
        color_pairs = zip(*(tuple(c[n] * weights[i] / sum(weights)
            for n in xrange(self.ps)) for i, c in enumerate((top, bottom))))
        alpha = bottom[-1] + (255 - bottom[-1]) * top[-1] / 255
        return tuple([int(round(sum(pair))) for pair in color_pairs] + [alpha])
    def pixel(self, z, fp, c, a):
        # out of bounds check
        if not all([0 <= fp[n] < self.image.shape[n] for n in xrange(2)]):
            return
#        if not self.negative_z and z < 0:
#            print 'WARNING: negative Z-index encountered'
#            self.negative_z = True
        # determine where to insert pixel in z-buffer
        zbuf = self.zbuffer[fp[1]][fp[0]]
        pixels = self.image[fp[1]][fp[0]]
        for i, layer in enumerate(zbuf):
            # if the previous pixel we checked was solid, don't bother
            if i and pixels[i - 1][-1] == 255:
                break
            # otherwise, see if it fits
            if z == None or z < layer:
                zbuf[i + 1:] = zbuf[i:-1]
                pixels[-2] = self.blend_colors(pixels[-2], pixels[-1])
                pixels[i + 1:] = pixels[i:-1]
                zbuf[i] = z if z != None else 0
                pixels[i] = self.shade(z, c) + (self.float_to_uint8(a),)
                break
    def point(self, p, c, a=1.0):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        fp = self.flatten_point(p)
        floor = [int(n) for n in fp]
        frac = [n - int(n) for n in fp]
        self.pixel(p[2], (floor[0], floor[1]), c, a * (1 - frac[0]) * (1 - frac[1]))
        self.pixel(p[2], (floor[0], floor[1] + 1), c, a * (1 - frac[0]) * frac[1])
        self.pixel(p[2], (floor[0] + 1, floor[1]), c, a * frac[0] * (1 - frac[1]))
        self.pixel(p[2], (floor[0] + 1, floor[1] + 1), c, a * frac[0] * frac[1])
    # from http://nodedangles.wordpress.com/2010/05/16/measuring-distance-from-a-point-to-a-line-segment/
    def _distancepointline(self, a, b, p):
        LineMag = math.hypot(b[0] - a[0], b[1] - a[1])
        if LineMag < 0.00000001:
            return 9999
        u1 = (((p[0] - a[0]) * (b[0] - a[0])) + ((p[1] - a[1]) * (b[1] - a[1])))
        u = u1 / (LineMag * LineMag)
        if (u < 0.00001) or (u > 1):
            # closest point does not fall within the line segment,
            # take the shorter distance to an endpoint
            ix = math.hypot(a[0] - p[0], a[1] - p[1])
            iy = math.hypot(b[0] - p[0], b[1] - p[1])
            if ix > iy:
                return iy
            else:
                return ix
        else:
            # Intersecting point is on the line, use the formula
            ix = a[0] + u * (b[0] - a[0])
            iy = a[1] + u * (b[1] - a[1])
            return math.hypot(ix - p[0], iy - p[1])    
    def _line_builder(self, start, end, c, a):
        if all([-1 <= start[n] - end[n] <= 1 for n in xrange(3)]):
            return
        midpoint = tuple(itertools.imap(lambda a, b: (a + b) / 2., start, end))
        if midpoint in (start, end):
            return
        for dx, dy in itertools.product(xrange(-2, 3), repeat=2):
            p = [int(n) for n in self.flatten_point(
                (midpoint[0] + dx, midpoint[1] + dy, midpoint[2]))]
            if p in self._already_drawn:
                continue
            d = self._distancepointline(self._line_cap[0], self._line_cap[1], p)
            if d > 1:
                continue
            self.pixel(midpoint[2], p, c, a * (1 - d))
            self._already_drawn.append(p)
        self._line_builder(start, midpoint, c, a)
        self._line_builder(midpoint, end, c, a)
    def line(self, start, end, c, a=1.0):
        if len(c) != self.ps:
            raise ValueError("invalid color %s" % (c,))
        if frozenset((start, end)) in self._facelines:
            #print 'ignoring line already drawn by a face'
            return
        clear_when_done = False
        if self._already_drawn == None:
            clear_when_done = True
            self._already_drawn = []
        self._line_cap = (self.flatten_point(start), self.flatten_point(end))
        self._line_builder(start, end, c, a)
        if clear_when_done:
            self._already_drawn = None
    def lines(self, lines, c, a=1.0):
        for i, line in enumerate(lines):
            self.line(lines[i - 1], line, c)
    # from http://en.wikipedia.org/wiki/Barycentric_coordinates_%28mathematics%29
    def _barycenter(self, a, b, c, p):
        a, b, c = [[float(coord) for coord in coords] for coords in (a, b, c)]
        l1 = (
            ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) /
            ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1]))
        )
        l2 = (
            ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) /
            ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1]))
        )
        return [l1, l2, 1 - l1 - l2]
    def _interpolated(self, a, b, c, bc):
        z_inv = [1.0 / (p[2] + self.image.shape[0]) for p in (a, b, c)]
        z = z_inv[0] + bc[1] * (z_inv[1] - z_inv[0]) + bc[2] * (z_inv[2] - z_inv[0])
        return 1.0 / z - self.image.shape[0]
    def face(self, p1, p2, p3, c, a=1.0, aa=True, shaded=True):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        self._already_drawn = []
        fp = numpy.array([
            [int(round(coord)) for coord in self.flatten_point(p)]
            for p in (p1, p2, p3)
        ])
        for x in xrange(min(fp[...,0]), max(fp[...,0]) + 1):
            for y in xrange(min(fp[...,1]), max(fp[...,1]) + 1):
                # already drawn for this face
                if p in self._already_drawn:
                    continue
                # barycentric coordinates
                try:
                    bc = self._barycenter(fp[0], fp[1], fp[2], (x, y))
                except ZeroDivisionError:
                    return
                # out of the triangle
                if not all(0 <= coord <= 1 for coord in bc):
                    continue
                if shaded:
                    # compensate for Z-indices
                    z = self._interpolated(p1, p2, p3, bc)
                    # actual point = sums of weighted indices of the triangle
                    self.pixel(z, (x, y), c, a)
                # TODO: this doesn't determine whether the pixel is inside of the triangle yet
                else:
                    self.pixel(None, (x, y), c, a)
                self._already_drawn.append((x, y))
        if aa:
            self.lines((p1, p2, p3), c, a)
            self._facelines.update([
                frozenset((p1, p2)),
                frozenset((p2, p3)),
                frozenset((p3, p1))
            ])
        self._already_drawn = None
    def quad(self, p1, p2, p3, p4, c, a=1.0, aa=True, shaded=True):
        self.face(p1, p2, p3, c, a, aa, shaded)
        self.face(p1, p4, p3, c, a, aa, shaded)
    def import_model(self, model, scale=1):
        for i, thing in enumerate(model):
            sys.stdout.write('\r%s / %s' % (i, len(model)))
            sys.stdout.flush()
            if scale != 1:
                thing = [thing[0]] + [[p * scale for p in t] for t in thing[1:-1]] + [thing[-1]]
            # point
            if thing[0] == 0:
                self.point(*thing[1], **thing[2])
            # line
            if thing[0] == 1:
                self.line(*thing[1], **thing[2])
            # face
            if thing[0] == 2:
                self.face(*thing[1], **thing[2])
            # quad
            if thing[0] == 3:
                self.quad(*thing[1], **thing[2])
        sys.stdout.write('\n')
    def background(self, texture):
            self.bg = texture
    def write(self, name, raw=False, resize='100%'):
        # Flatten image
        t = time.time()
        optimal = 0
        flat = StringIO()
        for ix, x in enumerate(self.image):
            for iy, y in enumerate(x):
                # nothing on this pixel?
                if not numpy.any(y[..., -1]):
                    flat.write(''.join([chr(bg) for bg in self.bg[ix][iy]]))
                    continue
                color = [int(bgc) for bgc in self.bg[ix][iy]]
                for z in reversed(y):
                    # nothing in this slot?
                    if not z[-1]:
                        optimal += 1
                        continue
                    # 'cc' is a color component
                    for i, cc in enumerate(z[:-1]):
                        color[i] = int(color[i] + (cc - color[i]) * z[-1] / 255.)
                flat.write(''.join(chr(min(255, max(0, c))) for c in color))
        print time.time() - t
        if raw:
            with open(base_dir + 'render/%s.raw' % name, 'wb') as fh:
                fh.write(flat.getvalue())
            return
        proc = subprocess.Popen(
            ['convert', '-depth', '8', '-resize', resize, '-size',
            '%sx%s' % self.image.shape[:2], '%s:-' % self.color,
            base_dir + 'render/%s.png' % name], stdin=subprocess.PIPE)
        proc.communicate(flat.getvalue())
        proc.wait()
