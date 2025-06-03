import pygame

class GameRenderer:
    def __init__(self, virtual_size, scale):
        self.virtual_width, self.virtual_height = virtual_size
        self.scale = scale
        self.window_width = int(self.virtual_width * self.scale)
        self.window_height = int(self.virtual_height * self.scale)

        # Virtuelles Surface und echter Bildschirm
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def begin_frame(self):
        self.virtual_surface.fill((0, 0, 0))  # Frame leeren

    def get_surface(self):
        return self.virtual_surface

    def end_frame(self):
        # Skalieren und anzeigen
        scaled = pygame.transform.scale(self.virtual_surface, (self.window_width, self.window_height))
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()

    def resize_if_needed(self, new_scale):
        if new_scale != self.scale:
            self.scale = new_scale
            self.window_width = int(self.virtual_width * self.scale)
            self.window_height = int(self.virtual_height * self.scale)
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))
