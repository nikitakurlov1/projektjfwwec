
import tkinter as tk
import random

# Константи гри
WINDOW_SIZE = 800
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -15
OBSTACLE_INTERVAL = 90

# Кольори
WHITE = "#ffffff"
PLAYER_COLOR = "#00ff96"
OBSTACLE_COLOR = "#ff3264"
GROUND_COLOR = "#282850"
BG_COLOR = "#0f0f23"
PLAYER_SIZE = 40

# Клас гравця
class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = PLAYER_SIZE
        self.x = 100
        self.y = WINDOW_SIZE - 80 - self.size
        self.vel_y = 0
        self.on_ground = True
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.size, self.y + self.size,
            fill=PLAYER_COLOR, outline=""
        )

    # Метод для стрибка гравця
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    # Метод для оновлення позиції гравця
    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        ground_y = WINDOW_SIZE - 80 - self.size
        if self.y >= ground_y:
            self.y = ground_y
            self.vel_y = 0
            self.on_ground = True

        self.canvas.coords(
            self.rect, self.x, self.y, self.x + self.size, self.y + self.size
        )

    # Метод для отримання координат гравця
    def get_coords(self):
        return (self.x, self.y, self.x + self.size, self.y + self.size)

# Клас перешкоди
class Obstacle:
    def __init__(self, canvas, speed):
        self.canvas = canvas
        self.width = 30
        self.height = random.randint(40, 70)
        self.x = WINDOW_SIZE
        self.y = WINDOW_SIZE - 80 - self.height
        self.speed = speed
        self.rect = self.canvas.create_rectangle(
            self.x + self.width, self.y + self.height,
            fill=OBSTACLE_COLOR, outline=""
        )

    # Метод для оновлення позиції перешкоди
    def update(self):
        self.x -= self.speed
        self.canvas.coords(
            self.rect, self.x, self.y, self.x + self.width, self.y + self.height
        )

    # Метод для отримання координат перешкоди
    def get_coords(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

# Головний клас гри
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Runner")
        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg=BG_COLOR)
        self.canvas.pack()

        # Створення меню
        self.menu_frame = tk.Frame(root, bg=BG_COLOR)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(self.menu_frame, text="Старт", width=15, command=self.start_game).pack(pady=5)
        tk.Button(self.menu_frame, text="Управление", width=15, command=self.show_controls).pack(pady=5)
        tk.Button(self.menu_frame, text="Выход", width=15, command=self.root.quit).pack(pady=5)

        self.controls_window = None

    # Метод для показу вікна з керуванням
    def show_controls(self):
        if self.controls_window and tk.Toplevel.winfo_exists(self.controls_window):
            return
        self.controls_window = tk.Toplevel(self.root)
        self.controls_window.title("Управление")
        tk.Label(self.controls_window, text="Пробел — прыжок\nR — перезапуск", font=("Arial", 14)).pack(padx=20, pady=20)

    # Метод для початку гри
    def start_game(self):
        self.menu_frame.destroy()
        self.score = 0
        self.speed = 6
        self.timer = 0
        self.spawn_timer = OBSTACLE_INTERVAL
        self.obstacles = []
        self.running = True
        self.game_over = False

        self.canvas.delete("all")
        self.ground = self.canvas.create_rectangle(0, WINDOW_SIZE - 80, WINDOW_SIZE, WINDOW_SIZE, fill=GROUND_COLOR, outline="")
        self.player = Player(self.canvas)

        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill=WHITE)
        self.button_counter = 0
        self.button_counter_text = self.canvas.create_text(10, 40, anchor="nw", text=f"Space pressed: {self.button_counter}", fill=WHITE)

        self.root.bind("<space>", self.space_pressed)
        self.root.bind("<r>", lambda e: self.start_game() if self.game_over else None)

        self.update_game()
        self.increase_speed()

    # Метод для обробки натискання пробілу
    def space_pressed(self, event):
        self.player.jump()
        self.button_counter += 1
        self.canvas.itemconfig(self.button_counter_text, text=f"Space pressed: {self.button_counter}")

    # Метод для оновлення стану гри
    def update_game(self):
        if not self.running or self.game_over:
            return

        self.player.update()

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.obstacles.append(Obstacle(self.canvas, self.speed))
            self.spawn_timer = OBSTACLE_INTERVAL

        for obs in self.obstacles[:]:
            obs.update()
            if obs.x + obs.width < 0:
                self.obstacles.remove(obs)
                self.canvas.delete(obs.rect)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

            if self.check_collision(self.player.get_coords(), obs.get_coords()):
                self.game_over = True
                self.canvas.create_text(
                    WINDOW_SIZE//2, WINDOW_SIZE//2,
                    text="Game Over! Press R to restart",
                    fill=WHITE, font=("Arial", 24)
                )

        self.root.after(1000//FPS, self.update_game)

    # Метод для збільшення швидкості гри
    def increase_speed(self):
        if self.game_over:
            return
        self.speed += 0.5
        self.root.after(1000, self.increase_speed)

    # Метод для перевірки зіткнення
    def check_collision(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or 
                    rect1[3] < rect2[1] or rect1[1] > rect2[3])

# Створення та запуск гри
root = tk.Tk()
game = Game(root)
root.mainloop()
