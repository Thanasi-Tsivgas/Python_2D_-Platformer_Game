#Athanasios Tsivgas, 2d pixel art side scrolling platformer game (Super Mario Bro's Esk)
#import dependencies
import pygame as pg #use pg instead of pygame
import random
from settings import *
from sprites import *
from os import path


#main game class
class Game():
    #game class init method
    def __init__(self):
        pg.init() #initialize pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #sets window size, see settings
        pg.display.set_caption(HEAD) #set game window headder, sets window title see settings
        self.clock = pg.time.Clock() #create game clock
        self.running = True # sets running to true for loop in main
        self.fontName = pg.font.match_font(FONTNAME) #sets font see settings
        self.load_data() #calls load data method


    def load_data(self):
        #load or create high score file
        self.dir = path.dirname(__file__) #get current directory
        img_dir = path.join(self.dir, 'assets') #appends the assets folder to directory string
        try:
            #try to read this file
            with open(path.join(self.dir, hsFile), 'r+') as f:
                self.highscore = int(f.read())
        except:
            #create file if dosent exist or cant read
            with open(path.join(self.dir, hsFile), 'w'):
                self.highscore = 0

        #load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, spriteSheetFile))
        self.platSheet = Spritesheet(path.join(img_dir, spriteSheetFilePlat))
        self.charSheet = Spritesheet(path.join(img_dir, CHARSHEET))
        self.eneSheet = Spritesheet(path.join(img_dir, ENESHEET))
        #background layer
        self.bgOne = pg.image.load(path.join(img_dir, BGONE)) #in game background image
        self.bgOne = pg.transform.scale(self.bgOne, (1280, 720))

        self.start = pg.image.load(path.join(img_dir, START)) #start screen background image
        self.start = pg.transform.scale(self.start, (1280, 720))

        self.end = pg.image.load(path.join(img_dir, END)) #game over screen background image
        self.end = pg.transform.scale(self.end, (1280, 720))

    #game loop that runs while playing = True
    def run(self):
        #game loop
        self.playing = True #set default var of playing boolian to true


        while self.playing:
            self.clock.tick(FPS) #keeps loop running at tick rate of the fps var, see settings
            self.events() #calls events method
            self.update() #calls update method
            self.draw() #calls draw method



    def new(self):
        self.score = 0 #creates base score var of 0
        #creates default sprite pos
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.objects2 = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mob_timer = 0
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        #make platforms from platform list
        for plat in platformList:
            if random.randrange(10) == 1:
                Pow(self, Platform(self, *plat))
            else:
                Platform(self, *plat)
        for obj in objList:
            if random.randrange(10) == 1:
                Pow(self, Object(self, *obj))
            else:
                Object(self, *obj)
        for obj2 in objList2:
            if random.randrange(10) == 1:
                Pow(self, Object2(self, *obj2))
            else:
                Object2(self, *obj2)
        g.run()


    def update(self):
        self.all_sprites.update() #update all sprites group

        #spawn mob at timer + random range time
        now = pg.time.get_ticks()
        if now - self.mob_timer > 1200 + random.randrange(-500, 500):
            self.mob_timer = now
            Mob(self)
        if now - self.mob_timer > 2200 + random.randrange(-500, 500):
            self.mob_timer = now
            Mob2(self)
        #if player hits power up delete image and boost player
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.x = +boostPower


        #checks if player hits a platform only if falling down, if they do sets they y vel to 0 and lets them stand on platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            self.player.jumping = False
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 40 and self.player.pos.x > lowest.rect.left - 40:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False
        #moves right when player gets close to edge of screen on the right
        if self.player.rect.right >= WIDTH - (WIDTH / 3):
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x), 2)
                if plat.rect.right <= 0: #kills platforms off the left edge of the screen
                            plat.kill()
                            self.score += 10
            for obj in self.objects:
                obj.rect.x -= max(abs(self.player.vel.x), 2)
                if obj.rect.right <= 0: #kills platforms off the left edge of the screen
                            obj.kill()
                            self.score += 10
            for obj2 in self.objects2:
                obj2.rect.x -= max(abs(self.player.vel.x), 2)
                if obj2.rect.right <= 0: #kills platforms off the left edge of the screen
                            obj2.kill()
                            self.score += 10
            for mob in self.mobs:
                mob.rect.x -= max(abs(self.player.vel.x), 2)
                if mob.rect.right <= 0: #kills bats off the left edge of the screen
                            mob.kill()
                            self.score += 10
            for pow in self.powerups:
                pow.rect.x -= max(abs(self.player.vel.x), 2)
                if pow.rect.right <= 0: #kills bats off the left edge of the screen
                            pow.kill()
                            self.score += 10
        if self.player.rect.left <= 1: #stops player from walking back to the left of the screen
            self.player.pos.x += max(abs(self.player.vel.x), 0)
        bat = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask) #if the player hits a mob they get game over screen
        if bat:
            self.playing = False
            g.show_game_over_screen()
        if self.player.rect.top > 729:
            self.playing = False


    #game loop events
    def events(self):
        #check for input
        for event in pg.event.get():
            #check if user closes Game
            if event.type == pg.QUIT: #if the player closes the game end stuff
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP: #if the player hits space or up arrow
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_UP: #if they player lets go of space or up arrow quickly make the players jump smaller
                    self.player.jump_cut()

    #game loop draw
    def draw(self):
        #render Screen
        self.screen.fill(black) #sets background colors
        self.screen.blit(self.bgOne, (0,0))
        self.all_sprites.draw(self.screen) #draws sprites to screen
        self.screen.blit(self.player.image, self.player.rect) #makes sure player and its image is always on the top layer
        self.draw_text(str(self.score), 22, white, WIDTH / 2, 15) #writes text to the screen to show score
        pg.display.flip() #not sure why i need this but i think i do

    #creates and shows start screen
    def show_start_screen(self):
        if not self.running: #makes sure game is running, if not return aka end game
            return
        self.screen.fill(BGCOLOR) #fills background color
        self.screen.blit(self.start, (0,0))
        #self.draw_text(HEAD, 48, white, WIDTH / 2, HEIGHT / 4) #draws game header as title
        #self.draw_text("Arrows to move, Space to jump", 22, white, WIDTH / 2, HEIGHT / 2) #tells player the controls
        #self.draw_text("Press a key to play", 22, white, WIDTH / 2, HEIGHT * 3 / 4) #tells user prest a key to play
        self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2 , 15) #shows high score


        pg.display.flip()
        pg.time.delay(40)
        self.wait_for_key()

    #creates and shows game over screen when player has died
    def show_game_over_screen(self):
        if not self.running: #checks if the game is running, if it isint returns
            return
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.end, (0,0))
        #self.draw_text("Game Over!", 48, white, WIDTH / 2, HEIGHT / 4) #writes game over to screen
        self.draw_text("Score: " + str(self.score), 22, white, WIDTH / 2, HEIGHT / 2) #writes players score to screen
        #self.draw_text("Press a key to play again", 22, white, WIDTH / 2, HEIGHT * 3 / 4) #tells user press a key to play again
        #check if player beat high score
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New high score!", 22, white, WIDTH / 2, HEIGHT / 2 + 40) #if the user got a new high score it shows it
            with open(path.join(self.dir, hsFile), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2, HEIGHT /2 + 40) #if they didnt get a new high score it shows the old one
        pg.display.flip()
        pg.time.delay(40)
        self.wait_for_key()

    #class to make game wait for user to press a key
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get(): #if the user quits the game stop waiting
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP: #if the user clicks somthing stop waiting
                    waiting = False

    #method to draw text
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game() #creates game object as g
def main():

    g.show_start_screen() #runs start screen for game object g
    while g.running:
        g.new() #when the game is running run new game stuff
        g.show_game_over_screen()#if game loop ever ends show game over screen

    pg.quit() #if game loop ends quit game

#runs main function if name == main
if __name__ == "__main__":
    main()
