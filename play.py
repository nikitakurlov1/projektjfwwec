import pygame
import random
import os
import json

pygame.init()
WINDOW_SIZE = 800
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -15
OBSTACLE_INTERVAL = 90

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Neon Runner")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Кольори
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 255, 150)
OBSTACLE_COLOR = (255, 50, 100)
GROUND_COLOR = (40, 40, 80)
BG_COLOR = (15, 15, 35)
PLAYER_SIZE = 40

# Гравець
class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = 100
        self.y = WINDOW_SIZE - 80 - self.size
        self.vel_y = 0
        self.on_ground = True
        self.speed = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        ground_y = WINDOW_SIZE - 80 - self.size
        if self.y >= ground_y:
            self.y = ground_y
            self.vel_y = 0
            self.on_ground = True

        self.speed += 0.01

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

# Перешкоди
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.randint(40, 70)
        self.x = WINDOW_SIZE
        self.y = WINDOW_SIZE - 80 - self.height
        self.speed = 6

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Гра
class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.spawn_timer = OBSTACLE_INTERVAL
        self.running = True
        self.game_over = False
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as f:
                return json.load(f).get("high_score", 0)
        return 0

    def save_high_score(self):
        with open("high_score.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def reset(self):
        self.__init__()

    def update(self):
        if self.game_over:
            return

        self.player.update()

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.obstacles.append(Obstacle())
            self.spawn_timer = OBSTACLE_INTERVAL

        for obs in self.obstacles[:]:
            obs.update()
            if obs.x + obs.width < 0:
                self.obstacles.remove(obs)
                self.score += 1

            if self.player.get_rect().colliderect(obs.get_rect()):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

    def draw(self):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, (0, WINDOW_SIZE - 80, WINDOW_SIZE, 80))

        self.player.draw(screen)
        for obs in self.obstacles:
            obs.draw(screen)

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            over_text = font.render("Game Over! Press R to restart", True, WHITE)
            screen.blit(over_text, (WINDOW_SIZE//2 - 160, WINDOW_SIZE//2))

        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 40))

# Основний цикл
game = Game()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.player.jump()
            elif event.key == pygame.K_r and game.game_over:
                game.reset()

    game.update()
    game.draw()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
