import pygame, sys

pygame.init()
clock = pygame.time.Clock()

#sets up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15,  30, 30)

while True:
    # Handles input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #updates the window
    pygame.display.flip()
    clock.tick(60)



