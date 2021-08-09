import pygame, sys, random
import numpy as np
from torch.nn import functional as F
import torch
import math


class Pong():
    def __init__(self, border=True, show=False):
        self.show = show
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.env_treffer = 0
        self.max_speed = 30
        self.opponent_score = 0
        self.done = False
        self.reward = 1
        pygame.init()
        self.clock = pygame.time.Clock()
        self.restart = False
        self.border = border

        # Main Window
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pong')

        # Colors
        self.light_grey = (200, 200, 200)
        self.bg_color = pygame.Color('grey12')

        # Game Rectangles
        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 20, self.screen_height / 2 - 70, 10, 100)
        self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10, 100)

        # Game Variables
        self.start = True
        self.first_touch_opponent = True
        self.ball_speed = 12
        self.start_speed = 5
        angle = random.uniform(45, 335)
        while True:
            if 45 < angle < 70:
                break
            elif 120 < angle < 145:
                break
            elif 200 < angle < 245:
                break
            elif 290 < angle < 335:
                break
            angle = random.uniform(45, 335)
        self.ball_speed_x = self.ball_speed * math.sin(math.radians(angle))
        self.ball_speed_y = self.ball_speed * math.cos(math.radians(angle))

        self.start_count = 0
        self.player_speed = 0
        self.opponent_speed = 5
        self.ball_moving = False
        self.score_time = True

        # Score Text
        self.score = 0
        self.opponent_score = 0
        self.basic_font = pygame.font.Font('freesansbold.ttf', 32)
        # self.env_state = [self.player.top / self.screen_height, self.opponent.top / self.screen_height, self.ball.left / self.screen_width, self.ball.top / self.screen_height, self.ball_speed_x/30, self.ball_speed_y/30]
        self.env_state = [self.player.top / self.screen_height, self.opponent.top / self.screen_height,
                          self.ball.left / self.screen_width, self.ball.top / self.screen_height,
                          self.ball_speed_x / 30, self.ball_speed_y / 30]
        # raw = [self.player.top, self.opponent.top,
        #        self.ball.left, self.ball.top,
        #        self.ball_speed_x, self.ball_speed_y]
        #
        # self.env_state = [float(i) / sum(raw) for i in raw]

    def ball_animation(self):
        if self.start:
            self.ball.x += self.ball_speed_x * self.start_speed * (1/self.ball_speed)
            self.ball.y += self.ball_speed_y * self.start_speed * (1/self.ball_speed)
        else:
            # print('ball x1 speed: ', self.ball_speed_x,end='\r')
            # print('ball y1 speed: ', self.ball_speed_y,end='\r')
            self.ball.x += self.ball_speed_x
            self.ball.y += self.ball_speed_y
            # print('ball x2 speed: ', self.ball_speed_x,end='\r')
            # print('ball y2 speed: ', self.ball_speed_y,end='\r')

        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y *= -1

        # Player Score
        if self.ball.left <= 0:
            self.restart = True
            self.score += 1
            self.reward = 2

        # Opponent Score
        if self.ball.right >= self.screen_width:
            self.restart = True
            self.reward = -2
            self.opponent_score += 1

        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            if abs(self.ball.right - self.player.left) < 10:
                self.ball_speed_x *= -1.05
                self.env_treffer += 1
            elif abs(self.ball.bottom - self.player.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1.05
                self.env_treffer += 1
            elif abs(self.ball.top - self.player.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1.05
                self.env_treffer += 1
            self.start = False

        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            if abs(self.ball.left - self.opponent.right) < 10:
                self.ball_speed_x *= -1.05
            elif abs(self.ball.bottom - self.opponent.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1.05
            elif abs(self.ball.top - self.opponent.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1.05
            self.start = False
            self.first_touch_opponent = False


    def player_animation(self):
        self.player.y += self.player_speed

        if self.border:
            if self.player.top <= 0:
                self.player.top = 0
            if self.player.bottom >= self.screen_height:
                self.player.bottom = self.screen_height


    def opponent_ai(self):
        if self.first_touch_opponent:
            self.opponent.y = self.ball.y
        else:
            if self.opponent.top < self.ball.y:
                self.opponent.y += 10
            if self.opponent.bottom > self.ball.y:
                self.opponent.y -= 10



        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    # 45 - 70 ; 120 - 145 ; 200 - 245 ; 290 - 335
    def ball_start(self):
        self.reward = 1
        self.ball.center = (self.screen_width / 2, self.screen_height / 2)
        angle = random.uniform(45, 335)
        while True:
            if 45 < angle < 70:
                break
            elif 120 < angle < 145:
                break
            elif 200 < angle < 245:
                break
            elif 290 < angle < 335:
                break
            angle = random.uniform(45, 335)
        self.ball_speed_x = self.ball_speed * math.sin(math.radians(angle))
        self.ball_speed_y = self.ball_speed * math.cos(math.radians(angle))
        # print('ball speed x: ', self.ball_speed_x)
        # print('ball speed y: ', self.ball_speed_y)
        # print('angle: ', angle)
        self.score_time = False
        self.restart = False
        self.start = True
        self.first_touch_opponent = True
        self.reward = 1



    def step(self, action):
        if self.restart:
            self.ball_start()
        if not self.done:
            if action == 0:
                self.player_speed -= 25

            if action == 1:
                self.player_speed += 25

            if self.opponent_score == 10 or self.score == 10:
                self.done = True
            # Game Logic
            self.ball_animation()
            self.player_animation()
            self.opponent_ai()



            self.screen.fill(self.bg_color)
            if self.show:
                pygame.draw.rect(self.screen, self.light_grey, self.player)
                pygame.draw.rect(self.screen, self.light_grey, self.opponent)
                pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
                pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0), (self.screen_width / 2, self.screen_height))
                player_text = self.basic_font.render(f'{self.score}', False, self.light_grey)
                self.screen.blit(player_text, (self.screen_width-50, 50))

                opponent_text = self.basic_font.render(f'{self.opponent_score}', False, self.light_grey)
                self.screen.blit(opponent_text, (50, 50))

                pygame.display.flip()

            self.env_state = [self.player.top / self.screen_height, self.opponent.top / self.screen_height,
                              self.ball.left / self.screen_width, self.ball.top / self.screen_height,
                              self.ball_speed_x / 30, self.ball_speed_y / 30]



            return np.array(self.env_state), self.reward, self.done

        else:
            return np.array(self.env_state), self.reward, self.done
            # if self.reward == 10:
            #     self.reward = 1
            #     return np.array(self.env_state), 2, self.done
            # elif self.reward == -10:
            #     self.reward = 1
            #     print('reward verloren')
            #     return np.array(self.env_state), -2, self.done
            # else:
            #     return np.array(self.env_state), 1, self.done

    def reset(self):
        self.__init__(show=self.show, border=self.border)
        return np.array(self.env_state), self.done

    def reward(self):
        return self.reward

if __name__ == '__main__':
    import time
    env = Pong(show=True, border=True)
    env.reset()
    while True:
        state, reward, done = env.step(0)
        if done:
            env.reset()
        time.sleep(0.01)

