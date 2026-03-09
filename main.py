import pygame
from game.tile import Tile
from system.screen import Screen
from system.constants import GRID_CONSTANT, GameState as gs


pygame.init()


def get_delta_time(clock: pygame.Clock, fps: int):
    delta_time: float = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    return delta_time


screen: Screen = Screen(grid_constant=GRID_CONSTANT)

tile: Tile = Tile(surface=screen.logical)

if __name__ == "__main__":

    color_seq: float = 0
    game_state: gs = gs.PLAY

    while screen.running:
        for event in pygame.event.get():
            if screen.running:
                screen.handle_events(event=event, game_state=game_state)

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)

        color_seq += 50 * delta_time
        red: int = int(color_seq) % 255
        green: int = (int(color_seq) + 85) % 255
        blue: int = (int(color_seq) + 170) % 255
        screen.logical.fill((red, green, blue))

        tile.create_platform(width=10, height=10)

        screen.draw_overlay()
        screen.scale_flip()

    pygame.quit()
