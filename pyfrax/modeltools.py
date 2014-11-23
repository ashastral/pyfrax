#!/usr/bin/env python
import math, random

def simplify(points, degree):
    if type(degree) is not int:
        raise TypeError("degree must be an integer")
    new_points = set()
    for point in points:
        new_point = []
        for axis in point:
            new_point.append(int(axis) / degree * degree)
        new_points.add(tuple(new_point))
    return list(new_points)

def scale(data, degree):
    new_data = []
    for thing in data:
        new_thing = [thing[0]]
        for p in xrange(1, thing[0] + 2):
            new_thing.append(tuple([thing[p][n] / degree for n in xrange(3)]))
        new_data.append(tuple(new_thing + [thing[-1]]))
    return new_data

def fuzz(points, distances, triangular_power=False):
    new_points = []
    for point in points:
        new_point = []
        for axis, distance in zip(point, distances):
            if distance <= 0:
                new_point.append(axis)
                break
            if triangular_power is not False:
                offset = (random.triangular(0, distance) ** triangular_power / ((distance / 2) ** (triangular_power - 1))) - distance / 2
            else:
                offset = random.random() * distance - distance / 2
            new_point.append(axis + offset)
        new_points.append(tuple(new_point))
    return new_points

def sinusodial_rotation(position, angle):
    return (1 - math.cos(math.pi * position)) * angle / 2
