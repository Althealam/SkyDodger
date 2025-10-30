# player.py
import pygame, os
from settings import W, H, SAFE_MARGIN, PLAYER_SPEED, ASSET_PATH

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load(os.path.join(ASSET_PATH, "plane.png")).convert_alpha()
        scale = 0.15
        w, h = img.get_size()
        img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))

        self.image = img
        self.rect  = self.image.get_rect(center=(x, y))
        # 关键：基于透明度的像素级碰撞掩码
        self.mask  = pygame.mask.from_surface(self.image)

        self.speed = PLAYER_SPEED

    def update(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN]  - keys[pygame.K_UP])   * self.speed
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(SAFE_MARGIN, min(W - SAFE_MARGIN - self.rect.width,  self.rect.x))
        self.rect.y = max(SAFE_MARGIN, min(H - SAFE_MARGIN - self.rect.height, self.rect.y))
