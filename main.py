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
                      pygame.image.load('char_ani/char2.png'),
                      pygame.image.load('char_ani/char1.png'),
                      pygame.image.load('char_ani/char3.png')]  # the animation frames for the character
        self.image = self.animg[0]  # starting image for idle position

        self.x = 0  # X Position
        self.y = 0  # Y Position
        self.vel = 3  # velocity of character movement
        self.dir = ''  # direction of character (starts as nothing, moves to north, east, south, or west).


    def handle_keys(self):  # checks which key is pressed for movement.
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:  # key A, moves west/-x
            self.x -= self.vel
            self.dir = 'west'
        elif key[pygame.K_d]:  # key D, moves east/+x
            self.x += self.vel
            self.dir = 'east'
        elif key[pygame.K_w]:  # key W, moves north/+y (for pygame its actually -y because of positioning, but whatever)
            self.y -= self.vel
            self.dir = 'north'
        elif key[pygame.K_s]:  # key S, moves south/ -y (same at W)
            self.y += self.vel
            self.dir = 'south'

    def draw(self, surface):
        self.n_img = None

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
        player.draw(screen)
        player.handle_keys()



player = Player()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))

    player.char_action()

    # display action
    pygame.display.update()

    clock.tick(40)