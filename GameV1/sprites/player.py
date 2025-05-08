import pygame
import json
from GameV1.tools.spritesheet import SpriteSheet
from GameV1.tools.collisionhelper import CollisionHelper

def resolve_platform_collision(player, platform, velocity):
    """
    Überprüft die Kollision und passt die Spielerposition so an, dass er nicht in die Plattform bohrt.
    :param player: Spieler-Objekt
    :param platform: Plattform-Objekt
    :param velocity: Geschwindigkeit des Spielers
    """
    directions = CollisionHelper.detect_direction(player, platform)

    if "bottom" in directions:  # Kollision mit der unteren Plattformkante
        # Position des Spielers an die Plattform anpassen, um ein "Durchbohren" zu verhindern
        player.rect.bottom = platform.rect.top
        player.on_ground = True
        velocity.y = 0  # Geschwindigkeit zurücksetzen, wenn der Spieler auf dem Boden ist
    elif "top" in directions:  # Spieler trifft von oben auf die Plattform
        player.rect.top = platform.rect.bottom
        velocity.y = 0  # Geschwindigkeit zurücksetzen, wenn er auf der Plattform landet
    elif "left" in directions or "right" in directions:
        # Kollisionsbehandlung an den Seiten (optional für seitliche Kollision)
        if "left" in directions:
            player.rect.left = platform.rect.right
        elif "right" in directions:
            player.rect.right = platform.rect.left

        velocity.x = 0  # Geschwindigkeit zurücksetzen, um das Durchrutschen zu verhindern

class Player:
    def __init__(self, x, y):

        with open("assets/images/Player/p1_spritesheet.json", "r") as f:
            rects = json.loads(f.read())

        ss = SpriteSheet("assets/images/Player/p1_spritesheet.png")
        self.images = ss.load_from_dict(rects, -1)
        self.i = 4
        self.image = self.images[self.i]

        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.velocity_y = 0



    def update(self, platforms):

        self.velocity_y += 1

        keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT]:
        #    self.rect.x -= 1
        #if keys[pygame.K_RIGHT]:
        #    self.rect.x += 1

        # im Player-Update
        collision_helper = CollisionHelper()

        directions = set()

        for p in platforms:
            for i in collision_helper.detect_direction(self, p):
                directions.add(i)

        if directions:
            print(f"Kollision auf Seite(n):", directions)
            if "bottom" in directions:
                self.velocity_y = -1
            if not "left" in directions and keys[pygame.K_LEFT]:
                self.rect.x -= 4
            if not "right" in directions and keys[pygame.K_RIGHT]:
                self.rect.x += 4

        if keys[pygame.K_SPACE]:
            self.velocity_y = -10



        self.rect.y += self.velocity_y



    def draw(self, screen):
        screen.blit(self.images[self.i], self.rect)
