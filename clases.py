import pygame, math
import os, sys, pygame
import logging
import time
import pprint

class Partida():

    def __init__(self,read_mode):
        self.read_mode = read_mode 
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
        self.logger = logging.getLogger('simple_example')
        self.dragging = False
        self.sprite = None
        self.desde = (0,0)

    def main(self):
        pygame.init()
        self.start()
        self.leer()
        if self.read_mode:
            self.test()
        while True:
            self.turno(self.blancas,self.negras)
            self.turno(self.negras,self.blancas)
    
    def turno(self, jugador, oponente):
        
        sigue_mi_turno = True
        event= None
        neutral = False
        while sigue_mi_turno:
            self.screen.blit(self.tablero_sprite,self.tablero_sprite.get_rect())
            if not (self.sprite and self.sprite.king_me):
                sigue_mi_turno = self.cach_event(jugador,oponente)
            else:
                sigue_mi_turno, neutral = self.king_me(neutral)
            self.negras.draw(self.screen)
            self.blancas.draw(self.screen)
            self.negras.add_pos_moves()
            self.blancas.add_pos_moves()
            if self.dragging:
                self.sprite.show_moves(self.screen)
            if not sigue_mi_turno:
                self.logger.info(f"{self.desde[0]}, {self.desde[1]} {self.hacia[0]}, {self.hacia[1]}")
            pygame.display.flip()

    def cach_event(self,jugador, oponente):
        sigue_mi_turno = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sprite = jugador.click(event.pos)
                if self.sprite:
                    self.dragging = True
                    mouse_x,mouse_y =event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    if jugador.color == "negras":
                        self.desde = jugador.b_to_n(self.sprite.pos)
                        sigue_mi_turno = self.sprite.try_move(jugador.b_to_n(self.centrar(event.pos)), oponente, self.screen)
                    else:
                        self.desde = self.sprite.pos
                        sigue_mi_turno = self.sprite.try_move(self.centrar(event.pos), oponente, self.screen)
                    self.hacia = self.centrar(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.sprite.rect.center=event.pos
        return sigue_mi_turno

    def start(self):
        self.logger.setLevel(logging.INFO)
        logging.Formatter('%(message)s')
        handler = logging.FileHandler("jugadas.log","w")
        self.logger.addHandler(handler)
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
            #pieza = Peon(pygame.transform.scale(pygame.image.load(dir_piezas["peon"]).convert_alpha(),(50,50)),(i+1,2))
            pieza_im= pygame.transform.smoothscale(pygame.image.load(dir_piezas["peon"]), (50,50))
            pieza = Peon(pieza_im,(i+1,2))
            pieza.rect.center = jugador.tablero_virtual[(i+1,2)]["pos"]
            jugador.tablero_virtual[(i+1,2)]["pieza"] = pieza
            jugador.add(pieza)
        piezas["torre_L"] = Torre(pygame.image.load(dir_piezas["torre"]))
        piezas["caballo_L"] = Caballo(pygame.image.load(dir_piezas["caballo"]))
        piezas["alfil_L"] = Alfil(pygame.image.load(dir_piezas["alfil"]))
        piezas["reina"] = Reina(pygame.image.load(dir_piezas["reina"]))
        piezas["rey"] = Rey(pygame.image.load(dir_piezas["rey"]))
        piezas["alfil_D"] = Alfil(pygame.image.load(dir_piezas["alfil"]))
        piezas["caballo_D"] = Caballo(pygame.image.load(dir_piezas["caballo"]))
        piezas["torre_D"] = Torre(pygame.image.load(dir_piezas["torre"]))
        for i, pieza in enumerate(piezas):
            piezas[pieza].image = pygame.transform.smoothscale(piezas[pieza].image,(50,50))
            piezas[pieza].pos = (i+1,1)
            piezas[pieza].rect.center = jugador.tablero_virtual[piezas[pieza].pos]["pos"]
            jugador.tablero_virtual[piezas[pieza].pos]["pieza"] = piezas[pieza]
            jugador.add(piezas[pieza])

    def centrar(self,pos):
        x = pos[0]/self.cas_x
        y = pos[1]/self.cas_y
        return (math.ceil(x),9-math.ceil(y))
    
    def int_to_pix(self,pos):
        x = pos[0]*self.cas_x-self.center_x
        y = (9-pos[1])*self.cas_y-self.center_y
        return (int(x),int(y))

    def leer(self):
        jugadas = []
        f = open("jugadas2.log","r")
        for line in f.read().splitlines():
            lline = line.replace(",","").split(" ")
            jugadas.append(((int(lline[0]),int(lline[1])),(int(lline[2]),int(lline[3]))))
        return jugadas

    def test(self):
        pos = self.leer()
        turno_blancas = True
        for i in range(len(pos)):
            if turno_blancas:
                sprite = self.blancas.click(self.int_to_pix(pos[i][0]))
                sprite.pos_moves()
                sprite.try_move(pos[i][1], self.negras, self.screen)
                turno_blancas = False
            else:
                sprite = self.negras.click(self.int_to_pix(pos[i][0]))
                sprite.try_move(self.negras.b_to_n(pos[i][1]), self.blancas, self.screen)
                turno_blancas = True
            self.screen.blit(self.tablero_sprite,self.tablero_sprite.get_rect())
            self.negras.draw(self.screen)
            self.blancas.draw(self.screen)
            pygame.display.flip()

    def king_me(self, neutral):
        if not neutral: 
            neutral = self.load_neutral()
        choosing = True
        self.king_me_screen()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_sprite = neutral.click(event.pos)
                if new_sprite:
                    new_sprite.pos = self.sprite.pos
                    self.sprite.groups()[0].tablero_virtual[new_sprite.pos]["pieza"] = new_sprite
                    self.sprite.groups()[0].add(new_sprite)
                    new_sprite.rect.center = self.sprite.rect.center
                    new_sprite.groups()[0].remove(new_sprite)
                    self.sprite.kill()
                    self.sprite = new_sprite
                    self.sprite.king_me = False
                    return False, neutral
        neutral.draw(self.screen)
            
        return True, neutral
    
    def king_me_screen(self):
        color = (0, 0, 0)
        R = pygame.Rect( 10,10, 1860/8+10,int(1055/8)+10)
        R.center = ((self.width-self.x_axis)/2, (self.height-self.y_axis)/2)
        shape_surf_2 = pygame.Surface(R.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf_2, color, shape_surf_2.get_rect(), border_radius=10)
        self.screen.blit(shape_surf_2,(R.left+8,R.top+5,R.width, R.height))
        color = (62, 106, 109)
        R = pygame.Rect( 0,0, 1860/8,int(1055/8)+1)
        R.center = ((self.width-self.x_axis)/2, (self.height-self.y_axis)/2)
        shape_surf = pygame.Surface(R.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=10)
        self.screen.blit(shape_surf,(R.left+8,R.top+5,R.width, R.height))

        
    def load_neutral(self):
        jugador = Jugador("Neutro")
        dir_piezas = {}
        piezas ={}
        for i in os.scandir(os.path.join(self.BASE_image, self.sprite.groups()[0].color)):
            dir_piezas[i.name.split(".")[0]] = i.path
        piezas["torre"] = Torre(pygame.image.load(dir_piezas["torre"]))
        piezas["caballo"] = Caballo(pygame.image.load(dir_piezas["caballo"]))
        piezas["alfil"] = Alfil(pygame.image.load(dir_piezas["alfil"]))
        piezas["reina"] = Reina(pygame.image.load(dir_piezas["reina"]))
        for i, pieza in enumerate(piezas):
            piezas[pieza].image = pygame.transform.smoothscale(piezas[pieza].image,(50,50))
            piezas[pieza].rect.center = ((self.width-self.x_axis-self.cas_x+100+ 100*i)/2, (self.height-self.y_axis)/2)
            jugador.add(piezas[pieza])
        return jugador

class Jugador(pygame.sprite.Group):

    def __init__(self, color, tablero_virtual={}):
        pygame.sprite.Group.__init__(self)
        self.color = color
        self.jaque = False
        self.en_pass = False
        self.pos_moves = []
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

    def check_piezas(self):
        for pos in self.tablero_virtual:
            if self.tablero_virtual[pos]["pieza"] != None:
                if len(self.tablero_virtual[pos]["pieza"].groups())< 1:
                    print(self.tablero_virtual[pos])
                    print(pos)

    def add_pos_moves(self):
        self.pos_moves = []
        for sprite in self.sprites():
            sprite.pos_moves()
            self.pos_moves.append(sprite.moves)

class Pieza(pygame.sprite.Sprite):

    def __init__(self, image,pos=(0,0)):

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.moves = []
        self.special_moves = {}
        self.it_move = False 
        self.en_pass = False
        self.king_me = False

    def move(self,new_pos, can_move, oponente):
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        pieza_atacada = self.groups()[0].tablero_virtual[new_pos]["pieza"] 
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.check_jaque(oponente, pieza_atacada)
        if can_move and not self.groups()[0].jaque:
            oponente.flip_the_table(self.groups()[0].tablero_virtual)
            self.pos = new_pos
            if pieza_atacada != None:
                pieza_atacada.kill()
            self.rect.center=self.groups()[0].tablero_virtual[new_pos]["pos"]
            self.it_move = True
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
        for pos in self.special_moves:
            shape_surf = pygame.Surface(pygame.Rect( 0,0, 1860/8,int(1055/8)+1).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            R = pygame.Rect( 0,0, 1860/8,int(1055/8))
            R.center = self.groups()[0].tablero_virtual[pos]['pos']
            screen.blit(shape_surf,(R.left+8,R.top+5,R.width, R.height))

    def try_move(self, new_pos, oponente, screen):
        if new_pos != self.pos:
            can_move = new_pos in self.moves
            self.move(new_pos,can_move, oponente)
            if new_pos == self.pos:
                self.it_move = True
                self.pos_moves()
                return False
        return True

    def can_kill(self, pos):
        pieza = self.groups()[0].tablero_virtual[pos]['pieza']
        if pieza.groups()[0].color!=self.groups()[0].color:
            self.moves.append(pos)
            if isinstance(pieza, Rey):
                pieza.groups()[0].jaque = True
    
    def check_jaque(self, oponente, pieza_atacada):
        self.groups()[0].jaque = False
        for sprite in oponente.sprites():
            if sprite is not pieza_atacada:
                sprite.pos_moves()

class Peon(Pieza):

    def try_move(self, new_pos, oponente, screen):
        np = (self.pos[0],self.pos[1]+2)
        if new_pos != self.pos:
            if new_pos in self.special_moves:
                self.special_move(new_pos,oponente)
            else:
                can_move = new_pos in self.moves
                self.move(new_pos,can_move, oponente)
            if new_pos == self.pos:
                if new_pos == np:
                    self.en_pass = True
                    self.groups()[0].en_pass = True
                elif self.groups()[0].en_pass:
                    self.groups()[0].en_pass = False
                    for sprite in self.groups()[0].sprites():
                        sprite.en_pass = False
                if self.pos[1] == 8:
                    self.king_me = True
                    return True
                self.pos_moves()
                return False
        return True      
    
    def special_move(self,new_pos,oponente):
        pos_pieza = (new_pos[0],new_pos[1]-1)     
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        pieza_atacada = self.groups()[0].tablero_virtual[pos_pieza]["pieza"] 
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.check_jaque(oponente,pieza_atacada)
        if not self.groups()[0].jaque:
            self.groups()[0].tablero_virtual[pos_pieza]["pieza"] = None
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
        self.special_moves = {}
        self.moves = []

        if self.pos[1] != 8:
            if (self.pos[0]+1 < 9) and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1]+1)]["pieza"] != None:
                self.can_kill((self.pos[0]+1,self.pos[1]+1))

            if (self.pos[0]-1 > 0) and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1]+1)]["pieza"] != None:
                self.can_kill((self.pos[0]-1,self.pos[1]+1))

            if self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+1)]["pieza"] == None:
                self.moves.append((self.pos[0],self.pos[1]+1))
                if not self.it_move and self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+2)]["pieza"] == None:
                    self.moves.append((self.pos[0],self.pos[1]+2))

            if (self.pos[0]+1 < 9) and self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1])]["pieza"] != None:
                self.try_en_pass((self.pos[0]+1,self.pos[1]))
            if (self.pos[0]-1 > 0) and self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1])]["pieza"] != None:
                self.try_en_pass((self.pos[0]-1,self.pos[1]))

    def try_en_pass(self,move):
        pieza = self.groups()[0].tablero_virtual[move]["pieza"]
        if pieza.groups()[0].color!=self.groups()[0].color and pieza.en_pass:
            self.special_moves[(move[0],move[1]+1)] = "en_pass"

