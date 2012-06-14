#!/usr/bin/env python
import array, cPickle, gzip, itertools, math, subprocess, time

# TODO:
#       what else can I make? bezier curves? circles?
#       SO INEFFICIENT JESUS DICK
#       alpha channels aren't handled properly in the least yet; putting a transparent pixel in front of a solid one will override the solid pixel
#       merge some of the canvas code!
#       find a better way to handle resolutions - think flood fill algorithm, binary search trees, etc.
# TERMINOLOGY:
#       point: an entity with a three-dimensional position and a color
#       line: a linear set of points such that the entire line segment is filled
#       face: a set of lines arranged in a triangle such that the entire triangle is filled
#       model: a set of points (and eventually lines, faces, etc.) stored as a list
#       canvas: a map of pixels stored in memory as a two-dimensional array with a depth map
#       render: a canvas stored on the disk as a flattened (no depth map) image



def colorspace_to_ps(colorspace):
    return {"rgb": 3, "rgba": 4, "gray": 1}[colorspace]

def gif(name, resize="100%"):
    proc = subprocess.Popen(['convert', '-scale', resize, '-delay', '2.5',
                             '/home/fraxtil/root/pyfrax/render/%s.*.png' % name,
                             '/home/fraxtil/root/pyfrax/gif/%s.gif' % name],
                             stdin=subprocess.PIPE)
    proc.wait()
