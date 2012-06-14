import array, itertools, subprocess, time
from common import *

class canvas_common:
    def pixel_at(self, x, y):
        byte_start = (y * self.dim[0] + x) * self.ps
        return str(self.image[byte_start:byte_start + self.ps])
    def line(self, start, end, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        self.point(start, c)
        self._line_builder(start, end, c)
    def lines(self, lines, c):
        for i, line in enumerate(lines):
            self.line(lines[i - 1], line, c)
    def shade(self, p, c):
        return c

class canvas_2d(canvas_common):
    def __init__(self, width, height, colorspace):
        self.color = colorspace
        self.ps = colorspace_to_ps(colorspace)
        self.image = bytearray('\x00' * (width * height * self.ps))
        self.dim = (width, height)
    def point(self, p, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        # out of bounds check
        if not all([0 <= p[n] < self.dim[n] for n in xrange(2)]):
            return
        pixel = int(p[0]) + int(p[1]) * self.dim[0]
        c = self.shade(p, c)
        byte_start = pixel * self.ps
        self.image[byte_start:byte_start + self.ps] = c
    def _line_builder(self, start, end, c):
        if all([-1 <= start[n] - end[n] <= 1 for n in xrange(2)]):
            return
        midpoint = tuple(itertools.imap(lambda a, b: (a + b) / 2, start, end))
        self.point(midpoint, c)
        self._line_builder(start, midpoint, c)
        self._line_builder(midpoint, end, c)
    def face(self, point1, point2, point3, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        self._face_builder((point1, point2, point3), c, 0)
    def import_model(self, model, scale=1):
#        thing_count = 0
#        things = len(model.data)
        for thing in model.data:
#            print "%s / %s" % (thing_count, things)
#            thing_count += 1
            if scale != 1:
                thing = [thing[0]] + [[p * scale for p in t] for t in thing[1:-1]] + [thing[-1]]
            # point
            if thing[0] == 0:
                self.point(thing[1], thing[2])
            # line
            if thing[0] == 1:
                self.line(thing[1], thing[2], thing[3])
            # face
            if thing[0] == 2:
                self.face(thing[1], thing[2], thing[3], thing[4])
    def write(self, name, raw=False, resize="100%"):
        if raw:
            with open(base_dir + 'render/%s.raw' % name, 'wb') as fh:
                fh.write(str(self.image))
            return
        proc = subprocess.Popen(['convert', '-depth', '8', '-resize', resize,
                                 '-size', '%sx%s' % tuple(self.dim), '%s:-' % self.color,
                                 base_dir + 'render/%s.png' % name], stdin=subprocess.PIPE)
        proc.communicate(str(self.image))
        proc.wait()        

class canvas_3d(canvas_common):
    def __init__(self, width, height, colorspace, fast_faces=False, fill=None):
        self.color = colorspace
        # we generally don't care what each channel represents, just how many there are
        self.ps = colorspace_to_ps(colorspace)
        if fill is None:
            fill = '\x00' * self.ps
        elif len(fill) != self.ps:
            raise ValueError("invalid color")
        self.image = bytearray(fill * (width * height))
        self.zbuffer = array.array("f", [float("inf")] * (width * height))
        self.vanishing_point(width / 2, height / 2)
        self.dim = (width, height)
        self.fast_faces = fast_faces
    def background(self, canvas):
        if canvas.ps != self.ps:
            raise ValueError("incompatible byte schemes: %s and %s" % (canvas.ps, self.ps))
        for pixel in xrange(len(canvas.image) / canvas.ps):
            if self.zbuffer[pixel] < float("inf"):
                continue
            byte_start = pixel * canvas.ps
            c = canvas.image[byte_start:byte_start + canvas.ps]
            p = (pixel / canvas.dim[0], pixel % canvas.dim[0])
            byte_start = self.ps * (int(p[0]) + int(p[1]) * self.dim[0])
            self.image[byte_start:byte_start + self.ps] = c
    def vanishing_point(self, x, y):
        self.vp = (x, y)
    def point(self, p, c):
        if len(c) != self.ps:
            raise ValueError("invalid color")
        fp = self.flatten_point(p)
        # out of bounds check
        if not all([0 < fp[n] < self.dim[n] for n in xrange(2)]):
            return
        pixel = int(fp[0]) + int(fp[1]) * self.dim[0]
        if self.zbuffer[pixel] < p[2]:
            return
        c = self.shade(p, c)
        byte_start = pixel * self.ps
        self.image[byte_start:byte_start + self.ps] = c
        self.zbuffer[pixel] = p[2]
    def _line_builder(self, start, end, c):
        start_pixel = self.flatten_point(start)
        end_pixel = self.flatten_point(end)
        if all([-1 <= start[n] - end[n] <= 1 for n in xrange(3)]):
            return
        midpoint = tuple(itertools.imap(lambda a, b: (a + b) / 2, start, end))
        if midpoint in (start, end):
            return
        self.point(midpoint, c)
        self._line_builder(start, midpoint, c)
        self._line_builder(midpoint, end, c)
#    def _face_builder(self, points, c):
#        pixels = [self.flatten_point(point) for point in points]
#        # if the distance between each pair of pixels is less than one:
#        if all([-1 <= pixels[combo[0]][0] - pixels[combo[1]][0] <= 1 and
#                -1 <= pixels[combo[0]][1] - pixels[combo[1]][1] <= 1
#                for combo in itertools.combinations((0, 1, 2), 2)]):
#            return
#        # https://en.wikipedia.org/wiki/Median_(geometry)
#        midpoint = (
#            (points[0][0] + points[1][0]) / 2,
#            (points[0][1] + points[1][1]) / 2,
#            (points[0][2] + points[1][2]) / 2,
#        )
#        if self.flatten_point(midpoint) in pixels:
#            return
#        self.line(points[2], midpoint, c)
#        self._face_builder((points[0], points[2], midpoint), c)
#        self._face_builder((points[1], points[2], midpoint), c)
#        return
    def _face_builder(self, points, c):
        start_pixel = self.flatten_point(points[0])
        end_pixel = self.flatten_point(points[1])
        if -1 <= start_pixel[0] - end_pixel[0] <= 1 and -1 <= start_pixel[1] - end_pixel[1] <= 1:
            return
        midpoint = tuple(itertools.imap(lambda a, b: (a + b) / 2, points[0], points[1]))
        if midpoint in points:
            return
        self.line(midpoint, points[2], c)
        self._face_builder((points[0], midpoint, points[2]), c)
        self._face_builder((midpoint, points[1], points[2]), c)
        return
#    def face(self, point1, point2, point3, c): # bisect the triangle recursively
#        if len(c) != self.ps:
#            raise ValueError("invalid color")
#        clock = time.time()
#        self.line(point1, point2, c)
#        self.line(point1, point3, c)
#        self.line(point2, point3, c)
#        self._face_builder((point1, point2, point3), c)
#        print "%s iterations to draw face" % (time.time() - clock)
    def face(self, point1, point2, point3, c): # draw lines from each point on the triangle to each point on the opposite line
        if len(c) != self.ps:
            raise ValueError("invalid color")
        clock = time.time()
        self._face_builder((point1, point2, point3), c)
        if not self.fast_faces:
            self._face_builder((point2, point3, point1), c)
            self._face_builder((point3, point1, point2), c)
        print "%s seconds to draw face" % (time.time() - clock)
    # optimized version
    def flatten_point(self, p):
        return (self.vp[0] + (p[0] - self.vp[0]) / (1 + float(p[2]) / self.dim[0]),
                self.vp[1] + (p[1] - self.vp[1]) / (1 + float(p[2]) / self.dim[0]))
    # readable version
#    def flatten_point(self, p):
#        distance = (p[0] - self.vp[0], p[1] - self.vp[1])
#        distance = [d / (1 + float(p[2]) / self.dim[0]) for d in distance]
#        return [self.vp[0] + d[0], self.vp[1] + d[1] for vp, d in zip(self.vp, distance)]
    def import_model(self, model, scale=1):
        for thing in model.data:
            if scale != 1:
                thing = [thing[0]] + [[p * scale for p in t] for t in thing[1:-1]] + [thing[-1]]
            # point
            if thing[0] == 0:
                self.point(thing[1], thing[2])
            # line
            if thing[0] == 1:
                self.line(thing[1], thing[2], thing[3])
            # face
            if thing[0] == 2:
                self.face(thing[1], thing[2], thing[3], thing[4])
    def write(self, name, raw=False, resize="100%"):
        if raw:
            with open(base_dir + 'render/%s.raw' % name, 'wb') as fh:
                fh.write(str(self.image))
            return
        proc = subprocess.Popen(['convert', '-depth', '8', '-resize', resize,
                                 '-size', '%sx%s' % tuple(self.dim), '%s:-' % self.color,
                                 base_dir + 'render/%s.png' % name], stdin=subprocess.PIPE)
        proc.communicate(str(self.image))
        proc.wait()
