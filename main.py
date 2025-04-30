import pygame

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Рисование фигур")

# Цвета
BACKGROUND = (0, 0, 0)
PALETTE_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (255, 255, 255), (128, 128, 128), (0, 0, 0)
]
PALETTE_SIZE = 40
PALETTE_MARGIN = 10
PALETTE_START_X = WIDTH - (PALETTE_SIZE + PALETTE_MARGIN) * len(PALETTE_COLORS)

# Текущий цвет рисования
current_color = (255, 255, 255)

# Для хранения всех кружочков
circles = []  # Будем хранить (pos, color, radius)

# Для прямоугольников
rectangles = []
rect_start_pos = None
rect_current_pos = None
drawing_rect = False

# Для рисования
drawing = False
CIRCLE_RADIUS = 5

# Основной флаг работы программы
running = True

# Частота кадров
FPS = 60
clock = pygame.time.Clock()


def draw_palette():
    """Рисует палитру цветов в правой части экрана"""
    for i, color in enumerate(PALETTE_COLORS):
        pygame.draw.rect(
            screen,
            color,
            (PALETTE_START_X + i * (PALETTE_SIZE + PALETTE_MARGIN),
             PALETTE_MARGIN,
             PALETTE_SIZE,
             PALETTE_SIZE)
        )


# Основной цикл программы
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Левая кнопка мыши
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            # Проверка клика на палитре
            if PALETTE_START_X <= mouse_x <= WIDTH - PALETTE_MARGIN and \
                    PALETTE_MARGIN <= mouse_y <= PALETTE_MARGIN + PALETTE_SIZE:
                # Вычисляем индекс цвета
                idx = (mouse_x - PALETTE_START_X) // (PALETTE_SIZE + PALETTE_MARGIN)
                if 0 <= idx < len(PALETTE_COLORS):
                    current_color = PALETTE_COLORS[idx]
            else:
                # Начало рисования
                drawing = True
                # Добавляем первый кружок
                circles.append((event.pos, current_color, CIRCLE_RADIUS))

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False

        # Правая кнопка мыши
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            rect_start_pos = event.pos
            rect_current_pos = event.pos
            drawing_rect = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if drawing_rect:
                # Проверяем минимальный размер прямоугольника
                width = abs(rect_current_pos[0] - rect_start_pos[0])
                height = abs(rect_current_pos[1] - rect_start_pos[1])
                if width > 5 and height > 5:
                    # Создаем прямоугольник
                    x = min(rect_start_pos[0], rect_current_pos[0])
                    y = min(rect_start_pos[1], rect_current_pos[1])
                    rect = pygame.Rect(x, y, width, height)
                    rectangles.append((rect, current_color))
            drawing_rect = False

        # Движение мыши
        elif event.type == pygame.MOUSEMOTION:
            # Рисование кружочков при движении с зажатой левой кнопкой
            if drawing and event.buttons[0]:
                circles.append((event.pos, current_color, CIRCLE_RADIUS))

            # Обновление текущей позиции для прямоугольника
            if drawing_rect and event.buttons[2]:
                rect_current_pos = event.pos

    # Очистка экрана
    screen.fill(BACKGROUND)

    # Рисование палитры
    draw_palette()

    # Рисование всех кружочков
    for pos, color, radius in circles:
        pygame.draw.circle(screen, color, pos, radius)

    # Рисование всех прямоугольников
    for rect, color in rectangles:
        pygame.draw.rect(screen, color, rect, 2)

    # Рисование текущего прямоугольника (при перетаскивании)
    if drawing_rect and rect_start_pos and rect_current_pos:
        rect = pygame.Rect(
            min(rect_start_pos[0], rect_current_pos[0]),
            min(rect_start_pos[1], rect_current_pos[1]),
            abs(rect_current_pos[0] - rect_start_pos[0]),
            abs(rect_current_pos[1] - rect_start_pos[1])
        )
        pygame.draw.rect(screen, current_color, rect, 1)

    # Отображение текущего цвета
    font = pygame.font.SysFont(None, 36)
    color_text = f"Текущий цвет: RGB{current_color}"
    color_surface = font.render(color_text, True, current_color)
    screen.blit(color_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()