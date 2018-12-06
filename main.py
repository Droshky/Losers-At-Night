'''

DONE:
    Initialization, could still use clean up.

REVIEW:
    Check with everyone on moving only in NSEW or in diagonal direction as well
                (just change lines for 'player.handle_keys()' from elifs to ifs.

    How many animation frames were working with on movement.

TO-DO:
    Work on animating the steps into the character movement.
    Add in borders/collision detection of walls or any other boundaries

'''

import pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))  # choose a better size later

clock = pygame.time.Clock()

object_list = pygame.sprite.Group()


class Player:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animg = [pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char2.png'),
                      pygame.image.load('char_ani/char2.png'),
                      pygame.image.load('char_ani/char2.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char 3.png'),
                      pygame.image.load('char_ani/char 3.png'),
                      pygame.image.load('char_ani/char 3.png')]  # the animation frames for the character
        self.image = self.animg[0]  # starting image for idle position
        self.rect = self.image.get_rect()
        self.x = 0  # X Position
        self.y = 0  # Y Position
        self.vel = 3  # velocity of character movement
        self.dir = ''  # direction of character (starts as nothing, moves to north, east, south, or west).
        self.is_walking = False
        self.steps = 0

    def handle_keys(self):  # checks which key is pressed for movement.
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:  # key A, moves west/-x
            self.x -= self.vel
            self.dir = 'west'
            self.is_walking = True
        elif key[pygame.K_d]:  # key D, moves east/+x
            self.x += self.vel
            self.dir = 'east'
            self.is_walking = True
        elif key[pygame.K_w]:  # key W, moves north/+y (for pygame its actually -y because of positioning, but whatever)
            self.y -= self.vel
            self.dir = 'north'
            self.is_walking = True
        elif key[pygame.K_s]:  # key S, moves south/ -y (same at W)
            self.y += self.vel
            self.dir = 'south'
            self.is_walking = True
        else:
            self.is_walking = False

            # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
    def animation(self, rotation):
        if self.steps > len(self.animg) - 1:
            self.steps = 0
        self.step_ani = pygame.transform.rotate(self.animg[self.steps], rotation)
        screen.blit(self.step_ani, (self.x, self.y))

    def draw(self, surface):
        self.n_img = None
        if self.is_walking == True:
            self.steps += 1

            if self.dir == 'north':
                self.animation(0)
            elif self.dir == 'south':
                self.animation(180)
            elif self.dir == 'east':
                self.animation(270)
            elif self.dir == 'west':
                self.animation(90)
        else:
            if self.dir == 'south':
                self.n_img = pygame.transform.rotate(self.image, 180)
            elif self.dir == 'east':
                self.n_img = pygame.transform.rotate(self.image, 270)
            elif self.dir == 'west':
                self.n_img = pygame.transform.rotate(self.image, 90)
            else:
                self.n_img = self.image
            surface.blit(self.n_img, (self.x, self.y))

    def char_action(self):
        self.draw(screen)
        self.handle_keys()


class Wall:

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


walls = []
player = Player()
running = True

level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                                    W",
"W                         E          W",
"W                                    W",
"W                                    W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))

    player.char_action()

    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)

    if player.rect.colliderect(end_rect):
        print("rees")

    # display action
    pygame.display.update()

    clock.tick(40)