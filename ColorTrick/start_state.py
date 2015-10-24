import game_framework
import main_state

from My_pico2d import *
from background import Background

name = "StartState"
image = None
frames = 0
Timer = SDL_GetTicks()

def enter():
    global image
    global background
    open_canvas(1024, 768)
    hide_lattice()

    background = Background()
    image = load_image('res/menu/colortrick.png')

def exit():
    global background
    global image
    del(background)
    del(image)

def update():
    global frames
    global Timer
    if(SDL_GetTicks() - Timer > 200):
            frames = (frames + 1) % 2
            Timer = SDL_GetTicks()
    background.update()


def draw():
    global image
    clear_canvas()
    background.draw()
    image.clip_draw(frames * 716, 0, 716, 303, 150, 75)
    update_canvas()
    delay(0.025)

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


