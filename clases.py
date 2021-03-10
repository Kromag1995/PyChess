import pygame

class Pieza(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

class Jugador(pygame.sprite.Group):
    def __init__(self, color):
        pygame.sprite.Group.__init__(self)
        self.color = color 
    def click(self,pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                return sprite