# File Name: game_loop.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# Active gameplay inner loop.  Spawns ducks, handles shooting, tracks score/lives/ammo,
# and draws the HUD overlay each frame.
# Returns ("win" | "lose", final_score) to the caller (game_manager).
#
# Uses Connor's NormalDuck / SuperDuck from models/Duck.py for all duck behaviour.
# ----------------------------------------------------------------------------------------

import os
import random
import sys

import pygame

from data_structures.my_queue import Queue
from engine.level import Level
from engine.score import calculate_score
from models.Duck import NormalDuck, SuperDuck
from models.Gun import Gun
from screens import overlay

# MACROS
WIDTH, HEIGHT      = 960, 540
FPS                = 60
FALLBACK_BG_COLOR  = (34, 85, 34)   # dark green
SPAWN_INTERVAL_SEC = 3.0             # seconds between duck spawns
SHOT_RECT_SIZE     = 10              # collision box size around cursor
GUN_DISPLAY_POS    = (800, 10)
AMMO_DISPLAY_POS   = (750, 10)

_BG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "Images")


# ──────────────────────────────────────────────────────────────────────────────
# Main run function
# ──────────────────────────────────────────────────────────────────────────────

def run(screen, clock, landscape: str = "forest", level: Level = None):
    """Active gameplay inner loop.

    Args:
        screen:    The pygame display surface.
        clock:     The pygame Clock.
        landscape: Key for the background image ("forest", "desert", "artic").
        level:     Level object; defaults to Level(1) if None.

    Returns:
        tuple: ("win" | "lose", final_score)
    """
    if level is None:
        level = Level(1)

    # Background
    bg = None
    try:
        raw = pygame.image.load(os.path.join(_BG_DIR, f"{landscape}.png")).convert()
        bg  = pygame.transform.scale(raw, (WIDTH, HEIGHT))
    except Exception:
        bg = None
    fallback_color = FALLBACK_BG_COLOR

    #Initialize the gun for the game
    gun = Gun(level.number)

    hits        = 0
    misses      = 0
    start_ticks = pygame.time.get_ticks()

    active_ducks = pygame.sprite.Group()

    # Pre-schedule duck spawns: one duck every 3 seconds
    spawn_queue: Queue = Queue()
    for i in range(level.duck_count):
        spawn_queue.enqueue(i * SPAWN_INTERVAL_SEC)

    while True:
        clock.tick(FPS)
        elapsed        = (pygame.time.get_ticks() - start_ticks) / 1000.0
        time_remaining = max(0.0, level.time_limit - elapsed)
        score          = calculate_score(hits, misses, level.number, time_remaining)

        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                    gun.reload()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if gun.current_mag > 0:
                    mx, my    = pygame.mouse.get_pos()
                    shot_rect = pygame.Rect(mx - SHOT_RECT_SIZE // 2, my - SHOT_RECT_SIZE // 2, SHOT_RECT_SIZE, SHOT_RECT_SIZE)
                    hit_list  = [d for d in active_ducks if d.life and d.rect.colliderect(shot_rect)]
                    if hit_list:
                        for duck in hit_list:
                            killed = duck.shoot()
                            if killed:
                                hits += 1
                    else:
                        misses += 1
                    gun.shoot()
                else:
                    gun.shoot()

        # ── Spawn ─────────────────────────────────────────────────────────────
        while not spawn_queue.empty() and spawn_queue.read() <= elapsed:
            spawn_queue.dequeue()
            is_special = random.random() < level.special_duck_chance
            if is_special:
                active_ducks.add(SuperDuck(level.number))
            else:
                active_ducks.add(NormalDuck(level.number))

        # ── Update ────────────────────────────────────────────────────────────
        #Call duck update method from ducks.py for movements and animation
        active_ducks.update()

        for duck in list(active_ducks):
            if duck._should_remove:
                if duck.escaped:
                    pass
                active_ducks.remove(duck)

        # ── Draw ──────────────────────────────────────────────────────────────
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(fallback_color)

        active_ducks.draw(screen)

        #Update the gun display
        gun.update()
        screen.blit(gun.image, GUN_DISPLAY_POS)
        gun.render_ammo_display(screen, AMMO_DISPLAY_POS)  #Display of ammo mag on screen
        overlay.draw(
            screen,
            score          = score,
            time_remaining = time_remaining,
        )
        pygame.display.flip()

        # ── Win / Lose checks ─────────────────────────────────────────────────
        if time_remaining <= 0:
            return ("win" if score >= level.point_threshold else "lose"), score

        # All ducks cleared and score threshold met → win early
        if spawn_queue.empty() and len(active_ducks) == 0:
            return ("intermediate" if score >= level.point_threshold else "lose"), score

        #Player runs out of ammo and ducks still left, they lose
        if gun.current_ammo == 0 and gun.current_mag ==0 and len(active_ducks) > 0:
            return "lose", score