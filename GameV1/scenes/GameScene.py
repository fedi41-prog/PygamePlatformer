import pygame

from GameV1.assets.assets import AssetManager
from GameV1.core.camera import Camera
from GameV1.hud.HUDManager import HUDManager
from GameV1.sprites.Entities.coin import Coin
from GameV1.sprites.Entities.deco import Deco
from GameV1.sprites.Entities.flag import Flag
from GameV1.sprites.StaticBlocks.staticblock import StaticBlock
from GameV1.sprites.UpdateBlocks.MovingBlock import MovingBlock
from GameV1.sprites.player import Player
from GameV1.sprites.Entities.particle import ParticleManager
from GameV1.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT, ADMIN_PASSWORD

class GameScene:
    def __init__(self, game, lvl_size, static_blocks, update_blocks, entities, player, background_image, parallax=0.3):
        self.game = game
        self.level_length, self.level_height = lvl_size
        self.static_blocks = static_blocks
        self.update_blocks = update_blocks
        self.entities = entities
        self.player = player
        self.particle_manager = ParticleManager()
        self.hud_manager = HUDManager(game)

        self.admin = False
        self.password_index = 0

        # Hintergrundbild
        self.background_image = background_image
        # Parallax-Faktor (kleiner als 1 = langsamer als Vordergrund)
        self.parallax = parallax

        # Kamera initialisieren
        self.camera = Camera(game.scaled_width, game.scaled_height, self.level_length, self.level_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == ADMIN_PASSWORD[self.password_index]:
                    self.password_index += 1
                    if self.password_index == len(ADMIN_PASSWORD):
                        self.admin = True
                        self.password_index = 0
                else:
                    self.password_index = 0

    def update(self):
        self.entities = [e for e in self.entities if not getattr(e, 'to_remove', False)]

        # Update beweglicher Blocks und Entities
        for obj in self.update_blocks + self.entities:
            obj.update()
        self.particle_manager.update()

        # Spieler-Update mit allen Kollisionen
        self.player.update(self.static_blocks + self.update_blocks)

        self.hud_manager.update()

        # Kamera folgt Spieler
        self.camera.update(self.player.hitbox)

    def draw(self, screen):
        # Sichtbarer Viewport in Welt-Koordinaten
        view_rect = pygame.Rect(
            int(self.camera.offset.x),
            int(self.camera.offset.y),
            self.game.scaled_width,
            self.game.scaled_height
        )

        # Hintergrund kacheln und scrollen mit Parallax-Effekt
        bg_w, bg_h = self.background_image.get_size()
        offset_x = int(self.camera.offset.x * self.parallax) % bg_w
        for x in range(-offset_x, self.game.scaled_width, bg_w):
            for y in range(0, self.game.scaled_height, bg_h):
                screen.blit(self.background_image, (x, y))

        # Kombinierte Liste aller Objekte mit .rect und .draw
        all_drawables = self.static_blocks + self.update_blocks + self.entities

        for obj in all_drawables:
            if obj.rect.colliderect(view_rect):
                obj.draw(screen, self.camera)

        self.particle_manager.draw(screen, self.camera)

        # Spieler zeichnen
        self.player.draw(screen, self.camera)

        self.hud_manager.draw(screen)

        pygame.display.flip()

    @staticmethod
    def generate_scene_from_xml(game, filename, scale_faktor):
        import xml.etree.ElementTree as ET

        tree = ET.parse(filename)
        root = tree.getroot()

        length = int(root.get('length', 0)) * scale_faktor
        height = int(root.get('height', 0)) * scale_faktor

        # Hintergrund
        bg_elem = root.find('Background')
        bg_img = AssetManager.get(bg_elem.get('texture'))
        parallax = float(bg_elem.get('parallax', 0.5))

        # Spieler
        pl = root.find('Player')
        player = Player(
            game=game,
            x=int(pl.get('x', 0)) * scale_faktor,
            y=int(pl.get('y', 0)) * scale_faktor,
            texture_key=pl.get('textures'),
            gravity=float(pl.get("gravity")) * scale_faktor,
            max_fall_speed=int(pl.get("max_fall_speed")) * scale_faktor,
            jump_power=int(pl.get("jump_power")) * scale_faktor
        )

        static_blocks = []
        update_blocks = []
        entities = []

        # Factory-Map, die für jeden Tag das richtige Objekt baut
        factories = {
            'StaticBlock': lambda e: StaticBlock(
                x=int(e.get('x', 0)) * scale_faktor,
                y=int(e.get('y', 0)) * scale_faktor,
                texture=e.get('texture')
            ),
            'MovingBlock': lambda e: MovingBlock(
                x=int(e.get('x', 0)) * scale_faktor,
                y=int(e.get('y', 0)) * scale_faktor,
                xd=int(e.get('xd', 0)) * scale_faktor,
                yd=int(e.get('yd', 0)) * scale_faktor,
                texture=e.get('texture'),
                speed=int(e.get('speed', 2)) * scale_faktor,
                game=game
            ),
            'Flag': lambda e: Flag(
                x=int(e.get('x', 0)) * scale_faktor,
                y=int(e.get('y', 0)) * scale_faktor,
                color=e.get('color'),
                game=game
            ),
            'Coin': lambda e: Coin(
                x=int(e.get('x', 0)) * scale_faktor,
                y=int(e.get('y', 0)) * scale_faktor,
                texture=e.get('texture'),
                game=game
            ),
            'Deco': lambda e: Deco(
                x=int(e.get('x', 0)) * scale_faktor,
                y=int(e.get('y', 0)) * scale_faktor,
                texture=e.get('texture'),
                game=game
            ),
        }

        sprites_root = root.find('Sprites')
        if sprites_root is not None:
            for elem in sprites_root:
                tag = elem.tag
                if tag in factories:
                    obj = factories[tag](elem)
                    # je nach Typ in die richtige Liste
                    if tag == 'StaticBlock':
                        static_blocks.append(obj)
                    elif tag == 'MovingBlock':
                        update_blocks.append(obj)
                    else:
                        entities.append(obj)

        return GameScene(
            game=game,
            lvl_size=(length, height),
            static_blocks=static_blocks,
            update_blocks=update_blocks,
            entities=entities,
            player=player,
            background_image=bg_img,
            parallax=parallax
        )
