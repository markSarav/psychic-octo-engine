import pygame
from ship import Ship

class AlienShip(Ship):
    """An alien ship (child of Ship)"""
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)
        self.image = pygame.image.load('images/alien_ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
    