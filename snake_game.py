"""Игра Змейка - классическая аркадная игра."""

import random
import pygame

# Константы
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, color):
        """Инициализация объекта."""
        self.position = position
        self.body_color = color

    def draw(self, surface):
        """Отрисовка объекта."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self):
        """Случайная позиция яблока."""
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(start, GREEN)
        self.positions = [start]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT

    def update_direction(self):
        """Обновление направления движения."""
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if self.next_direction and self.next_direction != opposites.get(self.direction):
            self.direction = self.next_direction

    def move(self):
        """Перемещение змейки."""
        head = self.get_head_position()
        dx = self.direction[0] * CELL_SIZE
        dy = self.direction[1] * CELL_SIZE
        new_head = ((head[0] + dx) % SCREEN_WIDTH, (head[1] + dy) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Получение позиции головы."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT

    def check_self_collision(self):
        """Проверка столкновения с собой."""
        return self.get_head_position() in self.positions[1:]


def handle_keys(snake):
    """Обработка нажатий клавиш."""
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


def main():
    """Главный игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
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
            apple.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':
    main()