import pygame
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/users/Tema/project/game_log.txt"),
        logging.StreamHandler()
    ]
)

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Типо Super Mario")
background = pygame.image.load("/Users/Tema/project/background2.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Шрифт
font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.vel_x = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = True

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.vel_x
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.vel_x
        if keys[pygame.K_UP] and self.on_ground or keys[pygame.K_w] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            logging.info("Player jumped!")

        self.y += self.vel_y
        self.vel_y += self.gravity

        # Переход через границы экрана
        if self.x < -self.size:
            self.x = WIDTH
            logging.info("Player has crossed the screen!")
        elif self.x > WIDTH:
            self.x = -self.size

    def draw(self):
        # Отрисовка игрока в виде человечка
        head_radius = self.size // 6
        body_height = self.size // 3
        leg_length = self.size // 4

        # Координаты частей тела
        head_center = (self.x + self.size // 2, self.y + head_radius)
        body_start = (self.x + self.size // 2, self.y + 2 * head_radius)
        body_end = (body_start[0], body_start[1] + body_height)
        left_leg = (body_end[0] - head_radius, body_end[1] + leg_length)
        right_leg = (body_end[0] + head_radius, body_end[1] + leg_length)
        left_arm = (body_start[0] - head_radius, body_start[1] + body_height // 3)
        right_arm = (body_start[0] + head_radius, body_start[1] + body_height // 3)

        # Рисование частей
        pygame.draw.circle(screen, RED, head_center, head_radius)  # голова
        pygame.draw.line(screen, RED, body_start, body_end, 2)  # туловище
        pygame.draw.line(screen, BLUE, body_start, left_arm, 2)  # левая рука
        pygame.draw.line(screen, BLUE, body_start, right_arm, 2)  # правая рука
        pygame.draw.line(screen, BLUE, body_end, left_leg, 2)  # левая нога
        pygame.draw.line(screen, BLUE, body_end, right_leg, 2)  # правая нога

    def collide_with_platforms(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if platform.collides_with_player(self):
                self.y = platform.y - self.size
                self.vel_y = 0
                self.on_ground = True

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

    def collides_with_player(self, player):
        return (
            player.x + player.size > self.x and
            player.x < self.x + self.width and
            player.y + player.size > self.y and
            player.y + player.size <= self.y + self.height
        )

class Coin:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.size = size

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.rect.centerx, self.rect.centery), self.size // 2)

    def check_collision(self, player):
        return self.rect.colliderect(pygame.Rect(player.x, player.y, player.size, player.size))

# Инициализация объектов
class Game:
    def __init__(self):
        self.player = Player(50, HEIGHT - 60, 60)
        self.platforms = [
             Platform(0, HEIGHT - 20, WIDTH, 20), 
             Platform(300, HEIGHT - 100, 150, 20), 
             Platform(550, HEIGHT - 200, 150, 20),
             Platform(50, HEIGHT - 230, 170, 20), 
             Platform(700, HEIGHT - 300, 180, 20), 
             Platform(650, HEIGHT - 450, 120, 20),
             Platform(500, HEIGHT - 550, 150, 20), 
             Platform(320, HEIGHT - 350, 180, 20),
             Platform(125, HEIGHT - 400, 130, 20),
             Platform(40, HEIGHT - 600, 150, 20), 
             Platform(1100, HEIGHT - 90, 150, 20), 
             Platform(840, HEIGHT - 600, 170, 20),
             Platform(900, HEIGHT - 210, 150, 20), 
             Platform(570, HEIGHT - 700, 150, 20), 
             Platform(300, HEIGHT - 750, 150, 20)
        ]
        self.coins = [
            Coin(random.randint(200, WIDTH - 50), random.randint(50, HEIGHT - 50), 25)
            for _ in range(15)
        ]
        self.score = 0
        self.running = True
        self.game_over = False
        logging.info("Game Started!")

    def reset_game(self):
        self.__init__()  # Просто пересоздаём игру
        #logging.info("Game started again!")

    def end_screen(self):
        screen.fill(WHITE)
        text = font.render("Поздравляем, вы справились!", True, BLACK)
        button_text = small_font.render("Начать заново", True, WHITE)

        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)

        # Кнопка
        button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
        pygame.draw.rect(screen, GREEN, button_rect)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        # Обработка событий экрана окончания
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            if self.game_over:
                self.end_screen()
                continue

            # Основной игровой цикл
            screen.blit(background, (0, 0))
            keys = pygame.key.get_pressed()
            self.player.move(keys)

            # Проверка столкновений
            self.player.collide_with_platforms(self.platforms)
            for coin in self.coins[:]:
                if coin.check_collision(self.player):
                    self.coins.remove(coin)
                    self.score += 1
                    logging.info(f"Монета собрана! Счёт: {self.score}")

            # Проверка окончания игры
            if not self.coins:
                self.game_over = True
                logging.info("Game Over! Все монеты собраны!")

            # Отрисовка объектов
            for platform in self.platforms:
                platform.draw()
            for coin in self.coins:
                coin.draw()
            self.player.draw()

            # Отображение счёта
            score_text = small_font.render(f"Счёт: {self.score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
if __name__ == "__main__":
    game = Game()
    game.run()
