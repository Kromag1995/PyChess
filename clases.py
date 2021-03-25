import pygame, math
from pprint import pprint
import os, sys, pygame


class Partida():
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.size = (self.width, self.height)
        self.x_axis = 80 
        self.cas_x = (self.width-self.x_axis)/8
        self.center_x = self.cas_x/2
        self.y_axis = 25
        self.cas_y = int((self.height-self.y_axis)/8)
        self.center_y = self.cas_y/2
        self.BASE_image = os.path.join(os.getcwd(),"imagenes")
        self.blancas = None
        self.negras = None
        self.tablero_sprite = None
        self.screen = None

    def main(self):
        pygame.init()

        self.start()
        dragging = False

        while True:
            self.turno(self.blancas,self.negras)
            self.turno(self.negras,self.blancas)
   
    def turno(self, jugador, oponente):
        dragging = False
        sigue_mi_turno = True
        while sigue_mi_turno:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sprite = jugador.click(event.pos)
                    if sprite:
                        dragging = True
                        mouse_x,mouse_y =event.pos
                        sprite.pos_moves()
                if event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        dragging = False
                        if jugador.color == "negras":
                            sigue_mi_turno = sprite.try_move(jugador.b_to_n(self.centrar(event.pos)), oponente)
                        else:
                            sigue_mi_turno = sprite.try_move(self.centrar(event.pos), oponente)
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        sprite.rect.center=event.pos
            self.screen.blit(self.tablero_sprite,self.tablero_sprite.get_rect())
            self.negras.draw(self.screen)
            self.blancas.draw(self.screen)
            if dragging:
                sprite.show_moves(self.screen)
            pygame.display.flip()

    def start(self):
        self.screen = pygame.display.set_mode(self.size)
        tablero_virtual = self.crear_tablero()
        self.tablero_sprite =  pygame.image.load(os.path.join(self.BASE_image, "tablero.jpg")).convert()
        self.tablero_sprite = pygame.transform.scale(self.tablero_sprite, self.size)
        self.blancas = Jugador("blancas", tablero_virtual.copy())
        self.negras = Jugador("negras")
        self.cargar_piezas(self.blancas)
        self.negras.flip_the_table(tablero_virtual)
        self.cargar_piezas(self.negras)
        self.blancas.flip_the_table(self.negras.tablero_virtual)
        
    def crear_tablero(self):
        tablero_virtual = {}
        for i in range(8):
            for j in range(8):
                tablero_virtual[(j+1,i+1)]= {"pos": (self.center_x+j*self.cas_x,self.center_y+(7-i)*self.cas_y), "pieza": None}
        return tablero_virtual

    def cargar_piezas(self,jugador):
        dir_piezas = {}
        piezas ={}
        for i in os.scandir(os.path.join(self.BASE_image, jugador.color)):
            dir_piezas[i.name.split(".")[0]] = i.path
        for i in range(8):
            pieza = Peon(pygame.image.load(dir_piezas["peon"]).convert_alpha(),(i+1,2))
            pieza.rect.center = jugador.tablero_virtual[(i+1,2)]["pos"]
            jugador.tablero_virtual[(i+1,2)]["pieza"] = pieza
            jugador.add(pieza)
        piezas["torre_L"] = Torre(pygame.image.load(dir_piezas["torre"]).convert_alpha())
        piezas["caballo_L"] = Caballo(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
        piezas["alfil_L"] = Alfil(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
        piezas["reina"] = Reina(pygame.image.load(dir_piezas["reina"]).convert_alpha())
        piezas["rey"] = Rey(pygame.image.load(dir_piezas["rey"]).convert_alpha())
        piezas["alfil_D"] = Alfil(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
        piezas["caballo_D"] = Caballo(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
        piezas["torre_D"] = Torre(pygame.image.load(dir_piezas["torre"]).convert_alpha())
        for i, pieza in enumerate(piezas):
            piezas[pieza].pos = (i+1,1)
            piezas[pieza].rect.center = jugador.tablero_virtual[piezas[pieza].pos]["pos"]
            jugador.tablero_virtual[piezas[pieza].pos]["pieza"] = piezas[pieza]
            jugador.add(piezas[pieza])

    def centrar(self,pos):
        x = pos[0]/self.cas_x
        y = pos[1]/self.cas_y
        return (math.ceil(x),9-math.ceil(y))

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
    
    def b_to_n(self, pos):
        return pos[0],9-pos[1]

class Pieza(pygame.sprite.Sprite):

    def __init__(self, image,pos=(0,0),moves=[(1,1)]):

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.moves = moves[:]
        self.special_moves = {}
        self.it_move = False 
        self.en_pass = False

    def move(self,new_pos, can_move, oponente):
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        pieza_atacada = self.groups()[0].tablero_virtual[new_pos]["pieza"] 
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.check_jaque(oponente)
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
        if new_pos != self.pos:
            can_move = new_pos in self.moves
            self.move(new_pos,can_move, oponente)
            if new_pos == self.pos:
                self.pos_moves()
                return False
        return True

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


    def try_move(self, new_pos, oponente):
        if new_pos != self.pos:
            if new_pos in self.special_moves:
                self.special_move()
            else:
                can_move = new_pos in self.moves
                self.move(new_pos,can_move, oponente)
            if new_pos == self.pos:
                self.pos_moves()
                return False
        return True      
    
    def special_move(self,new_pos):
        if self.special_moves[new_pos] == "king_me":
            self.kingme()
            return
        pos_pieza = (new_pos[0],new_pos[1]-1)     
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        pieza_atacada = self.groups()[0].tablero_virtual[pos_pieza]["pieza"] 
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.check_jaque(oponente)
        if not self.groups()[0].jaque:
            oponente.flip_the_table(self.groups()[0].tablero_virtual)
            self.pos = new_pos
            if pieza_atacada != None:
                pieza_atacada.kill()
            self.rect.center=self.groups()[0].tablero_virtual[new_pos]["pos"]
            del(pieza_atacada)
        else:
            self.groups()[0].tablero_virtual[self.pos]["pieza"] = self
            self.groups()[0].tablero_virtual[pos_pieza]["pieza"] = pieza_atacada
            self.rect.center=self.groups()[0].tablero_virtual[self.pos]["pos"]
            self.groups()[0].jaque = False


    def pos_moves(self):

        moves = [] 
        if (self.pos[0]+1 < 9) and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"] != None:
            self.can_kill((self.pos[0]+1,self.pos[1]+1),moves)

        if (self.pos[0]-1 > 0) and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"] != None:
            self.can_kill((self.pos[0]-1,self.pos[1]+1),moves)

        if self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+1)]["pieza"] == None:
            moves.append((self.pos[0],self.pos[1]+1))
            if not self.it_move and self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+2)]["pieza"] == None:
                moves.append((self.pos[0],self.pos[1]+2))

        if (self.pos[0]+1 < 9) and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1])]["pieza"] != None:
            self.try_en_pass((self.pos[0]+1,self.pos[1]))
        if (self.pos[0]-1 > 0) and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1])]["pieza"] != None:
            self.try_en_pass((self.pos[0]-1,self.pos[1]))
        self.moves = moves[:]

    def kingme(self):
        # Aparece recuadro con todas las piezas menos el peon.
        # Al hacer click se cambia el sprite del peon
        pass

    def try_en_pass(self,move):
        self.special_moves = {}
        pieza = self.groups()[0].tablero_virtual[move]["pieza"]
        if pieza.groups()[0].color!=self.groups()[0].color and pieza.en_pass:
            self.special_moves[move] = "en_pass"

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
