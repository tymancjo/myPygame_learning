# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 11
# Video link: https://youtu.be/n4TQfKt4wpQ
# Character animation (part 2)
# Art from Kenney.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image and images
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.shadow = path.join(img_dir, SHADOW)
        self.background = path.join(img_dir, BCK_IMAGE)
        self.foreground = path.join(img_dir, FRT_IMAGE)
        self.rocket = path.join(img_dir, ROCKET_IMAGE)
        self.splash = path.join(img_dir, SPLASH_IMAGE)

        # MOBs pictures
        self.mobs_images = []
        for mi in MOB_IMAGES:
            self.mobs_images.append(path.join(img_dir, mi))


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.bck_01 = pg.sprite.Group()
        self.frt_01 = pg.sprite.Group()
        self.shad_01 = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shoots = pg.sprite.Group()

        self.Bck = Bck(self, self.background)
        self.bck_01.add(self.Bck)

        self.Frt = Front(self, self.foreground)
        self.frt_01.add(self.Frt)

        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.pShadow = shadow(self, self.shadow)
        self.shad_01.add(self.pShadow)

        for m in range(8):
            mob = Mob(self)
            self.all_sprites.add(mob)
            self.mobs.add(mob)

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        # spawn new platforms to keep same average number
        while len(self.platforms) < 0:
            width = random.randrange(100, 250)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(200, HEIGHT - 200),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)



        self.run()


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.fps = self.clock.get_fps()
            self.dt = 1 / self.fps
            self.events()
            self.update()
            self.draw()


            # lets see FPS
            title = '{} /{}FPS/'.format(TITLE, int(self.fps))
            pg.display.set_caption(title)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 10
                self.player.vel.y = 0

        mobsTouch = pg.sprite.spritecollide(self.player, self.mobs, True)
        if mobsTouch:
            self.player.health -= 20
            self.score += 20

            if self.player.health <= 0:
                self.playing = False

        rocketTouch = pg.sprite.groupcollide(self.shoots, self.mobs, True, True)
        if rocketTouch:
            self.score += 5
            # Spawn new mobs instead death one
            for m in range(1):
                mob = Mob(self)
                self.all_sprites.add(mob)
                self.mobs.add(mob)



        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.mobs) == 0:
            self.playing = False

        self.Bck.update()
        self.shad_01.update()
        self.frt_01.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()

                if event.key == pg.K_b:
                    sht = Shoot(self)
                    self.shoots.add(sht)
                    self.all_sprites.add(sht)


    def draw(self):
        # Game Loop - draw
        self.bck_01.draw(self.screen)
        self.shad_01.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.frt_01.draw(self.screen)

        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.draw_text('Enemy ships count: {}'.format(len(self.mobs)), 22, WHITE, WIDTH / 2, 35)
        self.hud()
        # *after* drawing everything, flip the display
        pg.display.flip()

    def hud(self):
        healthWidth = int(230 * self.player.health / PLAYER_HEALT)
        if self.player.health > 60:
            col = GREEN
        elif self.player.health > 30:
            col = YELLOW
        else:
            col = RED

        self.health_bar = pg.Rect(5, 8, healthWidth, 30)
        pg.draw.rect(self.screen, col, self.health_bar)

        self.draw_text('BB8 ENERGY: {}%'.format(self.player.health), 24,
        BLACK, 120, 10)

    def show_start_screen(self):
        # game splash/start screen
        # self.screen.fill(BGCOLOR)
        splashImg = pg.image.load(self.splash).convert()
        self.screen.blit(splashImg, (0, 0))

        self.draw_text(TITLE, 48, WHITE, WIDTH / 5, HEIGHT / 2)
        self.draw_text("Arrows to move, Space to jump, B to shoot", 22, WHITE, WIDTH / 5, 100 + HEIGHT / 2)
        self.draw_text("Press ENTER to play", 22, WHITE, WIDTH / 5, HEIGHT * 4 / 5)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press ENTER to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()

        pg.time.wait(1200)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
