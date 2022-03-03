#Athanaios Tsivgas, Sprite stuff for game
#import dependencies
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2
from random import choice, randrange

#class for loading and parsing spritesheet
class Spritesheet:

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        #grab an image out of a Spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w // 2, h // 2))
        return image

    def get_image_bigger(self, x, y, w, h):
        #grab an image out of a Spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w * 4, h * 4))
        return image

    def get_image_med(self, x, y, w, h):
        #grab an image out of a Spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w * 3, h * 2))
        return image

    def get_image_sm(self, x, y, w, h):
        #grab an image out of a Spritesheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w, h))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.jumpUp = False
        self.jumpDown = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self): #loads load_images
        self.jumping_frames = [self.game.charSheet.get_image_bigger(425, 42, 15, 22)]
        for frame in self.jumping_frames:
            frame.set_colorkey(white)
        self.standing_frames = [self.game.charSheet.get_image_bigger(9, 42, 15, 22),
                               self.game.charSheet.get_image_bigger(72, 42, 15, 22)]
        for frame in self.standing_frames:
            frame.set_colorkey(white)
        self.walk_frames_r = [self.game.charSheet.get_image_bigger(489, 42, 15, 22),
                              self.game.charSheet.get_image_bigger(552, 42, 16, 22)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(white)
        self.walk_frames_l = []
        #flip right walking frames for left walking frames
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
            frame.set_colorkey(white)
        self.jump_frame = self.game.charSheet.get_image_bigger(425, 42, 15, 22)
        self.jump_frame.set_colorkey(white)

    def jump_cut(self): #if jumping and let go of jump keys
        if self.jumping:
            if self.vel.y <- 5:
                self.vel.y = -5


    def jump(self): #method that lets the player jump
        #jump only if standing on platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = jumpSpeed

    def update(self): #update for player
        self.animate()
        self.acc = vec(0, gravity)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -playerAcc
        if keys[pg.K_RIGHT]:
            self.acc.x = playerAcc
        #apply friction
        self.acc.x += self.vel.x * playerFriction
        #calculate motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc



        #sets sprite to pos
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0 and self.jumping == False:
            self.walking = True
        else:
            self.walking = False
        if self.vel.y != 0:
            self.walking = False
            self.jumpUp = True
        else:
            self.jumpUp = False

        #show walking animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumpUp:
            self.image = self.jumping_frames[0]

        self.mask = pg.mask.from_surface(self.image)#creates hit box that matches the player image

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.platSheet.get_image_bigger(0, 192, 160, 32),
                  self.game.platSheet.get_image_bigger(0, 192, 160, 32)]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Object(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.platSheet.get_image_bigger(0, 112, 48, 48)]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Object2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.platSheet.get_image_med(257, 128, 112, 48)]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#Spawns bats from left and right sides and random speeds and locations on the screen
class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.eneSheet.get_image_sm(412, 128, 136, 96)
        self.image_up.set_colorkey(white)
        self.image_down = self.game.eneSheet.get_image_sm(733, 129, 140, 99)
        self.image_down.set_colorkey(white)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(650)
        self.vy = 0
        self.dy = 0.1

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Mob2(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.eneSheet.get_image(412, 128, 136, 96)
        self.image_up.set_colorkey(white)
        self.image_down = self.game.eneSheet.get_image(733, 129, 140, 99)
        self.image_down.set_colorkey(white)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image) #creates hit box that matches the bat image
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = Height - 100
        self.vy = 0
        self.dy = 0.1

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image) #creates hit box that matches the bat image
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Pow(pg.sprite.Sprite): #power up class for speed boost
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups #set all sprites and powerups groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game #set global var from local
        self.plat = plat #set global var from local
        self.type = choice(['boost']) #sets self type but I only have one right now
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70) #get image from sprite sheet
        self.image.set_colorkey(black) #color key to ignore, black is refrence from settings
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5


        def update(self):
            self.rect.bottom = self.plat.rect.top - 5
            if not self.game.platforms.has(self.plat):
                self.kill()
