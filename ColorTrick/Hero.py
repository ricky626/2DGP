import game_framework
import random

from My_pico2d import *
from map import Map

name = "Hero"


map = None

class Hero:
    left_stand = None

    def __init__(self):
        self.map = Map()

        self.HeroX = self.map.HeroX
        self.HeroY = self.map.HeroY
        self.run_frames = 0
        self.jump_frames = 0

        self.moveTime = SDL_GetTicks()

        self.m_CharState = 4              # 1 : Left Run # 2 : Right Run # 3: Left Stand # 4 : Right Stand # 5 : Left Jump # 6 : Right Jump
        self.m_Movestate = 0
        self.m_JTime = 0
        self.m_nSwitchNo = 0
        self.m_nDropSpeed = 0


        if(Hero.left_stand == None):
            self.left_run           = load_image("res/hero/left_run.png")
            self.right_run          = load_image("res/hero/right_run.png")

            self.left_stand         = load_image("res/hero/left_stand.png")
            self.right_stand        = load_image("res/hero/right_stand.png")

            self.left_jump          = load_image("res/hero/left_jump.png")
            self.right_jump         = load_image("res/hero/right_jump.png")
        pass

    def CrashDetection(self, x, y):
        XTile = x / 64 #X 타일의 번호
        YTile = y / 64 #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40

        for i in range(0, 12):
            for j in range(0, 16):
                if(self.map.object[i][j] == range(1, 7)): #블록이면
                    if(self.objectX[i][j] == XTile and self.object.Y[i][j] == YTile): return 1

                elif(self.object[i][j] == range(14, 19)): #스위치이면 #꺼진거만 함
                    if(self.objectX[i][j] == XTile and self.objectY[i][j] == YTile):
                        tmpX = self.objectX[i][j] * 64
                        tmpY = self.objectY[i][j] * 64

                    #if(m_Object[i][5] == 1)#켜진 스위치이면
                        #tmpMX = 42

                    if(tmpX + 20 <= x and tmpX + 40 >= x and (tmpY + 80 > y and tmpY + tmpMX < y - 2)):
                        return 1
        return 0

    def GetCharCrash(self, x, y, w):
        if(w == 0):
            if(self.CrashDetection(x + 2, y)): return 1
            elif(self.CrashDetection(x + 18,y)): return 1
        elif(w == 1):
            if(self.CrashDetection(x + 2, y)): return 1
            elif(self.CrashDetection(x + 18,y)): return 1
            elif(self.CrashDetection(x + 2, y + 48)): return 1
            elif(self.CrashDetection(x + 18, y + 48)): return 1
        return 0

    def update(self):
        if(self.m_CharState == 1):
            self.HeroX -= 4
            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()


        if(self.m_CharState == 2):
            self.HeroX += 4
            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()

        elif(self.m_CharState == 5 or self.m_CharState == 6):
            self.jump_frames = (self.jump_frames + 1) % 3


        if(self.m_JTime > 0):
            if(self.GetCharCrash(self.HeroX, self.HeroY - (self.m_JTime / 5) * 2, 0) == False):
                self.HeroY -= self.mJTime / 5 * 2
                self.m_JTime -= 1
            else:
                self.m_nSwitchNo = 0
                self.m_JTime = 0
                self.m_nDropSpeed = 10
                self.m_MoveState = 2
        elif(self.m_JTime == 0):
            self.m_JTime = 0
            self.m_Movestate = 2

        if(self.HeroX < 0):
            self.HeroX = 0
        if(self.HeroX > 999):
            self.HeroX = 999
        pass

    def draw(self):
        if(self.m_CharState == 1):
            self.left_run.clip_draw(self.run_frames * 25, 0, 25, 50, self.HeroX, self.HeroY)
        elif(self.m_CharState == 2):
            self.right_run.clip_draw(self.run_frames * 25, 0, 25, 50, self.HeroX, self.HeroY)
        elif(self.m_CharState == 3):
            self.left_stand.draw(self.HeroX, self.HeroY)
        elif(self.m_CharState == 4):
            self.right_stand.draw(self.HeroX, self.HeroY)
        elif(self.m_CharState == 5):
            self.left_jump.clip_draw(self.jump_frames * 29, 0, 29, 61, self.HeroX, self.HeroY)
        elif(self.m_CharState == 6):
            self.right_jump.clip_draw(self.jump_frames * 29, 0, 29, 61, self.HeroX, self.HeroY)
        pass

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                if(self.m_Movestate == 0):
                    self.m_CharState = 1
                elif(self.m_Movestate > 0 and self.m_CharState == 6):
                    self.m_CharState = 5
                pass

            if event.key == SDLK_RIGHT:
                if(self.m_Movestate == 0):
                    self.m_CharState = 2
                elif(self.m_Movestate > 0 and self.m_CharState == 5):
                    self.m_CharState = 6
                pass

            if event.key == SDLK_SPACE:
                if(self.GetCharCrash(self.HeroX, self.HeroY - 10, 0) == False):
                    if(self.m_MoveState == 0):
                        if(self.m_JTime <= 0):
                            self.m_JTime = 25
                            self.m_Movestate = 1

                        if(self.m_CharState == 1 or self.m_CharState == 3):
                            self.m_CharState = 5
                        elif(self.m_CharState == 2 or self.m_CharState == 4):
                            self.m_CharState = 6

                pass

            elif(event.type == SDL_KEYUP):
                if(self.m_Movestate == 0):
                    if(self.m_CharState == 1 or self.m_CharState == 5):
                        self.m_CharState = 3
                    if(self.m_CharState == 2 or self.m_CharState == 6):
                        self.m_CharState = 4
                pass

