import pygame, sys, time
from settings import *
from spritegroups import Background, Dirt, Plane, Mountain_Obstacle, Plane2


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
        # Taron Madison helped me understand how to use sprites in my code
        self.sprites_all = pygame.sprite.Group()
        # collision sprites contains all of the things the player can collide with
        self.sprite_collisions = pygame.sprite.Group()

        # scaling factor to prevent stretch/misfit in the window
        background_height = pygame.image.load('graphics/environment/background.png').get_height()
        # Taron Madison helped me figure out that I had to use the path of the image to display it
        # do not necessarily need the image, just the dimension, hence .get_height()
        # running print on this gives a dimension height of background_height = 480
        self.scale_factor = WINDOW_HEIGHT / background_height
        # scale factor is 800/480 = 1.66, and so I apply this to the background class in spritegroups.py to
        # size the image as scale_factor

        # setting up the sprite groups
        Background(self.sprites_all, self.scale_factor)
        Dirt([self.sprites_all, self.sprite_collisions], self.scale_factor)
        self.plane = Plane(self.sprites_all, self.scale_factor / 1.8) # divide this in order to make plane smaller
        # Jordan Quiles helped me figure out that I could just divide the self.scale_factor to make it smaller
        self.plane_2 = Plane2(self.sprites_all, self.scale_factor / 1.8) # divide this in order to make plane smaller

        # setting a timer
        # this timer will help us spawn obstacles continuously
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
        # starts the timer, how long it should run

        # inserting the text fonts and scores
        # pulling text from kenney
        self.font = pygame.font.Font('graphics/font/kenvector_future.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # displaying the menu screen
        # Taron Madison helped me with displaying a menu screen
        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # adding sound effect of music
        self.music = pygame.mixer.Sound('sounds/sounds_music.wav')
        self.music.play(loops=-1)

    # creating collisions that will track when planes run into obstacles
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.sprite_collisions, False, pygame.sprite.collide_mask) \
                or self.plane.rect.top <= 0:
            for sprite in self.sprite_collisions.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            # game will reset when plane collides with obstacles
            # restarting in the game
            self.active = False
            self.plane_2.kill()
            self.plane.kill()

    # Jordan Quiles helped me with displaying the score
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            # dividing this score by 1000 to make sure score doesn't get too high too fast
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        # the score (a string) must be changed into a surface (self.font.render)
        score_surf = self.font.render(str(self.score), True, 'black')
        # from surface get a rectangle
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        # places score in middle of window, at the middle top (need x and y)
        # blit both of these on a display surface
        self.display_surface.blit(score_surf, score_rect)

    # settings while loop, update pygame, and call the framerate, event loop, and call delta time
    def run(self):
        last_time = time.time()
        while True:

            # call delta time (this makes the background and images continuous)
            delta_time = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                # the keydown will call the jump of the plane when pressing up and q keys
                # Jordan Quiles helped me turn my MOUSEBUTTONDOWN into a multiplayer KEYDOWN game for w and up
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    # this entire event loop is very similar to alien_invasion
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

                # connects the timer
                if event.type == self.obstacle_timer and self.active:
                    Mountain_Obstacle([self.sprites_all, self.sprite_collisions], self.scale_factor * 1.1)

            # setting up the game logic
            # calling methods
            self.display_surface.fill('black')
            # had to give the background a default color --> also helped display error in animation
            self.sprites_all.update(delta_time)
            # At first the dimensions for the window is too small
            self.sprites_all.draw(self.display_surface)
            # order matters, ^ draw must be above score
            self.display_score()

            # this displays the menu when collisions are detected
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
