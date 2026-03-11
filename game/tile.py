import pygame


class TileConfiguration:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = grid_constant

    def create_tile(self, x: int, y: int, color: pygame.typing.ColorLike) -> Tile:
        tile: Tile = Tile(surface=self.surface, size=self.size, x=x, y=y, color=color)
        return tile


class Tile:
    def __init__(self, surface: pygame.Surface, size: int, x: int, y: int, color: pygame.typing.ColorLike) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size
        self.x_pos: float = x
        self.y_pos: float = y
        self.color: pygame.typing.ColorLike = color

    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.get_rect(), border_radius=2)
