from spritesheet_functions import SpriteSheet

import pygame

from random import randint

import constants
import platforms

import animales

import csv

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None
    animalList = None

    animalN = 0

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    SPRITE_SIZE = 72 # tamaño de cada sprite en el sprite sheet
    SPRITES_PER_ROW = 13  # número de sprites por fila en el sprite sheet
    SPRITES_PER = 11
    SPRITES = {}

    


    


    def __init__(self, player, screen):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.animalList = pygame.sprite.Group()
        self.screen = screen

        self.player = player
        for i in range(self.SPRITES_PER_ROW):
            for j in range(self.SPRITES_PER):
                sprite_id = i * self.SPRITES_PER_ROW + j + 1
                x = j * self.SPRITE_SIZE
                y = i * self.SPRITE_SIZE
                rect = pygame.Rect(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)
                self.SPRITES[sprite_id] = {'image': 'tiles_spritesheet.png', 'rect': rect}

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.animalList.update()
        lA = len(self.animalList) 
        self.animalN = lA if lA>self.animalN else self.animalN 


    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.animalList.draw(screen)


    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for animal in self.animalList:
            animal.rect.x += shift_x

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    

    def __init__(self, player, screen):

        

        with open('nivel1.csv', 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            arr = []
            for fila in lector_csv:
                arr.append([int(valor) for valor in fila])
            

        

        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("nivel11.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -7460

        # Array with type of platform, and x, y location of the platform.
        level = []
        
        desplazamientoY = 31*25+24
        
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                d=arr[i][j]
                if d!=0:
                    rectPlataforma = self.SPRITES[d]['rect']
                    if(d==135):
                        rectPlataforma.height = 36
                        level.append([(rectPlataforma.x, rectPlataforma.y+41, rectPlataforma.width, rectPlataforma.height), i*35,j*35+21-desplazamientoY, False, False])
                    else:
                        level.append([rectPlataforma, i*35,j*35-desplazamientoY, (d==20 or d==28 or d==41 or d==15 or d==57 or d==44 or d==21 or d==162), d==82])

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0], platform[4])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            if(platform[3]):
                block.rect.width = 0
            block.player = self.player
            self.platform_list.add(block)

        # Añadimos los animales al nivel
        
        for i in range(2):
            animalmrd2 = animales.Tortuga(screen, ("SpritesAnimales/Tortuga/walk.png", "SpritesAnimales/Tortuga/idle.png"))
            animalmrd2.rect.x = randint(500, 7000)
            animalmrd2.rect.y = constants.SCREEN_HEIGHT-50
            animalmrd2.player = self.player
            animalmrd2.level = self
            self.animalList.add(animalmrd2)

        for i in range(3):
            animalmrd = animales.Perro(screen, ("SpritesAnimales/Perro/walk.png", "SpritesAnimales/Perro/idle.png"))
            animalmrd.rect.x = randint(500, 2000)
            animalmrd.rect.y = 20
            animalmrd.player = self.player
            animalmrd.level = self
            self.animalList.add(animalmrd)

            animalmrd.walking_frames_r = []
            animalmrd.walking_frames_l = []
            animalmrd.idle_frames_l = []
            animalmrd.idle_frames_r = []

            sprite_sheet = SpriteSheet("SpritesAnimales/Perro/walk.png")
            sprite_sheet.scaled_sprite(1/11)
            w,h = sprite_sheet.getSize()
            wS = w//4
            for i in range(4):
                image = sprite_sheet.get_image(i*wS, 0, wS, h)
                animalmrd.walking_frames_r.append(image)
                image = pygame.transform.flip(image, True, False)
                animalmrd.walking_frames_l.append(image)
            
            sprite_sheet = SpriteSheet("SpritesAnimales/Perro/idle.png")
            sprite_sheet.scaled_sprite(1/11)
            w,h = sprite_sheet.getSize()
            wS = w//4
            for i in range(4):
                image = sprite_sheet.get_image(i*wS, 0, wS, h)
                animalmrd.idle_frames_r.append(image)
                image = pygame.transform.flip(image, True, False)
                animalmrd.idle_frames_l.append(image)
        for i in range(3):
            animalmrd = animales.Lobo(screen, ("SpritesAnimales/Perro/walk.png", "SpritesAnimales/Perro/idle.png"))
            animalmrd.rect.x = randint(500, 2000)
            animalmrd.rect.y = 20
            animalmrd.player = self.player
            animalmrd.level = self
            self.animalList.add(animalmrd)

            animalmrd.walking_frames_r = []
            animalmrd.walking_frames_l = []
            animalmrd.idle_frames_l = []
            animalmrd.idle_frames_r = []

            sprite_sheet = SpriteSheet("SpritesAnimales/lobo Mexicano/walk.png")
            sprite_sheet.scaled_sprite(1/11)
            w,h = sprite_sheet.getSize()
            wS = w//4
            for i in range(4):
                image = sprite_sheet.get_image(i*wS, 0, wS, h)
                animalmrd.walking_frames_r.append(image)
                image = pygame.transform.flip(image, True, False)
                animalmrd.walking_frames_l.append(image)
            
            sprite_sheet = SpriteSheet("SpritesAnimales/lobo Mexicano/idle.png")
            sprite_sheet.scaled_sprite(1/11)
            w,h = sprite_sheet.getSize()
            wS = w//4
            for i in range(4):
                image = sprite_sheet.get_image(i*wS, 0, wS, h)
                animalmrd.idle_frames_r.append(image)
                image = pygame.transform.flip(image, True, False)
                animalmrd.idle_frames_l.append(image)

        # for anim in self.animalList:
        #     sda = anim.image
        #     for i in range(100):
        #         screen.blit(sda, (0,0))
        #         pygame.display.update()
        #         pygame.time.delay(10)
                
        
        # for i in range(6):
        #     animalmrd = animales.Perro(screen)
        #     animalmrd.rect.x = randint(500, 7200)
        #     animalmrd.rect.y = constants.SCREEN_HEIGHT-50
        #     animalmrd.player = self.player
        #     animalmrd.level = self
        #     self.animalList.add(animalmrd)
        # for i in range(3):
        #     animalmrd2 = animales.Lobo(screen)
        #     animalmrd2.rect.x = randint(500, 7200)
        #     animalmrd2.rect.y = constants.SCREEN_HEIGHT-50
        #     animalmrd2.player = self.player
        #     animalmrd2.level = self
        #     self.animalList.add(animalmrd2)
        # for i in range(2):
        #     animalmrd3 = animales.Tortuga(screen)
        #     animalmrd3.rect.x = randint(500, 7200)
        #     animalmrd3.rect.y = constants.SCREEN_HEIGHT-50
        #     animalmrd3.player = self.player
        #     animalmrd3.level = self
        #     self.animalList.add(animalmrd3)

        # Add a custom moving platform
        # block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        # block.rect.x = 1350
        # block.rect.y = 280
        # block.boundary_left = 1350
        # block.boundary_right = 1600
        # block.change_x = 1
        # block.player = self.player
        # block.level = self
        # self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player, screen):

        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("bg.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_03(Level):
    """ Definition for level 3. """

    def __init__(self, player, screen):

        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("apocalipsis.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)





class Level_04(Level):
    """ Definition for level 4. """

    def __init__(self, player, screen):
        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("spacex (1).png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_05(Level):
    """ Definition for level 5. """

    

    def __init__(self, player, screen):

        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("ruin.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_06(Level):
    """ Definition for level 6. """

    def __init__(self, player, screen):

        # Call the parent constructor
        Level.__init__(self, player, screen)

        self.background = pygame.image.load("thesubmarine.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
