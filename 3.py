import pygame
import sounddevice as sd
import numpy as np
from random import randint

pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
pipe_speed = 6
y_vel = 0.0
gravity = 0.4
THRESH = 0.01
IMPULSE = -8.0
mic_level = 0.0
score = 0
font = pygame.font.Font(None, 80)
background = pygame.image.load("fon.png")
bird_img = pygame.image.load("b1.png")
pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (140, 440))
bird_img = pygame.transform.scale(bird_img, (50, 50))
background = pygame.transform.scale(background, (1200, 800))


def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata ** 2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = 1200
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = pygame.Rect(start_x, 0, pipe_width, height)
        bottom_pipe = pygame.Rect(start_x, height + gap, pipe_width, 800 - (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def show_menu():
    while True:
        screen.fill((0, 0, 0))
        start_button = pygame.Rect(500, 350, 200, 80)
        draw_button("Start", start_button, (0, 255, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(pygame.mouse.get_pos()):
                return
        pygame.display.update()
        clock.tick(60)

def show_restart():
    global score
    while True:
        screen.fill((0, 0, 0))
        restart_button = pygame.Rect(500, 350, 200, 80)
        draw_button("Restart", restart_button, (180, 0, 0))
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (420, 200))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(pygame.mouse.get_pos()):
                score = 0
                return
        pygame.display.update()
        clock.tick(60)

def game_loop():
    global y_vel, score
    print(sd.query_devices())
    bird = pygame.Rect(100, 400, 50, 50)
    pipes = generate_pipes(3)
    run = True
    with sd.InputStream(device=3, samplerate=40000, channels=1, blocksize=1000, callback=audio_cb):
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if mic_level > THRESH:
                y_vel = IMPULSE
            y_vel += gravity
            bird.y += int(y_vel)
            if bird.top < 0:
                bird.top = 0
                y_vel = 0
            if bird.bottom > 800:
                bird.bottom = 800
                y_vel = 0
            for p in pipes:
                p.x -= pipe_speed
            if pipes[0].right < 0:
                pipes.pop(0)
                pipes.pop(0)
                score += 1
                last_x = pipes[-1].x
                new = generate_pipes(1)
                for n in new:
                    n.x = last_x + 650
                pipes.extend(new)
            screen.blit(background, (0, 0))
            for p in pipes:
                pygame.draw.rect(screen, (0, 255, 0), p)
                if bird.colliderect(p):
                    run = False
            screen.blit(bird_img, (bird.x, bird.y))
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (0,0))
            pygame.display.update()
            clock.tick(60)
    show_restart()

while True:
    show_menu()
    game_loop()
