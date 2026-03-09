import pygame
from enum import Enum, auto

# main
GRID_CONSTANT: int = 32  # tile size in px

# screen
LOGICAL_WIDTH: int = 640
LOGICAL_HEIGHT: int = 360
FPS: int = 120

# image
IMAGE_PATH: str = "assets/images/"

# music
MUSIC_PATH: str = "assets/audio/"


# color palette
class ColorPalette:
    BLACK: pygame.typing.ColorLike = (0, 0, 0)


# game state
class GameState(Enum):
    MAIN_MENU = auto()
    PLAY = auto()
    QUIT = auto()
    SETTINGS = auto()
    PAUSE = auto()


# fonts
class Font: ...
