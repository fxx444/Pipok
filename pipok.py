import pygame
import sys

WIDTH, HEIGHT = 1000, 800
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 3, 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Пипок")

font_big = pygame.font.SysFont("comicsansms", 64, bold=True)
font_small = pygame.font.SysFont("comicsansms", 36, bold=True)

paddle_img = pygame.image.load("racket.png").convert_alpha()
paddle_img = pygame.transform.smoothscale(paddle_img, (20*4, 120)) 
ball_img = pygame.image.load("tenis_ball.png").convert_alpha()
ball_img = pygame.transform.smoothscale(ball_img, (64, 64))         

PADDLE_WIDTH, PADDLE_HEIGHT = paddle_img.get_width(), paddle_img.get_height()
BALL_SIZE = ball_img.get_width()

def reset():
    global left_paddle_y, right_paddle_y, ball_x, ball_y, ball_spd_x, ball_spd_y, playing, loser
    left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_spd_x = BALL_SPEED_X if pygame.time.get_ticks() % 2 else -BALL_SPEED_X
    ball_spd_y = BALL_SPEED_Y if pygame.time.get_ticks() % 2 else -BALL_SPEED_Y
    playing = True
    loser = None

def draw():
    screen.fill((40, 40, 60))
    screen.blit(paddle_img, (30, left_paddle_y))
    screen.blit(paddle_img, (WIDTH - 30 - PADDLE_WIDTH, right_paddle_y))
    screen.blit(ball_img, (ball_x - BALL_SIZE//2, ball_y - BALL_SIZE//2))

def show_gameover(loser_side):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 20, 210))
    screen.blit(overlay, (0, 0))
    text1 = font_big.render("боже чел ты лох...", True, (255,255,255))
    text2 = font_small.render(f"{loser_side} чел, ты улитка!", True, (255, 220, 70))
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 90))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 10))
    text_restart = font_small.render("если хочешь жить - жми R!", True, (255,255,255))
    screen.blit(text_restart, (WIDTH // 2 - text_restart.get_width() // 2, HEIGHT // 2 + 70))

reset()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and not playing:
            if event.key == pygame.K_r:
                reset()

    keys = pygame.key.get_pressed()
    if playing:
        if keys[pygame.K_w]:
            left_paddle_y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle_y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            right_paddle_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle_y += PADDLE_SPEED

        left_paddle_y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle_y))
        right_paddle_y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle_y))

        ball_x += ball_spd_x
        ball_y += ball_spd_y

        if ball_y - BALL_SIZE//2 < 0 or ball_y + BALL_SIZE//2 > HEIGHT:
            ball_spd_y *= -1

        if (ball_x - BALL_SIZE//2 < 30 + PADDLE_WIDTH and
            left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT):
            ball_spd_x = abs(ball_spd_x) * 1.07
            ball_spd_y *= 1.07

        if (ball_x + BALL_SIZE//2 > WIDTH - 30 - PADDLE_WIDTH and
            right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT):
            ball_spd_x = -abs(ball_spd_x) * 1.07
            ball_spd_y *= 1.07

        if ball_x - BALL_SIZE//2 < 0:
            loser = "Левый игрок"
            playing = False
        elif ball_x + BALL_SIZE//2 > WIDTH:
            loser = "Правый игрок"
            playing = False

    draw()
    if not playing and loser:
        show_gameover(loser)
    pygame.display.flip()
    clock.tick(60)
