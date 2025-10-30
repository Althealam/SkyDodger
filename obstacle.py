import pygame, random
from settings import H, RED, OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, w=28, h=28):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (w//2, h//2), min(w, h)//2)
        self.rect = self.image.get_rect(midtop=(x, -h))
        self.vy = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED)

    def update(self):
        self.rect.y += self.vy
        if self.rect.top > H + 40:
            self.kill()
