import pygame

pygame.init()

imgBck = pygame.image.load('img/bck.png')
imBx, imBy = imgBck.get_size()

display_width = imBx
display_height = imBy

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')



black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False

imgBck = imgBck.convert()

gameImg1 = pygame.image.load('img/malwina.png').convert_alpha()
imx, imy = gameImg1.get_size()

gameImg2 = pygame.image.load('img/tymek.png').convert_alpha()
imx2, imy2 = gameImg2.get_size()




def car(x,y):
    gameDisplay.blit(gameImg1, (x,y))
    gameDisplay.blit(gameImg2, (x2,y2))

x =  (display_width / 4) - imx /2
y = display_height - imy -10

x2 =  (display_width *3 / 4) - imx2 /2
y2 = display_height - imy2 -10


x_change = 0
x2_change = 0

car_speed = 0

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        ############################
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5

            if event.key == pygame.K_a:
                x2_change = -5
            elif event.key == pygame.K_d:
                x2_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x2_change = 0

        ######################
    ##
    x += x_change
    x2 += x2_change

    if x > display_width - imx:  x = display_width - imx
    if x2 > display_width - imx2:  x2 = display_width - imx2

    if x<=0: x=0
    if x2<-0: x2=0


   ##
    # gameDisplay.fill(white)
    gameDisplay.blit(imgBck, (0,0))
    car(x,y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
