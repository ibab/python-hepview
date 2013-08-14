
import sys
from time import sleep

import pyglet
from pyglet.gl import *
from pyglet.window import key

from graph import iterate_events

config = Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(800, 600)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

zoom = 1
y_angle = 0
x_angle = 0
evts = iterate_events(sys.argv[1])
evt = next(evts)
time = 0

def draw_vector(v1, v2):
    glBegin(GL_LINES)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glEnd()

def draw_coords():
    glColor4f(1, 0, 0, 0.5)
    glLineWidth(2.0)
    draw_vector((0, 0, 0), (500, 0, 0))
    draw_vector((0, 0, 0), (0, 500, 0))
    draw_vector((0, 0, 0), (0, 0, 500))

def draw_particles(evt):
    for p in evt.edges(data=True):
        glLineWidth(1.5)
        if 2 < p[2]['obj'].momentum().eta() < 5:
            if p[2]['status'] == 1:
                glColor4f(1, 1, 1, 0.6)
            else:
                glColor4f(1, 1, 1, 0.3)
            pid = str(p[2]['obj'].pdg_id())
            if len(pid) > 1 and '5' in pid:
                glLineWidth(3)
                glColor4f(1, 1, 0, 0.8)
        else:
            glColor4f(1, 1, 1, 0.1)
        mom = p[2]['obj'].momentum()
        v1 = p[2]['obj'].production_vertex()
        v2 = p[2]['obj'].end_vertex()
        if not v1:
            v1 = (0, 0, 0)
        else:
            v1 = v1.position()
            v1 = (v1.x(),
                  v1.y(),
                  v1.z())
        if not v2:
            glColor4f(1, 1, 1, 0.2)
            v2 = p[2]['obj'].momentum()
            v2 = (10000 * v2.x(),
                  10000 * v2.y(),
                  10000 * v2.z())
            # TODO: testing
            #v2 = p[2]['obj'].production_vertex().position()
        else:
            v2 = v2.position()
            v2 = (v2.x(),
                  v2.y(),
                  v2.z())
        draw_vector(v1, v2)

@window.event
def on_draw():
    global time, zoom, x_angle, y_angle
    global evt

    window.clear()
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    w = zoom * window.width / 2
    h = zoom * window.height / 2
    glOrtho(-w, w, -h, h, -10000.0, 10000.0)
    glRotatef(x_angle, 1, 0, 0)
    glRotatef(y_angle, 0, 1, 0)

    draw_coords()

    draw_particles(evt)

def callback(dt):
    global time, zoom, x_angle, y_angle
    global evt, evts

    if time < 1000:
        time += 10
    if keys[key.A]:
        zoom /= 1 + dt * 10
    if keys[key.Z]:
        zoom *= 1 + dt * 10
    if zoom < 1e-8:
        zoom = 1e-8

    if keys[key.UP] or keys[key.K]:
        x_angle -= 40 * dt
    if keys[key.DOWN] or keys[key.J]:
        x_angle += 40 * dt
    if keys[key.RIGHT] or keys[key.L]:
        y_angle += 40 * dt
    if keys[key.LEFT] or keys[key.H]:
        y_angle -= 40 * dt
    if keys[key.SPACE]:
        time = 0
        evt = next(evts)

if __name__ == '__main__':
    pyglet.clock.schedule(callback)
    pyglet.clock.set_fps_limit(60)
    pyglet.app.run()

