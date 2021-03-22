import pygame
import sys
from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sketch with pygame")
clock = pygame.time.Clock()

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (103, 47, 120)
YELLOW = (247, 222, 27)
MENU_BG = (44, 47, 82)

color = BLACK
bg_color = WHITE
size = 25
nodes = []
x = y = None

menu_bar = pygame.Surface((40, SCREEN_HEIGHT))
menu_bar.fill(MENU_BG)

canvas_background = pygame.Surface((SCREEN_WIDTH - 40, SCREEN_HEIGHT))
canvas_background.fill(WHITE)

canvas = pygame.Surface((SCREEN_WIDTH - 40, SCREEN_HEIGHT), pygame.SRCALPHA)

class Mouse:
    left = 1
    middle = 2
    right = 3
    scroll_up = 4
    scroll_down = 5

def get_distance(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** (1/2)

def draw_button(color, pos):
    button = pygame.rect.Rect(pos)
    pygame.draw.rect(menu_bar, color, button)
    return button

class Grid:
    def __init__(self):
        self.show_grid = False
        self.grid_size = canvas_background.get_size()
        self.grid = pygame.Surface(self.grid_size, pygame.SRCALPHA)

    def draw_grid(self):
        for i in range(0, self.grid_size[0], 50):
            pygame.draw.aaline(self.grid, BLACK, (i, 0), (i, SCREEN_HEIGHT))
        for i in range(0, self.grid_size[1], 50):
            pygame.draw.aaline(self.grid, BLACK, (0, i), (SCREEN_WIDTH, i))
        self.grid.set_alpha(255)
        canvas_background.blit(self.grid, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if event.button == Mouse.left:
                if x in range(10, 30):
                    if y in range(10, 30):
                        color = RED
                    elif y in range(50, 70):
                        color = BLACK
                    elif y in range(90, 110):
                        color = BLUE
                    elif y in range(130, 150):
                        color = GREEN
                    elif y in range(170, 190):
                        color = PURPLE
                    elif y in range(210, 230):
                        color = YELLOW
                    elif y in range(SCREEN_HEIGHT-10-20, SCREEN_HEIGHT-10):
                        color = WHITE
                
                if x not in range(0, 40):
                    # adjusting x for drawing in a canvas
                    x -= 40
                    point = pygame.rect.Rect(x - size/2, y - size /2, size, size)
                    nodes.append(point)
                    pygame.draw.ellipse(canvas, color, point)
                else:
                    x = y = None
                    
            elif event.button == Mouse.right:
                if x in range(10, 30):
                    if y in range(10, 30):
                        bg_color = RED
                    elif y in range(50, 70):
                        bg_color = BLACK
                    elif y in range(90, 110):
                        bg_color = BLUE
                    elif y in range(130, 150):
                        bg_color = GREEN
                    elif y in range(170, 190):
                        bg_color = PURPLE
                    elif y in range(210, 230):
                        bg_color = YELLOW
                    elif y in range(SCREEN_HEIGHT-10-20, SCREEN_HEIGHT-10):
                        bg_color = WHITE
                
                canvas_background.fill(bg_color)

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                x, y = event.pos

                if x not in range(0, 40):
                    # adjusting x for drawing in a canvas
                    x -= 40
                    point = pygame.rect.Rect(x - size/2, y - size /2, size, size)
                    if nodes and get_distance(nodes[-1].center, (x, y)) <= size * 2:
                        pygame.draw.line(canvas, color, (x, y), nodes[-1].center, size)
                    nodes.append(point)
                    pygame.draw.ellipse(canvas, color, point)
                else:
                    x = y = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # clear screen with escape
                # clean up the nodes and the last clicked point
                canvas_background.fill(bg_color)
                canvas.fill((0, 0, 0, 0))
                x = y = None
                nodes.clear()
            
            if event.key == pygame.K_s:
                # save as image [Ctrl + S]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    filename = filedialog.asksaveasfilename(
                        defaultextension=".jpg", 
                        filetypes=[("JPEG", '*.jpg'), ("PNG", "*.png")]
                    )

                    if filename:
                        pygame.image.save(canvas_background, filename)

            if event.key == pygame.K_l:
                # draw a line [Ctrl + L]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    if x and y and len(nodes) >= 2:
                        pygame.draw.line(canvas, color, (x, y), nodes[-2].center, size)

            if event.key == pygame.K_c:
                # connect a node with the corners of the canvas [Ctrl + C]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    if x and y:
                        corners = [(0, 0), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0)]
                        for corner in corners:
                            pygame.draw.line(canvas, color, (x, y), corner, size)
            
            if event.key == pygame.K_n:
                # connect a node with other nodes [Ctrl + N]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    if len(nodes) >= 2:
                        for node in nodes[:-1]:
                            pygame.draw.line(canvas, color, nodes[-1].center, node.center, size)

            if event.key == pygame.K_a:
                # connect a node with all other nodes [Ctrl + A]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    if len(nodes) >= 2:
                        for node in nodes:
                            for other_node in nodes:
                                if node is not other_node:
                                    pygame.draw.line(canvas, color, node.center, other_node.center, size)

            if event.key == pygame.K_r:
                # clear list of nodes [Ctrl + R]
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    nodes.clear()

            if event.key == pygame.K_z:
                # Undo [Ctrl + Z]
                # Not a perfect implementation since the lines
                # drawn are not stored in nodes
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    if nodes:
                        last_node = nodes.pop()
                        point = pygame.rect.Rect((last_node.x, last_node.y), last_node.size)
                        pygame.draw.ellipse(canvas, bg_color, point)

            if event.key == pygame.K_LEFTBRACKET:
                # Minimum size 10
                if size > 10:
                    size -= 10
        
            if event.key == pygame.K_RIGHTBRACKET:
                # Maximum size 100
                if size < 100:
                    size += 10

    screen.blit(menu_bar, (0, 0))
    screen.blit(canvas_background, (40, 0))
    canvas_background.blit(canvas, (0, 0))

    draw_button(RED, (10, 10, 20, 20))
    draw_button(BLACK, (10, 50, 20, 20))
    draw_button(BLUE, (10, 90, 20, 20))
    draw_button(GREEN, (10, 130, 20, 20))
    draw_button(PURPLE, (10, 170, 20, 20))
    draw_button(YELLOW, (10, 210, 20, 20))
    draw_button(WHITE, (10, SCREEN_HEIGHT-10-20, 20, 20))

    # grid = Grid()
    # grid.draw_grid()

    pygame.display.update()
    clock.tick(FPS)