class Rey(Pieza):

    def pos_moves(self):
        self.moves = []
        self.special_moves = {}
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                move = (self.pos[0]+i,self.pos[1]+j)
                if min(move)>0 and max(move)<9:
                    if self.groups()[0].tablero_virtual[move]["pieza"] != None:
                        self.can_kill(move)
                    else:
                        self.moves.append(move)
        if not self.it_move:
            self.check_rock()

    def check_rock(self):
        cond_1 = self.groups()[0].tablero_virtual[(self.pos[0]-1,self.pos[1])]["pieza"] == None
        cond_2 = self.groups()[0].tablero_virtual[(self.pos[0]-2,self.pos[1])]["pieza"] == None
        cond_3 = self.groups()[0].tablero_virtual[(self.pos[0]-3,self.pos[1])]["pieza"] == None
        if self.groups()[0].tablero_virtual[(self.pos[0]-4,self.pos[1])]["pieza"]:
            cond_4 = not self.groups()[0].tablero_virtual[(self.pos[0]-4,self.pos[1])]["pieza"].it_move
            if cond_1 and cond_2 and cond_3 and cond_4:
                self.special_moves[(self.pos[0]-2,self.pos[1])] = [(self.pos[0]-4,self.pos[1]), (self.pos[0]-1,self.pos[1])]
        cond_1 = self.groups()[0].tablero_virtual[(self.pos[0]+1,self.pos[1])]["pieza"] == None
        cond_2 = self.groups()[0].tablero_virtual[(self.pos[0]+2,self.pos[1])]["pieza"] == None
        if self.groups()[0].tablero_virtual[(self.pos[0]+3,self.pos[1])]["pieza"]:
            cond_3 = not self.groups()[0].tablero_virtual[(self.pos[0]+3,self.pos[1])]["pieza"].it_move
            if cond_1 and cond_2 and cond_3:
                self.special_moves[(self.pos[0]+2,self.pos[1])] = [(self.pos[0]+3,self.pos[1]), (self.pos[0]+1,self.pos[1])]

    def try_move(self, new_pos, oponente, screen):
        if new_pos != self.pos:
            if new_pos in self.special_moves:
                self.special_move(new_pos,oponente)
            else:
                can_move = new_pos in self.moves
                self.move(new_pos,can_move, oponente)
            if new_pos == self.pos:
                if self.groups()[0].en_pass:
                    self.groups()[0].en_pass = False
                    for sprite in self.groups()[0].sprites():
                        sprite.en_pass = False
                if not self.it_move:
                    self.it_move = True
                self.pos_moves()
                return False
        return True  

    def special_move(self,new_pos,oponente):
        old_r_pos = self.special_moves[new_pos][0]
        new_r_pos = self.special_moves[new_pos][1]
        rock = self.groups()[0].tablero_virtual[old_r_pos]["pieza"]
        self.groups()[0].tablero_virtual[self.pos]["pieza"] = None
        self.groups()[0].tablero_virtual[new_pos]["pieza"] = self
        self.groups()[0].tablero_virtual[old_r_pos]["pieza"] = None
        self.groups()[0].tablero_virtual[new_r_pos]["pieza"] = rock
        oponente.flip_the_table(self.groups()[0].tablero_virtual)
        self.pos = new_pos
        rock.pos = new_r_pos
        self.rect.center=self.groups()[0].tablero_virtual[new_pos]["pos"]
        rock.rect.center=self.groups()[0].tablero_virtual[new_r_pos]["pos"]
        
