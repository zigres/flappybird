import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
pipe_speed = 6
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 50)
background = pygame.image.load("fon.png")
bird_img = pygame.image.load("b1.png")
pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (140, 440))
bird_img = pygame.transform.scale(bird_img, (50, 50))
background = pygame.transform.scale(background, (1200, 800))
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
        screen.fill((0,0,0))
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
                return

        pygame.display.update()
        clock.tick(60)

def game_loop():
    bird = pygame.Rect(100, 400, 50, 50)
    pipes = generate_pipes(3)
    y_move = 0
    run = True

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    y_move = -5
                if e.key == pygame.K_s:
                    y_move = 5
            if e.type == pygame.KEYUP:
                if e.key in (pygame.K_w, pygame.K_s):
                    y_move = 0

        bird.y += y_move
        if bird.top < 0:
            bird.top = 0
        if bird.bottom > 800:
            bird.bottom = 800

        for p in pipes:
            p.x -= pipe_speed

        if pipes[0].right < 0:
            pipes.pop(0)
            pipes.pop(0)
            last_x = pipes[-1].x
            new = generate_pipes(1)
            for n in new:
                n.x = last_x + 650
            pipes.extend(new)

        for p in pipes:
            if bird.colliderect(p):
                run = False

        screen.blit(background, (0, 0))
        screen.blit(bird_img, (bird.x, bird.y))
        screen.blit(pipe_img, (pipes[0].x, pipes[0].y))
        for p in pipes:
            pygame.draw.rect(screen, (0, 255, 0), p)

        pygame.display.update()
        clock.tick(60)

    show_restart()

while True:
    show_menu()
    game_loop()
