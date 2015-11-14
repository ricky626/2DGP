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
    hero                = Hero()
    pass

def exit():
    global background, map, hero

    del(background)
    del(map)
    del(hero)
    pass

def update(frame_time):
    background.update(frame_time)
    hero.update(frame_time)
    map.update(frame_time)
    #delay(0.014)
    pass

def draw(frame_time):
    clear_canvas()
    background.draw(frame_time)
    #map.draw()
    hero.draw(frame_time)

    update_canvas()

def handle_events(frame_time):
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        hero.handle_events(event, frame_time)

