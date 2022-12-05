import pygame, sys, time
from settings import *
from spritegroups import Background, Dirt, Plane, Obstacle, Plane2


class TappyJet:
    # initialize the plane and set starting position
    def __init__(self):
        # set display window, activate time
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprites
        # all sprites will draw and update sprites
        self.sprites_all = pygame.sprite.Group()
        # collision sprites contains all of the things the player can collide with
        self.sprite_collisions = pygame.sprite.Group()

        # scaling factor to prevent stretch/misfit in the window
        background_height = pygame.image.load('graphics/environment/background.png').get_height()
        # do not necessarily need the image, just the dimension, hence .get_height()
        # running print on this gives a dimension height of background_height = 480
        self.scale_factor = WINDOW_HEIGHT / background_height
        # scale factor is 800/480 = 1.66, and so I apply this to the background class in spritegroups.py to
        # size the image as scale_factor

        # setting up the sprite groups
        Background(self.sprites_all, self.scale_factor)
        Dirt([self.sprites_all, self.sprite_collisions], self.scale_factor)
        self.plane = Plane(self.sprites_all, self.scale_factor / 1.8) # divide this in order to make plane smaller
        self.plane_2 = Plane2(self.sprites_all, self.scale_factor / 1.8) # divide this in order to make plane smaller



    # settings while loop, update pygame, and call the framerate, event loop, and call delta time
    def run(self):
        last_time = time.time()
        while True:

            # call delta time (continuous)
            delta_time = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                # the keydown will call the jump of the plane when pressing up and q keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        if self.active:
                            self.plane.jump()
                        else:
                            self.plane = Plane(self.sprites_all, self.scale_factor / 1.7)
                            self.active = True
                            self.start_offset = pygame.time.get_ticks()
                    elif event.key == pygame.K_w:
                        if self.active:
                            self.plane_2.jump()
                        else:
                            self.plane_2 = Plane2(self.sprites_all, self.scale_factor / 1.7)
                            self.active = True
                            self.start_offset = pygame.time.get_ticks()


                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.sprites_all, self.sprite_collisions], self.scale_factor * 1.1)

            # setting up the game logic
            self.display_surface.fill('black')
            # had to give the background a default color --> also helped display error in animation
            self.sprites_all.update(delta_time)
            # At first the dimensions for the window is too small
            self.sprites_all.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            # self.clock.tick(FRAMERATE)

# check if current file is main file, call game to run
if __name__ == '__main__':
    TJ = TappyJet()
    TJ.run()