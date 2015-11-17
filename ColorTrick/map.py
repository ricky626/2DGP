import game_framework
import random

from My_pico2d import *

name                        = "Map"
map                         = None

class Map:
    flag = None

    def __init__(self):
        self.m_nStage       = 1
        self.object         = [[0 for row in range(0, 16)] for col in range(0, 12)]
        self.dot_frames     = 0
        self.flag_frames    = 0
        self.name           = "res/Stage/Stage-.txt"
        self.dotTime        = SDL_GetTicks()
        self.flagTime       = SDL_GetTicks()
        self.objectX    = [[0 for row in range(0, 16)] for col in range(0, 12)]
        self.objectY    = [[0 for row in range(0, 16)] for col in range(0, 12)]

        
        if(Map.flag == None):
            #self.hero       = load_image("res/hero/right_stand.png")
            Map.flag       = load_image("res/hero/flag.png")
            Map.black      = load_image("res/block/black.png")
            Map.red        = load_image("res/block/red.png")
            Map.yellow     = load_image("res/block/yellow.png")
            Map.green      = load_image("res/block/green.png")
            Map.blue       = load_image("res/block/blue.png")
            Map.purple     = load_image("res/block/purple.png")
            Map.dot_red    = load_image("res/block/dot_red.png")
            Map.dot_yellow = load_image("res/block/dot_yellow.png")
            Map.dot_green  = load_image("res/block/dot_green.png")
            Map.dot_blue   = load_image("res/block/dot_blue.png")
            Map.dot_purple = load_image("res/block/dot_purple.png")

            Map.red_on     = load_image("res/switch/red_on.png")
            Map.red_off    = load_image("res/switch/red_off.png")
            Map.yellow_on  = load_image("res/switch/yellow_on.png")
            Map.yellow_off = load_image("res/switch/yellow_off.png")
            Map.green_on   = load_image("res/switch/green_on.png")
            Map.green_off  = load_image("res/switch/green_off.png")
            Map.blue_on    = load_image("res/switch/blue_on.png")
            Map.blue_off   = load_image("res/switch/blue_off.png")
            Map.purple_on  = load_image("res/switch/purple_on.png")
            Map.purple_off = load_image("res/switch/purple_off.png")
        self.LoadMap(self.m_nStage)
        self.Init()
        pass

    def Init(self):
        for i in range(0, 12):
            for j in range(0, 16):
                self.objectX[i][j] = j * 64
                self.objectY[i][j] = i * 64

                if(self.object[i][j] == 7):
                    self.objectX[i][j] += 7
                    #self.objectY[i][j] += 10
                    self.HeroX = self.objectX[i][j]
                    self.HeroY = self.objectY[i][j]
                elif(self.object[i][j] == 8):
                    self.EndX = self.objectX[i][j]
                    self.EndY = self.objectY[i][j]
        pass
    def LoadMap(self, m_nStage):
        f = open(self.name.replace('-', str(m_nStage)), 'r')

        for col in range(0, 12):
            for row in range(0, 16):
                self.object[col][row] = int(f.read(3).strip())
        f.close()
        pass

    def update(self):
        pass

    def draw(self):
        for i in range(0, 12):
            for j in range(0, 16):

                if(self.object[i][j] == 1): self.red.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 2): self.yellow.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 3): self.green.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 4): self.blue.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 5): self.purple.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 6): self.black.draw(self.objectX[i][j], self.objectY[i][j])
                #if(self.object[i][j] == 7): self.hero.draw(self.HeroX, self.HeroY)
                elif(self.object[i][j] == 8): self.flag.clip_draw(self.flag_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 9): self.dot_red.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 10):self.dot_yellow.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 11):self.dot_green.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 12):self.dot_blue.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == 13):self.dot_purple.clip_draw(self.dot_frames * 64, 0, 64, 64, self.objectX[i][j], self.objectY[i][j])

                elif(self.object[i][j] == 14): self.red_off.draw(self.objectX[i][j] + 12, self.objectY[i][j] + 28)
                elif(self.object[i][j] == 15): self.yellow_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 16): self.green_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 17): self.blue_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 18): self.purple_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)

                elif(self.object[i][j] == 19): self.red_on.draw(self.objectX[i][j] + 12, self.objectY[i][j] + 28)
                elif(self.object[i][j] == 20): self.yellow_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 21): self.green_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 22): self.blue_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == 23): self.purple_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)


        pass