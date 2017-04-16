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


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, picture, x=WIDTH / 2, y=HEIGHT / 2, kLEFT = pygame.K_LEFT, kRIGHT = pygame.K_RIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.y_speed = 5
        self.x_speed = 0

        self.kLEFT = kLEFT
        self.kRIGHT = kRIGHT

    def update(self):
        # self.x_speed = 0

        keystate = pygame.key.get_pressed()
        if keystate[self.kLEFT]:
            self.x_speed = -8
        if keystate[self.kRIGHT]:
            self.x_speed = 8
        self.rect.x += self.x_speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            if self.x_speed > 0: self.x_speed *= -1

        if self.rect.left < 0:
            self.rect.left = 0
            if self.x_speed < 0: self.x_speed *= -1

        if self.rect.bottom > HEIGHT - 10:
            self.y_speed *= -1

        if self.rect.top < 10 and self.y_speed < 0:
            self.y_speed *= -1

class Mob(pygame.sprite.Sprite):

    eggs = ['egg01.png','egg02.png','egg03.png', 'egg04.png']

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        picture = Mob.eggs[int(random.randrange(3))]
        self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -120)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-1, 1)
        self.angle = random.randrange(-1,1)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # self.image = pygame.transform.rotate(self.image, self.angle)
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            picture = Mob.eggs[int(random.randrange(3))]
            self.image = pygame.image.load(os.path.join(img_folder, picture)).convert_alpha()




def scores(name1, name2,score1, score2, font):

    scoretext=font.render("{}: {}".format(name1, score1), 1,(255,255,255))
    screen.blit(scoretext, (10, 20))

    scoretext2=font.render("{}: {}".format(name2, score2), 1,(255,255,255))
    screen.blit(scoretext2, (10, 50))







# initialize pygame and create window
pygame.init()
pygame.mixer.init()

imgBck = pygame.image.load(os.path.join(img_folder, 'bck.png'))
imBx, imBy = imgBck.get_size()

WIDTH = imBx
HEIGHT = imBy

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font=pygame.font.Font(None,30)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
dzieci = pygame.sprite.Group()



tymek = Player('tymek.png', WIDTH*3/4, HEIGHT-30, kLEFT = pygame.K_a, kRIGHT = pygame.K_d)
all_sprites.add(tymek)
dzieci.add(tymek)
tymekCount = 0

malwinka = Player('malwina.png',WIDTH /4, HEIGHT-50, kLEFT = pygame.K_LEFT, kRIGHT = pygame.K_RIGHT)
all_sprites.add(malwinka)
dzieci.add(malwinka)
malwinaCount = 0

totalEggs = 12

for i in range(totalEggs+2):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

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

    # Draw / render
    # screen.fill(BLUE)

    if  tymekCount + malwinaCount < totalEggs:
        all_sprites.update()
        screen.blit(imgBck, (0,0))

        all_sprites.draw(screen)
        # *after* drawing everything, flip the display
        scores('Malwinka','Tymek',malwinaCount,tymekCount,font)

    else:
        if tymekCount < malwinaCount:
            wynik=font.render("KONIEC! Wygrała Malwinka!", 1,(255,255,255))
        elif tymekCount > malwinaCount:
            wynik=font.render("KONIEC! Wygrał Tymek!", 1,(255,255,255))
        elif tymekCount == malwinaCount:
            wynik=font.render("KONIEC! Remis! Naciśnij ESC aby wznowić", 1,(255,255,255))
        else:
            wynik=font.render("KONIEC! Naciśnij ESC aby wznowić", 1,(255,255,255))

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
