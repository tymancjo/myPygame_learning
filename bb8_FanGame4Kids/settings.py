# game options/settings
TITLE = "BB8 Jumpy!"
WIDTH = 1280
HEIGHT = 720
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "bb8_pack_scl.png"
SHADOW = "shadow.png"
BCK_IMAGE = "main_bck.png"
FRT_IMAGE = "front.png"
MOB_IMAGES = ['probe_droid.png', 'sith_probe.png']
ROCKET_IMAGE = 'rocket.png'

# Player properties
PLAYER_ACC = 75
PLAYER_FRICTION = -.15
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25
PLAYER_SPEED_TRESHOLD = 250
PLAYER_SPEED_TRESHOLD_SLOW = 70
PLAYER_HEALT = 100
BULLET_ACC = 30
BULLET_VEL = 200
PLAYER_HEALT = 100

# MObs options
MOB_SPEED_L = 50
MOB_SPEED_H = 150

# Starting platforms
# Only one bottom platform for the moment is in use
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
