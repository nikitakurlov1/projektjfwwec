import tkinter as tk
import random
import os
import json

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

class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = PLAYER_SIZE
        self.x = 100
        self.y = WINDOW_SIZE - 80 - self.size
        self.vel_y = 0
        self.on_ground = True
        self.speed = 0
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.size, self.y + self.size,
            fill=PLAYER_COLOR, outline=""
        )

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
        self.canvas.coords(
            self.rect, self.x, self.y, self.x + self.size, self.y + self.size
        )

    def get_coords(self):
        return (self.x, self.y, self.x + self.size, self.y + self.size)

class Obstacle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 30
        self.height = random.randint(40, 70)
        self.x = WINDOW_SIZE
        self.y = WINDOW_SIZE - 80 - self.height
        self.speed = 6
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=OBSTACLE_COLOR, outline=""
        )

    def update(self):
        self.x -= self.speed
        self.canvas.coords(
            self.rect, self.x, self.y, self.x + self.width, self.y + self.height
        )

    def get_coords(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Runner")
        
        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        
        self.ground = self.canvas.create_rectangle(
            0, WINDOW_SIZE - 80, WINDOW_SIZE, WINDOW_SIZE,
            fill=GROUND_COLOR, outline=""
        )
        
        self.player = Player(self.canvas)
        self.obstacles = []
        self.score = 0
        self.spawn_timer = OBSTACLE_INTERVAL
        self.running = True
        self.game_over = False
        self.high_score = self.load_high_score()
        
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill=WHITE)
        self.high_score_text = self.canvas.create_text(10, 40, anchor="nw", text=f"High Score: {self.high_score}", fill=WHITE)
        self.game_over_text = None
        
        self.root.bind("<space>", lambda e: self.player.jump())
        self.root.bind("<r>", lambda e: self.reset() if self.game_over else None)
        
        self.update()
    
    def load_high_score(self):
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as f:
                return json.load(f).get("high_score", 0)
        return 0
    
    def save_high_score(self):
        with open("high_score.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)
    
    def reset(self):
        self.canvas.delete("all")
        self.__init__(self.root)
    
    def update(self):
        if not self.running:
            return
            
        if self.game_over:
            return

        self.player.update()

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.obstacles.append(Obstacle(self.canvas))
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
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                    self.canvas.itemconfig(self.high_score_text, text=f"High Score: {self.high_score}")
                
                self.game_over_text = self.canvas.create_text(
                    WINDOW_SIZE//2, WINDOW_SIZE//2, 
                    text="Game Over! Press R to restart", 
                    fill=WHITE, font=("Arial", 24)
                )

        self.root.after(1000//FPS, self.update)
    
    def check_collision(self, rect1, rect2):
        # rect format: (x1, y1, x2, y2)
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or 
                   rect1[3] < rect2[1] or rect1[1] > rect2[3])

root = tk.Tk()
game = Game(root)
root.mainloop()
