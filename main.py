import pygame ,sys,random


#general setup
pygame.init()
clock = pygame.time.Clock()

f = open("hi_score.txt", "r")
hi_score = int(f.read())
f.close()

# Setting up the main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('dino')

# Game rects
background_imgs = [pygame.image.load("assets/environment/ground_1.png"),pygame.image.load("assets/environment/ground_2.png")]
background_cactus = pygame.image.load("assets/environment/background_cactus.png")
enemies_img =[[pygame.image.load("assets/enemies/Cactus-1.png"),pygame.image.load("assets/enemies/Cactus-2.png"),pygame.image.load("assets/enemies/Cactus-3.png"),pygame.image.load("assets/enemies/Cactus-4.png"),pygame.image.load("assets/enemies/Cactus-5.png")],
{"img":[pygame.image.load("assets/enemies/bird_1.png"),pygame.image.load("assets/enemies/bird_2.png")],
"current":0}]
player_imgs = {"img":{"up":[pygame.image.load("assets/player/Dino-left-up.png"),pygame.image.load("assets/player/Dino-right-up.png")],
                    "down":[pygame.image.load("assets/player/Dino-below-left-up.png"),pygame.image.load("assets/player/Dino-below-right-up.png")]},
                "current":0}
replay_img = pygame.image.load("assets/replay.png")

speed = 0
# colors
bg_color= pygame.Color(255,255,255)
obj_color= pygame.Color(102,102,102)



#text font
font = pygame.font.Font("assets/fonts/score.ttf",24)
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
    def move(self):
        self.rect.left-=speed
class Replay:
    def __init__(self,img,x,y,scale=0.8):
        self.scale =scale
        self.set_img(img)
        self.rect = self.img.get_rect()
        self.rect.topleft=(x,y)
        self.vissible = False
    def set_img(self,img):
        width = img.get_width()
        print(width)
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*self.scale),int(height*self.scale)))     
    def draw(self):
        screen.blit(self.img,(self.rect.x,self.rect.y))
class Enemie:
    def __init__(self,img,x,y,scale=2):
        self.scale =scale
        self.set_img(img)
        self.rect = self.img.get_rect()
        self.rect.bottomleft=(x,y)
    def set_img(self,img):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*self.scale),int(height*self.scale*1.2))) 
    def draw(self):
        screen.blit(self.img,(self.rect.x,self.rect.y))
    def move(self):
        self.rect.left-=speed
class Background:
    def __init__(self,images):
        self.img1 = Obj(images[0],-1150,580)
        self.img2 = Obj(images[1],1280,580)
        self.turn = 2
    def draw(self):
        self.img1.draw()
        self.img2.draw()
    def move(self):
        self.img2.move()
        if self.img2.rect.left<=0:
            self.img1.rect.left=self.img2.rect.right
        if self.img2.rect.left>0:
            self.img1.rect.right=self.img2.rect.left
        if self.img2.rect.right<=0:
            self.img2.rect.left=screen_width
        
class Cactus:
    def __init__(self,x,y) -> None:
        self.img = Enemie(enemies_img[0][random.randint(0,4)],x,y)
    def move(self):
        self.img.move()
    def draw(self):
        self.img.draw()
class bird:
    def __init__(self,x,y) -> None:
        self.img = Enemie(enemies_img[1]["img"][0],x,y,0.1)
        self.count = 0
    def move(self):
        self.img.move()
        self.count+=1
        if self.count>=5:
            self.swap()
            self.count=0
    def swap(self):
        if enemies_img[1]["current"]==0:
            self.img.set_img(enemies_img[1]["img"][1])
            enemies_img[1]["current"]=1
        else:
            self.img.set_img(enemies_img[1]["img"][0])
            enemies_img[1]["current"]=0
    def draw(self):
        self.img.draw()


class Enemies:
    def __init__(self,x,y,s):
        self.list = [
            Cactus(x,y),
            Cactus(x+s,y),
            Cactus(x+2*s,y),
        ]
    def move(self):
        for i in range(3):
            self.list[i].move()
            if self.list[i].img.rect.right<=0:
                chois = random.randint(0,1)
                if chois and player.score>0:
                    chois = random.randint(0,2)
                    if chois==1:
                        self.list[i]=bird( self.list[(i+2)%3].img.rect.right+600,600)
                    elif chois==2:
                        self.list[i]=bird( self.list[(i+2)%3].img.rect.right+600,530)
                    else:
                        self.list[i]=bird( self.list[(i+2)%3].img.rect.right+600,510)
                else:
                    self.list[i]=Cactus( self.list[(i+2)%3].img.rect.right+600,600)
    def draw(self):
        for i in range(3):
            self.list[i].draw()
    def kill(self,player):
        for i in range(3):
            if pygame.Rect.collidepoint(self.list[i].img.rect, player.rect.center) or pygame.Rect.collidepoint(self.list[i].img.rect, player.rect.topright):
                global game_run,speed , replay_v
                game_run = False
                speed = 0
                replay.vissible = True


class Player():
    def __init__(self,img,x,y,scale=2):
        self.scale =scale
        self.y =y
        self.set_img(img)
        self.rect = self.img.get_rect()
        self.rect.bottomleft=(x,y)
        self.speed=0
        self.count=0
        self.state ="up"
        self.score = 0
    def jump(self):
        if self.rect.bottom == self.y:
            self.speed = 30
    def swap(self):
        if player_imgs["current"]==0:
            self.set_img(player_imgs["img"][self.state][1])
            player_imgs["current"]=1
        else:
            self.set_img(player_imgs["img"][self.state][0])
            player_imgs["current"]=0
        y = player.rect.bottom
        self.rect = self.img.get_rect()
        self.rect.bottomleft=(20,y)
    def process(self):
        self.score +=1
        self.count+=1
        global hi_score
        if self.count>=50/speed:
            self.swap()
            self.count=0
        if self.score > hi_score:
            hi_score = self.score
            f = open("hi_score.txt", "w")
            f.write(f"{hi_score}")
            f.close()
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
        
player = Player(player_imgs["img"]["up"][0],20,600)
background = Background(background_imgs)
enemies = Enemies(1280,600,600)

replay = Replay(replay_img,0,0)
replay.rect.center = (screen_width//2,screen_height//2)
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
                    player = Player(player_imgs["img"]["up"][0],20,600)
                    background = Background(background_imgs)
                    enemies = Enemies(1280,600,600)
                    game_run=True
                    speed=10
                    replay.vissible = False
            elif event.key == pygame.K_DOWN:
                if game_run:
                    player.state = "down"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if game_run:
                    player.state = "up"

    screen.fill(bg_color)
    if game_run:
        player.process()
        enemies.kill(player)
        speed+=0.005
        background.move()
        enemies.move()
    

    background.draw()
    enemies.draw()
    player.draw()
    if replay.vissible:
        replay.draw()

    score_text = font.render(f"HI {hi_score:07} {player.score:07}",False,obj_color)
    screen.blit(score_text,(screen_width-450,10))

    
    # Updating the window
    pygame.display.flip()
    clock.tick(30)