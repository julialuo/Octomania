import pygame
import random

#with 1 shark everything works, with > 1 somehow one deletes itself as soon as the other appears
pygame.init()

#constants
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 700
WATER_START = 80
BTM_HEIGHT = 80
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
grey = (71, 71, 71)
yellow = (255, 255, 89)
small_font = pygame.font.SysFont('Calibri', 24)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Octopus Mania')


#easing movement
class Movement:
    timer = 0
    acceleration = 0 #1 means accelerate, -1 means decelerate, 0 means not moving
    speed = 0

    def check(self):

        if self.acceleration == 1:
            self.timer += 1

            #increase speed every 6th of a second until max speed
            if self.timer != 0 and self.speed <= MAX_SPEED and self.timer % 5 == 0:
                self.speed += 1

        if self.acceleration == -1:
            self.timer -= 1

            if self.speed == 0:
                self.timer = 0

            #decrease speed every 6th of a second until timer is 0
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

    def __init__(self, pos_input, color_input, speed_input, direction_input):
        self.pos = pos_input
        self.color = color_input
        self.speed = speed_input
        self.direction = direction_input

    def draw(self):
        pygame.draw.rect(game_display, self.color, [self.pos[0], self.pos[1], OCTOPUS_SIZE, OCTOPUS_SIZE])

    def reg_move(self, current_speed):
        if self.direction == 1:
            if self.pos[0] + current_speed > DISPLAY_WIDTH - OCTOPUS_SIZE:
                self.pos[0] = DISPLAY_WIDTH - OCTOPUS_SIZE #snap to boundary
                self.direction = -1
            else:
                self.pos[0] += current_speed

        elif self.direction == -1:
            if self.pos[0] - current_speed < 0:
                self.pos[0] = 0
                self.direction = 1
            else:
                self.pos[0] -= current_speed

    def agitated_move(self, hook_x):
        if hook_x > self.pos[0]:
            self.direction = -1
            self.reg_move(self.speed + 1)
        elif hook_x < self.pos[0]:
            self.direction = 1
            self.reg_move(self.speed + 1)
        elif self.pos[0] == 0:
            self.direction = 1
            self.reg_move(self.speed + 1)

    def fall(self):
        self.pos[1] += self.speed/2


class Shark:
    speed = 0
    size = [0, 0]
    init_side = 1 #1 is from the right, -1 is from the left
    pos = [0, 0]

    def __init__(self):
        self.speed = random.randint(1, 4)

        random_size = random.randint(1, 3)
        if random_size == 1:
            self.size = [60, 40]
        elif random_size == 2:
            self.size = [90, 60]
        else:
            self.size = [120, 80]

        random_x = random.randint(1, 2)
        if random_x == 1:
            self.init_side = -1
            self.pos[0] = -self.size[0]
        else:
            self.init_side = 1
            self.pos[0] = DISPLAY_WIDTH

        self.pos[1] = random.randint(WATER_START, DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE - self.size[1])
        print(self.speed, self.pos[0], self.pos[1], self.init_side)

    def draw(self):
        pygame.draw.rect(game_display, grey, [self.pos[0], self.pos[1], self.size[0], self.size[1]])

    def move(self):
        if self.init_side == 1:
            self.pos[0] -= self.speed
        else:
            self.pos[0] += self.speed

    def off_screen(self):
        if self.pos[0] < -self.size[0] and self.init_side == 1:
            return True
        elif self.pos[0] > DISPLAY_WIDTH and self.init_side == -1:
            return True
        else:
            return False


def draw_hook(hook_pos):
    pygame.draw.rect(game_display, black, [hook_pos[0], hook_pos[1], HOOK_WIDTH, HOOK_HEIGHT])
    for i in range(0, int(hook_pos[1])):
        pygame.draw.rect(game_display, black, [hook_pos[0], i, HOOK_WIDTH, 2])
        i += 2


