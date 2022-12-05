import pygame
from settings import *
from random import choice, randint

# class for the background
class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        # must call super method
        super().__init__(groups)
        # must add a convert() because convert() returns a copy of this image, and translates pixels that can
        # be represented w/o palette.
        background_image = pygame.image.load('graphics/environment/background.png').convert()

        # At first, the image was far too small for the window, so I had to pass in surface and scale attributes
        # and multiply the height and width of the image by a scale factor that will fit the window of 800, almost
        # like holding shift on an image to drag it and maintain its proper proportions
        # however, I wanted to be able to reuse this value to I put it in my init class as scale_factor in tappyjet.py
        # I figured out the scale factor by dividing the height of the window/ height of the background image and
        # named it scale_factor
        final_height = background_image.get_height() * scale_factor
        final_width = background_image.get_width() * scale_factor
        final_sized_image = pygame.transform.scale(background_image, (final_width, final_height))

        # Creating a surface that is twice as wide as the background image because of animation problem
        self.image = pygame.Surface((final_width * 2, final_height))
        # self.image will be twice as wide as background_image
        self.image.blit(final_sized_image, (0, 0))
        self.image.blit(final_sized_image, (final_width, 0))
        # the blit functions are drawing/placing the background image side by side, one at posn (0,0) and one
        # exactly placed to the right of that original blit so that the game does not run off of the image
        # and into a black screen as delta time continuously keeps the background image moving to the right

        # creating the image and placing it in the topleft of the window
        self.rect = self.image.get_rect(topleft=(0, 0))
        # get a vector at position (0,0)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # when using delta time, we cannot put the position in the direct attribute any more because
        # the class only stores integers, but delta time creates a lot of floating point integers, and
        # if we make them integers, we will have inconsistent movement, hence self.pos

    # animating our background to run continuously using delta time
    def update(self, delta_time):
        # whenever we move anything with delta time we have to multiply by delta time
        # set speed of frame
        self.pos.x -= 300 * delta_time
        if self.rect.centerx <= 0:
            # need to check center of the 2 background images because this is the right side of original blit
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
        # only way to get consistent movement with delta time


class Dirt(pygame.sprite.Sprite):
    # have to use scale factor so that the background and dirt stay relative to each other
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'dirt'

        # image
        ground_surf = pygame.image.load('graphics/environment/groundDirt.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        # must change to vector to multiply by number

        # places position of ground at the bottom left of screen, x 0 by default, y window height
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        # animates the ground
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # this mask will check the collisions between the plane and the ground
        self.mask = pygame.mask.from_surface(self.image)

    # very similar to Background class
    def update(self, delta_time):
        self.pos.x -= 360 * delta_time
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)


class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        # placing the planes position, adjusting the coordinates so that it is in the
        # center of window height, for x posn, dividing width by 20 because the window width
        # is 480/20 = 24
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600
        self.direction = 0
        # we need direction because our plane can go up or down

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # this calls the jump sound and sets how loud it will be
        self.jump_sound = pygame.mixer.Sound('sounds/sounds_jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'graphics/plane/planeBlue1.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    # gravity is not linear, the longer you fall, the faster you fall, and so we must model this
    def apply_gravity(self, delta_time):
        self.direction += self.gravity * delta_time
        self.pos.y += self.direction * delta_time
        self.rect.y = round(self.pos.y)

    # this depends on the direction, up or down
    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, delta_time):
        self.frame_index += 10 * delta_time
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.apply_gravity(delta_time)
        self.animate(delta_time)
        self.rotate()


# everything is the same as Plane, except that the image changes from blue to yellow
class Plane2(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.jump_sound = pygame.mixer.Sound('sounds/sounds_jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            # getting the surface
            surf = pygame.image.load(f'graphics/plane/planeYellow1.png').convert_alpha()
            # scaling the plane
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)
    def apply_gravity(self, delta_time):
        self.direction += self.gravity * delta_time
        self.pos.y += self.direction * delta_time
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, delta_time):
        self.frame_index += 10 * delta_time
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.apply_gravity(delta_time)
        self.animate(delta_time)
        self.rotate()

