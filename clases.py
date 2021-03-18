import pygame, math

class Pieza(pygame.sprite.Sprite):

    def __init__(self, image,pos=0):

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos

    def move(self,new_pos,tablero_virtual, can_move):

        if can_move:
            tablero_virtual[self.pos]["pieza"] = None
            self.rect.center=tablero_virtual[new_pos]["pos"]
            self.pos = new_pos
            tablero_virtual[new_pos]["pieza"] = self
        else:
            self.rect.center=tablero_virtual[self.pos]["pos"]

class Torre(Pieza):

    def __init__(self, image, pos=0):
        Pieza.__init__(self, image, pos)

    def pos_moves(self, tablero_virtual):
        moves = []
        for i in range(1,9-self.pos[1]):
            if not tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"] == None:
                break
            moves.append((self.pos[0],self.pos[1]+i))

        for i in range(self.pos[1]-1,0, -1):
            if not tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                break
            moves.append((self.pos[0],i))

        for i in range(1,9-self.pos[0]):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1])]["pieza"] == None:
                break
            moves.append((self.pos[0]+i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                break
            moves.append((i,self.pos[1]))

        return moves

    def try_move(self, new_pos,tablero_virtual):
        moves = self.pos_moves(tablero_virtual)
        can_move = new_pos in moves
        self.move(new_pos,tablero_virtual,can_move)

class Peon(Pieza):
    def __init__(self, image,pos=0):

        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):

        moves = [] 
        if (self.pos[0]+1 < 9) and tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"]:
            moves.append((self.pos[0]+1,self.pos[1]+1))

        if (self.pos[0]-1 > 0) and tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"]:
            moves.append((self.pos[0]-1,self.pos[1]+1))

        if tablero_virtual[(self.pos[0],self.pos[1]+1)]["pieza"] == None:
            moves.append((self.pos[0],self.pos[1]+1))

        return moves

    def try_move(self, new_pos,tablero_virtual):

        moves = self.pos_moves(tablero_virtual)
        can_move = new_pos in moves
        self.move(new_pos,tablero_virtual,can_move)



class Alfil(Pieza):
    def __init__(self, image,pos=0):

        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):

        moves = []

        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>=10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<=10 ) else 8 - self.pos[1]
        for i in range(1,9-max_pos):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                break
            moves.append((self.pos[0]+i,self.pos[1]+i))

        for i in range(1,min_pos):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                break
            moves.append((self.pos[0]-i,self.pos[1]-i))

        for i in range(1,min_min):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                break
            moves.append((self.pos[0]+i,self.pos[1]-i))
        
        for i in range(1,max_max):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                break
            moves.append((self.pos[0]-i,self.pos[1]+i))

        return moves

    def try_move(self, new_pos, tablero_virtual):
        moves = self.pos_moves(tablero_virtual)
        can_move = new_pos in moves
        self.move(new_pos,tablero_virtual,can_move)

class Reina(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def try_move(self, new_pos,tablero_virtual):
        pos_int = self.pos[0]*10 + self.pos[1]
        new_pos_int = new_pos[0]*10 + new_pos[1]
        can_move = ((pos_int-new_pos_int)%11==0 or (pos_int-new_pos_int)%9==0) or (self.pos[0] == new_pos[0]) or (self.pos[1] == new_pos[1])
        self.move(new_pos,tablero_virtual,can_move)


class Rey(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def try_move(self, new_pos,tablero_virtual):
        pos_moves = [((self.pos[0]+p),(self.pos[1]+j)) for j in [-1,0,1] for p in [-1,0,1]]
        can_move = new_pos in pos_moves
        self.move(new_pos,tablero_virtual,can_move)

class Caballo(Pieza):
    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)
    def try_move(self, new_pos,tablero_virtual):
        pos_moves = {(self.pos[0]+p,self.pos[1]+j) for j in [-2,2] for p in [-1,1]}
        pos_moves2 = {(self.pos[0]+p,self.pos[1]+j) for p in [-2,2] for j in [-1,1]}
        can_move = new_pos in pos_moves or new_pos in pos_moves2
        self.move(new_pos,tablero_virtual,can_move)
        


class Jugador(pygame.sprite.Group):
    def __init__(self, color):
        pygame.sprite.Group.__init__(self)
        self.color = color 
    def click(self,pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                return sprite