def game_loop():
    game_exit = False
    score = 0
    hook_pos = [40, 40]
    up_movement = Movement()
    down_movement = Movement()
    right_movement = Movement()
    left_movement = Movement()
    octopus = [Octopus([0, DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE], red, 4, 1), Octopus([DISPLAY_WIDTH -
           OCTOPUS_SIZE, DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE], yellow, 4, -1)] #two octopus
    octopus_fall = [False, False]
    current_catch = -1 #-1 means nothing caught, otherwise will be index of octopus caught
    escape_time = 15
    escape_timer = 0
    sharks = [Shark(), Shark()]
    shark_timer = 0

    while not game_exit:

        up_movement.check()
        down_movement.check()
        right_movement.check()
        left_movement.check()

        shark_timer += 1

        print(sharks[0].speed, sharks[0].pos[0], sharks[0].pos[1], sharks[0].init_side)
        print(sharks[1].speed, sharks[1].pos[0], sharks[1].pos[1], sharks[1].init_side)

        #if shark_timer % 120 == 0:
            #sharks.append(Shark())

        for i in range(0, len(sharks)):
            sharks[i].move()

            if sharks[i].off_screen():
                del sharks[i]

        #work the escape timer
        if current_catch != -1:
            escape_timer += 1

            if escape_timer != 0 and escape_timer % 30 == 0:
                escape_time -= 1

            if escape_time == 0:
                octopus_fall[current_catch] = True
                escape_time = 15
                escape_timer = 0
                current_catch = -1

            if octopus[current_catch].pos[1] == 0:
                score += 100
                pygame.time.wait(1000)
                octopus.append(Octopus([0, DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE], octopus[current_catch].color, 4,
                                       1))
                del octopus[current_catch]
                escape_time = 15
                escape_timer = 0
                current_catch = -1

        for i in range(0, len(octopus)):
            if octopus_fall[i]:
                if octopus[i].pos[1] < DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE:
                    octopus[i].fall()
                else:
                    octopus_fall[i] = False
            elif current_catch == -1:
                if hook_pos[0] in range(int(octopus[i].pos[0]), int(octopus[i].pos[0] + OCTOPUS_SIZE - HOOK_WIDTH)):
                    if hook_pos[1] in range(int(octopus[i].pos[1] - HOOK_HEIGHT / 2), int(octopus[i].pos[1] +
                                            OCTOPUS_SIZE)):
                        current_catch = i

        for i in range(0, len(octopus)):
            if not octopus_fall[i] and current_catch != i:
                if hook_pos[1] <= DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE * 3 or current_catch != -1:
                    octopus[i].reg_move(octopus[i].speed)
                else:
                    octopus[i].agitated_move(hook_pos[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                elif event.key == pygame.K_UP and down_movement.acceleration != 1:
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
                elif event.key == pygame.K_SPACE and current_catch != -1: #drop current caught octopus
                    octopus_fall[current_catch] = True
                    escape_time = 15
                    escape_timer = 0
                    current_catch = -1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and down_movement.acceleration != 1:
                    up_movement.acceleration = -1
                elif event.key == pygame.K_DOWN and up_movement.acceleration != 1:
                    down_movement.acceleration = -1
                elif event.key == pygame.K_RIGHT and left_movement.acceleration != 1:
                    right_movement.acceleration = -1
                elif event.key == pygame.K_LEFT and right_movement.acceleration != 1:
                    left_movement.acceleration = -1

        #calculate overall change in x and y
        x_change = right_movement.speed - left_movement.speed
        y_change = down_movement.speed - up_movement.speed

        if current_catch == -1:
            #boundaries based on hook position
            if hook_pos[0] + x_change > DISPLAY_WIDTH - HOOK_WIDTH:
                x_change = DISPLAY_WIDTH - HOOK_WIDTH - hook_pos[0] #snap to boundary
            elif hook_pos[0] + x_change < 0:
                x_change = -hook_pos[0]

            if hook_pos[1] + y_change > DISPLAY_HEIGHT - BTM_HEIGHT - HOOK_HEIGHT:
                y_change = DISPLAY_HEIGHT - BTM_HEIGHT - HOOK_HEIGHT - hook_pos[1]
            elif hook_pos[1] + y_change < 0:
                y_change = -hook_pos[1]

        else:
            #boundaries based on position of caught octopus (so it doesn't go off the screen)
            if octopus[current_catch].pos[0] + x_change > DISPLAY_WIDTH - OCTOPUS_SIZE:
                x_change = DISPLAY_WIDTH - OCTOPUS_SIZE - octopus[current_catch].pos[0]
            elif octopus[current_catch].pos[0] + x_change < 0:
                x_change = -octopus[current_catch].pos[0]
            if octopus[current_catch].pos[1] + y_change > DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE:
                y_change = DISPLAY_HEIGHT - BTM_HEIGHT - OCTOPUS_SIZE - octopus[current_catch].pos[1]
            elif octopus[current_catch].pos[1] + y_change < 0:
                y_change = -octopus[current_catch].pos[1]

        hook_pos[0] += x_change
        hook_pos[1] += y_change

        #move caught octopus with hook
        if current_catch != -1:
            octopus[current_catch].pos[0] += x_change
            octopus[current_catch].pos[1] += y_change

        #draw all objects to display
        pygame.draw.rect(game_display, water_blue, [0, WATER_START, DISPLAY_WIDTH, DISPLAY_HEIGHT - WATER_START -
                                                    BTM_HEIGHT])
        pygame.draw.rect(game_display, white, [0, 0, DISPLAY_WIDTH, WATER_START])
        pygame.draw.rect(game_display, grey, [0, DISPLAY_HEIGHT - BTM_HEIGHT, DISPLAY_WIDTH, BTM_HEIGHT])

        for i in range(0, len(sharks)):
            print('draw shark ' + str(i) + ', pos: ', sharks[i].pos)
            sharks[i].draw()

        draw_hook(hook_pos)

        for i in range(len(octopus) - 1, -1, -1):
            octopus[i].draw()

        score_text = small_font.render('Score: ' + str(score), True, white)
        game_display.blit(score_text, [DISPLAY_WIDTH/2 - score_text.get_rect().width/2, DISPLAY_HEIGHT - BTM_HEIGHT + 10])
        if current_catch != -1:
            escape_text = small_font.render('Octopus will escape in ' + str(escape_time) + ' seconds...', True, white)
            game_display.blit(escape_text, [DISPLAY_WIDTH/2 - escape_text.get_rect().width/2, DISPLAY_HEIGHT -
                              escape_text.get_rect().height - 5])
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()