#!/usr/bin/env python
# Pygame sprite Example
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class RollingBck(pygame.sprite.Sprite):

    def __init__(self, picture, rollSpeed=1):

        pygame.sprite.Sprite.__init__(self)

        self.rollSpeed = rollSpeed

        self.image1 = pygame.image.load(os.path.join(img_folder, picture)).convert()
        self.bX, self.bY = self.image1.get_size()

        self.image1 = pygame.transform.scale(self.image1, (2*self.bX, 2*self.bY))
        self.bX, self.bY = self.image1.get_size()

        self.image = pygame.Surface((self.bX*2, self.bY))
        self.image.blit(self.image1, (0,0))
        self.image.blit(self.image1, (self.bX,0))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        print(self.bX)

    def update(self):
        self.rect.x -= self.rollSpeed
        if self.rect.x < -self.bX:
            self.rect.x = 0


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, picture, x=WIDTH / 2, y=HEIGHT / 2, kLEFT = pygame.K_LEFT,
     kRIGHT = pygame.K_RIGHT, kJUMP = pygame.K_SPACE, jumpHeight = 50):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.y_speed = 0
        self.x_speed = 0

        self.kLEFT = kLEFT
        self.kRIGHT = kRIGHT
        self.kJUMP = kJUMP

        self.jump = False
        self.jumpHeight = jumpHeight

        self.y_init = self.rect.y

    def jumpUp(self):

        if self.jump:
            self.rect.y -= self.y_speed

            self.y_speed -= self.jumpHeight / 10


            if self.rect.y >= self.y_init:
                self.y_speed = 0
                self.rect.y = self.y_init
                self.jump = False
        else:
            keystate = pygame.key.get_pressed()
            if keystate[self.kJUMP]:
                self.jump = True
                self.y_speed = self.jumpHeight


    def update(self):

        keystate = pygame.key.get_pressed()
        if keystate[self.kLEFT]:
            self.x_speed = -8
        if keystate[self.kRIGHT]:
            self.x_speed = 8
        self.rect.x += self.x_speed


        self.jumpUp()

        if self.rect.right > 0.75*WIDTH:
            self.rect.right = 0.75*WIDTH
            if self.x_speed > 0: self.x_speed *= -1

        if self.rect.left < 0.1 * WIDTH:
            self.rect.left = 0.1 * WIDTH
            if self.x_speed < 0: self.x_speed *= -1



class Mob(pygame.sprite.Sprite):

    eggs = ['egg01.png','egg02.png','egg03.png', 'egg04.png']

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        picture = Mob.eggs[int(random.randrange(3))]
        self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()

        # self.image = pygame.Surface((50, 50))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH*1/4, 1.5*WIDTH)
        self.rect.y = random.randrange(-300, -120)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-10, -3)
        self.angle = random.randrange(-1,1)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # self.image = pygame.transform.rotate(self.image, self.angle)
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH*1/4, 1.5*WIDTH)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            picture = Mob.eggs[int(random.randrange(3))]
            self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()

class Obstacle(pygame.sprite.Sprite):

    images = []
    faces =[]

    @staticmethod
    def loaddata():
        Obstacle.faces = ['snake.png','rabbit.png','pig.png','hippo.png','elephant.png']
        Obstacle.images =[]
        for face in Obstacle.faces:
                image = pygame.image.load(os.path.join(img_folder, face)).convert_alpha()
                image = pygame.transform.scale(image, (100,100))
                Obstacle.images.append(image)


    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface((75, 75))
        # self.image.fill(RED)


        self.image = Obstacle.images[int(random.randrange(len(self.images)))]

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WIDTH*1.5, 5*WIDTH)
        self.rect.y = HEIGHT - 200 + random.randrange(-5,5)

        self.speedy = 0
        self.speedx = random.randrange(-10, -7)

    def update(self):

        self.rect.x += self.speedx

        if self.rect.right < -20: #went off screen
            self.rect.x = random.randrange(WIDTH*1.5, 5*WIDTH)
            self.speedx = random.randrange(-15, -10)
            self.rect.y = HEIGHT - 200 + random.randrange(-5,5)


