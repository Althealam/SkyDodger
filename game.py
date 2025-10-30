import pygame, random, time
from settings import *
from player import Player
from obstacle import Obstacle
from ui import draw_hud, draw_frame, game_over_screen

def run_game():
    pygame.init()
    pygame.display.set_caption("Sky Dodger Modular")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 22)
    big_font = pygame.font.SysFont(FONT_NAME, 32, bold=True)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player(W//2, H - 120)
    all_sprites.add(player)

    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, OBSTACLE_SPAWN_INTERVAL)

    running, paused, game_over = True, False, False
    score, best_score, alive_time = 0, 0, 0.0
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
                    # 重置
                    all_sprites.empty(); obstacles.empty()
                    player = Player(W//2, H - 120)
                    all_sprites.add(player)
                    score, alive_time = 0, 0
                    start_time = time.time()
                    game_over, paused = False, False

        keys = pygame.key.get_pressed()
        if not paused and not game_over:
            player.update(keys)
            obstacles.update()
            score += 1
            alive_time = time.time() - start_time
            for o in list(obstacles):
                if o.rect.top > H//2 and not hasattr(o, "_passed"):
                    o._passed = True
                    score += 9
            if pygame.sprite.spritecollide(player, obstacles, False):
                best_score = max(best_score, score)
                game_over = True

        draw_frame(screen, SKY, SAFE_MARGIN)
        all_sprites.draw(screen)
        draw_hud(screen, font, score, best_score, paused, alive_time)
        if game_over:
            game_over_screen(screen, big_font, score, best_score)
        pygame.display.flip()

    pygame.quit()
