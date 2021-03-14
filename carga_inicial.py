import os, sys, pygame
from clases import *

def carga_inicial():
    global casillero_x
    global casillero_y
    global centro_x 
    global centro_y
    global BASE_DIR
    global BASE_image
    size = width, height = 1920, 1080
    casillero_x = 1860/8
    casillero_y = int(1055/8)
    centro_x = casillero_x/2
    centro_y = casillero_y/2
    screen = pygame.display.set_mode(size)
    BASE_DIR = os.getcwd()
    BASE_image = os.path.join(BASE_DIR,"imagenes")
    tablero_virtual = crear_tablero()
    tablero_sprite =  pygame.image.load(os.path.join(BASE_image, "tablero.jpg")).convert()
    tablero_sprite = pygame.transform.scale(tablero_sprite, size)
    blancas = Jugador("blancas")
    negras = Jugador("negras")
    cargar_piezas(blancas,tablero_virtual)
    cargar_piezas(negras,tablero_virtual)

    return blancas, negras, tablero_sprite, screen
    
def crear_tablero():
    tablero_virtual = {}
    for i in range(8):
        for j in range(8):
            tablero_virtual[str(j+1)+str(i+1)]= {"pos": (centro_x+j*casillero_x,centro_y+i*casillero_y), "pieza": None}
    return tablero_virtual

def cargar_piezas(jugador,tablero_virtual):
    dir_piezas = {}
    piezas ={}
    for i in os.scandir(os.path.join(BASE_image, jugador.color)):
        dir_piezas[i.name.split(".")[0]] = i.path
    offset = '2'
    if jugador.color == "blancas":
        offset = '7'
    for i in range(8):
        pieza = Pieza(pygame.image.load(dir_piezas["peon"]).convert_alpha(),str(i+1)+offset)
        pieza.rect.center = tablero_virtual[str(i+1)+offset]["pos"]
        tablero_virtual[str(i+1)+offset]["pieza"] = pieza
        jugador.add(pieza)
    piezas["torre_L"] = Torre(pygame.image.load(dir_piezas["torre"]).convert_alpha())
    piezas["torre_D"] = Torre(pygame.image.load(dir_piezas["torre"]).convert_alpha())
    piezas["caballo_L"] = Caballo(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
    piezas["caballo_D"] = Caballo(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
    piezas["alfil_L"] = Alfil(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
    piezas["alfil_D"] = Alfil(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
    piezas["reina"] = Reina(pygame.image.load(dir_piezas["reina"]).convert_alpha())
    piezas["rey"] = Rey(pygame.image.load(dir_piezas["rey"]).convert_alpha())
    offset = '1'
    if jugador.color == "blancas":
        offset = '8'
    for i, pieza in enumerate(piezas):
        piezas[pieza].rect.center = tablero_virtual[str(i+1)+offset]["pos"]
        piezas[pieza].pos = str(i+1)+offset
        tablero_virtual[str(i+1)+offset]["pieza"] = pieza
        jugador.add(piezas[pieza])