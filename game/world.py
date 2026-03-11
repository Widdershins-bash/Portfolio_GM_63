import pygame
from game.floor import FloorManager
from game.camera import Camera
from game.player import Player


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)

        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(
            surface=self.surface,
            player_x=self.player.x_pos,
            player_y=self.player.y_pos,
            grid_constant=self.grid_constant,
        )

    def update(self, delta_time: float):
        self.camera_offset = self.camera.get_offset(
            player_x=self.player.x_pos, player_y=self.player.y_pos, delta_time=delta_time
        )

        self.floor_manager.update(camera_offset=self.camera_offset)
        self.player.update(delta_time=delta_time, camera_offset=self.camera_offset)

    def draw(self):
        self.floor_manager.draw()
        self.player.draw()
