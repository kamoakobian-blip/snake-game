"""
Игра «Змейка» (Snake)
Классическая реализация с использованием Pygame и ООП.
"""

import pygame
import random
from typing import List, Tuple


# Константы игры
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для игровых объектов."""
    
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]):
        self.position = position
        self.body_color = color

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод отрисовки."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""
    
    def __init__(self):
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайную позицию."""
        grid_x = random.randint(0, GRID_WIDTH - 1)
        grid_y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (grid_x * CELL_SIZE, grid_y * CELL_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Класс змейки."""
    
    def __init__(self):
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(start_position, GREEN)
        
        self.positions: List[Tuple[int, int]] = [start_position]
        self.length: int = 1
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Tuple[int, int] = RIGHT

    def update_direction(self) -> None:
        """Обновляет направление движения."""
        if self.next_direction:
            opposite_directions = {
                UP: DOWN, DOWN: UP,
                LEFT: RIGHT, RIGHT: LEFT
            }
            if self.next_direction != opposite_directions.get(self.direction):
                self.direction = self.next_direction

    def move(self) -> None:
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        
        new_head_x = (head_x + dir_x * CELL_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dir_y * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        
        self.positions.insert(0, new_head)
        
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку."""
        for segment in self.positions:
            rect = pygame.Rect(segment, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT

    def check_self_collision(self) -> bool:
        """Проверяет столкновение с собой."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def grow(self) -> None:
        """Увеличивает длину."""
        self.length += 1


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main() -> None:
    """Главный игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона — Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()
            while apple.position in snake.positions:
                apple.randomize_position()
            continue

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()