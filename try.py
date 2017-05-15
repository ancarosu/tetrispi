import pygame, sense_hat, time, random
from pygame.color import Color

sense = sense_hat.SenseHat()

WIDTH = 8
HEIGHT = 12
SIZE = WIDTH, WIDTH
VIRTUAL_SIZE = WIDTH, HEIGHT
DISPLAY_SIZE = WIDTH * WIDTH
CLEAR = (0, 0, 0, 0)
THRESHOLD = 10
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


def new_canvas(size=VIRTUAL_SIZE):
    s = pygame.Surface(size, pygame.SRCALPHA)
    s.fill(CLEAR)
    return s

def block_mask(block, x, y):
    block_canvas = new_canvas()
    block_canvas.blit(block, [x, y], special_flags=pygame.BLEND_RGBA_ADD)
    return pygame.mask.from_surface(block_canvas, THRESHOLD)

class Game:

    def __init__ (self, size = VIRTUAL_SIZE):
        pygame.init()
        self.background = new_canvas()
        self.width = size[0]
        self.height = size[1]
        self.blocks = blocks_list()
        self.new_block()

    def new_block(self):
        block = self.blocks[random.randrange(0, len(self.blocks))]
        new_x = 3
        new_y = 3 - block.get_height()
        if self.can_place_block(block, new_x, new_y):
            self.block = block
            self.block_x = new_x
            self.block_y = new_y
            return True
        else:
            return False

    def can_place_block(self, block, x, y):
        border_violation = x < 0 or y < 0 or  \
            x + block.get_width() > self.width or \
            y + block.get_height() > self.height
        background_mask = pygame.mask.from_surface(self.background, THRESHOLD)
        collision = background_mask.overlap(block_mask(block, x, y), (0, 0))
        return not (border_violation or collision)

    def move_block(self, x, y):
        if self.can_place_block(self.block, self.block_x + x, self.block_y+y):
            self.block_x = self.block_x + x
            self.block_y = self.block_y + y
            return True
        else:
            return False

    def rotate_block(self, angle):
        rotated_block = pygame.transform.rotate(self.block, angle)
        if self.can_place_block(rotated_block, self.block_x, self.block_y):
            self.block = rotated_block
            return True
        else:
            return False

    def render(self):
        canvas = new_canvas()
        canvas.fill(CLEAR)
        canvas.blit( self.block, [self.block_x, self.block_y], special_flags=pygame.BLEND_RGBA_ADD)
        display_surface(canvas)


sense.clear()
pygame.init()
pygame.display.set_mode((1, 1))
s = Game()

while True:
#    block = blocks[random.randrange(0, 8)]
#   p1 = random.randrange(2,6)
#    pos = [p1, 3]
#   while(pos[1] <= HEIGHT):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved = s.move_block(-1,0)
                elif event.key == pygame.K_RIGHT:
                    moved = s.move_block(1,0)
                elif event.key == pygame.K_UP:
                    moved = s.rotate_block(90)
                elif event.key == pygame.K_DOWN:
                    moved = s.rotate_block(-90)
        s.move_block(0,1)
        s.render()
        time.sleep(1)
sense.clear()
