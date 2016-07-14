import pygame
import time

pygame.init()

DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 700
WATER_START = 80
HOOK_HEIGHT = 40
HOOK_WIDTH = 20
FPS = 30
MAX_SPEED = 6

clock = pygame.time.Clock()

red = (255, 0, 0)
water_blue = (68, 255, 255)
white = (255, 255, 255)

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
                self.acceleration = 0




def draw_hook(hook_pos):
    pygame.draw.rect(game_display, red, [hook_pos[0], hook_pos[1], HOOK_WIDTH, HOOK_HEIGHT])
    for i in range(0, hook_pos[1]):
        pygame.draw.rect(game_display, red, [hook_pos[0], i, HOOK_WIDTH, 2])
        i += 2


def game_loop():
    game_exit = False
    hook_pos = [40, 40]
    x_change = 0
    y_change = 0
    up_movement = Movement()
    down_movement = Movement()
    right_movement = Movement()
    left_movement = Movement()

    while not game_exit:

        up_movement.check()
        down_movement.check()
        right_movement.check()
        left_movement.check()

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

        hook_pos[0] += right_movement.speed
        hook_pos[0] -= left_movement.speed
        hook_pos[1] += down_movement.speed
        hook_pos[1] -= up_movement.speed

        pygame.draw.rect(game_display, water_blue, [0, WATER_START, DISPLAY_WIDTH, DISPLAY_HEIGHT - WATER_START])
        pygame.draw.rect(game_display, white, [0, 0, DISPLAY_WIDTH, WATER_START])
        draw_hook(hook_pos)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()