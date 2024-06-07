import pygame
from pygame.sprite import Sprite


class StarBackground(Sprite):
    """Background of stars to brighten the background."""

    def __init__(self, ai_game) -> None:
        super().__init__()
        """Init surface, rect, game screen"""
        self.screen = ai_game.screen
        self.image = pygame.image.load("images/star.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