class Caballo(Pieza):

    def pos_moves(self):
        self.moves = []
        pos_moves = [(self.pos[0]+p,self.pos[1]+j) for j in [-2,2] for p in [-1,1]] + [(self.pos[0]+p,self.pos[1]+j) for p in [-2,2] for j in [-1,1]]
        for move in pos_moves:
            if min(move)>0 and max(move)<9:
                if self.groups()[0].tablero_virtual[move]["pieza"] != None:
                    self.can_kill(move)
                else:
                    self.moves.append(move)

class Torre(Pieza):

    def pos_moves(self):
        self.moves = []
        for i in range(self.pos[1]+1,9):
            if not self.groups()[0].tablero_virtual[(self.pos[0],self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0],self.pos[1]+i))
                break
            self.moves.append((self.pos[0],self.pos[1]+i))

        for i in range(self.pos[1]-1,0, -1):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i))
                break
            self.moves.append((self.pos[0],i))

        for i in range(self.pos[0]+1,9):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]))
                break
            self.moves.append((i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]))
                break
            self.moves.append((i,self.pos[1]))

class Alfil(Pieza):

    def pos_moves(self):

        self.moves = []
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<10 ) else 9 - self.pos[1]
        #Diagonal izquierda hacia adelante
        for i in range(1,9-max_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]+i))
                break
            self.moves.append((self.pos[0]+i,self.pos[1]+i))

        #Diagonal izquierda hacia atras
        for i in range(1,min_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]-i))
                break
            self.moves.append((self.pos[0]-i,self.pos[1]-i))

        #Diagonal derecha hacia adelante
        for i in range(1,max_max):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]+i))
                break
            self.moves.append((self.pos[0]-i,self.pos[1]+i))

        #Diagonal derecha hacia atras
        for i in range(1,min_min):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]-i))
                break
            self.moves.append((self.pos[0]+i,self.pos[1]-i))

