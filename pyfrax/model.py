import gzip
import itertools
import math
try:
    import cPickle as pickle
except ImportError:
    import pickle

from __init__ import *

__all__ = ['Model']

class Model(list):
    def __init__(self, data=None, from_file=None):
        if from_file:
            fh = gzip.GzipFile(base_dir + 'model/%s.model' % from_file, "rb")
            data = pickle.load(fh)
        if not data:
            data = []
        return list.__init__(self, data)
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, list.__repr__(self))
    def _object(self, n, *args, **kwargs):
        self.append((n, args, kwargs))
    def point(self, *args, **kwargs):
        self._object(0, *args, **kwargs)
    def line(self, *args, **kwargs):
        self._object(1, *args, **kwargs)
    def face(self, *args, **kwargs):
        self._object(2, *args, **kwargs)
    def quad(self, *args, **kwargs):
        self._object(3, *args, **kwargs)
    def lines(self, lines, *args, **kwargs):
        for i, line in enumerate(lines):
            self.line(lines[i - 1], lines[i], *args, **kwargs)
    def _rotate_point(self, point, center, amounts):
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
    def _translate_point(self, point, amounts):
        new_point = []
        for axis, amount in zip(point, amounts):
            new_point.append(axis + amount)
        return tuple(new_point)
    def _reflect_point(self, point, axes):
        new_point = []
        for i, axis in enumerate(axes):
            if axis != None:
                new_point.append(2 * axis - point[i])
            else:
                new_point.append(point[i])
        return tuple(new_point)
    def _scale_point(self, point, amount):
        return tuple([axis * amount for axis in point])
    def _map(self, method, *args):
        for i, thing in enumerate(self):
            self[i] = (
                thing[0],
                tuple(method(point, *args) for point in thing[1][:thing[0] + 1]) +
                thing[1][thing[0] + 1:],
                thing[2]
            )
    def rotate(self, center, amounts):
        return self._map(self._rotate_point, center, amounts)
    def translate(self, amounts):
        return self._map(self._translate_point, amounts)
    def reflect(self, axes):
        return self._map(self._reflect_point, axes)
    def scale(self, amount):
        return self._map(self._scale_point, amount)
    def write(self, name):
        fh = gzip.GzipFile(base_dir + 'model/%s.model' % name, "wb")
        pickle.dump(self, fh)
        fh.close()
