import pygame
from system.constants import Audio as ad


class SFX:
    def __init__(self) -> None:
        self.path: str = ad.AUDIO_PATH
        self.audio_state: AudioState = AudioState(volume=50)

        self.swoosh_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "click_shortened.ogg")
        self.swoosh_sfx.set_volume(0)
        self.click_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "click_shortened.ogg")
        self.hover_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "hover_click_shortened.ogg")
        self.walking_sfx: list[pygame.mixer.Sound] = [
            pygame.mixer.Sound(self.path + "stone_step_1.ogg"),
            pygame.mixer.Sound(self.path + "stone_step_2.ogg"),
            pygame.mixer.Sound(self.path + "stone_step_3.ogg"),
            pygame.mixer.Sound(self.path + "stone_step_4.ogg"),
        ]
        self.upgrade_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "collect.ogg")
        self.level_complete_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "shortwin.ogg")

        pygame.mixer.music.load(self.path + "VGM.mp3")
        pygame.mixer.music.play(-1)

        self.audio_state.set_volume(value=50)
        self.update_volume()

    def update_volume(self) -> None:
        converted_volume: float = self.audio_state.volume / 100

        self.click_sfx.set_volume(converted_volume)
        self.hover_sfx.set_volume(converted_volume)
        for step in self.walking_sfx:
            step.set_volume(converted_volume)
        pygame.mixer.music.set_volume(converted_volume - 0.2)


class AudioState:
    def __init__(self, volume: int = 50) -> None:
        self.volume: int = max(0, min(100, volume))

    def set_volume(self, value: int) -> None:
        self.volume: int = max(0, min(100, value))
