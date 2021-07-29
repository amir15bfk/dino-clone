import pygame
pygame.init()
pygame.display.set_mode((1000, 200))
background1 = pygame.image.load("environment/ground_1.png")
background2 = pygame.image.load("environment/ground_2.png")
background_cactus = pygame.image.load("environment/background_cactus.png")

def gameWorld():
    screen.fill()
#Game loop
while True:
    pygame.time.delay(100)
