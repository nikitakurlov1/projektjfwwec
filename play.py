import pygame
import random

pygame.init()

WINDOW_SIZE = 800
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# Параметры игрока
PLAYER_SIZE = 40
player_x = 50
player_y = WINDOW_SIZE - PLAYER_SIZE - 10
player_velocity = 0
gravity = 1.5
jump_power = -25

# Параметры игры
obstacles = []
min_obstacle_distance = 1200  # Увеличено расстояние между препятствиями
game_speed = 1.5
speed_increase = 0.1
score = 0

def create_bush_segments(x, base_width, base_height):
    segments = []
    segment_count = random.randint(3, 5)
    for i in range(segment_count):
        segment_width = base_width // segment_count
        segment_height = random.randint(10, 20)
        segment_x = x + (i * segment_width)
        segments.append({
            'x': segment_x,
            'width': segment_width,
            'height': segment_height,
            'y': base_height - segment_height
        })
    return segments

def create_obstacle():
    # Создаем препятствие-куст
    is_wide = random.random() < 0.3  # 30% шанс широкого препятствия
    base_width = random.randint(120, 200) if is_wide else random.randint(30, 50)
    base_height = random.randint(40, 60)
    base_y = WINDOW_SIZE - base_height - 10
    
    obstacle = {
        'x': WINDOW_SIZE,
        'width': base_width,
        'height': base_height,
        'y': base_y,
        'is_bush': True,
        'segments': create_bush_segments(WINDOW_SIZE, base_width, base_y)
    }
    return obstacle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player_y >= WINDOW_SIZE - PLAYER_SIZE - 10:
                player_velocity = jump_power

    # Физика прыжка
    player_velocity += gravity
    player_y += player_velocity
    if player_y > WINDOW_SIZE - PLAYER_SIZE - 10:
        player_y = WINDOW_SIZE - PLAYER_SIZE - 10
        player_velocity = 0

    # Создание препятствий
    if not obstacles or WINDOW_SIZE - obstacles[-1]['x'] >= min_obstacle_distance:
        obstacles.append(create_obstacle())

    # Движение препятствий и подсчет очков
    for obstacle in obstacles[:]:
        move_distance = 8 * game_speed
        obstacle['x'] -= move_distance
        # Обновляем позиции сегментов куста
        for segment in obstacle['segments']:
            segment['x'] -= move_distance
        
        if obstacle['x'] < -30:
            obstacles.remove(obstacle)
            score += 1
            game_speed += speed_increase

    # Проверка столкновений
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for obstacle in obstacles:
        if player_rect.colliderect(pygame.Rect(obstacle['x'], obstacle['y'], 
                                              obstacle['width'], obstacle['height'])):
            running = False

    # Отрисовка
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), player_rect)
    for obstacle in obstacles:
        # Отрисовка основания куста
        pygame.draw.rect(window, (34, 139, 34), 
                        (obstacle['x'], obstacle['y'], 
                         obstacle['width'], obstacle['height']))
        # Отрисовка верхних сегментов куста
        for segment in obstacle['segments']:
            pygame.draw.rect(window, (0, 100, 0),
                           (segment['x'], segment['y'],
                            segment['width'], segment['height']))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
