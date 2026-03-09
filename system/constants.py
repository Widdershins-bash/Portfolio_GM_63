import pygame
from enum import Enum, auto


class Main:
    GRID_CONSTANT: int = 32  # tile size in px


class Screen:
    LOGICAL_WIDTH: int = 640
    LOGICAL_HEIGHT: int = 360
    FPS: int = 120


class Image:
    IMAGE_PATH: str = "assets/images/"


class Audio:
    AUDIO_PATH: str = "assets/audio/"


# color palette
class ColorPalette:
    BLACK: pygame.typing.ColorLike = (0, 0, 0)
    WHITE: pygame.typing.ColorLike = (255, 255, 255)


class GameState(Enum):
    MAIN_MENU = auto()
    PLAY = auto()
    QUIT = auto()
    SETTINGS = auto()
    PAUSE = auto()


class Font:
    BASE: pygame.Font = pygame.Font("freesansbold.ttf")
