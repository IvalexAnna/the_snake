from random import choice, randint

import pygame as pg

# Инициализация pg:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Константы для типизации:
POINTER = tuple[int, int]
COLOUR_POINTER = tuple[int, int, int]

# Направления движения:
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)

DIC: dict = {
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (LEFT, pg.K_DOWN): DOWN
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOUR_POINTER = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOUR_POINTER = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOUR_POINTER = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOUR_POINTER = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(f'Змейка,cкорость:{SPEED}')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Объявление родительского класса."""

    def __init__(self, bg_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = bg_color

    def draw(self):
        """Абстрактный метод."""
        raise NotImplementedError()


class Apple(GameObject):
    """Объявление класса яблоко."""

    def __init__(self, bg_color=APPLE_COLOR):
        super().__init__(bg_color)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """Провоцируцем появлние змейки в случайном месте."""
        if snake_positions is None:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
        else:
            while True:
                new_position = (
                    randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                )
                if new_position not in snake_positions:
                    self.position = new_position
                    break

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявление класса змейка."""

    def __init__(self, bg_color=SNAKE_COLOR, length=1, direction=RIGHT,
                 next_direction=None, last=None, record=0):
        super().__init__(bg_color)
        self.positions = [self.position]
        self.length = length
        self.last = last
        self.next_direction = next_direction
        self.direction = direction
        self.record = record

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
            if len(self.positions) > self.record:
                self.record = len(self.positions)
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
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last is not None:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывание змейки в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            new_direction = DIC.get((game_object.direction, event.key), None)
            if new_direction is not None:
                game_object.update_direction(new_direction)


def main():
    """Основной цикл игры"""
    # Экземпляры классов.
    apple = Apple()
    snake = Snake()
    pg.mixer.init()
    bite = pg.mixer.Sound('bite.wav')

    running = True
    while running:
        """Объявление цикла"""
        clock.tick(SPEED)
        handle_keys(snake)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if snake.get_head_position() == apple.position:
            snake.length += 1
            bite.play()
            apple.randomize_position(snake.positions)
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        caption = f'Змейка, скорость: {SPEED}, рекорд: {snake.record}'
        pg.display.set_caption(caption)
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main()
"""Вызов функции"""
