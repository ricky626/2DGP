import game_framework

from My_pico2d import *

name                        = "Map"
map                         = None

class Map:
    flag = None
    EMPTY, RED_BLOCK, YELLOW_BLOCK, GREEN_BLOCK, BLUE_BLOCK, PURPLE_BLOCK, BLACK_BLOCK, HERO = range(0, 8)
    FLAG, RED_DOT_BLOCK, YELLOW_DOT_BLOCK, GREEN_DOT_BLOCK, BLUE_DOT_BLOCK, PURPLE_DOT_BLOCK = range(8, 14)
    RED_OFF_SWITCH, YELLOW_OFF_SWITCH, GREEN_OFF_SWITCH, BLUE_OFF_SWITCH, PURPLE_OFF_SWITCH,  = range(14, 19)
    RED_ON_SWITCH, YELLOW_ON_SWITCH, GREEN_ON_SWITCH, BLUE_ON_SWITCH, PURPLE_ON_SWITCH,  = range(19, 24)
    WIDTH, HEIGHT = 16, 12
    TILE_SIZE = 64

    def __init__(self):
        self.Stage_number       = 0
        self.object         = [[0 for row in range(0, self.WIDTH)] for col in range(0, self.WIDTH)]
        self.dot_frames     = 0
        self.flag_frames    = 0
        self.name           = "res/Stage/Stage-.txt"
        self.dotTime        = SDL_GetTicks()
        self.flagTime       = SDL_GetTicks()
        self.objectX    = [[0 for row in range(0, self.WIDTH)] for col in range(0, self.HEIGHT)]
        self.objectY    = [[0 for row in range(0, self.WIDTH)] for col in range(0, self.HEIGHT)]

        
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
        self.LoadMap(self.Stage_number)
        self.Init()
        pass

    def Init(self):
        for i in range(0, self.HEIGHT):
            for j in range(0, self.WIDTH):
                self.objectX[i][j] = j * self.TILE_SIZE
                self.objectY[i][j] = i * self.TILE_SIZE

                if(self.object[i][j] == self.HERO):
                    self.HeroX = self.objectX[i][j] + 8
                    self.HeroY = self.objectY[i][j]

                elif(self.object[i][j] == self.FLAG):
                    self.EndX = self.objectX[i][j]
                    self.EndY = self.objectY[i][j]
        pass
    def LoadMap(self, Stage_number):
        f = open(self.name.replace('-', str(Stage_number)), 'r')

        for col in range(0, self.HEIGHT):
            for row in range(0, self.WIDTH):
                self.object[col][row] = int(f.read(3).strip())
        f.close()
        pass

    def update(self):
        pass

    def draw(self):
        for i in range(0, self.HEIGHT):
            for j in range(0, self.WIDTH):

                if(self.object[i][j] == self.RED_BLOCK): self.red.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.YELLOW_BLOCK): self.yellow.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.GREEN_BLOCK): self.green.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.BLUE_BLOCK): self.blue.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.PURPLE_BLOCK): self.purple.draw(self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.BLACK_BLOCK): self.black.draw(self.objectX[i][j], self.objectY[i][j])
                #if(self.object[i][j] == 7): self.hero.draw(self.HeroX, self.HeroY)
                elif(self.object[i][j] == self.FLAG): self.flag.clip_draw(self.flag_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.RED_DOT_BLOCK): self.dot_red.clip_draw(self.dot_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.YELLOW_DOT_BLOCK):self.dot_yellow.clip_draw(self.dot_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.GREEN_DOT_BLOCK):self.dot_green.clip_draw(self.dot_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.BLUE_DOT_BLOCK):self.dot_blue.clip_draw(self.dot_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])
                elif(self.object[i][j] == self.PURPLE_DOT_BLOCK):self.dot_purple.clip_draw(self.dot_frames * self.TILE_SIZE, 0, self.TILE_SIZE, self.TILE_SIZE, self.objectX[i][j], self.objectY[i][j])

                elif(self.object[i][j] == self.RED_OFF_SWITCH): self.red_off.draw(self.objectX[i][j] + 12, self.objectY[i][j] + 28)
                elif(self.object[i][j] == self.YELLOW_OFF_SWITCH): self.yellow_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.GREEN_OFF_SWITCH): self.green_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.BLUE_OFF_SWITCH): self.blue_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.PURPLE_OFF_SWITCH): self.purple_off.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)

                elif(self.object[i][j] == self.RED_ON_SWITCH): self.red_on.draw(self.objectX[i][j] + 12, self.objectY[i][j] + 28)
                elif(self.object[i][j] == self.YELLOW_ON_SWITCH): self.yellow_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.GREEN_ON_SWITCH): self.green_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.BLUE_ON_SWITCH): self.blue_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)
                elif(self.object[i][j] == self.PURPLE_ON_SWITCH): self.purple_on.draw(self.objectX[i][j]+ 12, self.objectY[i][j]+ 28)


        pass