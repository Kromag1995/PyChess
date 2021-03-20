import pygame, math

class Pieza(pygame.sprite.Sprite):

    def __init__(self, image,pos=(0,0),moves=[(1,1)]):

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.moves = moves[:] 

    def move(self,new_pos,tablero_virtual, can_move):

        if can_move:
            tablero_virtual[self.pos]["pieza"] = None
            self.rect.center=tablero_virtual[new_pos]["pos"]
            self.pos = new_pos
            if tablero_virtual[new_pos]["pieza"] != None:
                 tablero_virtual[new_pos]["pieza"].kill()
            tablero_virtual[new_pos]["pieza"] = self
        else:
            self.rect.center=tablero_virtual[self.pos]["pos"]
            
    def show_moves(self,screen, tablero_virtual):
        color = (2, 176, 40, 100)
        for pos in self.moves:
            shape_surf = pygame.Surface(pygame.Rect( 0,0, 1860/8,int(1055/8)+1).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            R = pygame.Rect( 0,0, 1860/8,int(1055/8))
            R.center = tablero_virtual[pos]['pos']
            screen.blit(shape_surf,(R.left+8,R.top+5,R.width, R.height))
    
    def try_move(self, new_pos,tablero_virtual):
        can_move = new_pos in self.moves
        self.move(new_pos,tablero_virtual,can_move)
        self.pos_moves(tablero_virtual)

    def can_kill(self, pieza, moves):
        if pieza.groups()[0].color!=self.groups()[0].color:
            moves.append(pieza.pos)

class Torre(Pieza):

    def __init__(self, image, pos=0):
        Pieza.__init__(self, image, pos)

    def pos_moves(self, tablero_virtual):
        moves = []
        for i in range(1,9-self.pos[1]):
            if not tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0],self.pos[1]+i))

        for i in range(self.pos[1]-1,0, -1):
            if not tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0],i)]["pieza"],moves)
                break
            moves.append((self.pos[0],i))

        for i in range(1,9-self.pos[0]):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1])]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1])]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill(tablero_virtual[(i,self.pos[1])]["pieza"],moves)
                break
            moves.append((i,self.pos[1]))

        self.moves = moves[:]

class Peon(Pieza):
    def __init__(self, image,pos=0):

        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):

        moves = [] 
        if (self.pos[0]+1 < 9) and tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"]:
            self.can_kill(tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"],moves)

        if (self.pos[0]-1 > 0) and tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"]:
            self.can_kill(tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"],moves)

        if tablero_virtual[(self.pos[0],self.pos[1]+1)]["pieza"] == None:
            moves.append((self.pos[0],self.pos[1]+1))

        self.moves = moves[:]



class Alfil(Pieza):
    def __init__(self, image,pos=0):

        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):

        moves = []
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<10 ) else 9 - self.pos[1]
        #Diagonal izquierda hacia adelante
        for i in range(1,9-max_pos):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]+i))

        #Diagonal izquierda hacia atras
        for i in range(1,min_pos):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"],moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]-i))

        #Diagonal derecha hacia adelante
        for i in range(1,max_max):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]+i))

        #Diagonal derecha hacia atras
        for i in range(1,min_min):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]-i))
        
        self.moves = moves[:]


class Reina(Pieza):

    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):

        moves = []

        #Movimientos tipo alfil
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>=10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<=10 ) else 8 - self.pos[1]
        
        for i in range(1,9-max_pos):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]+i))

        for i in range(1,min_pos):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"],moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]-i))

        for i in range(1,min_min):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]-i))
        
        for i in range(1,max_max):
            if not tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]+i))

        #Movimientos tipo torre
        for i in range(1,9-self.pos[1]):
            if not tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"],moves)
                break
            moves.append((self.pos[0],self.pos[1]+i))

        for i in range(self.pos[1]-1,0, -1):
            if not tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0],i)]["pieza"],moves)
                break
            moves.append((self.pos[0],i))

        for i in range(1,9-self.pos[0]):
            if not tablero_virtual[(self.pos[0]+i,self.pos[1])]["pieza"] == None:
                self.can_kill(tablero_virtual[(self.pos[0]+i,self.pos[1])]["pieza"],moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill(tablero_virtual[(i,self.pos[1])]["pieza"],moves)
                break
            moves.append((i,self.pos[1]))
        self.moves = moves[:]


class Rey(Pieza):

    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):
        moves = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                move = (self.pos[0]+i,self.pos[1]+j)
                if min(move)>0 and max(move)<9:
                    if tablero_virtual[move]["pieza"] != None:
                        self.can_kill(tablero_virtual[move]["pieza"],moves)
                    moves.append(move)
        self.moves = moves[:]

class Caballo(Pieza):

    def __init__(self, image,pos=0):
        Pieza.__init__(self,image,pos)

    def pos_moves(self, tablero_virtual):
        moves = []
        pos_moves = [(self.pos[0]+p,self.pos[1]+j) for j in [-2,2] for p in [-1,1]] + [(self.pos[0]+p,self.pos[1]+j) for p in [-2,2] for j in [-1,1]]
        for move in pos_moves:
            if min(move)>0 and max(move)<9:
                if tablero_virtual[move]["pieza"] != None:
                    self.can_kill(tablero_virtual[move]["pieza"],moves)
                moves.append(move)
        self.moves = moves[:]
        


class Jugador(pygame.sprite.Group):
    def __init__(self, color):
        pygame.sprite.Group.__init__(self)
        self.color = color 
    def click(self,pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                return sprite