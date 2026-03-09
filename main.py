import pygame
from game.tile import Tile
from system.screen import Screen
from system.constants import GRID_CONSTANT, GameState as gs, IMAGE_PATH


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

    image_x: float = 300
    image_y: float = 200

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

        # ----------------------------- testing image ------------------------------

        placeholder_image: pygame.Surface = pygame.image.load(IMAGE_PATH + "Boat.png")

        speed: float = 60 * delta_time

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            image_x += speed

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            image_x -= speed

        if pygame.key.get_pressed()[pygame.K_UP]:
            image_y -= speed

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            image_y += speed

        screen.logical.blit(placeholder_image, (image_x, image_y))

        # -------------------------------- end test --------------------------------

        screen.draw_overlay()
        screen.scale_flip()

    pygame.quit()
