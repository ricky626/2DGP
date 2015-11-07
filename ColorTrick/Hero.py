import game_framework
import random

from My_pico2d import *
from map import Map

name = "Hero"

class Hero:
    left_stand = None


    def __init__(self):
        self.map = Map()

        self.HeroX = self.map.HeroX
        self.HeroY = self.map.HeroY
        self.run_frames = 0
        self.jump_frames = 0

        self.moveTime = SDL_GetTicks()

        LEFT_RUN, RIGHT_RUN, LEFT_STAND, self.RIGHT_STAND, LEFT_JUMP, RIGHT_JUMP = range(1, 7)
        self.m_CharState = self.RIGHT_STAND              # 1 : Left Run # 2 : Right Run # 3: Left Stand # 4 : Right Stand # 5 : Left Jump # 6 : Right Jump

        self.m_Movestate = 0 # 0: default 1: air 2 : jump
        self.m_nSwitchNo = 0
        self.m_nDropSpeed = 10
        self.m_JTime = -1

        self.leftbutton = False
        self.rightbutton = False
        self.jumpbutton = False


        if(Hero.left_stand == None):
            self.left_run           = load_image("res/hero/left_run.png")
            self.right_run          = load_image("res/hero/right_run.png")

            self.left_stand         = load_image("res/hero/left_stand.png")
            self.right_stand        = load_image("res/hero/right_stand.png")

            self.left_jump          = load_image("res/hero/left_jump.png")
            self.right_jump         = load_image("res/hero/right_jump.png")
        pass

    def CrashDetection(self, x, y):
        XTile = int(x / 64) #X 타일의 번호
        YTile = int(y / 64) #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40
        for i in range(0, 12):
            for j in range(0, 16):
                if(self.map.object[i][j] == 0): continue
                if(self.map.object[i][j] in [1, 2, 3, 4, 5, 6]):
                    if(self.map.objectX[i][j]/64 == XTile and self.map.objectY[i][j]/64 == YTile): return 1

                #elif(self.map.object[i][j] == (14, 15, 16, 17, 18)): #스위치이면 #꺼진거만 함
                #    if(self.map.objectX[i][j] == XTile and self.map.objectY[i][j] == YTile):
                #        tmpX = self.map.objectX[i][j]
                #        tmpY = self.map.objectY[i][j]

                    #if(m_Object[i][5] == 1)#켜진 스위치이면
                        #tmpMX = 42

                    if(tmpX + 20 <= x and tmpX + 40 >= x and (tmpY + 80 > y and tmpY + tmpMX < y - 2)):
                        return 1
        #print(int(XTile), int(YTile))
        #print(self.map.objectX[11][0]/64, self.map.objectY[11][0]/64)
        return 0

    def GetCharCrash(self, x, y, w):
        if (w == 0):
            if (self.CrashDetection(x + 2, y) != 0): return 1
            elif (self.CrashDetection(x + 18, y) != 0): 	return 1
        elif (w == 1):
            if (self.CrashDetection(x + 2, y) == 1): return 1
            elif(self.CrashDetection(x + 18, y) != 0): return 1
            elif (self.CrashDetection(x + 2, y + 48) != 0): return 1
            elif (self.CrashDetection(x + 18, y + 48) != 0): return 1
        return 0

    def update(self):
        if(self.leftbutton == True):
            if(self.m_Movestate == 0):
                self.m_CharState = 1
                if(self.GetCharCrash(self.HeroX - 4, self.HeroY, 1) == 0):
                    self.HeroX = max(0, self.HeroX - 4)

            else:
                if(self.m_Movestate > 0 and self.m_CharState == 6):
                    self.m_CharState = 5
                if(self.GetCharCrash(self.HeroX - 2.3, self.HeroY, 1) == 0):
                    self.HeroX = max(0, self.HeroX - 2.3)


            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()

        elif(self.rightbutton == True):
            if(self.m_Movestate == 0):
                self.m_CharState = 2
                if(self.GetCharCrash(self.HeroX + 4, self.HeroY, 1) == 0):
                    self.HeroX = min(999, self.HeroX + 4)

            else:
                if(self.m_Movestate > 0 and self.m_CharState == 5):
                    self.m_CharState = 6
                if(self.GetCharCrash(self.HeroX + 2.3, self.HeroY, 1) == 0):
                    self.HeroX = min(999, self.HeroX + 2.3)

            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()
        else:
            if(self.m_Movestate == 0):
                if(self.m_CharState == 1 or self.m_CharState == 5):
                    self.m_CharState = 3
                if(self.m_CharState == 2 or self.m_CharState == 6):
                    self.m_CharState = 4

        if(self.jumpbutton == True):
            if(self.GetCharCrash(self.HeroX, self.HeroY - 10, 0) == 0):
                if(self.m_CharState != 5 and self.m_CharState != 6):
                    if(self.m_MoveState == 0):
                        if(self.m_JTime <= 0):
                            self.m_JTime = 25
                            self.m_Movestate = 1

                        if(self.m_CharState == 1 or self.m_CharState == 3):
                            self.m_CharState = 5
                        elif(self.m_CharState == 2 or self.m_CharState == 4):
                            self.m_CharState = 6

        if(self.m_CharState == 5 or self.m_CharState == 6):
            self.jump_frames = (self.jump_frames + 1) % 3


        if(self.m_JTime > 0):
            if(self.GetCharCrash(self.HeroX, self.HeroY - (self.m_JTime / 5) * 2, 0) == 0):
                self.HeroY -= self.m_JTime / 5 * 2
                self.m_JTime -= 1

            else:                                       #면 위에 부딪힐 때
                self.m_nSwitchNo = 0
                self.m_JTime = 0
                self.m_nDropSpeed = 10
                self.m_MoveState = 2
                print("#########")

        elif(self.m_JTime == 0):
            #self.m_JTime = -1
            self.m_Movestate = 2
        elif(self.m_JTime == -1):
            self.m_Movestate = 0


        if(self.m_Movestate == 0 or self.m_Movestate == 2):
            if (self.GetCharCrash(self.HeroX, (self.HeroY + (self.m_nDropSpeed / 10) * 2 + 48), 0) == 0):
                self.HeroY += self.m_nDropSpeed / 10 * 2
                self.m_nDropSpeed += 1
            else:#######################
                self.m_nDropSpeed = 10
                self.m_MoveState = 0
                self.m_JTime = -1



        print(self.m_JTime)
        print(self.m_Movestate)
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
                self.leftbutton = True
                pass

            if event.key == SDLK_RIGHT:
                self.rightbutton = True
                pass

            if event.key == SDLK_SPACE:# and (self.m_CharState != 5 or self.m_CharState != 6):# and (self.m_CharState != 5 or self.m_CharState != 6):
                self.jumpbutton = True

                pass

        elif(event.type == SDL_KEYUP):
            if(event.key == SDLK_LEFT) and self.leftbutton == True:
                self.leftbutton = False
            if(event.key == SDLK_RIGHT) and self.rightbutton == True:
                self.rightbutton = False
            if(event.key == SDLK_SPACE) and self.jumpbutton == True:
                self.jumpbutton = False
            pass

