import sys
import time
import pygame
import random
from pygame.locals import *

class Paddle():
    def __init__(self, x, y, size_x, size_y, color, momentum=5):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.color = color
        self.momentum = momentum

    def SetLocation(self, x, y, size_x, size_y):
        self.rect = pygame.Rect(x, y, size_x, size_y)

    def SetMomentum(self, momentum):
        self.momentum = momentum

    def GetRect(self):
        return self.rect

    def Draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def Move(self, direction, limit=False, window_width=False):
        if limit:
            if direction:   # if direction is 1, move to the right
                self.SetLocation(window_width - self.rect[2], self.rect[1],self.rect[2],self.rect[3])
            else:           # if direction is 0, move to the left
                self.SetLocation(0, self.rect[1],self.rect[2],self.rect[3])
        else:
            if direction:   # if direction is 1, move to the right
                self.SetLocation(self.rect[0] + self.momentum, self.rect[1],self.rect[2],self.rect[3])
            else:           # if direction is 0, move to the left
                self.SetLocation(self.rect[0] - self.momentum, self.rect[1],self.rect[2],self.rect[3])

class Ball():
    def __init__(self, x, y, size_x, size_y, color, momentum=(0,0)):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.color = color
        self.is_alive = True
        if momentum == (0,0):
            self.x_momentum, self.y_momentum = self.RandomMomentum()
        else:
            self.x_momentum, self.y_momentum = momentum

    def SetLocation(self, x, y, size_x, size_y):
        self.rect = pygame.Rect(x, y, size_x, size_y)

    def SetMomentum(self, momentum):
        self.x_momentum, self.y_momentum = momentum

    def GetMomentum(self):
        return self.x_momentum, self.y_momentum

    def GetRect(self):
        return self.rect

    def RandomMomentum(self):
        x_momentum, y_momentum = random.randint(2,4), random.randint(2,4)
        return x_momentum, y_momentum

    def Draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def Move(self, x_direction, y_direction):
        if x_direction and y_direction:
            self.SetLocation(self.rect[0] + self.x_momentum, self.rect[1] + self.y_momentum, self.rect[2], self.rect[3])
        elif not x_direction and y_direction:
            self.SetLocation(self.rect[0] - self.x_momentum, self.rect[1] + self.y_momentum, self.rect[2], self.rect[3])
        elif x_direction and not y_direction:
            self.SetLocation(self.rect[0] + self.x_momentum, self.rect[1] - self.y_momentum, self.rect[2], self.rect[3])
        elif not x_direction and not y_direction:
            self.SetLocation(self.rect[0] - self.x_momentum, self.rect[1] - self.y_momentum, self.rect[2], self.rect[3])

class Target():
    def __init__(self, x, y, size_x, size_y, color):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.color = color
        self.is_alive = True

    def SetLocation(self, x, y, size_x, size_y):
        self.rect = pygame.Rect(x, y, size_x, size_y)

    def GetRect(self):
        return self.rect

    def SetColor(self, color):
        self.color = color

    def Kill(self):
        self.is_alive = False
        self.rect = False

    def Draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

class Player():
    def __init__(self, starting_score=0, lives=3):
        self.score = starting_score
        self.lives = lives
        self.age = 0

    def subtract_life(self):
        self.lives = self.lives - 1
        if self.lives == 0:
            GameOver()

    def add_score(self, new_score=20):
        self.score = self.score + new_score

    def set_age(self, start, finish):
        self.age = finish - start

    def get_age(self):
        return self.age

