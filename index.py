import pygame
import sys
import random


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.shield_surface = pygame.image.load('shield.png')
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # get the position of you mouse
        self.screen_constraint()
        self.display_health()

    def screen_constraint(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10 + index * 40, 10))

    def getDamage(self, damage_amount):
        self.health -= damage_amount


class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.centery = self.rect.centery - self.speed
        if self.rect.centery <= -1:
            self.kill()


pygame.init()  # initiate pygame
# create a display and puts it into the screen variable
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()  # creates an object clock


# objects

s1 = SpaceShip('playerShip1_blue.png', 640, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(s1)

# m1 = Meteor('M1.png', 400, -100, 1, 4)
meteor_group = pygame.sprite.Group()


laser_group = pygame.sprite.Group()

# creating a timer

METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 100)

# this is the main game loop

while True:
    for event in pygame.event.get():  # check for the events in the game/ player inputs

        # this is a event check for a game loop
        if event.type == pygame.QUIT:  # close the game
            pygame.quit()
            sys.exit()

        if event.type == METEOR_EVENT:
            meteor_path = random.choice(('M1.png', 'M2.png', 'M3.png'))
            meteor_x_pos = random.randrange(0, 1280)
            meteor_y_pos = random.randrange(-500, -50)
            meteor_x_speed = random.randrange(-1, 1)
            meteor_y_speed = random.randrange(4, 10)
            meteor = Meteor(meteor_path, meteor_x_pos,
                            meteor_y_pos, meteor_x_speed, meteor_y_speed)
            meteor_group.add(meteor)

        if event.type == pygame.MOUSEBUTTONDOWN:
            laser = Laser('L1.png', event.pos, 10)
            laser_group.add(laser)

        # collision
        # between spaceship and meteor
        if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
            spaceship_group.sprite.getDamage(1)

        for i in laser_group:
            if pygame.sprite.spritecollide(laser, meteor_group, True):
                spaceship_group.sprite.getDamage(1)

    screen.fill((118, 54, 118))
    # this is what is drwaing the sprint on the screen

    laser_group.draw(screen)
    laser_group.update()

    spaceship_group.draw(screen)
    meteor_group.draw(screen)
    # this method updates the position of the sprite in the space_ship group
    spaceship_group.update()
    meteor_group.update()
    pygame.display.update()  # Draw frame
    clock.tick(120)  # control the frame rate
