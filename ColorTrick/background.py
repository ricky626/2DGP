import game_framework

from pico2d import *

name = "StartState"
image = None

class Background:
    pass
def enter():
    global image
    open_canvas(1024, 768)
    hide_lattice();
    image = load_image('res/background.png')

def exit():
    global image
    del(image)

def update():

    delay(0.01)


def draw():
    global image
    clear_canvas()
    image.draw(512, 384)
    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass

def handle_events():
    pass

