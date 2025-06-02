import pygame

VIRTUAL_WIDTH = 760 # VIRTUAL_WIDTH = 768
VIRTUAL_HEIGHT = 430 # VIRTUAL_HEIGHT = 432

FPS = 60
TITLE = "Fedi4's platformer game 😎"

KEYMAP = {

    "jump" : [pygame.K_SPACE, pygame.K_w],
    "duck" : [pygame.K_s, pygame.K_LSHIFT],
    "left" : pygame.K_a,
    "right" : pygame.K_d,
    "home" : pygame.K_h,
    "spectator_mode" : pygame.K_c,
    "normal_mode" : pygame.K_v

}

ADMIN_PASSWORD = [
    pygame.K_a,
    pygame.K_d,
    pygame.K_m,
    pygame.K_i,
    pygame.K_n
]

RESOURCE_PACKS = []