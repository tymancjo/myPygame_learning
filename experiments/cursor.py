import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, color=GREEN):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.color = color
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (random.randint(25, WIDTH-25),
                            random.randint(25, HEIGHT-25))
        self.iD = 'Item: {}'.format(random.randint(100, 900))
        self.isHigglighted = False

    def update(self):
        # any code here will happen every time the game loop updates
        # self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def onMouseClick(self):
        print('Im {}'.format(self.iD))
        self.higlight()

    def higlight(self):
        if not self.isHigglighted:
            self.image.fill(RED)
            self.isHigglighted = True

    def higlight_off(self):
        self.image.fill(self.color)
        self.isHigglighted = False


class Cursor(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, color=GREEN):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((50, 50))
        pygame.draw.rect(self.image, WHITE, (0, 0, 50, 50), 1)
        self.image.set_alpha(100)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        # any code here will happen every time the game loop updates
        pass

    def onMouseClick(self):
        pass


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Example")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tasks = pygame.sprite.Group()

taskList = []
for i in range(10):
    player = Player()
    all_sprites.add(player)
    tasks.add(player)
    taskList.append(player)

cursor = Cursor()
all_sprites.add(cursor)


# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)

    # Mose position check
    mousePos = pygame.mouse.get_pos()
    (MB1, MB2, MB3) = pygame.mouse.get_pressed()
    for currentSprite in all_sprites:
        if currentSprite.rect.collidepoint(mousePos) & MB1 == 1:
            if currentSprite is not cursor:
                currentSprite.rect.center = mousePos

    # Moving cursor like mouse
    cursor.rect.center = mousePos

    # collisions with cursor
    cursorHit = pygame.sprite.spritecollide(cursor, tasks, False)

    for task in tasks:
        if task in cursorHit:
            task.onMouseClick()
        elif task.isHigglighted:
            task.higlight_off()

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(WHITE)
    for index in range(len(taskList)):
        if index < len(taskList)-1:
            pygame.draw.aaline(screen, RED, taskList[index].rect.center,
                               taskList[index+1].rect.center)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
