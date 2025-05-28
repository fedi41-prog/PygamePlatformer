import pygame
import random

class Particle:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(
            random.uniform(-6, 6), random.uniform(-7, -4)
        )
        self.gravity = 0.5
        self.lifetime = random.randint(10, 20)
        self.age = 0
        self.size = random.randint(2, 4)
        self.color = (90, 90, 90)

    def update(self):
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.age += 1

    def is_alive(self):
        return self.age < self.lifetime

    def draw(self, surface, camera):
        if self.is_alive():
            alpha = max(0, 255 - int(255 * (self.age / self.lifetime)))
            particle_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, alpha), (self.size // 2, self.size // 2), self.size // 2)
            surface.blit(particle_surface, camera.apply(pygame.Rect(self.pos, (self.size, self.size))))


class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit(self, pos, amount=10):
        for _ in range(amount):
            self.particles.append(Particle(pos))

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface, camera):
        for particle in self.particles:
            particle.draw(surface, camera)
