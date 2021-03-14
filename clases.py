import pygame

class Pieza(pygame.sprite.Sprite):
    def __init__(self, image,pos=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos

class Torre(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        if (self.pos[0] == new_pos[0]) or (self.pos[1] == new_pos[1]):
            self.pos = new_pos

class Peon(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        if (int(self.pos[1])+1 == int(new_pos[1])):
            self.pos = new_pos

class Alfil(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        pos_int = int(self.pos[0])*10 + int(self.pos[1])*10
        if ((pos_int-new_pos)%11==0 or (pos_int-new_pos)%9==0):
            self.pos = new_pos

class Reina(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        pos_int = int(self.pos[0])*10 + int(self.pos[1])*10
        if ((pos_int-new_pos)%11==0 or (pos_int-new_pos)%9==0):
            self.pos = new_pos
        elif (self.pos[0] == new_pos[0]) or (self.pos[1] == new_pos[1]):
            self.pos = new_pos

class Rey(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        pos_moves = {str(self.pos[0]+p)+str(self.pos[1]+j) for j in [-1,0,1] for p in [-1,0,1]}
        if new_pos in pos_moves:
            self.pos = new_pos

class Caballo(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def move(self, new_pos):
        pos_moves = {str(self.pos[0]+p)+str(self.pos[1]+j) for j in [-2,2] for p in [-1,1]}
        pos_moves2 = {str(self.pos[0]+p)+str(self.pos[1]+j) for p in [-2,2] for j in [-1,1]}
        if (int(self.pos[1])+1 == int(new_pos[1])):
            self.pos = new_pos


class Jugador(pygame.sprite.Group):
    def __init__(self, color):
        pygame.sprite.Group.__init__(self)
        self.color = color 
    def click(self,pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                return sprite