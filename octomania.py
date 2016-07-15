import pygame
import time

pygame.init()

DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 700
WATER_START = 80
BTM_HEIGHT = 60
HOOK_HEIGHT = 40
HOOK_WIDTH = 20
OCTOPUS_SIZE = 60
FPS = 30
MAX_SPEED = 6

clock = pygame.time.Clock()

red = (255, 0, 0)
water_blue = (68, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (192, 192, 192)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Octopus Mania')


class Movement:
    timer = 0
    acceleration = 0
    speed = 0

    def check(self):

        if self.acceleration == 1:
            self.timer += 1

            if self.timer != 0 and self.speed <= MAX_SPEED and self.timer % 5 == 0:
                self.speed += 1

        if self.acceleration == -1:
            self.timer -= 1

            if self.speed == 0:
                self.timer = 0

            elif self.timer >= 0 and self.timer % 5 == 0:
                self.speed -= 1

            if self.timer == 0:
                self.speed = 0
                self.acceleration = 0


class Octopus:
    pos = [0, 0]
    color = [0, 0, 0]
    speed = 0
    direction = 1 #1 is right, -1 is left

    def __init__(self, pos_input, color_input, speed_input):
        self.pos = pos_input
        self.color = color_input
        self.speed = speed_input

    def draw(self):
        pygame.draw.rect(game_display, self.color, [self.pos[0], self.pos[1], OCTOPUS_SIZE, OCTOPUS_SIZE])

    def reg_move(self):
        if self.direction == 1:
            if self.pos[0] + self.speed > DISPLAY_WIDTH - OCTOPUS_SIZE:
                self.direction = -1
            else:
                self.pos[0] += self.speed

        elif self.direction == -1:
            if self.pos[0] - self.speed < 0:
                self.direction = 1
            else:
                self.pos[0] -= self.speed

    def agitated_move(self, hook_x):
        if hook_x in range (self.pos[0],  self.pos[0] + OCTOPUS_SIZE):
            self.direction = -self.direction
        self.reg_move()


def draw_hook(hook_pos):
    pygame.draw.rect(game_display, black, [hook_pos[0], hook_pos[1], HOOK_WIDTH, HOOK_HEIGHT])
    for i in range(0, hook_pos[1]):
        pygame.draw.rect(game_display, black, [hook_pos[0], i, HOOK_WIDTH, 2])
        i += 2


def game_loop():
    game_exit = False
    hook_pos = [40, 40]
    up_movement = Movement()
    down_movement = Movement()
    right_movement = Movement()
    left_movement = Movement()
    red_octopus = Octopus([0, DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE], red, 4)

    while not game_exit:

        up_movement.check()
        down_movement.check()
        right_movement.check()
        left_movement.check()

        if hook_pos[1] <= DISPLAY_HEIGHT / 2:
            red_octopus.reg_move()
        else:
            red_octopus.agitated_move(hook_pos[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and down_movement.acceleration != 1:
                    up_movement.acceleration = 1
                    up_movement.timer = 0
                elif event.key == pygame.K_DOWN and up_movement.acceleration != 1:
                    down_movement.acceleration = 1
                    down_movement.timer = 0
                elif event.key == pygame.K_RIGHT and left_movement.acceleration != 1:
                    right_movement.acceleration = 1
                    right_movement.timer = 0
                elif event.key == pygame.K_LEFT and right_movement.acceleration != 1:
                    left_movement.acceleration = 1
                    left_movement.timer = 0

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and down_movement.acceleration != 1:
                    up_movement.acceleration = -1
                elif event.key == pygame.K_DOWN and up_movement.acceleration != 1:
                    down_movement.acceleration = -1
                elif event.key == pygame.K_RIGHT and left_movement.acceleration != 1:
                    right_movement.acceleration = -1
                elif event.key == pygame.K_LEFT and right_movement.acceleration != 1:
                    left_movement.acceleration = -1

        x_change = right_movement.speed - left_movement.speed
        y_change = down_movement.speed - up_movement.speed

        if hook_pos[0] + x_change > DISPLAY_WIDTH - HOOK_WIDTH or hook_pos[0] + x_change < 0:
            x_change = 0
        if hook_pos[1] + y_change > DISPLAY_HEIGHT - BTM_HEIGHT - HOOK_HEIGHT or hook_pos[1] + y_change < 0:
            y_change = 0

        hook_pos[0] += x_change
        hook_pos[1] += y_change

        pygame.draw.rect(game_display, water_blue, [0, WATER_START, DISPLAY_WIDTH, DISPLAY_HEIGHT - WATER_START -
                                                    BTM_HEIGHT])
        pygame.draw.rect(game_display, white, [0, 0, DISPLAY_WIDTH, WATER_START])
        pygame.draw.rect(game_display, grey, [0, DISPLAY_HEIGHT - BTM_HEIGHT, DISPLAY_WIDTH, BTM_HEIGHT])
        draw_hook(hook_pos)
        red_octopus.draw()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()