import pygame
from system.constants import Font, ColorPalette as cp, Menu


class Stats:
    def __init__(self, surface: pygame.Surface, init_floor_size: tuple[int, int]) -> None:
        self.surface: pygame.Surface = surface

        self.font: pygame.Font = Font.STATS
        self.font_color: pygame.typing.ColorLike = cp.BLACK

        self.floor: int = 1
        self.highest_floor: int = self.floor
        self.speed: int = 0
        self.floor_size: tuple[int, int] = init_floor_size

        self.timer_on: bool = False
        self.initial_time: int = 1
        self.timer: float = self.initial_time

        self.margin: int = 5
        self.surfaces: list[pygame.Surface] = []

    def get_score_surface(self) -> pygame.Surface:
        text: str = f"Floor: {self.floor}"
        return self.font.render(text, True, self.font_color)

    def get_speed_surface(self) -> pygame.Surface:
        text: str = f"Speed: +%{self.speed}"
        return self.font.render(text, True, self.font_color)

    def get_floor_size_surface(self) -> pygame.Surface:
        text: str = f"Dungeon Size: {self.floor_size[0]} x {self.floor_size[1]}"
        return self.font.render(text, True, self.font_color)

    def get_timer_surface(self) -> pygame.Surface:
        text: str = f"Timer: {self.timer:.1f}"
        return self.font.render(text, True, self.font_color)

    def get_highest_floor_surface(self) -> pygame.Surface:
        text: str = f"Session Best: {self.highest_floor}"
        return self.font.render(text, True, self.font_color)

    def get_box_size(self) -> tuple[int, int]:
        largest_width: int = self.surfaces[0].width
        for surface in self.surfaces:
            if surface.width > largest_width:
                largest_width = surface.width

        stat_box_width: int = largest_width + self.margin * 2
        stat_box_height: int = self.surfaces[0].height * len(self.surfaces) + self.margin * 2

        return stat_box_width, stat_box_height

    def start_timer(self):
        self.timer = self.initial_time
        self.timer_on = True

    def update_timer(self, delta_time: float):
        if self.timer <= 0:
            self.timer = 0

        elif self.timer_on:
            self.timer -= delta_time

    def update(self, delta_time: float):
        self.update_timer(delta_time=delta_time)
        self.surfaces = [
            self.get_score_surface(),
            self.get_highest_floor_surface(),
            self.get_speed_surface(),
            self.get_floor_size_surface(),
            self.get_timer_surface(),
        ]

    def display_stat_box(self):
        size_point: tuple[int, int] = self.get_box_size()
        stat_box: pygame.Surface = pygame.Surface(size_point)
        stat_box.fill(cp.GRAY)

        for i, stat in enumerate(self.surfaces):
            stat_box.blit(stat, (self.margin, i * self.surfaces[0].height + self.margin))

        self.surface.blit(stat_box, (Menu.MENU_MARGIN, Menu.MENU_MARGIN))
