import pygame
from system.constants import Player as p, ColorPalette as cp


class Player:
    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size

        self.x_pos: float = self.surface.width // 2
        self.y_pos: float = self.surface.height // 2

    def handle_movement(self, delta_time: float) -> None:
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.y_pos -= p.SPEED * delta_time

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.y_pos += p.SPEED * delta_time

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x_pos += p.SPEED * delta_time

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x_pos -= p.SPEED * delta_time

    def get_rect(self) -> pygame.Rect:
        rect: pygame.Rect = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)
        return rect

    def update(self, delta_time: float, camera_offset: tuple[float, float]) -> None:
        self.handle_movement(delta_time=delta_time)

        self.x_pos += camera_offset[0]
        self.y_pos += camera_offset[1]

    def draw(self) -> None:
        pygame.draw.rect(self.surface, cp.YELLOW, self.get_rect())
