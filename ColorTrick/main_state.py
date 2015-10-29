import random

from My_pico2d import *

import game_framework
from background import Background
from map import Map
from hero import Hero



name        = "MainState"

hero        = None
background  = None
map         = None


def enter():
    global background, map, hero

    background          = Background()
    map                 = Map()
  #  hero                = Hero()
    pass

def exit():
    global background, map, hero

    del(background)
    del(map)
#    del(hero)
    pass

def update():
    background.update()
    map.update()
    delay(0.015)
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
    while (1):
        handle_events()
        update()
        draw()
        delay(0.05)
    exit()

if __name__ == '__main__':
    main()