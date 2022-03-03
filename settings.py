#Athanaios Tsivgas, Settings for game (Most of the things here are strings with vars for speed gravity and colors ect)
#making setting variables all caps so they are easy to look at in my code

WIDTH = 1280 #Screen width
HEIGHT = 720 #Screen Height
HEAD = "Athanasios Tsivgas - Python Final" #Game window name title thingy
FPS = 60 #set game tick rate


hsFile = "highScore.txt" #high score file
spriteSheetFile = "spritesheet_jumper.png" #Sprite Sheet
spriteSheetFilePlat = "tile.png" #Sprite Sheet platforms
BGONE = "one.png" #background layer one
CHARSHEET = "characters.png" #sprite sheet for character
ENESHEET = "eye.png" #enemy sprite sheet
START = "start.png" #start screen background image
END = "end.png" #game over screen background image

FONTNAME = "arial" #sets font, computer game is running on needs this font to work right

#Player settings
playerAcc = 1
playerFriction = -0.2
gravity = 0.5
jumpSpeed = -19

mopFreq = 200

#game properties
boostPower = 100
powSpawnPct = 10
platformList = [(0, HEIGHT - 100)]
i = 0
while i <= 100:
    i += 1
    string = 620 * i, HEIGHT - 100
    platformList.append(string)


objList = [(200, HEIGHT - 200),
           (500*2, HEIGHT - 200),
           (700*4, HEIGHT - 200),
           (600*8, HEIGHT - 200),
           (600*10, HEIGHT - 200),
           (700*13, HEIGHT - 200),
           (800*19, HEIGHT - 200),
           (500*22, HEIGHT - 200),
           (600*34, HEIGHT - 200),
           (700*39, HEIGHT - 200),
           (600*40, HEIGHT - 200)]

objList2 = [(700, HEIGHT - 350),
            (700*2, HEIGHT - 350),
            (700*4, HEIGHT - 350),
            (700*5, HEIGHT - 350),
            (700*7, HEIGHT - 350),
            (700*9, HEIGHT - 350),
            (700*11, HEIGHT - 350),
            (700*12, HEIGHT - 350),
            (700*14, HEIGHT - 350),
            (700*16, HEIGHT - 350),
            (700*20, HEIGHT - 350),
            (700*25, HEIGHT - 350),
            (700*27, HEIGHT - 350),
            (700*29, HEIGHT - 350),
            (700*32, HEIGHT - 350),
            (700*35, HEIGHT - 350),
            (700*37, HEIGHT - 350),
            (700*40, HEIGHT - 350),
            (800, HEIGHT - 650),
            (800*2, HEIGHT - 660),
            (800*4, HEIGHT - 560),
            (800*5, HEIGHT - 660),
            (800*7, HEIGHT - 560),
            (800*9, HEIGHT - 660),
            (800*11, HEIGHT - 550),
            (800*12, HEIGHT - 650),
            (800*14, HEIGHT - 650),
            (800*16, HEIGHT - 550),
            (800*20, HEIGHT - 650),
            (800*25, HEIGHT - 550),
            (800*27, HEIGHT - 650),
            (800*29, HEIGHT - 550),
            (800*32, HEIGHT - 650),
            (800*35, HEIGHT - 550),
            (800*37, HEIGHT - 650),
            (800*40, HEIGHT - 550)]

mobList = [(400, 500)]

#color values, mostly for testing stuff
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightBlue = (0, 155, 155)
BGCOLOR = red #sets background color, will mostlikely add background image so this is temp
