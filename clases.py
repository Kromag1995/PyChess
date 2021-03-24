import pygame, math
from pprint import pprint


class Pieza(pygame.sprite.Sprite):

    def __init__(self, image,pos=(0,0),moves=[(1,1)]):

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.moves = moves[:]
        self.it_move = False 

    def move(self,new_pos, can_move, oponente):
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        pieza_atacada = self.groups()[0].tablero_virtual[new_pos]["pieza"] 
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.check_jaque(oponente)
        pprint(self.groups()[0].tablero_virtual[(4,7)])
        if can_move and not self.groups()[0].jaque:
            oponente.flip_the_table(self.groups()[0].tablero_virtual)
            self.pos = new_pos
            if pieza_atacada != None:
                pieza_atacada.kill()
            self.rect.center=self.groups()[0].tablero_virtual[new_pos]["pos"]
            del(pieza_atacada)
        else:
            self.groups()[0].tablero_virtual[self.pos]["pieza"] = self
            self.groups()[0].tablero_virtual[new_pos]["pieza"] = pieza_atacada
            self.rect.center=self.groups()[0].tablero_virtual[self.pos]["pos"]
            self.groups()[0].jaque = False
            
    def show_moves(self,screen, color=(2, 176, 40, 100)):
        for pos in self.moves:
            shape_surf = pygame.Surface(pygame.Rect( 0,0, 1860/8,int(1055/8)+1).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            R = pygame.Rect( 0,0, 1860/8,int(1055/8))
            R.center = self.groups()[0].tablero_virtual[pos]['pos']
            screen.blit(shape_surf,(R.left+8,R.top+5,R.width, R.height))
    
    def try_move(self, new_pos, oponente):
        can_move = new_pos in self.moves
        self.move(new_pos,can_move, oponente)
        self.pos_moves()

    def can_kill(self, pos, moves):
        pieza = self.groups()[0].tablero_virtual[pos]['pieza']
        if pieza.groups()[0].color!=self.groups()[0].color:
            moves.append(pos)
            if isinstance(pieza, Rey):
                pieza.groups()[0].jaque = True
    
    def check_jaque(self, oponente):
        for sprite in oponente.sprites():
            sprite.pos_moves()

class Torre(Pieza):

    def pos_moves(self):
        moves = []
        for i in range(self.pos[1]+1,9):
            if not self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0],self.pos[1]+i),moves)
                break
            moves.append((self.pos[0],self.pos[1]+i))

        for i in range(self.pos[1]-1,0, -1):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i),moves)
                break
            moves.append((self.pos[0],i))

        for i in range(self.pos[0]+1,9):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]),moves)
                break
            moves.append((i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]),moves)
                break
            moves.append((i,self.pos[1]))

        self.moves = moves[:]

class Peon(Pieza):

    def pos_moves(self):

        moves = [] 
        if (self.pos[0]+1 < 9) and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"] != None:
            self.can_kill((self.pos[0]+1,self.pos[1]+1),moves)
            if not self.it_move and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1]+2)]["pieza"] != None:
                self.can_kill((self.pos[0]+1,self.pos[1]+2),moves)

        if (self.pos[0]-1 > 0) and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"] != None:
            self.can_kill((self.pos[0]-1,self.pos[1]+1),moves)
            if not self.it_move and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1]+2)]["pieza"] != None:
                self.can_kill((self.pos[0]-1,self.pos[1]+2),moves)

        if self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+1)]["pieza"] == None:
            moves.append((self.pos[0],self.pos[1]+1))
        
            

        self.moves = moves[:]

class Alfil(Pieza):

    def pos_moves(self):

        moves = []
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<10 ) else 9 - self.pos[1]
        #Diagonal izquierda hacia adelante
        for i in range(1,9-max_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]+i),moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]+i))

        #Diagonal izquierda hacia atras
        for i in range(1,min_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]-i),moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]-i))

        #Diagonal derecha hacia adelante
        for i in range(1,max_max):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]+i),moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]+i))

        #Diagonal derecha hacia atras
        for i in range(1,min_min):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]-i),moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]-i))
        
        self.moves = moves[:]

class Reina(Pieza):

    def pos_moves(self):

        moves = []

        #Movimientos tipo alfil
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<10 ) else 9 - self.pos[1]
        
        for i in range(1,9-max_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]+i),moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]+i))
        
        for i in range(1,min_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]-i),moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]-i))

        for i in range(1,min_min):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]-i),moves)
                break
            moves.append((self.pos[0]+i,self.pos[1]-i))
        for i in range(1,max_max):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]+i),moves)
                break
            moves.append((self.pos[0]-i,self.pos[1]+i))
        
        #Movimientos tipo torre
        
        for i in range(self.pos[1]+1,9):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i),moves)
                break
            moves.append((self.pos[0],i))

        for i in range(self.pos[1]-1,0, -1):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i),moves)
                break
            moves.append((self.pos[0],i))

        for i in range(1+self.pos[0],9):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]),moves)
                break
            moves.append((i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]),moves)
                break
            moves.append((i,self.pos[1]))

        self.moves = moves[:]

class Rey(Pieza):

    def pos_moves(self):
        moves = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                move = (self.pos[0]+i,self.pos[1]+j)
                if min(move)>0 and max(move)<9:
                    if self.groups()[0].tablero_virtual[move]["pieza"] != None:
                        self.can_kill(move,moves)
                    else:
                        moves.append(move)
        self.moves = moves[:]
        
class Caballo(Pieza):

    def pos_moves(self):
        moves = []
        pos_moves = [(self.pos[0]+p,self.pos[1]+j) for j in [-2,2] for p in [-1,1]] + [(self.pos[0]+p,self.pos[1]+j) for p in [-2,2] for j in [-1,1]]
        for move in pos_moves:
            if min(move)>0 and max(move)<9:
                #try:
                if self.groups()[0].tablero_virtual[move]["pieza"] != None:
                    self.can_kill(move,moves)
                else:
                    moves.append(move)
                #except:
                #    pass
        self.moves = moves[:]

class Jugador(pygame.sprite.Group):

    def __init__(self, color, tablero_virtual={}):
        pygame.sprite.Group.__init__(self)
        self.color = color
        self.jaque = False
        self.tablero_virtual = tablero_virtual.copy()

    def click(self, pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                return sprite

    def flip_the_table(self, tablero_virtual):
        self.tablero_virtual = {}
        for i in range(8):
            for j in range(8):
                self.tablero_virtual[(j+1,i+1)] = tablero_virtual[(j+1,8-i)]