import random
from typing import List, Tuple
import pygame
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class GameObject:
    def __init__(self, position, color):
        self.position = position
        self.body_color = color
    def draw(self, surface):
        raise NotImplementedError

class Apple(GameObject):
    def __init__(self):
        super().__init__((0, 0), RED)
        self.randomize_position()
    def randomize_position(self):
        self.position = (random.randint(0, 31) * 20, random.randint(0, 23) * 20)
    def draw(self, surface):
        pygame.draw.rect(surface, self.body_color, (self.position[0], self.position[1], 20, 20))

class Snake(GameObject):
    def __init__(self):
        super().__init__((320, 240), GREEN)
        self.positions = [(320, 240)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT
    def update_direction(self):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if self.next_direction and self.next_direction != opposites.get(self.direction):
            self.direction = self.next_direction
    def move(self):
        head = self.get_head_position()
        new_head = ((head[0] + self.direction[0] * 20) % 640, (head[1] + self.direction[1] * 20) % 480)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color, (pos[0], pos[1], 20, 20))
    def get_head_position(self):
        return self.positions[0]
    def reset(self):
        self.positions = [(320, 240)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT
    def check_self_collision(self):
        return self.get_head_position() in self.positions[1:]

def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: snake.next_direction = UP
            elif event.key == pygame.K_DOWN: snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT: snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT: snake.next_direction = RIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.check_self_collision():
            snake.reset()
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)

if __name__ == '__main__':
    main()
