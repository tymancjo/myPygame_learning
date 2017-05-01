# Sprite classes for platform game
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (int(width / (height/150)),
        #                                    int(height / (height/150))))
        return image

class Shoot(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = self.load_images()
        self.rect = self.image.get_rect()

        spanX = self.game.player.pos.x - self.game.Bck.pos.x
        spanY = self.game.player.rect.top + self.rect.height
        spanVel = self.game.player.vel
        spanAccl = self.game.player.acc

        if spanVel.x < 0:
            spanVelBulletX = spanVel.x - 2 * BULLET_VEL

        elif spanVel.x == 0:
            spanVelBulletX =0
        else:
            spanVelBulletX = spanVel.x + 2 * BULLET_VEL

        self.rect.midbottom = (spanX, spanY)
        self.pos = vec(spanX, spanY)

        self.vel = vec(2.5 * spanVel.x, -BULLET_VEL)

        self.acc = vec(0, -BULLET_ACC)

    def load_images(self):
        return pg.image.load(self.game.rocket).convert_alpha()

    def update(self):
        self.vel += self.acc

        # General movement equation for update (simple)
        dt = self.game.dt
        dy = self.vel.y * dt + 0.5 * self.acc.y * dt**2
        dx = self.vel.x * dt + 0.5 * self.acc.x * dt**2

        self.pos.x += dx
        self.pos.y += dy


        # Making the mob bouncing form the game area
        if self.rect.bottom < -5:
            self.kill()

        # converting to actual screen coordinates
        self.pos += self.game.Bck.pos
        # set for display
        self.rect.midbottom = self.pos
        # roll back to global
        self.pos -= self.game.Bck.pos

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = self.load_images()
        self.rect = self.image.get_rect()

        spanX = random.randrange(0,self.game.Bck.width)
        spanY = random.randrange(self.rect.height, HEIGHT - 100)

        self.rect.center = (spanX, spanY)
        self.pos = vec(spanX, spanY
        )

        self.vel = vec(random.randrange(MOB_SPEED_L, MOB_SPEED_H), 0)
        self.vel = self.vel * random.choice([-1,1])
        self.acc = vec(0, 0)

    def load_images(self):
        return pg.image.load(random.choice(self.game.mobs_images)).convert_alpha()

    def update(self):

        # General movement equation for update (simple)
        dt = self.game.dt
        dx = self.vel.x * dt + 0.5 * self.acc.x * dt**2
        dy = self.vel.y

        self.pos.x += dx
        self.pos.y += dy

        # Making the mob bouncing form the game area
        if self.rect.right - self.game.Bck.rect.x > self.game.Bck.width:
            self.vel.x *= -1
            self.pos.x = self.game.Bck.rect.x + self.game.Bck.width - self.rect.width / 2

        elif self.rect.left - self.game.Bck.rect.x < 0:
            self.vel.x *= -1
            self.pos.x = self.game.Bck.rect.x + self.rect.width / 2



        self.rect.midbottom = self.pos



class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.health = PLAYER_HEALT

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(285, 0, 399-285, 180)]

        self.walk_frames_r = [self.game.spritesheet.get_image(414, 0, 530-414, 180),
                              self.game.spritesheet.get_image(543, 0, 668-543, 180)]
        self.walk_frames_l = [self.game.spritesheet.get_image(153, 0, 270-153, 180),
                              self.game.spritesheet.get_image(10, 0, 136-10, 180)]

        self.jump_frame = self.standing_frames[0]


    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if self.vel.y == 0:
                self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            if self.vel.y == 0:
                self.acc.x = PLAYER_ACC

        # apply friction
        if self.vel.y == 0:
            self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 1:
            self.vel.x = 0

        # Oryginal movement
        # self.pos += self.vel + 0.5 * self.acc

        # Smoothing movement by making it a frame rate dependant
        dt = self.game.dt
        dx = self.vel.x * dt + 0.5 * self.acc.x * dt**2
        dy = self.vel.y

        # TODO: making possible to reach the map ends
        edgeDiv = 2
        self.pos.x += dx
        self.pos.y += dy

        # changing position only if we are in the middle zone
        if self.pos.x < self.rect.width / edgeDiv:
            self.pos.x = self.rect.width / edgeDiv

        elif self.pos.x + dx > WIDTH - self.rect.width / edgeDiv:
            self.pos.x = WIDTH - self.rect.width / edgeDiv

        self.rect.midbottom = self.pos

    def animate(self):
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # show walk animation
        if self.walking:
            bottom = self.rect.bottom

            if self.vel.x > PLAYER_SPEED_TRESHOLD_SLOW:
                if self.vel.x > PLAYER_SPEED_TRESHOLD:
                    self.image = self.walk_frames_r[1]
                else:
                    self.image = self.walk_frames_r[0]
            elif self.vel.x < -PLAYER_SPEED_TRESHOLD_SLOW:
                if self.vel.x < -PLAYER_SPEED_TRESHOLD:
                    self.image = self.walk_frames_l[1]
                else:
                    self.image = self.walk_frames_l[0]
            else:
                self.image = self.standing_frames[0]

            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
                bottom = self.rect.bottom
                self.image = self.standing_frames[0]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bck(pg.sprite.Sprite):
    def __init__(self, game, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = vec(-300, 0)
        self.rect.x = -300
        self.width = self.rect.width
        self.game = game
        self.factor = 0.2
        self.endOfMap = False

    def update(self):
        # Smoothing movement by making it a frame rate dependant
        dt = self.game.dt
        pX = self.game.player.pos.x

        # Making the 'quasi Paralax' movement od the background
        # It's based on the player vector of acc and vel and is
        # adjusted depending on player on screen position
        self.pos.x = self.rect.topleft[0]
        self.pos.y = self.rect.topleft[1]


        if pX - WIDTH / 2  > 0:
            self.factor = 0.5 + 1 * ((pX - WIDTH / 2) / WIDTH)
        else:
            self.factor = 0.5 + 1 * ((WIDTH / 2 - pX) / WIDTH)

        self.rect.x -= self.factor * (self.game.player.vel.x * dt + 0.5 *
                                      self.game.player.acc.x * dt**2)

        if self.rect.x > 0:
            self.rect.x = 0
            self.game.player.acc.x = 0
            self.endOfMap = True
        else:
            self.endOfMap = False

        if self.rect.x < -self.rect.width + WIDTH:
            self.rect.x = -self.rect.width +WIDTH
            self.game.player.acc.x = 0
            self.endOfMap = True
        else:
            self.endOfMap = False


class Front(pg.sprite.Sprite):
    def __init__(self, game, filename):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.game.Bck.rect.x
        self.rect.y = self.game.Bck.rect.y

        self.width = self.rect.width

    def update(self):
        # Smoothing movement by making it a frame rate dependant
        self.rect.x = self.game.Bck.rect.x
        self.rect.y = self.game.Bck.rect.y

class shadow(pg.sprite.Sprite):
    def __init__(self, game, filename):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 10
        self.rect.x = self.game.player.rect.x
        self.width = self.rect.width

    def update(self):
        # Smoothing movement by making it a frame rate dependant
        self.rect.x = self.game.player.rect.x
        self.image.set_alpha(256)
