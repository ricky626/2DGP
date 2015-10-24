import game_framework
import random

from My_pico2d import *

name = "Hero"

class Hero:

    def __init__(self):
        self.ScreenSizeX = 2048
        self.ScreenSizeY = 1536

        self.Polygon_rectX   = [0 for i in range(0, 5)]
        self.Polygon_rectY   = [0 for i in range(0, 5)]

        self.Polygon_faX     = [0 for i in range(0, 5)]
        self.Polygon_faY     = [0 for i in range(0, 5)]

        self.Polygon_yutX    = [0 for i in range(0, 5)]
        self.Polygon_yutY    = [0 for i in range(0, 5)]

        self.Polygon_cirX    = [0 for i in range(0, 5)]
        self.Polygon_cirY    = [0 for i in range(0, 5)]

        self.Polygon_trX     = [0 for i in range(0, 5)]
        self.Polygon_trY     = [0 for i in range(0, 5)]


        self.moveX          = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.moveY          = [[0 for j in range(0, 5)] for i in range(0, 5)]

        for i in range(0, 5):
            for j in range(0, 5):
                self.moveX[i][j], self.moveY[i][j] = random.randint(1, 3), random.randint(1, 3)


        if(self.background == None):
            self.background = load_image("res/background.png")
        pass

    def update(self):
        pass

    def draw(self):
        self.background.draw(0, 0)
        pass
    pass

def enter():
    global background
    background = Background()
    pass

def exit():
    global background
    del(background)
    pass

def update():
    pass

def draw():
    clear_canvas()
    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass

def handle_events():
    pass

