import pygame
import random

pygame.init()

# настройки экрана
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Типо Super Mario")
#background = pygame.image.load("background.jpg")  
#background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# переменные игрока
player_size = 60
player_x = 50
player_y = HEIGHT - player_size
player_vel_x = 5
player_vel_y = 50
gravity = 0.5
jump_power = -10
on_ground = True

# монетки
coin_size = 25
coins = [(random.randint(200, WIDTH - 50), random.randint(50, HEIGHT - 50)) for i in range(15)]
score = 0

# платформы
platforms = [(0, HEIGHT - 20, WIDTH, 20), (300, HEIGHT - 100, 150, 20), (550, HEIGHT - 200, 150, 20),
            (50, HEIGHT - 230, 170, 20),  (700, HEIGHT - 300, 180, 20), (650, HEIGHT - 450, 120, 20), 
            (500, HEIGHT - 550, 150, 20), (320, HEIGHT - 350, 180, 20), (125, HEIGHT - 400, 130, 20),
            (40, HEIGHT - 600, 150, 20),  (1100, HEIGHT - 90, 150, 20), (840, HEIGHT - 600, 170, 20), 
            (900, HEIGHT - 210, 150, 20), (570, HEIGHT - 700, 150, 20), (300, HEIGHT - 750, 150, 20)]

# игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # проверка нажатия клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_vel_x
    if keys[pygame.K_UP] or keys[pygame.K_w]  and on_ground:
        player_vel_y = jump_power
        on_ground = False

    # обновление положения игрока
    player_y += player_vel_y
    player_vel_y += gravity

    # переход через границы экрана
    if player_x < -player_size:
        player_x = WIDTH
    elif player_x > WIDTH:
        player_x = -player_size

    # кпроверка столкновений с платформами
    on_ground = False
    for plat_x, plat_y, plat_w, plat_h in platforms:
        pygame.draw.rect(screen, GREEN, (plat_x, plat_y, plat_w, plat_h))
        if (player_x + player_size > plat_x and player_x < plat_x + plat_w and
            player_y + player_size > plat_y and player_y + player_size <= plat_y + plat_h):
            player_y = plat_y - player_size
            player_vel_y = 0
            on_ground = True

    # пол
    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_vel_y = 0
        on_ground = True

    # отрисовка игрока в виде человечка
    head_radius = player_size // 6
    body_height = player_size // 3
    leg_length = player_size // 4

    # координаты частей тела
    head_center = (player_x + player_size // 2, player_y + head_radius)
    body_start = (player_x + player_size // 2, player_y + 2 * head_radius)
    body_end = (body_start[0], body_start[1] + body_height)
    left_leg = (body_end[0] - head_radius, body_end[1] + leg_length)
    right_leg = (body_end[0] + head_radius, body_end[1] + leg_length)
    left_arm = (body_start[0] - head_radius, body_start[1] + body_height // 3)
    right_arm = (body_start[0] + head_radius, body_start[1] + body_height // 3)

    # рисование человечка
    pygame.draw.circle(screen, RED, head_center, head_radius)  # голова
    pygame.draw.line(screen, RED, body_start, body_end, 2)  # туловище
    pygame.draw.line(screen, BLUE, body_start, left_arm, 2)  # левая рука
    pygame.draw.line(screen, BLUE, body_start, right_arm, 2)  # правая рука
    pygame.draw.line(screen, BLUE, body_end, left_leg, 2)  # левая нога
    pygame.draw.line(screen, BLUE, body_end, right_leg, 2)  # правая нога

    # отрисовка монет и проверка на сбор
    for coin in coins[:]:
        pygame.draw.circle(screen, YELLOW, coin, coin_size // 2)
        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(
                pygame.Rect(coin[0] - coin_size // 2, coin[1] - coin_size // 2, coin_size, coin_size)):
            coins.remove(coin)
            score += 1

    # Проверка завершения игры (все монеты собраны)
    if not coins:
        print("Поздравляем, вы собрали все монетки!")
        running = False

    # Отображение счёта
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Счёт: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(40)

    # Выход из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
