import gzip, itertools, math
import cPickle as pickle
from common import *

class model_common:
    def __init__(self, data=None, from_name=None):
        if data is None and from_name is None:
            self.data = []
        elif from_name:
            fh = gzip.GzipFile(base_dir + 'model/%s.model' % from_name, "rb")
            self.data = pickle.load(fh)
        else:
            self.data = data
    def write(self, name):
        fh = gzip.GzipFile(base_dir + 'model/%s.model' % name, "wb")
        pickle.dump(self.data, fh)
        fh.close()
    
class model_2d(model_common):
    def point(self, p, c):
        self.data.append((0, p, c))
    def line(self, start, end, c):
        self.data.append((1, start, end, c))

class model_3d(model_common):
    def point(self, p, c):
        self.data.append((0, p, c))
    def line(self, start, end, c):
        self.data.append((1, start, end, c))
    def lines(self, lines, c):
        for i, line in enumerate(lines):
            self.line(lines[i - 1], line, c)
    def face(self, point1, point2, point3, c):
        self.data.append((2, point1, point2, point3, c))
    def _rotate_point(self, center, amounts, point):
        deltas = list(itertools.imap(lambda x, y: x - y, point, center))
        # WOW this needs some explanation
        # a[0] is the axis we're rotating - 0 for x, 1 for y, or 2 for z.
        # The following indices of 'a' just reference the axes that will need to be manipulated.
        # The formula being used here is really just this:
        # x' = x cos(theta) - y sin(theta); y' = x sin(theta) + y cos(theta)
        # Except serially applied to all three axes.
        for a in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            deltas[a[1]], deltas[a[2]] = (
                deltas[a[1]] * math.cos(amounts[a[0]]) - deltas[a[2]] * math.sin(amounts[a[0]]),
                deltas[a[1]] * math.sin(amounts[a[0]]) + deltas[a[2]] * math.cos(amounts[a[0]])
            )
        return tuple(itertools.imap(lambda x, y: x + y, center, deltas))
    def rotate(self, center, amounts):
        data = []
        for thing in self.data:
            # point
            if thing[0] == 0:
                data.append((0, self._rotate_point(center, amounts, thing[1]), thing[2]))
            # line
            if thing[0] == 1:
                data.append((
                    1,
                    self._rotate_point(center, amounts, thing[1]),
                    self._rotate_point(center, amounts, thing[2]),
                    thing[3]
                ))
            # face
            if thing[0] == 2:
                data.append((
                    2,
                    self._rotate_point(center, amounts, thing[1]),
                    self._rotate_point(center, amounts, thing[2]),
                    self._rotate_point(center, amounts, thing[3]),
                    thing[4]
                ))
        self.data = data
    def _translate_point(self, amounts, point):
        new_point = []
        for axis, amount in zip(point, amounts):
            new_point.append(axis + amount)
        return tuple(new_point)
    def translate(self, amounts):
        data = []
        for thing in self.data:
            # point
            if thing[0] == 0:
                data.append((0, self._translate_point(amounts, thing[1]), thing[2]))
            # line
            if thing[0] == 1:
                data.append((
                    1,
                    self._translate_point(amounts, thing[1]),
                    self._translate_point(amounts, thing[2]),
                    thing[3]
                ))
            # face
            if thing[0] == 2:
                data.append((
                    2,
                    self._translate_point(amounts, thing[1]),
                    self._translate_point(amounts, thing[2]),
                    self._translate_point(amounts, thing[3]),
                    thing[4]
                ))
        self.data = data
