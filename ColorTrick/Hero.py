import game_framework
import random

from My_pico2d import *
from map import Map

name = "Hero"


map = None

class Hero:
    left_stand = None
    right_stand = None
    left_run = None
    right_run = None
    left_jump = None
    right_jump = None

    def __init__(self):
        map = Map()

        self.HeroX = map.HeroX
        self.HeroY = map.HeroY
        self.run_frames = 0
        self.jump_frames = 0

        self.moveTime = SDL_GetTicks()

        self.m_CharState = 4              # 1 : Left Run # 2 : Right Run # 3: Left Stand # 4 : Right Stand # 5 : Left Jump # 6 : Right Jump
        self.m_Movestate = 0




        if(Hero.left_stand == None):
            self.left_run           = load_image("res/hero/left_run.png")
            self.right_run          = load_image("res/hero/right_run.png")

            self.left_stand         = load_image("res/hero/left_stand.png")
            self.right_stand        = load_image("res/hero/right_stand.png")

            self.left_jump          = load_image("res/hero/left_jump.png")
            self.right_jump         = load_image("res/hero/right_jump.png")
        pass

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

            if event.key == SDLK_RIGHT:
                if(self.m_Movestate == 0):
                    self.m_CharState = 2
                elif(self.m_Movestate > 0 and self.m_CharState == 5):
                    self.m_CharState = 6

            if event.key == SDLK_SPACE:
                pass
            pass

        elif(event.type == SDL_KEYUP):
            if(self.m_Movestate == 0):
                if(self.m_CharState == 1 or self.m_CharState == 5):
                    self.m_CharState = 3
                if(self.m_CharState == 2 or self.m_CharState == 6):
                    self.m_CharState = 4

            pass


    pass
