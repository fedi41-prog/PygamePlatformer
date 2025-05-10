import pygame
import xml.etree.ElementTree as ET

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    def image_at(self, rectangle):
        "Loads image from x,y,width,height"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def images_at(self, rects):
        "Loads multiple images from a list of rectangles"
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups)

    def load_from_dict(self, rects):
        return [self.image_at((x, y, w, h)) for x, y, w, h in rects.values()]

    def load_from_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        sprites = {}

        for subtexture in root.findall("SubTexture"):
            name = subtexture.get("name")
            x = int(subtexture.get("x"))
            y = int(subtexture.get("y"))
            width = int(subtexture.get("width"))
            height = int(subtexture.get("height"))

            sprites[name] = self.image_at((x, y, width, height))

        return sprites
