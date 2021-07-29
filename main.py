import pygame ,sys,random
import amir,talout



#general setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game rects
background_imgs = [pygame.image.load("assets/environment/ground_1.png"),pygame.image.load("assets/environment/ground_2.png")]
background_cactus = pygame.image.load("assets/environment/background_cactus.png")
player_imgs = {"img":[pygame.image.load("assets/player/dino_sprite_1.png"),pygame.image.load("assets/player/dino_sprite_2.png")],
                "current":0}
speed = 0
# colors
bg_color= pygame.Color(255,255,255)
obj_color= pygame.Color(0,206,0)



#text font
font = pygame.font.Font("freesansbold.ttf",72)
font_of_help = pygame.font.Font("freesansbold.ttf",16)

game_run = False
class Obj:
    def __init__(self,img,x,y,scale=0.1):
        self.scale =scale
        self.set_img(img)
        self.rect = self.img.get_rect()
        self.rect.topleft=(x,y)
    def set_img(self,img):
        width = img.get_width()
        print(width)
        height = img.get_height()
        self.img = pygame.transform.scale(img,(screen_width,int(height*self.scale)))    
    def draw(self):
        screen.blit(self.img,(self.rect.x,self.rect.y))
    def move(self,speed):
        self.rect.left-=speed
class Background:
    def __init__(self,images):
        self.img1 = Obj(images[0],0,580)
        self.img2 = Obj(images[1],1280,580)
        global speed 
        speed = 0
    def draw(self):
        self.img1.draw()
        self.img2.draw()
    def move(self):
        self.img1.move(speed)
        self.img2.move(speed)
        if self.img2.rect.left<=0:
            self.img1.rect.left=self.img2.rect.right
        if self.img1.rect.left<=0:
            self.img2.rect.left=self.img1.rect.right



class Player():
    def __init__(self,img,x,y,scale=0.05):
        self.scale =scale
        self.set_img(img)
        self.rect = self.img.get_rect()
        self.rect.bottomleft=(x,y)
        self.speed=0
        self.count=0
    def jump(self):
        self.speed = 30
    def swap(self):
        if player_imgs["current"]==0:
            self.set_img(player_imgs["img"][1])
            player_imgs["current"]=1
        else:
            self.set_img(player_imgs["img"][0])
            player_imgs["current"]=0
    def process(self):
        self.count+=1
        if self.count>=50/speed:
            self.swap()
            self.count=0
        
        # TODO : we made flapi bird
        self.rect.bottom-=self.speed 
        if self.rect.bottom<600:
            self.speed-=3
        elif self.rect.bottom>600:
            self.rect.bottom=600
            self.speed=0


    def draw(self):
        screen.blit(self.img,(self.rect.x,self.rect.y))
    def set_img(self,img):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*self.scale),int(height*self.scale)))
        
player = Player(player_imgs["img"][0],20,600)
background = Background(background_imgs)
#loop
while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_run:
                    player.jump()
                else:
                    game_run=True
                    speed=5

    screen.fill(bg_color)
    if game_run:
        player.process()
        speed+=0.01
    background.move()

    background.draw()
    player.draw()

    
    # Updating the window
    pygame.display.flip()
    clock.tick(30)