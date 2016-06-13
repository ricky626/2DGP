import game_framework
import random

from My_pico2d import *
from map import Map
from background import Background

name = "Hero"

class Hero:
    left_stand = None
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, LEFT_JUMP, RIGHT_JUMP = range(1, 7) #CharState
    CLEAR, AIR, JUMP = 0, 1, 2 #MoveState

    def __init__(self):
        self.map = Map()
        self.background = Background()

        self.HeroX = self.map.HeroX
        self.HeroY = self.map.HeroY
        self.EndX = self.map.EndX
        self.EndY = self.map.EndY
        self.run_frames = 0
        self.jump_frames = 0
        self.laser_frames = 0

        self.moveX = 4
        self.slowmoveX = 2.3
        self.maxjump = 23 #점프 최대치

        self.moveTime = SDL_GetTicks()
        self.jumpAnimationTime = SDL_GetTicks()
        self.laserTime = 0

        self.CharState = self.RIGHT_STAND
        self.MoveState = self.CLEAR
        self.SwitchNo = -1
        self.DropSpeed = 10
        self.JumpTime = -1
        self.isjump = False

        self.LeftButton = False
        self.RightButton = False
        self.JumpButton = False
        self.Charview = False


        self.stageclear_str = "res/stageclear/Stageclear_x.png"
        self.clearWin = False
        self.clearDir = False
        self.clearTime = 0
        self.clear_frames = 0

        if(Hero.left_stand == None):
            Hero.left_run           = load_image("res/hero/left_run.png")
            Hero.right_run          = load_image("res/hero/right_run.png")

            Hero.left_stand         = load_image("res/hero/left_stand.png")
            Hero.right_stand        = load_image("res/hero/right_stand.png")

            Hero.left_jump          = load_image("res/hero/left_jump.png")
            Hero.right_jump         = load_image("res/hero/right_jump.png")
            Hero.laser              = load_image("res/hero/laser.png")

            Hero.tutorial_image1       = load_image("res/tutorial/tu1.png")
            Hero.tutorial_image2       = load_image("res/tutorial/tu2.png")
            Hero.tutorial_image3       = load_image("res/tutorial/tu3.png")
            Hero.tutorial_image4       = load_image("res/tutorial/tu4.png")

            Hero.jump_sound = load_wav("res/sound/jump.wav")
            Hero.jump_sound.set_volume(32)

            Hero.switch_sound = load_wav("res/sound/switch.wav")
            Hero.switch_sound.set_volume(70)

            Hero.reset_sound = load_wav("res/sound/reset.wav")
            Hero.reset_sound.set_volume(32)
            Hero.reset_sound.play()

            Hero.clear_sound = load_wav("res/sound/clear.wav")
            Hero.clear_sound.set_volume(90)


            Hero.Stageclear_image = [0 for i in range(0, 18)]

            for i in range(0, 18):
                Hero.Stageclear_image[i] = load_image(self.stageclear_str.replace('x', str(i)))
            Hero.clearbg = load_image("res/stageclear/clearbg.png")

        pass

    def CrashDetection(self, x, y):
        XTile = int(x / self.map.TILE_SIZE) #X 타일의 번호
        YTile = int(y / self.map.TILE_SIZE) #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40

        for i in range(0, self.map.HEIGHT):
            for j in range(0, self.map.WIDTH):
                if(self.map.object[i][j] == self.map.EMPTY):
                    continue

                if(self.map.object[i][j] in range(self.map.RED_BLOCK, self.map.BLACK_BLOCK + 1)
                   and self.map.objectX[i][j] / self.map.TILE_SIZE == XTile and self.map.objectY[i][j] / self.map.TILE_SIZE == YTile): #블록이면
                    return 1

                if(self.map.object[i][j] in range(self.map.RED_OFF_SWITCH, self.map.PURPLE_ON_SWITCH + 1)
                   and self.map.objectX[i][j] / self.map.TILE_SIZE == XTile and self.map.objectY[i][j] / self.map.TILE_SIZE == YTile): #스위치이면
                    tmpX = self.map.objectX[i][j]
                    tmpY = self.map.objectY[i][j]

                    if(self.map.object[i][j] in range(self.map.RED_ON_SWITCH, self.map.PURPLE_ON_SWITCH + 1)):#켜진 스위치이면
                        tmpMX = 42

                    if(tmpX + 20 <= x and tmpX + 40 >= x and (tmpY + 80 > y and tmpY + tmpMX < y - 2)):
                        return 1
        return 0

    def SwitchDetection(self, x, y):
        XTile = int(x / self.map.TILE_SIZE) #X 타일의 번호
        YTile = int(y / self.map.TILE_SIZE) #Y 타일의 번호
        tmpX = 0
        tmpY = 0
        tmpMX = 40

        for i in range(0, self.map.HEIGHT):
            for j in range(0, self.map.WIDTH):

                if(self.map.object[i][j] in range(self.map.RED_OFF_SWITCH, self.map.PURPLE_ON_SWITCH + 1)
                   and self.map.objectX[i][j] / self.map.TILE_SIZE == XTile and self.map.objectY[i][j] / self.map.TILE_SIZE == YTile):#스위치이면
                    if(self.SwitchNo in range(self.map.RED_BLOCK, self.map.PURPLE_BLOCK + 1)):
                        return 0

                    if(self.map.object[i][j] in range(self.map.RED_ON_SWITCH, self.map.PURPLE_ON_SWITCH + 1)):
                        tmpMX = 42

                    tmpX = self.map.objectX[i][j]
                    tmpY = self.map.objectY[i][j]

                    if(tmpX + 5 <= x and tmpX + 35 >= x and (tmpY + 80 >= y and tmpY + tmpMX <= y - 2)):

                        if(self.map.object[i][j] in range(self.map.RED_ON_SWITCH, self.map.PURPLE_ON_SWITCH + 1)):
                            self.HeroY -= 2

                        if(self.map.object[i][j] in range(self.map.RED_OFF_SWITCH, self.map.PURPLE_OFF_SWITCH + 1)):
                            self.SwitchNo = self.map.object[i][j] - (self.map.RED_OFF_SWITCH - self.map.RED_BLOCK)
                        elif(self.map.object[i][j] in range(self.map.RED_ON_SWITCH, self.map.PURPLE_ON_SWITCH + 1)):
                            self.SwitchNo = self.map.object[i][j] - (self.map.RED_ON_SWITCH - self.map.RED_BLOCK)

                        if(self.map.object[i][j] == self.SwitchNo + (self.map.RED_OFF_SWITCH - self.map.RED_BLOCK)):
                            self.map.object[i][j] = self.SwitchNo + (self.map.RED_ON_SWITCH - self.map.RED_BLOCK)

                        elif(self.map.object[i][j] == self.SwitchNo + (self.map.RED_ON_SWITCH - self.map.RED_BLOCK)):
                            self.map.object[i][j] = self.SwitchNo + (self.map.RED_OFF_SWITCH - self.map.RED_BLOCK)

                        self.switch_sound.play()

                        return 1

        self.SwitchNo = -1

        return 0

    def SetSwitch(self, color):
        for i in range(0, self.map.HEIGHT):
            for j in range(0, self.map.WIDTH):
                #block change
                if(self.map.object[i][j] == color):
                    self.map.object[i][j] = self.map.object[i][j] + (self.map.RED_DOT_BLOCK - self.map.RED_BLOCK)

                elif(self.map.object[i][j] == color + (self.map.RED_DOT_BLOCK - self.map.RED_BLOCK)):
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

    def collide(self, aX, aY, bX, bY): # End라인 충돌처리
        left_a, top_a, right_a, bottom_a = aX, aY, aX + 25, aY + 50
        left_b, top_b, right_b, bottom_b = bX + 5, bY + 5, bX + 60, bY + 60

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a > bottom_b: return False
        if bottom_a < top_b: return False
        return True


    def update(self):
        self.background.update()

        if(self.clearWin):
            if(self.clearTime == 0):
                self.clearTime = SDL_GetTicks()

            if(SDL_GetTicks() - self.clearTime > 70):
                if(self.clearDir == False):
                    if(self.clear_frames < 10):
                        self.clear_frames += 1
                    elif(self.clear_frames < 17):
                        self.clear_frames += 1
                    else:
                        self.clear_frames = 10
                self.clearTime = SDL_GetTicks()
            return

        if(self.Charview == False):
            if(self.laserTime == 0):
                self.laserTime = SDL_GetTicks()

            if(SDL_GetTicks() - self.laserTime > 55):
                self.laser_frames = (self.laser_frames + 1) % 19
                self.laserTime = SDL_GetTicks()
            if(self.laser_frames == 18):
                self.Charview = True

        if(SDL_GetTicks() - self.map.dotTime > 200):
            self.map.dot_frames = (self.map.dot_frames + 1) % 2
            self.map.dotTime = SDL_GetTicks()

        if(SDL_GetTicks() - self.map.flagTime > 150):
            self.map.flag_frames = (self.map.flag_frames + 1) % 3
            self.map.flagTime = SDL_GetTicks()

        if(self.LeftButton == True):
            if(self.MoveState == self.CLEAR):
                self.CharState = self.LEFT_RUN
                if(self.GetCharCrash(self.HeroX - self.moveX, self.HeroY, 1) == 0):
                    self.HeroX = max(0, self.HeroX - self.moveX)

            else:
                if(self.MoveState > 0 and self.CharState == self.RIGHT_JUMP):
                    self.CharState = self.LEFT_JUMP
                if(self.GetCharCrash(self.HeroX - self.slowmoveX, self.HeroY, 1) == 0):
                    self.HeroX = max(0, self.HeroX - self.slowmoveX)


            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()

        elif(self.RightButton == True):
            if(self.MoveState == self.CLEAR):
                self.CharState = self.RIGHT_RUN
                if(self.GetCharCrash(self.HeroX + self.moveX, self.HeroY, 1) == 0):
                    self.HeroX = min(999, self.HeroX + self.moveX)

            else:
                if(self.MoveState > 0 and self.CharState == self.LEFT_JUMP):
                    self.CharState = self.RIGHT_JUMP
                if(self.GetCharCrash(self.HeroX + self.slowmoveX, self.HeroY, 1) == 0):
                    self.HeroX = min(999, self.HeroX + self.slowmoveX)

            if(SDL_GetTicks() - self.moveTime > 50):
                self.run_frames = (self.run_frames + 1) % 4
                self.moveTime = SDL_GetTicks()
        else:
            if(self.MoveState == self.CLEAR):
                if(self.CharState == self.LEFT_RUN or self.CharState == self.LEFT_JUMP):
                    self.CharState = self.LEFT_STAND
                if(self.CharState == self.RIGHT_RUN or self.CharState == self.RIGHT_JUMP):
                    self.CharState = self.RIGHT_STAND

        if(self.JumpButton == True and self.isjump == False):
            if(self.GetCharCrash(self.HeroX, self.HeroY - 10, 0) == 0):
                if(self.CharState != self.LEFT_JUMP and self.CharState != self.RIGHT_JUMP):
                    if(self.MoveState == self.CLEAR):
                        if(self.JumpTime <= 0):
                            self.JumpTime = self.maxjump
                            self.MoveState = self.AIR

                        if(self.CharState == self.LEFT_RUN or self.CharState == self.LEFT_STAND):
                            self.CharState = self.LEFT_JUMP
                        elif(self.CharState == self.RIGHT_RUN or self.CharState == self.RIGHT_STAND):
                            self.CharState = self.RIGHT_JUMP
                        self.jump_sound.play()


        if(self.CharState == self.LEFT_JUMP or self.CharState == self.RIGHT_JUMP):
            if(SDL_GetTicks() - self.jumpAnimationTime > 40):
                self.jump_frames = (self.jump_frames + 1) % 3
                self.jumpAnimationTime = SDL_GetTicks()


        if(self.JumpTime > 0):
            if(self.GetCharCrash(self.HeroX, self.HeroY - (self.JumpTime / 5) * 2, 0) == 0):
                self.HeroY -= self.JumpTime / 5 * 2
                self.JumpTime -= 1

            else:                                       #면 위에 부딪힐 때
                self.SwitchNo = 0
                self.JumpTime = 0
                self.DropSpeed = 10
                self.MoveState = self.JUMP

        elif(self.JumpTime == 0):
            #self.JumpTime = -1
            self.MoveState = self.JUMP
        elif(self.JumpTime == -1):
            self.MoveState = self.CLEAR


        if(self.MoveState == self.CLEAR or self.MoveState == self.JUMP):
            if (self.GetCharCrash(self.HeroX, (self.HeroY + (self.DropSpeed / 10) * 2 + 48), 0) == 0):
                self.HeroY += self.DropSpeed / 10 * 2
                self.DropSpeed += 1
                self.isjump = True
            else:#######################
                self.DropSpeed = 10
                self.MoveState = self.CLEAR
                self.JumpTime = -1
                self.isjump = False

        if(self.SwitchDetection(self.HeroX, self.HeroY + 52) == 1):
            self.SetSwitch(self.SwitchNo)

        if(self.HeroY > 768):
            self.LoadStage(self.map.Stage_number)

        if(self.collide(self.HeroX, self.HeroY, self.EndX, self.EndY)):
            if(self.clearWin == False):
                self.clear_sound.play()
                self.clearWin = True

        pass

    def tutorial_draw(self):
        self.tutorial_image1.draw(252, 500)
        self.tutorial_image2.draw(400, 400)
        self.tutorial_image3.draw(300, 300)

        if(self.map.object[8][8] != 14):
            self.tutorial_image4.draw(700, 370)
        pass

    def clear_draw(self):
        self.clearbg.draw(200, 154)
        self.Stageclear_image[self.clear_frames].draw(225, 250)

        pass

    def draw(self):
        self.background.draw()
        self.map.draw()

        if(self.map.Stage_number == 0):
            self.tutorial_draw()


        if(self.Charview == False):
            self.laser.clip_draw(self.laser_frames * 64, 0, 64, 768, self.HeroX - 17, self.HeroY - 720)
        else:
            if(self.CharState == self.LEFT_RUN):
                self.left_run.clip_draw(self.run_frames * 25, 0, 25, 50, self.HeroX, self.HeroY)
            elif(self.CharState == self.RIGHT_RUN):
                self.right_run.clip_draw(self.run_frames * 25, 0, 25, 50, self.HeroX, self.HeroY)
            elif(self.CharState == self.LEFT_STAND):
                self.left_stand.draw(self.HeroX, self.HeroY)
            elif(self.CharState == self.RIGHT_STAND):
                self.right_stand.draw(self.HeroX, self.HeroY)
            elif(self.CharState == self.LEFT_JUMP):
                self.left_jump.clip_draw(self.jump_frames * 29, 0, 29, 61, self.HeroX, self.HeroY)
            elif(self.CharState == self.RIGHT_JUMP):
                self.right_jump.clip_draw(self.jump_frames * 29, 0, 29, 61, self.HeroX, self.HeroY)

        if(self.clearWin):
            self.clear_draw()

        pass

    def PolygonReset(self):
        for i in range(0, 5):
            for j in range(0, 5):
                self.background.PolygonX[i][j], self.background.PolygonY[i][j] = 352, 254
                self.background.moveX[i][j], self.background.moveY[i][j] = random.randint(-4, 4), random.randint(-4, 4)
        pass

    def LoadStage(self, count):
        self.map.Stage_number = count
        self.map.LoadMap(self.map.Stage_number)
        self.map.Init()
        self.HeroX = self.map.HeroX
        self.HeroY = self.map.HeroY
        self.EndX = self.map.EndX
        self.EndY = self.map.EndY
        self.MoveState = self.CLEAR
        self.CharState = self.RIGHT_STAND
        self.DropSpeed = 10
        self.JumpTime = -1
        self.Charview = False
        self.LeftButton = False
        self.RightButton = False
        self.upbutton = False
        self.downbutton = False
        self.JumpButton = False

        self.laser_frames = 0
        self.laserTime = 0

        self.clearWin = False
        self.clearDir = False
        self.clear_frames = 0
        self.clearTime = 0

        self.reset_sound.play()
        print(count)
        pass

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN and self.Charview:

            if(self.clearWin == False):

                if event.key == SDLK_LEFT:
                    self.LeftButton = True
                    pass

                if event.key == SDLK_RIGHT:
                    self.RightButton = True
                    pass

                if event.key == SDLK_SPACE:# and (self.CharState != self.LEFT_JUMP or self.CharState != self.RIGHT_JUMP):# and (self.CharState != self.LEFT_JUMP or self.CharState != self.RIGHT_JUMP):
                    self.JumpButton = True
                    pass

                if event.key == SDLK_ESCAPE:
                    pass

            elif(self.clearWin):
                if(event.key == SDLK_SPACE):
                    self.LoadStage(self.map.Stage_number + 1)
                    self.PolygonReset()
                    pass

            if event.key == SDLK_1:
                if(self.map.Stage_number > 0):
                    self.LoadStage(self.map.Stage_number - 1)
                    self.PolygonReset()
                pass
            elif event.key == SDLK_2: # MaxStage
                if(self.map.Stage_number <= 18):
                    self.LoadStage(self.map.Stage_number + 1)
                    self.PolygonReset()
                pass

            if event.key == SDLK_r:
                self.LoadStage(self.map.Stage_number)

                pass



        elif(event.type == SDL_KEYUP):
            if(event.key == SDLK_LEFT) and self.LeftButton == True:
                self.LeftButton = False
            if(event.key == SDLK_RIGHT) and self.RightButton == True:
                self.RightButton = False
            if(event.key == SDLK_SPACE) and self.JumpButton == True:
                self.JumpButton = False
            pass

