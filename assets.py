import pygame
from main import SIZE


class Assets:
    """Przechowuje zasoby."""

    @staticmethod
    def load():
        """Wczytuje zasoby z dysku."""
        Assets.WHITE_PAWN = pygame.transform.scale(pygame.image.load("pawn_white.png"), (SIZE, SIZE))
        Assets.BLACK_PAWN = pygame.transform.scale(pygame.image.load("pawn_black.png"), (SIZE, SIZE))
        Assets.WHITE_QUEEN = pygame.transform.scale(pygame.image.load("queen_white.png"), (SIZE, SIZE))
        Assets.BLACK_QUEEN = pygame.transform.scale(pygame.image.load("queen_black.png"), (SIZE, SIZE))