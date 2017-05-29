import pygame, sense_hat, time, random, sys, math
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

def color_scheme(scheme = "DEFAULT"):
    if scheme == "WARM":
        colors = [Color('goldenrod3'), Color('orangered'), Color('red3'), Color('darkorange'), Color('sienna4'), Color('tomato4'), Color('red'), Color('orange'), Color('yellow')]
    elif scheme == "DEFAULT":
        colors = [Color('magenta'), Color('cyan'), Color('darkmagenta'), Color('darkorange'), Color('turquoise4'), Color('purple'), Color('pink'), Color('orange'), Color('yellow')]
    elif scheme == "COLD":
        colors = [Color('turquoise1'), Color('cyan'), Color('lightgray'), Color('white'), Color('limegreen'), Color('lightskyblue'), Color('lightcyan'), Color('honeydew')]
    return colors


def create_block(pattern):
    colors = color_scheme(theme)
    this_color = colors[random.randrange(0, len(colors))]
    height = len(pattern)
    width = (max(len(row) for row in pattern))
    block = pygame.Surface((width, height), pygame.SRCALPHA)
    block.fill(CLEAR)
    for x, row in enumerate(pattern):
        for y, element in enumerate(row):
            if element:
                block.set_at((x, y), this_color)
    return block


def blocks_list():
    blocks = []
    blocks.append(create_block([[1, 1], [1, 1]]))
    blocks.append(create_block([[1, 1], [1, 1]]))
    blocks.append(create_block([[1, 1, 0], [0, 1, 1]]))
    blocks.append(create_block([[0, 1, 1], [1, 1, 0]]))
    blocks.append(create_block([[1, 0, 0], [1, 1, 1]]))
    blocks.append(create_block([[0, 0, 1], [1, 1, 1]]))
    blocks.append(create_block([[1, 1, 1]]))
    blocks.append(create_block([[1, 0, 0], [1, 1, 1]]))
    blocks.append(create_block([[0, 1, 0], [0, 1, 0], [0, 1, 0]]))
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

def game_over(score):
    f = open('scores.txt', 'a')
    f.write(player_name + ": " + str(score) + "\n")
    message = "Score: " + str(score)
    sense.show_message(message, scroll_speed = 1)
    

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

    def add_block_to_background(self):
        self.background.blit(self.block, [self.block_x, self.block_y], special_flags=pygame.BLEND_RGBA_ADD)

    def remove_line(self):
        background_mask = pygame.mask.from_surface(self.background, THRESHOLD)
        for row in range(self.height):
            check_area = new_canvas()
            pygame.draw.line(check_area, Color('white'), (0, row), (self.width -1, row))
            check_area_mask = pygame.mask.from_surface(check_area, THRESHOLD)
            if background_mask.overlap_area(check_area_mask, (0,0)) == self.width:
                self.background.set_clip(pygame.Rect((0, 0), (self.width, row + 1)))
                self.background.scroll(0, 1)
                self.background.set_clip(None)
                background_mask = pygame.mask.from_surface(self.background, THRESHOLD)

    def render(self):
        canvas = new_canvas()
        canvas.fill(CLEAR)
        canvas.blit(self.background, (0, 0))
        canvas.blit(self.block, [self.block_x, self.block_y], special_flags=pygame.BLEND_RGBA_ADD)
        display_surface(canvas)


def tetris():
    sense.clear()
    pygame.init()
    pygame.display.set_mode((1, 1))
    s = Game()
    clock = pygame.time.Clock()
    frames = 0
    frames_before_drop = 10
    
    try:
        while True:
            frames += 1
            # One move event per frame simplifies collision detection and plays better
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return
                    if not moved:
                        if event.key == pygame.K_LEFT:
                            moved = s.move_block(-1,0)
                        if event.key == pygame.K_RIGHT:
                            moved = s.move_block(1,0)
                        if event.key == pygame.K_UP:
                            moved = s.rotate_block(90)
                        if event.key == pygame.K_DOWN:
                            moved = s.rotate_block(-90)
            frames_before_drop -= 1
            if frames_before_drop == 0:
                if s.move_block(0, 1): # Move down
                    pass
                else: # Collision downwards at pos_y+1
                    s.add_block_to_background()
                    s.remove_line()
                    if not s.new_block():
                        break # New block collides with existing blocks
                # Progressively reduce to make game harder,
                frames_before_drop = 10 - int(math.log(frames,5))
            s.render()
            clock.tick(FPS)
        game_over(frames)
    except KeyboardInterrupt:
        return


def main():
    global player_name
    global theme

    if len(sys.argv) == 3:
        player_name = sys.argv[1]
        theme = sys.argv[2]
    else:
        player_name = "Jane Doe"
        theme = "WARM"
    
    tetris()
    sense.clear()
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Clear screen before force exit"
        sense.clear()
        pygame.quit()
        sys.exit()
