import pygame
from system.constants import Screen as s, ColorPalette as cp, GameState as gs, Font


class Screen:
    def __init__(self) -> None:

        self.logical_width: int = s.LOGICAL_WIDTH
        self.logical_height: int = s.LOGICAL_HEIGHT

        self.font: pygame.Font = Font.BASE

        self.fps: int = s.FPS
        self.clock: pygame.Clock = pygame.time.Clock()

        self.running: bool = True

        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.logical_width, self.logical_height), pygame.RESIZABLE
        )

        self.logical: pygame.Surface = pygame.Surface((self.logical_width, self.logical_height))
        self.alpha: pygame.Surface = pygame.Surface((self.logical_width, self.logical_height), flags=pygame.SRCALPHA)
        self.viewport: pygame.Rect = pygame.Rect(0, 0, 0, 0)  # used to check mouse -> screen overlap (eventually)
        self.scalar: float = 1.0

    def handle_events(self, event: pygame.Event, game_state: gs) -> None:
        if game_state == gs.QUIT or event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.KEYDOWN:
            self.running = event.key != pygame.K_ESCAPE  # temporary escape option for testing

        if event.type == pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        elif event.type == pygame.WINDOWMINIMIZED:
            self.screen = pygame.display.set_mode((self.logical_width, self.logical_height), pygame.RESIZABLE)

    def clear(self):
        self.logical.fill(cp.BLACK)

    def scale_flip(self) -> None:
        self.logical.blit(self.alpha, (0, 0))

        screen_width: int = self.screen.get_width()
        screen_height: int = self.screen.get_height()
        fit_scale: float = min(screen_width / self.logical_width, screen_height / self.logical_height)
        self.scalar = fit_scale

        scaled_width: int = max(1, int(self.logical_width * fit_scale))
        scaled_height: int = max(1, int(self.logical_height * fit_scale))
        scale_point: tuple[int, int] = (scaled_width, scaled_height)
        logical_transform: pygame.Surface = pygame.transform.scale(self.logical, scale_point)
        logical_location: tuple[int, int] = (
            (screen_width - logical_transform.get_width()) // 2,
            (screen_height - logical_transform.get_height()) // 2,
        )

        self.viewport = pygame.Rect(logical_location, scale_point)
        self.screen.fill(cp.BLACK)
        self.screen.blit(logical_transform, logical_location)
        self.alpha.fill((0, 0, 0, 0))

        pygame.display.flip()
