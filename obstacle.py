# obstacle.py
import pygame, random, os
from settings import H, ASSET_PATH, OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        # === 加载贴图 ===
        img = pygame.image.load(os.path.join(ASSET_PATH, "meteor.png")).convert_alpha()
        scale = random.uniform(0.10, 0.14)
        w, h = img.get_size()
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))

        # === 初始化属性 ===
        self.image_original = img
        self.image = self.image_original
        self.rect = self.image.get_rect(midtop=(x, -img.get_height()))
        self.mask = pygame.mask.from_surface(self.image)  # ⭐ 初始 mask

        # === 动态参数 ===
        self.vy = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED)
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.randint(-4, 4)

    def update(self):
        # === 陨石旋转 ===
        self.angle = (self.angle + self.rotation_speed) % 360
        center = self.rect.center
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)  # ✅ 每帧重建 mask

        # === 下落移动 ===
        self.rect.y += self.vy

        # === 离开屏幕后删除 ===
        if self.rect.top > H + 40:
            self.kill()
