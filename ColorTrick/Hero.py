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
        self.EndX = self.map.EndX
        self.EndY = self.map.EndY
        self.run_frames = 0
        self.jump_frames = 0
        self.laser_frames = 0

        self.moveTime = SDL_GetTicks()
        self.jumpAnimationTime = SDL_GetTicks()
        self.laserTime = 0

        LEFT_RUN, RIGHT_RUN, LEFT_STAND, self.RIGHT_STAND, LEFT_JUMP, RIGHT_JUMP = range(1, 7)
        self.m_CharState = self.RIGHT_STAND              # 1 : Left Run # 2 : Right Run # 3: Left Stand # 4 : Right Stand # 5 : Left Jump # 6 : Right Jump

        self.m_Movestate = 0 # 0: default 1: air 2 : jump
        self.m_nSwitchNo = -1
        self.m_nDropSpeed = 10
        self.m_JTime = -1

        self.leftbutton = False
        self.rightbutton = False
        self.jumpbutton = False
        self.charview = False

        self.holdState = False

        if(Hero.left_stand == None):
            Hero.left_run           = load_image("res/hero/left_run.png")
            Hero.right_run          = load_image("res/hero/right_run.png")

            Hero.left_stand         = load_image("res/hero/left_stand.png")
            Hero.right_stand        = load_image("res/hero/right_stand.png")

            Hero.left_jump          = load_image("res/hero/left_jump.png")
            Hero.right_jump         = load_image("res/hero/right_jump.png")
            Hero.hold               = load_image("res/menu/hold.png")
            Hero.laser              = load_image("res/hero/laser.png")
        pass

    def CrashDetection(self, x, y):
        XTile = int(x / 64) #X 타일의 번호
        YTile = int(y / 64) #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40
        for i in range(0, 12):
            for j in range(0, 16):
                if(self.map.object[i][j] == 0):
                    continue

                if(self.map.object[i][j] in [1, 2, 3, 4, 5, 6] and self.map.objectX[i][j]/64 == XTile and self.map.objectY[i][j]/64 == YTile): #블록이면
                    return 1

                if(self.map.object[i][j] in [14, 15, 16, 17, 18, 19, 20, 21, 22, 23] and self.map.objectX[i][j]/64 == XTile and self.map.objectY[i][j]/64 == YTile): #스위치이면
                    tmpX = self.map.objectX[i][j]
                    tmpY = self.map.objectY[i][j]

                    if(self.map.object[i][j] in [19, 20, 21, 22, 23]):#켜진 스위치이면
                        tmpMX = 42

                    if(tmpX + 20 <= x and tmpX + 40 >= x and (tmpY + 80 > y and tmpY + tmpMX < y - 2)):
                        return 1
        #print(int(XTile), int(YTile))

        #print(self.map.objectX[11][0]/64, self.map.objectY[11][0]/64)
        return 0

    def SwitchDetection(self, x, y):
        XTile = int(x / 64) #X 타일의 번호
        YTile = int(y / 64) #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40
        for i in range(0, 12):
            for j in range(0, 16):

                if(self.map.object[i][j] in [14, 15, 16, 17, 18, 19, 20, 21, 22, 23] and self.map.objectX[i][j]/64 == XTile and self.map.objectY[i][j]/64 == YTile):#스위치이면
                    if(self.m_nSwitchNo in [1, 2, 3, 4, 5]):
                        return 0

                    if(self.map.object[i][j] in [19, 20, 21, 22, 23]):
                        tmpMX = 42

                    tmpX = self.map.objectX[i][j]
                    tmpY = self.map.objectY[i][j]

                    if(tmpX + 10 <= x and tmpX + 30 >= x and (tmpY + 80 >= y and tmpY + tmpMX <= y)):

                        if(self.map.object[i][j] in [19, 20, 21, 22, 23]):
                            self.HeroY -= 2

                        if(self.map.object[i][j] in [14, 15, 16, 17, 18]):
                            self.m_nSwitchNo = self.map.object[i][j] - 13
                        elif(self.map.object[i][j] in [19, 20, 21, 22, 23]):
                            self.m_nSwitchNo = self.map.object[i][j] - 18

                        if(self.map.object[i][j] == self.m_nSwitchNo + 13):
                            self.map.object[i][j] = self.m_nSwitchNo + 18

                        elif(self.map.object[i][j] == self.m_nSwitchNo + 18):
                            self.map.object[i][j] = self.m_nSwitchNo + 13

                        return 1

        self.m_nSwitchNo = -1

        return 0

    def SetSwitch(self, color):
        for i in range(0, 12):
            for j in range(0, 16):
                #block change
                if(self.map.object[i][j] == color):
                    self.map.object[i][j] = self.map.object[i][j] + 8

                elif(self.map.object[i][j] == color + 8):
                    self.map.object[i][j] = color


    def GetCharCrash(self, x, y, w):
        if (w == 0): #점프
            if (self.CrashDetection(x + 2, y) != 0): return 1
            elif (self.CrashDetection(x + 18, y) != 0): 	return 1
        elif (w == 1): #이동
            if (self.CrashDetection(x + 2, y) != 0): return 1
            elif(self.CrashDetection(x + 18, y) != 0): return 1
            elif (self.CrashDetection(x + 2, y + 48) != 0): return 1
            elif (self.CrashDetection(x + 18, y + 48) != 0): return 1
        return 0


    def collide(self, aX, aY, bX, bY):
        left_a, bottom_a, right_a, top_a = aX, aY, aX + 25, aY + 50
        left_b, bottom_b, right_b, top_b = bX, bY, bX + 64, bY + 64
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True


    def update(self):
        if(self.holdState):
            return
        if(self.charview == False):
            if(self.laserTime == 0):
                self.laserTime = SDL_GetTicks()

            if(SDL_GetTicks() - self.laserTime > 55):
                self.laser_frames = (self.laser_frames + 1) % 19
                self.laserTime = SDL_GetTicks()
            if(self.laser_frames == 18):
                self.charview = True

        if(SDL_GetTicks() - self.map.dotTime > 200):
            self.map.dot_frames = (self.map.dot_frames + 1) % 2
            self.map.dotTime = SDL_GetTicks()

        if(SDL_GetTicks() - self.map.flagTime > 150):
            self.map.flag_frames = (self.map.flag_frames + 1) % 3
            self.map.flagTime = SDL_GetTicks()

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
                            self.m_JTime = 23
                            self.m_Movestate = 1

                        if(self.m_CharState == 1 or self.m_CharState == 3):
                            self.m_CharState = 5
                        elif(self.m_CharState == 2 or self.m_CharState == 4):
                            self.m_CharState = 6

        if(self.m_CharState == 5 or self.m_CharState == 6):
            if(SDL_GetTicks() - self.jumpAnimationTime > 40):
                self.jump_frames = (self.jump_frames + 1) % 3
                self.jumpAnimationTime = SDL_GetTicks()


        if(self.m_JTime > 0):
            if(self.GetCharCrash(self.HeroX, self.HeroY - (self.m_JTime / 5) * 2, 0) == 0):
                self.HeroY -= self.m_JTime / 5 * 2
                self.m_JTime -= 1

            else:                                       #면 위에 부딪힐 때
                self.m_nSwitchNo = 0
                self.m_JTime = 0
                self.m_nDropSpeed = 10
                self.m_MoveState = 2

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

        if(self.SwitchDetection(self.HeroX, self.HeroY + 48) == 1):
            self.SetSwitch(self.m_nSwitchNo)

        if(self.HeroY > 768):
            self.LoadStage(self.map.m_nStage)

        if(self.collide(self.HeroX, self.HeroY, self.EndX, self.EndY)):
            self.LoadStage(self.map.m_nStage + 1)

        pass

    def draw(self):

        self.map.draw()
        if(self.charview == False):
            self.laser.clip_draw(self.laser_frames * 64, 0, 64, 768, self.HeroX - 17, self.HeroY - 720)
        else:
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

        if(self.holdState):
            self.hold.draw(0, 0)
        pass

    def LoadStage(self, count):
        self.map.m_nStage = count
        self.map.LoadMap(self.map.m_nStage)
        self.map.Init()
        self.HeroX = self.map.HeroX
        self.HeroY = self.map.HeroY
        self.EndX = self.map.EndX
        self.EndY = self.map.EndY
        self.m_Movestate = 0
        self.m_CharState = 4
        self.m_nDropSpeed = 10
        self.m_JTime = -1
        self.charview = False
        self.leftbutton = False
        self.rightbutton = False
        self.upbutton = False
        self.downbutton = False
        self.jumpbutton = False
        pass

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN and self.charview:
            if event.key == SDLK_LEFT:
                self.leftbutton = True
                pass

            if event.key == SDLK_RIGHT:
                self.rightbutton = True
                pass

            if event.key == SDLK_SPACE:# and (self.m_CharState != 5 or self.m_CharState != 6):# and (self.m_CharState != 5 or self.m_CharState != 6):
                self.jumpbutton = True
                pass

            if event.key == SDLK_ESCAPE:
                if(self.holdState == False):
                    self.holdState = True
                else:
                    self.holdState = False
                pass

            if event.key == SDLK_1:
                if(self.map.m_nStage > 1):
                    self.LoadStage(self.map.m_nStage - 1)
                pass
            elif event.key == SDLK_2:
                self.LoadStage(self.map.m_nStage + 1)
                pass

            if event.key == SDLK_r:
                self.LoadStage(self.map.m_nStage)
                pass



        elif(event.type == SDL_KEYUP):
            if(event.key == SDLK_LEFT) and self.leftbutton == True:
                self.leftbutton = False
            if(event.key == SDLK_RIGHT) and self.rightbutton == True:
                self.rightbutton = False
            if(event.key == SDLK_SPACE) and self.jumpbutton == True:
                self.jumpbutton = False
            pass

