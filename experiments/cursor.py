import pygame
import random
pg = pygame
vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


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
        self.pos = vec(self.rect.center[0], self.rect.center[1])
        self.target = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.iD = 'Item: {}'.format(random.randint(100, 900))
        self.isHigglighted = False
        self.fMouse = False
        self.damping = 0.1
        self.round = False
        self.font_name = pg.font.match_font('Arial')
        self.active = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.image.blit(text_surface, text_rect)

    def update(self):
        # any code here will happen every time the game loop updates

        if self.fMouse:
            self.pos = vec(mousePos[0], mousePos[1])
            self.higlight()
        elif self.isHigglighted:
            self.higlight_off()

        if not self.fMouse:
            # Movement equation
            self.vel += self.acc
            self.pos += self.vel

        if self.target is not self.pos:
            self.vel = (self.target - self.pos) / 5
        else:
            self.acc = vec(0, 0)
            self.vel = vec(0, 0)

        # self.acc -= self.vel * self.damping
        self.rect.center = self.pos

        if self.rect.right > WIDTH:
            self.vel.x *= -1
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.vel.x *= -1
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.vel.y *= -1
            self.rect.bottom = HEIGHT
        elif self.rect.top < 0:
            self.vel.y *= -1
            self.rect.top = 0

        # Higlighting if the task is active
        if len(drawList) > 0:
            if drawList[-1] is self:
                self.active = True
                self.image.fill(BLUE)
            else:
                self.active = False
                self.higlight_off()

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

    def followMouse(self, state):
        if state == 'Toggle':
            self.fMouse = not self.fMouse
        else:
            self.fMouse = state



class Cursor(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, color=GREEN):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, WHITE, (0, 0, 10, 10), 1)
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
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption("Sprite Example")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tasks = pygame.sprite.Group()

taskList = []
for i in range(10):
    player = Player()
    player.draw_text('Id: {}'.format(i), 12, WHITE, 3, 3)
    all_sprites.add(player)
    tasks.add(player)
    taskList.append(player)

cursor = Cursor()
all_sprites.add(cursor)
pygame.mouse.set_visible(False)

drawList = []
resized = False

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)

    # Mose position check
    mousePos = pygame.mouse.get_pos()
    (MB1, MB2, MB3) = pygame.mouse.get_pressed()

    # Moving cursor like mouse
    cursor.rect.center = mousePos

    # collisions with cursor
    cursorHit = pygame.sprite.spritecollide(cursor, tasks, False)



    for event in pygame.event.get():

        if event.type == pygame.VIDEORESIZE:
            # The main code that resizes the window:
            # (recreate the window with the new size)
            WIDTH = event.w
            HEIGHT = event.h
            print('there was resize')
            print(WIDTH, HEIGHT)

            resized = True

        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for task in tasks:
                if task in cursorHit:
                    # task.followMouse(True)
                    task.pos = vec(event.pos[0], event.pos[1])
                    task.fMouse = True

                elif task.isHigglighted:
                    task.higlight_off()



        elif event.type == pygame.MOUSEBUTTONUP:
            for task in tasks:
                if task in cursorHit:
                    if event.button == 1:
                        if task.fMouse:
                            task.followMouse(False)
                            task.pos = vec(event.pos[0], event.pos[1])
                            task.target = task.pos
                            task.vel = vec(0, 0)

                    if event.button == 3:
                        if len(drawList) > 0:
                            if task is not drawList[-1]:
                                drawList.append(task)
                        else:
                            drawList.append(task)





    # checking for in task collisions
    for task in tasks:
        for other in tasks:
            if task is not other:
                if task.rect.colliderect(other.rect):
                    # vector = task.pos - other.pos
                    # task.acc += 0.1 * vector.normalize()
                    if task.pos == other.pos:
                        task.pos += vec(10,10)
                    vy = max(task.rect.height / 2, other.rect.height / 2) - (task.pos.y - other.pos.y)
                    vx = max(task.rect.width / 2, other.rect.width / 2) - (task.pos.x - other.pos.x)

                    vector = vec(vx, vy)
                    vector = vector.normalize()
                    task.target = task.pos - 5 * vector


    # Update

    w, h = pygame.display.get_surface().get_size()

    if w != WIDTH or h != HEIGHT:
        resized = True
        WIDTH = w
        HEIGHT = h
        print('ISSSUUUEEEE')

    if resized:
        print('Im resizig it {}x{}'.format(WIDTH, HEIGHT))
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        resized = False


    all_sprites.update()

    # Draw / render
    screen.fill(WHITE)

    if len(drawList) > 1:
        for index in range(len(drawList)):
            if index < len(drawList)-1:
                pygame.draw.aaline(screen, RED, drawList[index].rect.center,
                                   drawList[index+1].rect.center)

    all_sprites.draw(screen)

    # Crosshair lines
    x = mousePos[0]
    y = mousePos[1]

    lh = pygame.draw.aaline(screen, GRAY, (0, y), (WIDTH, y), True)
    lv = pygame.draw.aaline(screen, GRAY, (x, 0), (x, HEIGHT))

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
