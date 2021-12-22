import pygame, sys

def ball_animation():
    global ball_speed_x, ball_speed_y
    #ball speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #ball boundries
    if ball.top <= 0 or ball.bottom >= screen_height: #verticle axis
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width: #horizontal axis
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x += -1

pygame.init()
clock = pygame.time.Clock()

#sets up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

#draws our ball and paddles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15,  30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

ball_speed_x = 7
ball_speed_y = 7

while True:
    # Handles input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_animation()



    #visuals-background is put first. Last thing to render goes up top.
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))


    #updates the window
    pygame.display.flip()
    clock.tick(60)



