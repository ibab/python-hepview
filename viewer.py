
from hepmc import *
import pyglet
from pyglet.gl import *
from pyglet.window import key
import sys

config = Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(800, 600)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

zoom = 1
y_angle = 0
x_angle = 0
vecs = []
marker = []
reader = IO_GenEvent(sys.argv[1], 'r')
time = 0
    
def load_event(fpath):
    reader = IO_GenEvent(fpath, 'r')
    evt = reader.get_next_event()
    return evt.fsParticles()

def draw_vector(vec, scale=1):
    v = (scale * vec[0],
         scale * vec[1],
         scale * vec[2])
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(*v)
    glEnd()

def rapidity(p):
    z = p.momentum().z()
    e = p.momentum().e()
    try:
        eta = 0.5 * (log(e + z) - log(e - z + 1e-20))
    except:
        eta = 10000000
    return eta

def draw_coords():
    draw_vector((500, 0, 0))
    draw_vector((0, 500, 0))
    draw_vector((0, 0, 500))

@window.event
def on_draw():
    global zoom, x_angle, y_angle, time
    window.clear()
    glClearColor(0.0, 0.0, 0.1, 1.0);
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

    glColor3f(1, 0, 0)
    glLineWidth(3.0)
    draw_coords()

    glLineWidth(1.5)
    for v, m in zip(vecs, marker):
        if m:
            glColor4f(0, 1, 1, 0.8)
        else:
            glColor4f(1, 1, 1, 0.5)
        draw_vector(v, scale=time)

def callback(dt):
    global zoom, x_angle, y_angle, reader, time
    if time < 1000:
        time += 10
    if keys[key.A]:
        zoom /= 1 + dt
    if keys[key.Z]:
        zoom *= 1 + dt
    if zoom < 0.0001:
        zoom = 0.0001

    if keys[key.UP] or keys[key.K]:
        x_angle -= 40 * dt
    if keys[key.DOWN] or keys[key.J]:
        x_angle += 40 * dt
    if keys[key.RIGHT] or keys[key.L]:
        y_angle += 40 * dt
    if keys[key.LEFT] or keys[key.H]:
        y_angle -= 40 * dt
    if keys[key.SPACE]:
        next_event()

def next_event():
    global vecs, reader, time
    vecs = []
    time = 0
    evt = reader.get_next_event()
    ps =  evt.fsParticles()
    for p in ps:
        #if p.status() == 1:
            vecs.append((p.momentum().x(),
                         p.momentum().y(),
                         p.momentum().z()))
            if str(p.pdg_id()) == '5' or str(p.pdg_id()) == '-5':
                marker.append(True)
                print('found')
            else:
                marker.append(False)

def main():
    next_event()
    pyglet.clock.schedule_interval(callback, 0.02)
    pyglet.app.run()

if __name__ == '__main__':
    main()

