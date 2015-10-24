import random

from My_pico2d import *

import game_framework
from background import Background
from map import Map



name = "MainState"

hero = None
background = None
map = None
running = True


def enter():
    global background, map
    background = Background()
    map = Map()
    pass

def exit():
    global background, map
    del(map)
    pass

def update():
    background.update()
    map.update()
    delay(0.05)
    pass

def draw():
    clear_canvas()
    background.draw()
    map.draw()
    update_canvas()

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


def main():
    enter()
    while (running):
        handle_events()
        update()
        draw()
        delay(0.05)
    exit()

if __name__ == '__main__':
    main()