import math, pygame
from utilities import colors

class Grid:
    def __init__(self, width, height, visible=True, font_path='fonts/Montserrat-LightItalic.ttf', position=(1196, 676)):
        self.covered_tiles = 0

        self.width = width
        self.height = height

        self.tile_size = math.gcd(self.width, self.height) / 2
        self.rows = int(height / self.tile_size)
        self.cols = int(width / self.tile_size)

        self.grid = [[False for x in range(self.cols)] for y in range(self.rows)]
        self.visible = visible
        self.font_path = font_path
        self.position = position

        self.text = None
        self.grid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self.visible:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    tile = pygame.rect.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                    pygame.draw.rect(self.grid_surface, colors.C_LIGHT_GRAY, tile, 1)

    def check_collision(self, node):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                tile = pygame.rect.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)

                if not self.grid[row][col] and tile.collidepoint(node.position):
                    self.grid[row][col] = True
                    self.covered_tiles += 1

    def draw(self, surface):
        surface.blit(self.grid_surface, (0, 0))

    def draw_percentage(self, display_surface):
        font = pygame.font.Font(self.font_path, 18)
        if self.text is not None:
            display_surface.fill(colors.C_WHITE, pygame.Rect(self.position, self.text.get_rect().size))
        self.text = font.render("Covered: " + str(self.get_covered_percentage()) + '%', True, colors.C_BLACK)
        display_surface.blit(self.text, self.position)

    def get_covered_percentage(self):
        return round(self.covered_tiles / (self.rows * self.cols) * 100, 2)

    def reset(self):
        self.covered_tiles = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.grid[row][col] = False



