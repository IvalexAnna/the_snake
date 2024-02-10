from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Объявление родительского класса."""

    def __init__(self, bg_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = bg_color

    def draw(self):
        """Абстрактный метод."""
        pass


class Apple(GameObject):
    """Объявление класса яблоко."""

    def __init__(self, bg_color=APPLE_COLOR):
        super().__init__(bg_color)
        self.randomize_position()

    def randomize_position(self):
        """Провоцируцем появлние змейки в случайном месте."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявление класса змейка."""

    def __init__(self, bg_color=SNAKE_COLOR, length=1, direction=RIGHT,
                 next_direction=None, last=None):
        super().__init__(bg_color)
        self.positions = [self.position]
        self.length = length
        self.last = last
        self.next_direction = next_direction
        self.direction = direction

    def update_direction(self, next_direction):
        """Обновление направление движения змейки."""
        self.direction = next_direction

    def get_head_position(self):
        """Получение текущей головной позиции."""
        return self.positions[0]

    def move(self):
        """Обновление позиции змейки."""
        head_position = self.get_head_position()
        height, width = self.direction
        new_head_position = (
            head_position[0] + (height * GRID_SIZE),
            head_position[1] + (width * GRID_SIZE)
        )
        # Проверяем, вышла ли змейка за пределы экрана по горизонтали.
        if new_head_position[0] < 0:
            new_head_position = (SCREEN_WIDTH - GRID_SIZE,
                                 new_head_position[1])
        elif new_head_position[0] >= SCREEN_WIDTH:
            new_head_position = (0, new_head_position[1])

        # Проверяем, вышла ли змейка за пределы экрана по вертикали.
        if new_head_position[1] < 0:
            new_head_position = (
                new_head_position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head_position[1] >= SCREEN_HEIGHT:
            new_head_position = (new_head_position[0], 0)

        if len(self.positions) > 2 and new_head_position in self.positions:
            self.reset()
        else:
            self.last = self.positions[-1]
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last is not None:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывание змейки в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основной цикл игры"""
    # Экземпляры классов.
    apple = Apple()
    snake = Snake()

    running = True
    while running:
        """Объявление цикла"""
        clock.tick(SPEED)
        handle_keys(snake)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
"""Вызов функции"""
