import pygame, sense_hat, time, random
from pygame.color import Color

sense = sense_hat.SenseHat()

WIDTH = 8
HEIGHT = 12
SIZE = WIDTH, WIDTH
VIRTUAL_SIZE = WIDTH, HEIGHT
DISPLAY_SIZE = WIDTH * WIDTH
CLEAR = (0, 0, 0, 0)
FPS = 10

def create_block(pattern, color):
    height = len(pattern)
    width = (max(len(row) for row in pattern))
    block = pygame.Surface((width, height), pygame.SRCALPHA)
    block.fill(CLEAR)
    for x, row in enumerate(pattern):
        for y, element in enumerate(row):
            if element:
                block.set_at((x, y), color)
    return block

def blocks_list():
    blocks = []
    colors = [Color('magenta'), Color('cyan'), Color('purple'), Color('pink'), Color('orange'), Color('yellow')]
    blocks.append(create_block([[1, 1, 1]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 0, 0], [1, 0, 0], [1, 0, 0]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 1, 0], [0, 1, 1]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 0, 0], [1, 1, 0], [0, 1, 0]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[0, 1, 0], [1, 1, 1]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 1, 1], [1, 0, 0]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 0, 0], [1, 0, 0], [1, 1, 0]], colors[random.randrange(0, 5)]))
    blocks.append(create_block([[1, 1], [1, 1]], colors[random.randrange(0, 5)]))
    return blocks

def display_surface(surface):
    fb = []
    w, h = surface.get_size()
    for y in range(h):
        row = ""
        for x in range(w):
            r, g, b, a = surface.get_at((x, y))
            red = int(r * a / 255)
            green = int(g * a / 255)
            blue = int(b * a / 255)
            fb.append((red, green, blue))

    sense.set_pixels(fb[-DISPLAY_SIZE:])

def render(shape, pos):
    canvas = new_canvas()
    canvas.fill(CLEAR)
    canvas.blit( shape, pos, special_flags=pygame.BLEND_RGBA_ADD)
    display_surface(canvas)


def new_canvas(size=VIRTUAL_SIZE):
    s = pygame.Surface(size, pygame.SRCALPHA)
    s.fill(CLEAR)
    return s

sense.clear()
pygame.init()
pygame.display.set_mode((1, 1))
blocks = blocks_list()

while True:
    block = blocks[random.randrange(0, 8)]
    p1 = random.randrange(2,6)
    pos = [p1, 3]
    while(pos[1] <= HEIGHT):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pos[0] > 0:
                    pos[0] -= 1
                elif event.key == pygame.K_RIGHT and pos[0] < 8 - block.get_width():
                    pos[0] += 1
        pos[1] += 1
        render(block, pos)
        time.sleep(1)
sense.clear()
