# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)



import pygame
import xml.etree.ElementTree as ET

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)


    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]


    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


    def load_from_dict(self, rects, colorkey = None):
        return [self.image_at((k[0], k[1], k[2], k[3]), colorkey) for k in rects.values()]


    def load_from_xml(self, filename, colorkey = None):
        tree = ET.parse(filename)
        root = tree.getroot()

        sprites = {}

        for subtexture in root.findall("SubTexture"):
            name = subtexture.get("name")
            x = int(subtexture.get("x"))
            y = int(subtexture.get("y"))
            width = int(subtexture.get("width"))
            height = int(subtexture.get("height"))

            sprites[name] = self.image_at((x, y, width, height), colorkey)

        return sprites