def scores(name1, name2,score1, score2, font):

    scoretext=font.render("{}: {}".format(name1, score1), 1,(255,255,255))
    screen.blit(scoretext, (10, 20))

    scoretext2=font.render("{}: {}".format(name2, score2), 1,(255,255,255))
    screen.blit(scoretext2, (10, 50))







# initialize pygame and create window
pygame.init()
pygame.mixer.init()

imgBck = pygame.image.load(os.path.join(img_folder, 'desert_BG.png'))
imBx, imBy = imgBck.get_size()


WIDTH = 2*imBx
HEIGHT = 2*imBy

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font=pygame.font.Font(None,30)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
dzieci = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
rollers = pygame.sprite.Group()

mainBck = RollingBck('desert_BG.png',10)
backgrounds.add(mainBck)

Obstacle.loaddata()


tymek = Player('tymek.png', WIDTH*0.4, HEIGHT-100, kLEFT = pygame.K_a,
                kRIGHT = pygame.K_d, kJUMP = pygame.K_w)
all_sprites.add(tymek)
dzieci.add(tymek)
tymekCount = 0

malwinka = Player('malwina.png',WIDTH /4, HEIGHT-100, kLEFT = pygame.K_LEFT,
                kRIGHT = pygame.K_RIGHT, kJUMP = pygame.K_UP, jumpHeight = 65)
all_sprites.add(malwinka)
dzieci.add(malwinka)
malwinaCount = 0

totalEggs = 12

for i in range(totalEggs+2):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(4):
    r = Obstacle()
    rollers.add(r)
    all_sprites.add(r)


# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False





    # Update


    hitsMalwina = pygame.sprite.spritecollide(malwinka, mobs, False)
    if hitsMalwina:
        malwinaCount += 1

    hitsTymek = pygame.sprite.spritecollide(tymek, mobs, False)
    if hitsTymek:
        tymekCount += 1

    hitsGeneral = pygame.sprite.groupcollide(mobs, dzieci, True, False)
    if hitsGeneral:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hitsRollersM = pygame.sprite.spritecollide(malwinka, rollers, True)
    if hitsRollersM:

        malwinaCount += 5
        # if malwinaCount < 0 : malwinaCount =0

        r = Obstacle()
        rollers.add(r)
        all_sprites.add(r)

    hitsRollersT = pygame.sprite.spritecollide(tymek, rollers, True)
    if hitsRollersT:

        tymekCount += 5
        # if tymekCount < 0: tymekCount = 0

        r = Obstacle()
        rollers.add(r)
        all_sprites.add(r)



    if  tymekCount + malwinaCount < 10*totalEggs:
        mainBck.update()

        all_sprites.update()
        backgrounds.draw(screen)
        all_sprites.draw(screen)

        scores('Malwinka','Tymek',malwinaCount,tymekCount,font)

    else:
        backgrounds.draw(screen)
        all_sprites.draw(screen)

        scores('Malwinka','Tymek',malwinaCount,tymekCount,font)

        if tymekCount < malwinaCount:
            wynik=font.render("KONIEC! Wygrała Malwinka!", 1,(255,255,255))
        elif tymekCount > malwinaCount:
            wynik=font.render("KONIEC! Wygrał Tymek!", 1,(255,255,255))
        elif tymekCount == malwinaCount:
            wynik=font.render("KONIEC! Remis! Naciśnij ESC aby wznowić", 1,(255,255,255))
        else:
            wynik=font.render("KONIEC! Naciśnij ESC aby wznowić", 1,(255,255,255))

        scores('Malwinka','Tymek',malwinaCount,tymekCount,font)
        screen.blit(wynik, (WIDTH/2, 150))



        for mob in mobs.sprites():
            mob.kill()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_ESCAPE]:
            for i in range(totalEggs+2):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)

            malwinaCount, tymekCount = 0, 0



    pygame.display.flip()

pygame.quit()
