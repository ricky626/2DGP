import random
import json
import os

from pico2d import *

import game_framework


name = "MainState"

map = None

class Map:
    hero = None
    flag = None

    black = None
    red = None
    yellow = None
    green = None
    blue = None
    purple = None
    dot_red = None
    dot_yellow = None
    dot_green = None
    dot_blue = None
    dot_purple = None


    def LoadMap(self):

        f = open(self.name.replace('-', str(self.m_nStage)), 'r')

        for col in range(0, 12):
	        for row in range(0, 16):
		        self.object[col][row] = int(f.read(3).strip())
        f.close()

        pass

    def __init__(self):
        self.m_nStage = 1
        self.object = [[0 for row in range(0, 16)] for col in range(0, 12)]
        self.name = "res/Stage/Stage-.txt"
        self.dot_frames = 0
        if(Map.hero == None):
            self.hero = load_image("res/hero/right_stand.png")
            self.flag = load_image("res/hero/flag1.png")
            self.black = load_image("res/block/black.png")
            self.red = load_image("res/block/red.png")
            self.yellow = load_image("res/block/yellow.png")
            self.green = load_image("res/block/green.png")
            self.blue = load_image("res/block/blue.png")
            self.purple = load_image("res/block/purple.png")
            self.dot_red = load_image("res/block/dot_red.png")
            self.dot_yellow = load_image("res/block/dot_yellow.png")
            self.dot_green = load_image("res/block/dot_green.png")
            self.dot_blue = load_image("res/block/dot_blue.png")
            self.dot_purple = load_image("res/block/dot_purple.png")

        self.LoadMap()
        pass

    def update(self):
        self.dot_frames = (self.dot_frames + 1) % 2
        delay(0.3)
        pass

    def draw(self):

        for i in range(0, 12):
            for j in range(0, 16):

                if(self.object[i][j] == 1): self.red.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 2): self.yellow.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 3): self.green.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 4): self.blue.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 5): self.purple.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 6): self.black.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 7): self.hero.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 8): self.flag.draw(j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 9): self.dot_red.clip_draw(self.dot_frames * 64, 0, 64, 64, j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 10):self.dot_yellow.clip_draw(self.dot_frames * 64, 0, 64, 64, j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 11):self.dot_green.clip_draw(self.dot_frames * 64, 0, 64, 64, j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 12):self.dot_blue.clip_draw(self.dot_frames * 64, 0, 64, 64, j * 64 + 32, i * 64 + 32)
                if(self.object[i][j] == 13):self.dot_purple.clip_draw(self.dot_frames * 64, 0, 64, 64, j * 64 + 32, i * 64 + 32)
        pass

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


running = True

def enter():
    global map
    map = Map()

    pass

def exit():
    global map
    del(map)

    pass

def update():
    global map
    map.update()
    delay(0.05)
    pass

def draw():
    global map
    clear_canvas()
    map.draw()
    update_canvas()

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