import pygame

import constants

class SpriteSheet(object):
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def getSize(self):
        width, height = self.sprite_sheet.get_size()
        return (width, height)


    def get_image(self, x, y, width, height):

        # Create a new blank image
        image = pygame.Surface([int(width), int(height)]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(constants.BLACK)

        # Return the image
        return image

    def scaled_sprite(self, scale_factor):
        # Get the original size of the sprite sheet
        original_size = self.sprite_sheet.get_size()

        # Calculate the new size after scaling
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))

        # Scale the sprite sheet using pygame.transform.scale()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, new_size)
    def scaled_sprite_to_size(self, new_width, new_height):

        # Scale the sprite sheet using pygame.transform.scale()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (abs(new_width), abs(new_height)))
