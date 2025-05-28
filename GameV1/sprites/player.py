import pygame

from GameV1.tools.tools import any_true
from GameV1.assets.assets import AssetManager
from GameV1.settings import KEYMAP
from GameV1.tools.collisionhelper import CollisionResolver

class Player:
    def __init__(self, game, x, y, texture_key, gravity, max_fall_speed, jump_power):
        self.game = game

        self.gravity, self.max_fall_speed = gravity, max_fall_speed
        self.jump_power = jump_power
        self.normal_jump_power = jump_power
        self.speed = 4
        self.spectator_speed = 8
        self.texture_key = texture_key
        self.spectator = False

        self.walkAnimation = [f"_walk{str(i).zfill(2)}.png" for i in range(1, 12)]
        self.walkStep = 0
        self.image = AssetManager.get(self.texture_key, self.texture_key + "_stand.png")

        self.rect = self.image.get_rect(topleft=(x, y))
        self.home_pos = (x, y)

        self._create_hitbox()

        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.direction = "right"

        self.slam_active = False
        self.slam_speed = 40
        self.slam_cooldown = 0

        self.collision_resolver = CollisionResolver(gravity=self.gravity, max_fall_speed=self.max_fall_speed)


    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.spectator:
            if any_true(keys, KEYMAP["jump"]):
                self.hitbox.y -= self.spectator_speed
            if any_true(keys, KEYMAP["left"]):
                self.hitbox.x -= self.spectator_speed
                self.direction = "left"
            if any_true(keys, KEYMAP["right"]):
                self.hitbox.x += self.spectator_speed
                self.direction = "right"
            if any_true(keys, KEYMAP["duck"]):
                self.hitbox.y += self.spectator_speed

        else:
            if self.slam_cooldown == 0:
                if any_true(keys, KEYMAP["jump"]) and self.on_ground:
                    self.velocity.y = -self.jump_power
                if any_true(keys, KEYMAP["left"]):
                    self.velocity.x = -self.speed
                    self.direction = "left"
                elif any_true(keys, KEYMAP["right"]):
                    self.velocity.x = self.speed
                    self.direction = "right"
                else:
                    self.velocity.x = 0
            else:
                self.velocity.x = 0

            if any_true(keys, KEYMAP["duck"]) and not self.on_ground and self.slam_cooldown == 0:
                self.slam_active = True
                self.velocity.y = self.slam_speed

        if any_true(keys, KEYMAP["home"]):
            self.hitbox.topleft = self.home_pos

        if any_true(keys, KEYMAP["spectator_mode"]) and self.game.scene.admin:
            self.spectator = True
        elif any_true(keys, KEYMAP["normal_mode"]):
            self.spectator = False




    def update(self, platforms):
        self.handle_input()

        if not self.spectator:
            self.collision_resolver.resolve_vertical(self, platforms)
            self.collision_resolver.resolve_horizontal(self, platforms)

        if self.on_ground and self.slam_active:
            self.trigger_slam_effect()
            self.slam_active = False
            self.slam_cooldown = 30

        if self.slam_cooldown > 0:
            self.slam_cooldown -= 1

        if self.hitbox.y > self.game.scene.level_height:
            self.hitbox.topleft = self.home_pos


        self.sync_rect()

    def trigger_slam_effect(self):
        print("BOOM!")  # Placeholder für Schockwellenlogik
        self.game.scene.particle_manager.emit(self.hitbox.midbottom, 1000)

    def draw(self, screen, camera):
        self.update_image()
        screen.blit(self.image, camera.apply(self.rect))
        # pygame.draw.rect(screen, (0, 255, 0), camera.apply(self.hitbox), 2)

    def update_image(self):
        if not self.on_ground:
            self.image = AssetManager.get(self.texture_key, self.texture_key + "_jump.png")
        elif self.velocity.x != 0:
            self.image = AssetManager.get(self.texture_key + "Walk",
                                          self.texture_key + self.walkAnimation[int(self.walkStep)])
            self.walkStep += 0.35
            if self.walkStep >= len(self.walkAnimation):
                self.walkStep = 0
        else:
            if self.slam_cooldown <= 0:
                self.image = AssetManager.get(self.texture_key, self.texture_key + "_stand.png")
            else:
                # Hole das Duck-Bild
                duck_image = AssetManager.get(self.texture_key, self.texture_key + "_duck.png")

                # Erstelle Surface mit voller Spielergröße und zentriere duck_image unten
                full_size_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                duck_rect = duck_image.get_rect()
                duck_rect.midbottom = full_size_image.get_rect().midbottom
                full_size_image.blit(duck_image, duck_rect)
                self.image = full_size_image

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def _create_hitbox(self):
        margin = 10
        hitbox_width = self.rect.width - margin * 2
        hitbox_height = self.rect.height
        hitbox_x = self.rect.centerx - hitbox_width // 2
        hitbox_y = self.rect.bottom - hitbox_height
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
        self.update_mask()

    def update_mask(self, rect=None, shrink=5):
        if rect is None:
            rect = self.hitbox
        hitbox = pygame.Rect(shrink, 0, rect.width - 2 * shrink, rect.height)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), hitbox)
        self.mask = pygame.mask.from_surface(surface)

    def get_hitbox_rect(self):
        return pygame.Rect(8, 4, self.hitbox.width, self.hitbox.height)

    def sync_rect(self):
        self.rect.midbottom = self.hitbox.midbottom

