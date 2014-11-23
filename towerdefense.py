#!/usr/bin/env python
import math
import random

from pyfrax.canvas import *
from pyfrax.model import *
from pyfrax.rendertools import *
from pyfrax.colors.rgb import *

WIDTH = 500
HEIGHT = 500
FRAMES = 32
MISSILES = 4
SPEED = 10
MAX_EXPLOSION = 16

ATTACKER = (WIDTH * .8, HEIGHT * .2, 0)
DEFENDER = (WIDTH * .2, HEIGHT * .8, 0)

missile = Model()
missile.lines(((0, 0, 0), (0, 1, 0), (0, 1, -1), (0, 0, -1), (0, 0, 0)), GRAY)
missile.line((0, 0, 0), (4, 0, 0), GRAY)
missile.line((0, 1, 0), (4, 1, 0), GRAY)
missile.line((0, 1, -1), (4, 1, -1), GRAY)
missile.line((0, 0, -1), (4, 0, -1), GRAY)
missile.lines(((5, 0, 0), (5, 1, 0), (5, 1, -1), (5, 0, -1), (5, 0, 0)), ORANGE)

missile.translate((-2., -.5, .5))
missile.scale(WIDTH / 125)

def get_explosion(color):
    explosion = Model()
    explosion.lines(((0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0)), color)
    explosion.lines(((0, -1, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0)), color)
    explosion.lines(((1, 0, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1), (1, 0, 0)), color)
    explosion.scale(WIDTH / 250)
    return explosion

def get_base(color):
    base = Model()
    base.lines(((-1, -1, -0.5), (-1, 1, -0.5), (1, 1, -0.5), (1, -1, -0.5), (-1, -1, -0.5)), color)
    base.lines(((-2, -2, 0), (-2, 2, 0), (2, 2, 0), (2, -2, 0), (-2, -2, 0)), color)
    base.line((-1, -1, -0.5), (-2, -2, 0), color)
    base.line((-1, 1, -0.5), (-2, 2, 0), color)
    base.line((1, 1, -0.5), (2, 2, 0), color)
    base.line((1, -1, -0.5), (2, -2, 0), color)
    base.scale(WIDTH / 20)
    return base

GRIDLINES = 10
grid = Model()
for i in xrange(GRIDLINES + 1):
    grid.point((0, HEIGHT / GRIDLINES * i, 0), WHITE)
    grid.point((WIDTH - 1, HEIGHT / GRIDLINES * i, 0), WHITE)
    grid.point((WIDTH / GRIDLINES * i, 0, 0), WHITE)
    grid.point((WIDTH / GRIDLINES * i, HEIGHT - 1, 0), WHITE)

for i, b in enumerate((ATTACKER, DEFENDER)):
    this_base = get_base((RED, BLUE)[i])
    this_base.translate(b)
    grid.extend(this_base)

missiles = [{'angle': (-math.pi / 4, math.pi / 8, -math.pi / 8, math.pi / 4)[m],
          # initial position is no longer used
          'position': ATTACKER,
          'real_position': ATTACKER,
          'exp_intensity': 0,
          'exp_position': None,
         } for m in xrange(MISSILES)]

trails = []

print "Precomputing negative frames"

for frame in xrange(-FRAMES, FRAMES):
    # XXX duplicated code on the following lines
    last_f = float((frame - 1) % FRAMES) / FRAMES + 0.0001
    f = float(frame) / FRAMES + 0.00001
    everything = Model(grid)

    for t in trails:
        everything.line(t[0], t[1], (t[2] * 15, 0, 0))
        t[2] -= 1
        if t[2] == 0:
            trails.remove(t)
    
    for i, m in enumerate(missiles):
        last_mf, mf = (
            ((_f + float(i) / MISSILES) % 1) * .8
            for _f in (last_f, f)
        )
        this_missile = Model(missile)
        # Get motion vector
        new_position = [a + (d - a) * mf for a, d in zip(ATTACKER, DEFENDER)]
        new_position[2] -= math.sin(mf * math.pi) * WIDTH / 4
        v = [a - b for a, b in zip(new_position, m['position'])]
        # Rotate and translate accordingly
        this_missile.rotate(
            (0, 0, 0),
            [0., -math.atan2(v[2], v[1]), -math.pi + math.atan2(v[1], v[0])]
        )
        this_missile.translate(new_position)
        this_missile.rotate(
            (new_position[0], new_position[1], 0),
            (m['angle'], m['angle'], 0)
        )
        # Used to calculate missile position
        dummy_point = Model()
        dummy_point.point(m['position'])
        # XXX duplicated code (see above: this_missile.rotate)
        dummy_point.rotate(
            (m['position'][0], m['position'][1], 0),
            (m['angle'], m['angle'], 0)
        )
        real_position = dummy_point[0][1][0]
        # Explosions!
        if mf < last_mf:
            m['exp_position'] = real_position
            m['exp_intensity'] = MAX_EXPLOSION
            everything.line(DEFENDER, m['exp_position'], YELLOW)
            this_missile = Model()
        # Don't draw the missile or its trail if it's exploding / resetting
        else:
            trails.append([real_position, m['real_position'], 8])
        # More explosion logic
        if m['exp_intensity']:
            this_explosion = get_explosion((
                int(float(m['exp_intensity']) / MAX_EXPLOSION * 255),
                int(float(m['exp_intensity']) / MAX_EXPLOSION * 255),
                0
            ))
            this_explosion.scale(MAX_EXPLOSION - m['exp_intensity'] + 1)
            this_explosion.rotate(
                (0, 0, 0),
                (0, math.pi * m['exp_intensity'] / MAX_EXPLOSION, 0)
            )
            this_explosion.translate(m['exp_position'])
            everything.extend(this_explosion)
        # Add to 'everything'
        everything.extend(this_missile)
        # Update position
        m['position'] = new_position
        m['real_position'] = real_position
        if m['exp_intensity']: m['exp_intensity'] -= 1

    if frame < 0: continue

    everything.rotate((WIDTH / 2, HEIGHT / 2, 0), (-math.pi / 4, 0, 0))
    everything.translate((0, -WIDTH / 10, WIDTH / 2))

    canvas = Canvas(WIDTH, HEIGHT, 'rgb')
    canvas.import_model(everything)
    canvas.write('missile.%s' % str(frame).zfill(3))
    print frame

gif('missile')
