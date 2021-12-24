import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_x < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_x *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_x > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_x *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center(screen_width/2, screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.rect.right >= screen_height:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width / 2 - 40, screen_height/2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)



# set up
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

#window
screen_width = 1200
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

#globals

bg_color = pygame.Color("#2F37dF")
accent_color = (27, 35, 43)
basic_font = pygame.cont.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)#line in middle of

player = Player('Paddle.png', screen_width - 20, screen_height/2, 5)
opponent = Opponent('Paddle.png', 20, screen_width/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)


while True:
    # Handles exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

screen.fill(bg_color)
pygame.draw.rect(screen, accent_color, middle_strip)

game_manager.run_game()

pygame.display.flip()
clock.tick(120)






# def ball_animation():
#     global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
#     #ball speed
#
#     ball.x += ball_speed_x
#     ball.y += ball_speed_y
#
#     #ball boundries
#     if ball.top <= 0 or ball.bottom >= screen_height: #player score
#         pygame.mixer.Sound.play(pong_sound)
#         ball_speed_y *= -1
#
#     if ball.left <= 0:
#         pygame.mixer.Sound.play(score_sound)
#         player_score += 1
#         score_time = pygame.time.get_ticks()
#
#     if ball.right >= screen_width: #opponent score
#         pygame.mixer.Sound.play(score_sound)
#
#         opponent_score += 1
#         score_time = pygame.time.get_ticks()
#
#     # bounce off paddles
#     if ball.colliderect(player) and ball_speed_x > 0:
#         pygame.mixer.Sound.play(pong_sound)
#
#         if abs(ball.right - player.left) < 10:
#             ball_speed_x *= -1
#         elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1
#
#     if ball.colliderect(opponent) and ball_speed_x < 0:
#         pygame.mixer.Sound.play(pong_sound)
#
#         if abs(ball.left - opponent.right) < 10:
#             ball_speed_x *= -1
#         elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1
#
#
# def player_animation():
#     player.y += player_speed
#     if player.top <= 0:
#         player.top = 0
#     if player.bottom >= screen_height:
#         player.bottom = screen_height
#
# def opponent_ai():
#     if opponent.top < ball.y:
#         opponent.top += opponent_speed
#     if opponent.bottom > ball.y:
#         opponent.bottom -= opponent_speed
#     if opponent.top <= 0:
#         opponent.top = 0
#     if opponent.bottom >= screen_height:
#         opponent.bottom = screen_height
#
# def ball_restart():
#     global ball_speed_x, ball_speed_y, score_time
#     current_time = pygame.time.get_ticks()
#     ball.center = (screen_width/2, screen_height/2)
#
#
#     if current_time - score_time < 700:
#         number_three = game_font.render("3", False, light_grey)
#         screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
#
#     if 700 < current_time - score_time < 1400:
#         number_three = game_font.render("2", False, light_grey)
#         screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
#
#     if 1400 < current_time - score_time < 2100:
#         number_three = game_font.render("1", False, light_grey)
#         screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
#
#     if current_time - score_time < 2100:
#         ball_speed_x, ball_speed_y = 0, 0
#     else:
#         ball_speed_y = 7 * random.choice((1, -1))
#         ball_speed_x = 7 * random.choice((1, -1))
#         score_time = None
#
#     ball_speed_y *= random.choice((1, -1))
#     ball_speed_x *= random.choice((1, -1))
#
# pygame.mixer.pre_init(44100, -16, 2, 512)
# pygame.init()
# clock = pygame.time.Clock()
#
# #sets up the main window
# screen_width = 1280
# screen_height = 960
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Pong")
#
# #draws our ball and paddles
# ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15,  30, 30)
# player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
# opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)
#
# bg_color = pygame.Color('grey12')
# light_grey = (200, 200, 200)
#
# # speeds inside game
# ball_speed_x = 7 * random.choice((1, -1))
# ball_speed_y = 7 * random.choice((1, -1))
# player_speed = 0
# opponent_speed = 7
#
# # score
# player_score = 0
# opponent_score = 0
# game_font = pygame.font.Font("freesansbold.ttf", 32)
#
# #sound
# pong_sound = pygame.mixer.Sound("pong.ogg")
# score_sound = pygame.mixer.Sound("score.ogg")
#
#
# # timer
#
# score_time = True
#
#
# while True:
#     # Handles exit game
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_DOWN:
#                 player_speed += 7
#             if event.key == pygame.K_UP:
#                 player_speed -= 7
#
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_DOWN:
#                 player_speed -= 7
#             if event.key == pygame.K_UP:
#                 player_speed += 7
#
#
#     ball_animation()
#     player_animation()
#     opponent_ai()
#
#     #visuals-background is put first. Last thing to render goes up top.
#     screen.fill(bg_color)
#     pygame.draw.rect(screen, light_grey, player)
#     pygame.draw.rect(screen, light_grey, opponent)
#     pygame.draw.ellipse(screen, light_grey, ball)
#     pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
#
#     if score_time:
#         ball_restart()
#
#
#     player_text = game_font.render(f"{player_score}", False, light_grey)
#     screen.blit(player_text, (660, 470)) # position of player score
#
#     opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
#     screen.blit(opponent_text, (600, 470)) # position of enemy score
#
#     #updates the window
#     pygame.display.flip()
#     clock.tick(60)
#
#

