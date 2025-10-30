import pygame
from settings import W, H, SAFE_MARGIN, YELLOW, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, w=36, h=36):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, YELLOW, [(0, h), (w//2, 0), (w, h)])
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED

    def update(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(SAFE_MARGIN, min(W - SAFE_MARGIN - self.rect.width, self.rect.x))
        self.rect.y = max(SAFE_MARGIN, min(H - SAFE_MARGIN - self.rect.height, self.rect.y))
