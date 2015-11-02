import game_framework
import random

from My_pico2d import *

name                                = "Background"


class Background:
    background                      = None
    Polygon                         = [[None for j in range(0, 5)] for i in range(0, 5)]

    def __init__(self):

        self.ScreenSizeX            = 1024
        self.ScreenSizeY            = 768
        self.rect                   = "res/rect/rect-.png"
        self.tr                     = "res/tr/tr-.png"
        self.cir                    = "res/cir/cir-.png"
        self.fa                     = "res/fa/fa-.png"
        self.yut                    = "res/yut/yut-.png"

        self.rotateTime             = SDL_GetTicks()
        self.moveTime               = SDL_GetTicks()
        self.PolygonDegree          = 0
        self.PolygonX               = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.PolygonY               = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.moveX                  = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.moveY                  = [[0 for j in range(0, 5)] for i in range(0, 5)]

        for i in range(0, 5):
            for j in range(0, 5):
                #self.PolygonX[i][j], self.PolygonY[i][j]    = random.randint(-self.ScreenSizeX/2, self.ScreenSizeX + 500), random.randint(-self.ScreenSizeY/2, self.ScreenSizeY + 500)
                self.PolygonX[i][j], self.PolygonY[i][j]    = self.ScreenSizeX/2-160, self.ScreenSizeY/2-130
                self.moveX[i][j], self.moveY[i][j]          = random.randint(-7, 7), random.randint(-7, 7)


        if(Background.background == None):
            self.background       = load_image("res/background.png")

            for i in range(0, 5):
               self.Polygon[0][i] = load_image(self.rect.replace('-', str(i+1)))
               self.Polygon[1][i] = load_image(self.tr.replace('-', str(i+1)))
               self.Polygon[2][i] = load_image(self.cir.replace('-', str(i+1)))
               self.Polygon[3][i] = load_image(self.fa.replace('-', str(i+1)))
               self.Polygon[4][i] = load_image(self.yut.replace('-', str(i+1)))

        pass

    def update(self):
        if(SDL_GetTicks() - self.moveTime > 10):
            for i in range(0, 5):
                for j in range(0, 5):
                    if(self.PolygonX[i][j] > self.ScreenSizeX+100 or self.PolygonX[i][j] < -self.ScreenSizeX+400):
                        self.moveX[i][j] *= -1
                    elif(self.PolygonY[i][j] > self.ScreenSizeY+100 or self.PolygonY[i][j] < -self.ScreenSizeY+400):
                        self.moveY[i][j] *= -1

                    self.PolygonX[i][j] += self.moveX[i][j]
                    self.PolygonY[i][j] += self.moveY[i][j]
            self.moveTime = SDL_GetTicks()

        if(SDL_GetTicks() - self.rotateTime > 15):
            self.PolygonDegree += 0.02
            self.rotateTime = SDL_GetTicks()
        pass

    def draw(self):
        self.background.draw(0, 0)

        for i in range(0, 5):
            for j in range(0, 5):
                self.Polygon[i][j].rotate_draw(self.PolygonDegree, self.PolygonX[i][j], self.PolygonY[i][j])
                pass
        pass