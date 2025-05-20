import pygame
import random
import os

# Инициализация Pygame
pygame.init() 

# Настройки окна
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Динозаврик")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Состояния игры
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Создаем спрайты для анимации динозавра
def create_dino_frame(frame_num):
    surf = pygame.Surface((50, 50))
    surf.fill(WHITE)
    surf.set_colorkey(WHITE)
    
    # Тело динозавра
    pygame.draw.rect(surf, GRAY, (0, 0, 50, 50))
# Создаем спрайты препятствий
def create_obstacle(obstacle_type):
    if obstacle_type == "cactus":
        surf = pygame.Surface((30, 50))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)
        surf.fill(GREEN)
        pygame.draw.rect(surf, BLACK, (0, 0, 30, 50), 2)
        pygame.draw.rect(surf, BLACK, (10, 10, 10, 30))
        return surf, 30, 50
    elif obstacle_type == "bird":
        surf = pygame.Surface((40, 30))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)
        pygame.draw.ellipse(surf, BLACK, (0, 0, 40, 30))
        pygame.draw.line(surf, BLACK, (20, 15), (30, 5), 2)
        return surf, 40, 30
    else:  # камень
        surf = pygame.Surface((40, 30))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)
        pygame.draw.ellipse(surf, GRAY, (0, 0, 40, 30))
        return surf, 40, 30

# Создаем анимацию динозавра
dino_frames = [create_dino_frame(0), create_dino_frame(1)]
current_frame = 0
frame_counter = 0

# Динозавр
dino_width = 50
dino_height = 50
dino_x = 50
dino_y = WINDOW_HEIGHT - dino_height - 10
dino_jump = False
gravity = 0.8
dino_velocity = 0

# Препятствия
obstacles = []
obstacle_types = ["cactus", "bird", "rock"]
obstacle_timer = 0
obstacle_delay = 60  # Задержка между появлением препятствий

# Земля
ground_height = 10
ground_y = WINDOW_HEIGHT - ground_height

# Счет
score = 0
high_score = 0
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Игровой цикл
game_state = MENU
running = True
clock = pygame.time.Clock()
game_speed = 1.0

def draw_menu():
    window.fill(WHITE)
    title = big_font.render("ДИНОЗАВРИК", True, BLACK)
    start_text = font.render("Нажмите ПРОБЕЛ чтобы начать", True, BLACK)
    window.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//3))
    window.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, WINDOW_HEIGHT//2))
    pygame.display.update()

def draw_game_over():
    window.fill(WHITE)
    game_over_text = big_font.render("ИГРА ОКОНЧЕНА", True, RED)
    score_text = font.render(f"Счет: {score}", True, BLACK)
    high_score_text = font.render(f"Рекорд: {high_score}", True, BLACK)
    restart_text = font.render("Нажмите ПРОБЕЛ чтобы начать заново", True, BLACK)
    
    window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//4))
    window.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, WINDOW_HEIGHT//2))
    window.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, WINDOW_HEIGHT//2 + 40))
    window.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 80))
    pygame.display.update()

def reset_game():
    global dino_y, dino_jump, dino_velocity, obstacles, score, game_speed
    dino_y = WINDOW_HEIGHT - dino_height - 10
    dino_jump = False
    dino_velocity = 0
    obstacles = []
    score = 0
    game_speed = 1.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                elif game_state == GAME_OVER:
                    reset_game()
                    game_state = PLAYING
                elif game_state == PLAYING and not dino_jump:
                    dino_jump = True
                    dino_velocity = -15

    if game_state == MENU:
        draw_menu()
        continue

    if game_state == GAME_OVER:
        draw_game_over()
        continue

    # Анимация динозавра
    frame_counter += 1
    if frame_counter >= 10:  # Смена кадра каждые 10 тиков
        current_frame = (current_frame + 1) % len(dino_frames)
        frame_counter = 0

    # Физика прыжка
    if dino_jump:
        dino_velocity += gravity
        dino_y += dino_velocity

        if dino_y >= WINDOW_HEIGHT - dino_height - ground_height:
            dino_y = WINDOW_HEIGHT - dino_height - ground_height
            dino_jump = False
            dino_velocity = 0

    # Создание препятствий
    obstacle_timer += 1
    if obstacle_timer >= obstacle_delay:
        obstacle_timer = 0
        obstacle_type = random.choice(obstacle_types)
        obstacle_sprite, width, height = create_obstacle(obstacle_type)
        y_pos = WINDOW_HEIGHT - height - ground_height
        if obstacle_type == "bird":
            y_pos = random.randint(100, 200)  # Птицы летают выше
        obstacles.append({
            "sprite": obstacle_sprite,
            "x": WINDOW_WIDTH,
            "y": y_pos,
            "width": width,
            "height": height
        })

    # Движение препятствий
    for obstacle in obstacles[:]:
        obstacle["x"] -= 5 * game_speed
        if obstacle["x"] < -obstacle["width"]:
            obstacles.remove(obstacle)
            score += 1
            game_speed += 0.1

    # Проверка столкновений
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], 
                                  obstacle["width"], obstacle["height"])
        if dino_rect.colliderect(obstacle_rect):
            if score > high_score:
                high_score = score
            game_state = GAME_OVER

    # Отрисовка
    window.fill(WHITE)
    
    # Рисуем землю
    pygame.draw.rect(window, GRAY, (0, ground_y, WINDOW_WIDTH, ground_height))
    
    # Рисуем динозавра
    window.blit(dino_frames[current_frame], (dino_x, dino_y))
    
    # Рисуем препятствия
    for obstacle in obstacles:
        window.blit(obstacle["sprite"], (obstacle["x"], obstacle["y"]))
    
    # Рисуем счет
    score_text = font.render(f"Счет: {score}", True, BLACK)
    high_score_text = font.render(f"Рекорд: {high_score}", True, BLACK)
    window.blit(score_text, (10, 10))
    window.blit(high_score_text, (10, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
