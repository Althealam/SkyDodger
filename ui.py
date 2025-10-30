import pygame
from settings import W, H, WHITE, GRAY

def draw_hud(screen, font, score, best, paused, alive_time):
    text = font.render(f"Score: {score}   Best: {best}", True, WHITE)
    screen.blit(text, (12, 10))
    if paused:
        tip = font.render("Paused - Press P to Resume", True, WHITE)
        screen.blit(tip, (W//2 - tip.get_width()//2, H//2 - 60))
    ttxt = font.render(f"Time: {alive_time:.1f}s", True, WHITE)
    screen.blit(ttxt, (W - ttxt.get_width() - 12, 10))

def draw_frame(screen, SKY, SAFE_MARGIN):
    screen.fill(SKY)
    pygame.draw.rect(screen, GRAY, (SAFE_MARGIN//2, SAFE_MARGIN//2, W-SAFE_MARGIN, H-SAFE_MARGIN), 2)

def game_over_screen(screen, big_font, score, best):
    over = big_font.render("GAME OVER", True, WHITE)
    tip  = big_font.render("Press R to Restart", True, WHITE)
    info = big_font.render(f"Score: {score}   Best: {best}", True, WHITE)
    screen.blit(over, (W//2 - over.get_width()//2, H//2 - 100))
    screen.blit(info, (W//2 - info.get_width()//2, H//2 - 30))
    screen.blit(tip,  (W//2 - tip.get_width()//2,  H//2 + 40))
