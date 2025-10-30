import os

# --- 全局配置 ---
W, H = 480, 720
FPS = 60
PLAYER_SPEED = 5
OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED = 3, 8
OBSTACLE_SPAWN_INTERVAL = 700
SAFE_MARGIN = 10

# --- 颜色 ---
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
SKY    = (40, 90, 180)
RED    = (235, 64, 52)
YELLOW = (252, 211, 3)
GRAY   = (210, 210, 210)
FONT_NAME = "arial"

# --- 资源路径 ---
ASSET_PATH = os.path.join("assets", "images")