class Reina(Pieza):

    def pos_moves(self):

        self.moves = []

        #Movimientos tipo alfil
        max_pos = max(self.pos)
        min_pos = min(self.pos)
        min_min = 9 - self.pos[0] if ( sum(self.pos)>10 ) else self.pos[1]
        max_max = self.pos[0] if ( sum(self.pos)<10 ) else 9 - self.pos[1]
        
        for i in range(1,9-max_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]+i))
                break
            self.moves.append((self.pos[0]+i,self.pos[1]+i))
        
        for i in range(1,min_pos):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]-i))
                break
            self.moves.append((self.pos[0]-i,self.pos[1]-i))

        for i in range(1,min_min):
            if not self.groups()[0].tablero_virtual[(self.pos[0]+i,self.pos[1]-i)]["pieza"] == None:
                self.can_kill((self.pos[0]+i,self.pos[1]-i))
                break
            self.moves.append((self.pos[0]+i,self.pos[1]-i))
        for i in range(1,max_max):
            if not self.groups()[0].tablero_virtual[(self.pos[0]-i,self.pos[1]+i)]["pieza"] == None:
                self.can_kill((self.pos[0]-i,self.pos[1]+i))
                break
            self.moves.append((self.pos[0]-i,self.pos[1]+i))
        
        #Movimientos tipo torre
        
        for i in range(self.pos[1]+1,9):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i))
                break
            self.moves.append((self.pos[0],i))

        for i in range(self.pos[1]-1,0, -1):
            if not self.groups()[0].tablero_virtual[(self.pos[0],i)]["pieza"] == None:
                self.can_kill((self.pos[0],i))
                break
            self.moves.append((self.pos[0],i))

        for i in range(1+self.pos[0],9):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]))
                break
            self.moves.append((i,self.pos[1]))

        for i in range(self.pos[0]-1,0,-1):
            if not self.groups()[0].tablero_virtual[(i,self.pos[1])]["pieza"] == None:
                self.can_kill((i,self.pos[1]))
                break
            self.moves.append((i,self.pos[1]))