class Scoreboard():
    def __init__(self, x, y, size_x, size_y, font, player, font_color=(255,255,255), primary_color=(0,0,255), secondary_color=(191,191,0)):

        self.font = font
        self.font_color = font_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        #Full Scoreboard View:

        ##SCORE#############PREDCTION##############LIVES##
        ##################################################
        ###VAL################TIME##################VAL###
        ##################################################

        self.rect_background = pygame.Rect(x, y, size_x, size_y)


        self.score_title_rect = pygame.Rect(x, y, (x + (size_x / 4)), size_y / 4)
        self.prediction_left_rect =   pygame.Rect(x + (size_x / 4) + (0 * (size_x / 6)), y, size_x / 6, size_y / 4)
        self.prediction_stop_rect =   pygame.Rect(x + (size_x / 4) + (1 * (size_x / 6)), y, size_x / 6, size_y / 4)
        self.prediction_right_rect =  pygame.Rect(x + (size_x / 4) + (2 * (size_x / 6)), y, size_x / 6, size_y / 4)
        self.lives_title_rect = pygame.Rect(x + (size_x * 3/4), y, size_x / 4, size_y / 4 )


        self.score_value_rect = pygame.Rect(x, y + (size_y / 4), ((x + size_x)/4), ((size_y / 4) * 3) )
        self.age_value_rect = pygame.Rect( (x + (size_x / 4)), y + (size_y / 4), size_x / 2, size_y * 3/4)
        self.lives_value_rect = pygame.Rect(x + (size_x * 3/4), y + (size_y / 4), size_x / 4, size_y * 3/4)

        self.score_value_text_size = self.font.size(str(player.score))
        self.age_value_text_size = self.font.size(str(player.age))
        self.lives_value_text_size = self.font.size(str(player.lives))

        self.score_title_text_size = self.font.size("Score:")
        self.score_title_pos = (self.score_title_rect[0] + (self.score_title_rect[2] / 2) - (self.score_title_text_size[0] / 2), (self.score_title_rect[1] + (self.score_title_rect[3] / 2) - (self.score_title_text_size[1] / 2)))
        self.score_title_text = self.font.render("Score:", True, self.font_color)

        self.lives_title_text_size = font.size("Lives:")
        self.lives_title_pos = (self.lives_title_rect[0] + (self.lives_title_rect[2] / 2) - (self.lives_title_text_size[0] / 2), (self.lives_title_rect[1] + (self.lives_title_rect[3] / 2) - (self.lives_title_text_size[1] / 2)))
        self.lives_title_text = self.font.render("Lives:", True, self.font_color)

        self.age_value_pos = (self.age_value_rect[0] + (self.age_value_rect[2] / 2) - (self.age_value_text_size[0] / 2), (self.age_value_rect[1] + (self.age_value_rect[3] / 2) - (self.age_value_text_size[1] / 2)))

        self.UpdateScoreBoardValues(player)

        self.rect_prediction = pygame.Rect(x, y, size_x, size_y)


    def UpdateScoreBoardValues(self, player):

        self.score_value_text_size = self.font.size(str(player.score))
        self.score_value_text = self.font.render(str(player.score), True, self.font_color)
        self.score_value_pos = self.score_value_rect[0] + (self.score_value_rect[2] / 2) - (self.score_value_text_size[0] / 2), self.score_value_rect[1] + (self.score_value_rect[3] / 2) - (self.score_value_text_size[1] / 2)

        self.lives_value_text_size = self.font.size(str(player.lives))
        self.lives_value_text = self.font.render(str(player.lives), True, self.font_color)
        self.lives_value_pos = (self.lives_value_rect[0] + (self.lives_value_rect[2] / 2) - (self.lives_value_text_size[0] / 2), self.lives_value_rect[1] + (self.lives_value_rect[3] / 2) - (self.lives_value_text_size[1] / 2))

        age_val = str(int(player.age)) + 's'
        self.age_value_text_size = self.font.size(age_val)
        self.age_value_text = self.font.render(age_val, True, self.font_color)
        self.age_value_pos = (self.age_value_rect[0] + (self.age_value_rect[2] / 2) - (self.age_value_text_size[0] / 2), (self.age_value_rect[1] + (self.age_value_rect[3] / 2) - (self.age_value_text_size[1] / 2)))





    def Draw(self, window, player, font):

        pygame.draw.rect(window, self.secondary_color, self.rect_background)
        pygame.draw.rect(window, self.primary_color, self.score_title_rect)
        pygame.draw.rect(window, self.primary_color, self.lives_title_rect)
        pygame.draw.rect(window, self.secondary_color, self.score_value_rect)
        pygame.draw.rect(window, self.secondary_color, self.lives_value_rect)

        window.blit(self.score_title_text, (self.score_title_pos))
        window.blit(self.score_value_text, (self.score_value_pos))

        window.blit(self.lives_title_text, (self.lives_title_pos))
        window.blit(self.lives_value_text, (self.lives_value_pos))

        window.blit(self.age_value_text, (self.age_value_pos))


