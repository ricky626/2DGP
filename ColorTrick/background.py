import game_framework
import random

from My_pico2d import *

name                                = "Background"


class Background:


    background                      = None
    Polygon                         = [[None for j in range(0, 5)] for i in range(0, 5)]

    def __init__(self):

        self.screenSizeX = 1024
        self.screenSizeY = 768
        self.rect = "res/rect/rect-.png"
        self.tr = "res/tr/tr-.png"
        self.cir = "res/cir/cir-.png"
        self.fa = "res/fa/fa-.png"
        self.yut = "res/yut/yut-.png"

        self.rotateTime = SDL_GetTicks()
        self.moveTime = SDL_GetTicks()
        self.PolygonDegree = 0
        self.PolygonX = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.PolygonY = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_X_KMPH = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_Y_KMPH = [[0 for j in range(0, 5)] for i in range(0, 5)]

        self.RUN_SPEED_X_MPM = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_X_MPS = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_X_PPS = [[0 for j in range(0, 5)] for i in range(0, 5)]

        self.RUN_SPEED_Y_MPM = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_Y_MPS = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.RUN_SPEED_Y_PPS = [[0 for j in range(0, 5)] for i in range(0, 5)]


        self.PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm

        for i in range(0, 5):
            for j in range(0, 5):
                #self.PolygonX[i][j], self.PolygonY[i][j]    = random.randint(-self.ScreenSizeX/2, self.ScreenSizeX + 500), random.randint(-self.ScreenSizeY/2, self.ScreenSizeY + 500)
                self.PolygonX[i][j], self.PolygonY[i][j] = self.screenSizeX/2-160, self.screenSizeY/2-130
                #self.moveX[i][j], self.moveY[i][j] = random.randint(-4, 4), random.randint(-4, 4)


                self.RUN_SPEED_X_KMPH[i][j] = random.randint(-20, 20)  # Km / Hour
                self.RUN_SPEED_Y_KMPH[i][j] = random.randint(-20, 20)  # Km / Hour

                self.RUN_SPEED_X_MPM[i][j] = self.RUN_SPEED_X_KMPH[i][j] * 1000.0 / 60.0
                self.RUN_SPEED_X_MPS[i][j] = self.RUN_SPEED_X_MPM[i][j] / 60.0
                self.RUN_SPEED_X_PPS[i][j] = self.RUN_SPEED_X_MPS[i][j] * self.PIXEL_PER_METER

                self.RUN_SPEED_Y_MPM[i][j] = self.RUN_SPEED_Y_KMPH[i][j] * 1000.0 / 60.0
                self.RUN_SPEED_Y_MPS[i][j] = self.RUN_SPEED_Y_MPM[i][j] / 60.0
                self.RUN_SPEED_Y_PPS[i][j] = self.RUN_SPEED_Y_MPS[i][j] * self.PIXEL_PER_METER


        if(Background.background == None):
            self.background = load_image("res/background.png")

            for i in range(0, 5):
               self.Polygon[0][i] = load_image(self.rect.replace('-', str(i+1)))
               self.Polygon[1][i] = load_image(self.tr.replace('-', str(i+1)))
               self.Polygon[2][i] = load_image(self.cir.replace('-', str(i+1)))
               self.Polygon[3][i] = load_image(self.fa.replace('-', str(i+1)))
               self.Polygon[4][i] = load_image(self.yut.replace('-', str(i+1)))

        pass

    def update(self, frame_time):
        for i in range(0, 5):
            for j in range(0, 5):
                if(self.PolygonX[i][j] > self.screenSizeX+100 or self.PolygonX[i][j] < -self.screenSizeX+400):
                    self.RUN_SPEED_X_PPS[i][j] *= -1
                elif(self.PolygonY[i][j] > self.screenSizeY+100 or self.PolygonY[i][j] < -self.screenSizeY+400):
                    self.RUN_SPEED_Y_PPS[i][j] *= -1

                self.PolygonX[i][j] += self.RUN_SPEED_X_PPS[i][j] * frame_time
                self.PolygonY[i][j] += self.RUN_SPEED_Y_PPS[i][j] * frame_time


        if(SDL_GetTicks() - self.rotateTime > 15):
            self.PolygonDegree += 0.02
            self.rotateTime = SDL_GetTicks()
        pass

    def draw(self, frame_time):
        self.background.draw(0, 0)

        for i in range(0, 5):
            for j in range(0, 5):
                self.Polygon[i][j].rotate_draw(self.PolygonDegree, self.PolygonX[i][j], self.PolygonY[i][j])
                pass
        pass