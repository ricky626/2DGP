import game_framework
import main_state

from My_pico2d import *
from background import Background

name = "StartState"
image = None
bgm = None
frames = 0
Timer = SDL_GetTicks()

def enter():
    global background, image, bgm
    open_canvas(1024, 768)
    hide_lattice()

    background = Background()
    image = load_image('res/menu/colortrick.png')
    bgm = load_music('res/sound/menu.wav')
    bgm.set_volume(64)
    bgm.repeat_play()

def exit():
    global background, image, bgm
    del(background)
    del(image)
    del(bgm)

def update():
    global frames
    global Timer
    if(SDL_GetTicks() - Timer > 200):
            frames = (frames + 1) % 2
            Timer = SDL_GetTicks()
    background.update()
    #delay(0.015)

def draw():
    global image
    clear_canvas()
    background.draw()
    image.clip_draw(frames * 716, 0, 716, 303, 150, 75)
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

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) or (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN) :
            game_framework.change_state(main_state)


