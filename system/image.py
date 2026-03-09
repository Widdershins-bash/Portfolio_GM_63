import pygame
from system.constants import Image as im


# NOTE: this will be updated in the future with more classes and definitions to accomadate.


class Image:
    def __init__(self) -> None:
        self.path: str = im.IMAGE_PATH

        self.boat: pygame.Surface = self.gen_image(path=self.path + "Boat.png")

    def gen_image(self, path: str, scalar: float | None = None) -> pygame.Surface:
        image: pygame.Surface = pygame.image.load(path)
        if scalar:
            pygame.transform.scale_by(image, scalar)

        return image
