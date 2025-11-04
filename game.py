# game.py
import pygame, random, time, os
from settings import *
from player import Player
from obstacle import Obstacle
from ui import draw_hud, game_over_screen

def run_game(agent=None):  # ✅ 新增 agent 参数
    pygame.init()
    pygame.display.set_caption("Sky Dodger (AI Edition)")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 22)
    big_font = pygame.font.SysFont(FONT_NAME, 32, bold=True)

    # === 加载背景 ===
    bg_img = pygame.image.load(os.path.join(ASSET_PATH, "background.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (W, H))
    bg_y = 0
    bg_speed = 2

    # === Sprite组 ===
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player(W // 2, H - 120)
    all_sprites.add(player)

    # === 定时器 ===
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, OBSTACLE_SPAWN_INTERVAL)

    running, paused, game_over = True, False, False
    score, best_score, alive_time = 0, 0, 0
    start_time = time.time()

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_event and not paused and not game_over:
                x = random.randint(SAFE_MARGIN + 20, W - SAFE_MARGIN - 20)
                o = Obstacle(x)
                obstacles.add(o)
                all_sprites.add(o)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    all_sprites.empty(); obstacles.empty()
                    player = Player(W // 2, H - 120)
                    all_sprites.add(player)
                    score, alive_time = 0, 0
                    start_time = time.time()
                    game_over, paused = False, False

        keys = pygame.key.get_pressed()
        if not paused and not game_over:
            if agent is None:
                # 手动控制
                player.update(keys)
            else:
                # === AI 控制 ===
                mets_xy = [o.rect.center for o in obstacles]
                action = agent.act(player.rect.centerx, player.rect.centery, mets_xy)
                dx = dy = 0
                if action == 1: dy = -PLAYER_SPEED
                elif action == 2: dy = PLAYER_SPEED
                elif action == 3: dx = -PLAYER_SPEED
                elif action == 4: dx = PLAYER_SPEED
                player.rect.x = max(SAFE_MARGIN, min(W - SAFE_MARGIN - player.rect.width,  player.rect.x + dx))
                player.rect.y = max(SAFE_MARGIN, min(H - SAFE_MARGIN - player.rect.height, player.rect.y + dy))

            obstacles.update()
            score += 1
            alive_time = time.time() - start_time

            for o in list(obstacles):
                if o.rect.top > H//2 and not hasattr(o, "_passed"):
                    o._passed = True
                    score += 9

            # === 碰撞检测 ===
            hit = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask)
            if hit:
                best_score = max(best_score, score)
                game_over = True

        # === 背景滚动 ===
        bg_y += bg_speed
        if bg_y >= H:
            bg_y = 0
        screen.blit(bg_img, (0, bg_y))
        screen.blit(bg_img, (0, bg_y - H))

        all_sprites.draw(screen)
        draw_hud(screen, font, score, best_score, paused, alive_time)
        if game_over:
            game_over_screen(screen, big_font, score, best_score)
        pygame.display.flip()

    pygame.quit()
