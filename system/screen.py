import pygame
from system.constants import FPS, LOGICAL_WIDTH, LOGICAL_HEIGHT, ColorPalette as cp, GameState as gs


class Screen:
    def __init__(self, grid_constant: int) -> None:
        self.grid_constant: int = grid_constant

        self.logical_width: int = LOGICAL_WIDTH
        self.logical_height: int = LOGICAL_HEIGHT

        self.fps_font: pygame.Font = pygame.Font("freesansbold.ttf", 12)
        self.tip_font: pygame.Font = pygame.Font("freesansbold.ttf")

        self.fps: int = FPS
        self.clock: pygame.Clock = pygame.time.Clock()

        self.running: bool = True
        self.fullscreen: bool = False

        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.logical_width, self.logical_height), pygame.RESIZABLE
        )

        self.logical: pygame.Surface = pygame.Surface((self.logical_width, self.logical_height))
        self.viewport: pygame.Rect = pygame.Rect(0, 0, 0, 0)  # used to check mouse -> screen overlap
        self.scalar: int = 1

    def display_tips(self) -> None:
        if not self.fullscreen:
            note_message: str = "Press F for Fullscreen"
            note_render: pygame.Surface = self.tip_font.render(note_message, False, cp.BLACK)
            note_pos: tuple[int, int] = (
                (self.logical_width - note_render.width) // 2,
                self.grid_constant + (self.grid_constant - note_render.height) // 2,
            )
            self.logical.blit(note_render, note_pos)

    def handle_events(self, event: pygame.Event, game_state: gs) -> None:
        if game_state == gs.QUIT or event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.KEYDOWN:
            self.running = event.key != pygame.K_ESCAPE or self.fullscreen  # temporary escape option for testing

            if event.key == pygame.K_f:
                if self.fullscreen:
                    self.screen = pygame.display.set_mode((self.logical_width, self.logical_height), pygame.RESIZABLE)

                else:
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.fullscreen = not self.fullscreen

    def draw_overlay(self) -> None:
        self.display_tips()

    def scale_flip(self) -> None:

        self.scalar = max(1, min(self.screen.width, self.screen.height) // self.logical_height)
        scale_point: tuple[int, int] = (self.logical_width * self.scalar, self.logical_height * self.scalar)
        logical_transform: pygame.Surface = pygame.transform.scale(self.logical, scale_point)
        logical_location: tuple[int, int] = (
            (self.screen.width - logical_transform.width) // 2,
            (self.screen.height - logical_transform.height) // 2,
        )

        self.viewport = pygame.Rect(logical_location, scale_point)
        self.screen.blit(logical_transform, logical_location)

        pygame.display.flip()
