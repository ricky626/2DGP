import game_framework
import main_state

from My_pico2d import *

name = "StartState"
image = None


def enter():
    global image
    open_canvas(1024, 768)
    hide_lattice();
    image = load_image('res/cir/cir1.png')

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
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(main_state)


