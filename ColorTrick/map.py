import game_framework
import random

from My_pico2d import *

name                        = "Map"
map                         = None

class Map:
    hero                    = None
    flag                    = None

    black                   = None
    red                     = None
    yellow                  = None
    green                   = None
    blue                    = None
    purple                  = None
    dot_red                 = None
    dot_yellow              = None
    dot_green               = None
    dot_blue                = None
    dot_purple              = None
    red_on                  = None
    red_off                 = None
    yellow_on               = None
    yellow_off              = None
    green_on                = None
    green_off               = None
    blue_on                 = None
    blue_off                = None
    purple_on               = None
    purple_off              = None


    def __init__(self):
        self.m_nStage       = 1
        self.object         = [[0 for row in range(0, 16)] for col in range(0, 12)]
        self.dot_frames     = 0
        self.name           = "res/Stage/Stage-.txt"
        self.dotTime        = SDL_GetTicks()

        self.LoadMap()

        if(Map.hero == None):
            self.hero       = load_image("res/hero/right_stand.png")
            self.flag       = load_image("res/hero/flag1.png")
            self.black      = load_image("res/block/black.png")
            self.red        = load_image("res/block/red.png")
            self.yellow     = load_image("res/block/yellow.png")
            self.green      = load_image("res/block/green.png")
            self.blue       = load_image("res/block/blue.png")
            self.purple     = load_image("res/block/purple.png")
            self.dot_red    = load_image("res/block/dot_red.png")
            self.dot_yellow = load_image("res/block/dot_yellow.png")
            self.dot_green  = load_image("res/block/dot_green.png")
            self.dot_blue   = load_image("res/block/dot_blue.png")
            self.dot_purple = load_image("res/block/dot_purple.png")

            self.red_on     = load_image("res/switch/red_on.png")
            self.red_off    = load_image("res/switch/red_off.png")
            self.yellow_on  = load_image("res/switch/yellow_on.png")
            self.yellow_off = load_image("res/switch/yellow_off.png")
            self.green_on   = load_image("res/switch/green_on.png")
            self.green_off  = load_image("res/switch/green_off.png")
            self.blue_on    = load_image("res/switch/blue_on.png")
            self.blue_off   = load_image("res/switch/blue_off.png")
            self.purple_on  = load_image("res/switch/purple_on.png")
            self.purple_off = load_image("res/switch/purple_off.png")


            self.objectX    = [[0 for row in range(0, 16)] for col in range(0, 12)]
            self.objectY    = [[0 for row in range(0, 16)] for col in range(0, 12)]

            for i in range(0, 12):
                for j in range(0, 16):
                    self.objectX[i][j] = j * 64
                    self.objectY[i][j] = i * 64

                    if(self.object[i][j] == 7):
                        self.objectX[i][j] += 7
                        self.objectY[i][j] += 10

                    for k in range(9, 14):
                        if(self.object[i][j] == k):
                            #self.objectX[i][j] += 12
                            #self.objectY[i][j] += 64

                            break



        pass

    def LoadMap(self):
        f = open(self.name.replace('-', str(self.m_nStage)), 'r')

        for col in range(0, 12):
	        for row in range(0, 16):
		        self.object[col][row] = int(f.read(3).strip())
        f.close()
        pass

    def update(self):
        if(SDL_GetTicks() - self.dotTime > 200):
            self.dot_frames = (self.dot_frames + 1) % 2
            self.dotTime = SDL_GetTicks()
        pass

    def draw(self):
        for i in range(0, 12):
            for j in range(0, 16):
                if(self.object[i][j] == 1): self.red.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 2): self.yellow.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 3): self.green.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 4): self.blue.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 5): self.purple.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 6): self.black.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 7): self.hero.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 8): self.flag.draw(self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 9): self.dot_red.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 10):self.dot_yellow.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 11):self.dot_green.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 12):self.dot_blue.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                if(self.object[i][j] == 13):self.dot_purple.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])

                if(self.object[i][j] == 14): self.red_off.draw(j * 64 + 12, self.objectY[i][j] + 27)
                if(self.object[i][j] == 15): self.yellow_off.draw(j * 64 + 12, self.objectY[i][j] + 27)
                if(self.object[i][j] == 16): self.green_off.draw(j * 64 + 12, self.objectY[i][j] + 27)
                if(self.object[i][j] == 17): self.blue_off.draw(j * 64 + 12, self.objectY[i][j] + 27)
                if(self.object[i][j] == 18): self.purple_off.draw(j * 64 + 12, self.objectY[i][j] + 27)


        pass