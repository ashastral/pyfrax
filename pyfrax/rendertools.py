#!/usr/bin/env python
import itertools
import subprocess

import numpy

from canvas import *
from common import base_dir

def gif(name, resize='100%'):
    proc = subprocess.Popen(['convert', '-scale', resize, '-delay', '2.5',
        base_dir + 'render/%s.*.png' % name,
        base_dir + 'gif/%s.gif' % name],
        stdin=subprocess.PIPE)
    # check return code
    if proc.wait():
        print 'error %s' % proc.returncode

def glow(name, radius=10):
    proc = subprocess.Popen(['convert', base_dir + 'render/%s.png' % name,
        '(', '+clone', '-gaussian-blur', str(radius), ')', '-compose',
        'Lighten', '-composite', 'render/glow-%s.png' % name],
        stdin=subprocess.PIPE)
    # check return code
    if proc.wait():
        print 'error %s' % proc.returncode

def info(image):
    proc = subprocess.Popen(['identify', '-format', '%w %h %[colorspace]',
                            base_dir + image],
                            stdout=subprocess.PIPE)
    result = proc.communicate()[0]
    proc.wait()
    return [int(n) for n in result.split(' ')[:2]] + [result.split(' ')[2].rstrip().lower()]

def load_texture(filename):
    image_info = info('texture/' + filename)
    colorspace = image_info[2]
    ps = 3 if colorspace == 'rgb' else 1
    texture = numpy.zeros((image_info[1], image_info[0], ps), dtype='uint8')
    proc = subprocess.Popen(['convert', base_dir + 'texture/' + filename,
                            '%s:-' % colorspace],
                            stdout=subprocess.PIPE)
    image = proc.communicate()[0]
    i = 0
    while i + ps < len(image):
        x = i / ps % image_info[0]
        y = i / ps / image_info[0]
        texture[y][x] = [ord(b) for b in image[i:i + ps]]
        i += ps
    return texture

def color_to_background(render, background, color):
    canvas = render_to_canvas(render, 'rgb')
    bg_canvas = render_to_canvas(background, 'rgb')
    replaced = 0
    for i, j in itertools.product(xrange(canvas.dim[0]), xrange(canvas.dim[1])):
        if canvas.pixel_at(i, j) == color:
            canvas.point((i, j), bg_canvas.pixel_at(i, j))
            replaced += 1
    return canvas
