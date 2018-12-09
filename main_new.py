import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))  # choose a better size later
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def billboard(message, x ,y):
    text = myfont.render(message, False, (255, 255, 255))
    screen.blit(text, (x, y))

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
        self.is_walking = False  # Boolean to see if player is walking (starts animation on True)
        self.dir = ''  # direction player is facing
        self.vel = 3
        self.steps = 0
        self.n_img = self.image
        self.inventory = []
        self.is_holding = None

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

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

    def update_position(self):
        key = pygame.key.get_pressed()
        self.is_walking = True
        if key[pygame.K_a]:
            self.dir = 'west'
            player.move(-self.vel, 0)
        elif key[pygame.K_d]:
            self.dir = 'east'
            player.move(4, 0)
        elif key[pygame.K_w]:
            self.dir = 'north'
            player.move(0, -4)
        elif key[pygame.K_s]:
            self.dir = 'south'
            player.move(0, 4)
        else:
            self.is_walking = False

    def animation(self, rotation):
        if self.steps > len(self.animg) - 1:
            self.steps = 0
        self.step_ani = pygame.transform.rotate(self.animg[self.steps], rotation)
        screen.blit(self.step_ani, (self.rect.x, self.rect.y))

    def animate_character(self):
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
            screen.blit(self.n_img, (self.rect.x, self.rect.y))

    def item_interact(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            try:
                self.is_holding = self.inventory[0]
            except IndexError:
                billboard("This item slot isn't full.", 0, 0)
        elif key[pygame.K_2]:
            try:
                self.is_holding = self.inventory[1]
            except IndexError:
                billboard("This item slot isn't full.", 0, 0)
        elif key[pygame.K_3]:
            try:
                self.is_holding = self.inventory[2]
            except IndexError:
                billboard("This item slot isn't full.", 0, 0)
        elif key[pygame.K_0]:
            try:
                self.is_holding = None
            except IndexError:
                billboard("This item slot isn't full.", 0, 0)

        if key[pygame.K_SPACE]:
            if len(self.inventory) > 2:
                billboard('Your Inventory is full (Press B to drop the current item)', 0, 0)
            else:
                for w in items:
                    if self.rect.colliderect(w.rect):
                        player.inventory.append(w)
                        items.remove(w)

        if key[pygame.K_b]:
            if self.is_holding != None:
                self.is_holding.rect.x = self.rect.x
                self.is_holding.rect.y = self.rect.y
                items.append(self.is_holding)
                self.inventory.remove(self.is_holding)
                self.is_holding = None
            else:
                billboard("You're not holding anything.", 0, 0)

    def display_inv(self):
        self.display_y = 400
        for item in self.inventory:
            billboard(item.weapon_name, 0, self.display_y)
            self.display_y += 20
        if self.is_holding != None:
            billboard(f'Holding: {self.is_holding.weapon_name}', 0, 300)
        else:
            billboard('Holding: None', 0 ,300)

    def player_update(self):
        self.animate_character()
        self.item_interact()
        self.display_inv()


class Wall:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        walls.append(self)


class Weapon:
    def __init__(self, pos, weapon_type):
        self.rect = pygame.Rect(pos[0], pos[1], 8, 8)
        items.append(self)
        self.weapon_name = weapon_type



items = []
walls = []
player = Player()
running = True
print(walls)
level = [
"                                    W",
"                W                   W",
"                W                   W",
"                W                   W",
"                W                   W",
"                                    W",
"                                    W",
"                                    W",
"                     S              W",
"            S                       W",
"                                    W",
"                              S      W",
"                                    W",
"             S                      W",
"                                    W",
"                                    W",
"                                    W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]
# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == 'W':
            Wall((x, y))
        if col == 'S':
            Weapon((x, y), 'Stapler')
        x += 16
    y += 16
    x = 0
running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Move the player if an arrow key is pressed
    player.update_position()

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for item in items:
        pygame.draw.rect(screen, (255, 0, 0), item.rect)
    player.player_update()
    pygame.display.flip()
