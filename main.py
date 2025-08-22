import pygame
import sys
import time
import os
import numpy as np
import wave
import struct

pygame.init()


WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clone Game")


BG_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 180)
CLONE_COLOR = (255, 80, 80)
TEXT_COLOR = (240, 240, 240)
ARENA_COLOR = (60, 60, 60)

font_title = pygame.font.SysFont("consolas", 48)
font = pygame.font.SysFont("consolas", 24)


player_size = 20


clock = pygame.time.Clock()
level_interval = 5000  

def gerar_beep(filename, freq=440, duration=0.2, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    amplitude = int(volume * 32767)
    t = np.linspace(0, duration, n_samples, False)
    wave_data = np.sin(2 * np.pi * freq * t)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, n_samples, 'NONE', 'not compressed'))
        for s in wave_data:
            wav_file.writeframes(struct.pack('h', int(amplitude * s)))

if not os.path.exists("clone.wav"):
    gerar_beep("clone.wav", freq=600, duration=0.15, volume=0.5)
if not os.path.exists("gameover.wav"):
    gerar_beep("gameover.wav", freq=400, duration=0.2, volume=0.6)

som_clone = pygame.mixer.Sound("clone.wav")
som_gameover = pygame.mixer.Sound("gameover.wav")


class Clone:
    def __init__(self, path, speed=3):
        self.pos = [path[0][0], path[0][1]]
        self.path = path[1:]
        self.index = 0
        self.speed = speed 

    def move(self):
        if self.index < len(self.path):
            target = self.path[self.index]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]

            if abs(dx) > self.speed or abs(dy) > self.speed:
                self.pos[0] += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pos[1] += self.speed if dy > 0 else -self.speed if dy < 0 else 0
            else:
                self.pos = list(target)
                self.index += 1

def tela_inicio():
    while True:
        WIN.fill(BG_COLOR)
        titulo = font_title.render("Clone Game", True, TEXT_COLOR)
        instrucoes = font.render("Use as setas para se mover", True, TEXT_COLOR)
        jogar = font.render("Pressione ENTER para jogar", True, TEXT_COLOR)

        WIN.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 3))
        WIN.blit(instrucoes, (WIDTH // 2 - instrucoes.get_width() // 2, HEIGHT // 2))
        WIN.blit(jogar, (WIDTH // 2 - jogar.get_width() // 2, HEIGHT // 1.5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def salvar_ranking(score):
    try:
        with open("ranking.txt", "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        scores = []

    scores.append(score)
    scores = sorted(scores, reverse=True)[:3]

    with open("ranking.txt", "w") as f:
        for s in scores:
            f.write(f"{s}\n")

    return scores

def tela_game_over(nivel_final, score):
    ranking = salvar_ranking(score)
    som_gameover.play()

    while True:
        WIN.fill(BG_COLOR)
        game_over_text = font_title.render("GAME OVER", True, CLONE_COLOR)
        nivel_text = font.render(f"Nível: {nivel_final} | Tempo: {score}s", True, TEXT_COLOR)
        restart_text = font.render("Pressione R para reiniciar", True, TEXT_COLOR)
        ranking_text = font.render("Ranking:", True, TEXT_COLOR)

        WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        WIN.blit(nivel_text, (WIDTH // 2 - nivel_text.get_width() // 2, HEIGHT // 2.8))
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(ranking_text, (WIDTH // 2 - ranking_text.get_width() // 2, HEIGHT // 1.5))

        for i, s in enumerate(ranking):
            r_text = font.render(f"{i+1}º - {s}s", True, TEXT_COLOR)
            WIN.blit(r_text, (WIDTH // 2 - r_text.get_width() // 2, HEIGHT // 1.5 + 30 + i*30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

def draw_window(player_pos, clones, level, score, arena_rect):
    WIN.fill(BG_COLOR)

    pygame.draw.rect(WIN, ARENA_COLOR, arena_rect, border_radius=15)

    pygame.draw.rect(WIN, PLAYER_COLOR, (*player_pos, player_size, player_size), border_radius=5)

    for clone in clones:
        pygame.draw.rect(WIN, CLONE_COLOR, (*clone.pos, player_size, player_size), border_radius=5)

    level_text = font.render(f"Nível: {level}", True, TEXT_COLOR)
    score_text = font.render(f"Tempo: {score}s", True, TEXT_COLOR)
    controls_text = font.render("←↑↓→ para mover", True, TEXT_COLOR)

    WIN.blit(level_text, (10, 10))
    WIN.blit(score_text, (10, 40))
    WIN.blit(controls_text, (WIDTH - controls_text.get_width() - 10, HEIGHT - 30))
    pygame.display.update()

def check_collision(player_pos, clones):
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for clone in clones:
        clone_rect = pygame.Rect(*clone.pos, player_size, player_size)
        if player_rect.colliderect(clone_rect):
            return True
    return False

def draw_window(player_pos, clones, level, score, arena_rect):
    WIN.fill(BG_COLOR)

    pygame.draw.rect(WIN, (80, 80, 80), arena_rect, 3)

    pygame.draw.rect(WIN, PLAYER_COLOR, (*player_pos, player_size, player_size), border_radius=5)

    for clone in clones:
        pygame.draw.rect(WIN, CLONE_COLOR, (*clone.pos, player_size, player_size), border_radius=5)

    level_text = font.render(f"Nível: {level}", True, TEXT_COLOR)
    score_text = font.render(f"Tempo: {score}s", True, TEXT_COLOR)
    WIN.blit(level_text, (10, 10))
    WIN.blit(score_text, (10, 40))

    pygame.display.update()

def jogo():
    player_pos = [WIDTH // 2, HEIGHT // 2]
    move_history = []
    clones = []
    clone_delay = 25
    level = 1
    level_timer = 0
    player_speed = 7
    start_time = time.time()
    arena_margin = 20

    while True:
        clock.tick(60)
        score = int(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]: player_pos[0] -= player_speed; moved = True
        if keys[pygame.K_RIGHT]: player_pos[0] += player_speed; moved = True
        if keys[pygame.K_UP]: player_pos[1] -= player_speed; moved = True
        if keys[pygame.K_DOWN]: player_pos[1] += player_speed; moved = True

        arena_rect = pygame.Rect(arena_margin, arena_margin, WIDTH - 2*arena_margin, HEIGHT - 2*arena_margin)

        player_pos[0] = max(arena_rect.left, min(arena_rect.right - player_size, player_pos[0]))
        player_pos[1] = max(arena_rect.top, min(arena_rect.bottom - player_size, player_pos[1]))

        if moved:
            move_history.append(list(player_pos))

        if len(move_history) > clone_delay:
            clone_path = move_history[:]
            for i in range(3):  
                clones.append(Clone(clone_path))
            move_history = []

            if len(clones) > 60:  
                clones.pop(0)

            try:
                som_clone.play()
            except:
                pass

        for clone in clones:
            clone.move()

        level_timer += clock.get_time()
        if level_timer >= 2500:
            level += 1
            level_timer = 0
            clone_delay = max(5, clone_delay - 4) 
            player_speed += 0.5
            arena_margin += 8 

        if check_collision(player_pos, clones):
            try:
                som_gameover.play()
            except:
                pass
            tela_game_over(level, score)
            return

        draw_window(player_pos, clones, level, score, arena_rect)


while True:
    tela_inicio()
    jogo()