def GameOver():
    pygame.quit()
    sys.exit()

def RandomColor():
    RED, GREEN, BLUE = ( 255, 0, 0), ( 0, 255, 0), ( 0, 0, 255)
    r = random.randint(0,2)
    if r == 0:
        return RED
    elif r == 1:
        return GREEN
    elif r == 2:
        return BLUE


def main():
    pygame.init()

    fps = 60
    window_width = 640
    window_height = 640

    BLACK, WHITE = ( 0, 0, 0), ( 255, 255, 255)
    GREY_DARK, GREY_LIGHT = ( 63, 63, 63), ( 191, 191, 191)
    RED, GREEN, BLUE = ( 255, 0, 0), ( 0, 255, 0), ( 0, 0, 255)


    root_window = pygame.display.set_mode((window_width,window_height))
    root_window_rect = pygame.Rect(0,0,window_width,window_height)
    root_window_above_rect = pygame.Rect(0, -1, window_width, 1)
    root_window_below_rect = pygame.Rect(0, window_height, window_width, 1)
    root_window_left_rect = pygame.Rect(-1, 0, 1, window_height)
    root_window_right_rect = pygame.Rect(window_width, 0, 1, window_height)
    clock = pygame.time.Clock()

    window_scaling = True

    paddle_width = 400
    paddle_height = 8
    paddle_start_pos = (window_width / 2) - (paddle_width / 2), (window_height * 70 / 100) - (paddle_height / 2)
    paddle_color = BLUE
    paddle_momentum = window_width / fps # Momentum will move the paddle quickly enough to cross the screen left to right in 1 second

    ball_width = 15
    ball_height = 15
    ball_start_pos = (window_height * 5 / 10) - (ball_height / 2), (window_width * 30 / 100) - (ball_width / 2)
    ball_color = RED

    target_width = 30
    target_height = 10
    target_width_buffer = 1
    target_height_buffer = 1
    target_columns = 20
    target_rows = 4
    targets_total_width = (target_width + target_width_buffer) * target_columns
    targets_start_x = (window_width - targets_total_width) / 2
    targets_start_y = (window_height) / 50

    width = window_width
    height = window_height - (paddle_start_pos[1] + 20)
    start_pos = 0, paddle_start_pos[1] + 20
    font = pygame.font.SysFont('Arial', 30)

    player = Player(lives=100)
    scoreboard = Scoreboard(start_pos[0], start_pos[1], width, height, font, player, font_color=WHITE, primary_color=BLUE, secondary_color=BLACK)
    paddle = Paddle(paddle_start_pos[0],paddle_start_pos[1], paddle_width, paddle_height, paddle_color, momentum=paddle_momentum)
    ball = Ball(ball_start_pos[0], ball_start_pos[1], ball_width, ball_height, ball_color)
    target_list = []

    for row in range(target_rows):
        for column in range(target_columns):
            #print("Creating new target!\nLocation:\t{}".format((column * target_width, row * target_height, target_width, target_height)))
            target_list.append(Target(column * (target_width + target_width_buffer) + targets_start_x, row * (target_height + target_height_buffer) + targets_start_y, target_width, target_height, RandomColor()))


    # Game Loop
    user_input_left = False
    user_input_right = False
    ball_direction = 1,1
    paddle_collision_limiter = time.time() - 1
    target_collision_limiter = time.time() - 1
    frames = 0
    quit = False
    t = time.time()
    game_start_time = t
    while not quit:
        #Gather User Input
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 276:
                    user_input_left = True
                elif event.key == 275:
                    user_input_right = True
            elif event.type == pygame.KEYUP:
                if event.key == 276:
                    user_input_left = False
                elif event.key == 275:
                    user_input_right = False

        #Move Objects
        if user_input_left:
            if paddle.rect[0] - paddle.momentum >= 0:
                paddle.Move(0)
            else:
                paddle.Move(0, limit=True, window_width=window_width)
        elif user_input_right:
            if paddle.rect[0] + paddle.rect[2] + paddle.momentum < window_width:
                paddle.Move(1)
            else:
                paddle.Move(1, limit=True, window_width=window_width)
        ball.Move(ball_direction[0], ball_direction[1])

        #Check for Collisions
        if ball.rect.colliderect(paddle.rect):
            if time.time() - paddle_collision_limiter < 1:
                pass
            else:
                paddle_collision_limiter = time.time()

                #Adjust ball momentum if it hits a paddle corner
                #if ball.rect[0] <= paddle.rect[0]:
                #    m = ball.x_momentum
                #    m = (m * 7/10) + ((m * 3/10) * (((ball.rect[0] + ball.rect[2]) - paddle.rect[0]) / ball.rect[2]))
                #    print('Adjusting Ball X Momentum. Old: {}\tNew: {}'.format(ball.x_momentum, m))
                #    ball.SetMomentum((m, ball.y_momentum))
                #
                #elif ball.rect[0] + ball.rect[2] >= paddle.rect[0] + paddle.rect[2]:
                #    m = ball.x_momentum
                #    m = m + ((m * 3/10) * (((ball.rect[0] + ball.rect[2]) - (paddle.rect[0] + paddle.rect[2])) / ball.rect[2]))
                #    print('Adjusting Ball X Momentum. Old: {}\tNew: {}'.format(ball.x_momentum, m))
                #    ball.SetMomentum((m, ball.y_momentum))





                #Flip ball y direction
                if ball_direction[1]:
                    ball_direction = ball_direction[0], 0
                else:
                    ball_direction = ball_direction[0], 1

        if ball.rect.colliderect(root_window_above_rect):
            ball_direction = ball_direction[0], 1
        if ball.rect.colliderect(root_window_below_rect):
            player.subtract_life()
            ball.SetLocation(ball_start_pos[0], ball_start_pos[1], ball_width, ball_height)
        if ball.rect.colliderect(root_window_left_rect):
            ball_direction = 1, ball_direction[1]
        if ball.rect.colliderect(root_window_right_rect):
            ball_direction = 0, ball_direction[1]

        c=0
        for target in target_list:
            if not target.is_alive:
                pass
            elif ball.rect.colliderect(target.rect):
                target_list[c].Kill()
                player.add_score()
                print('Killed Target # {}'.format(c))
                if time.time() - target_collision_limiter > 1:
                    target_collision_limiter = time.time()
                    if ball_direction[1]:
                        ball_direction = ball_direction[0], 0
                    else:
                        ball_direction = ball_direction[0], 1
            c+=1


        #Update Scoreboard
        scoreboard.UpdateScoreBoardValues(player)

        #Draw Objects
        scoreboard.Draw(root_window, player, font)
        paddle.Draw(root_window)
        ball.Draw(root_window)
        for target in target_list:
            if target.is_alive:
                target.SetColor(RandomColor())
                target.Draw(root_window)



        clock.tick(fps)
        pygame.display.update()
        root_window.fill(GREY_LIGHT)
        new_t = time.time()
        player.set_age(game_start_time, new_t)
        #print('Frame Took: {}s'.format(t - new_t))
        t = new_t



main()
GameOver()
#
