import os, sys, pygame
from clases import Pieza, Jugador

def carga_inicial():
    size = width, height = 1920, 1080
    global casillero_x
    casillero_x = 1860/8
    global casillero_y
    casillero_y = int(1055/8)
    global centro_x 
    centro_x = casillero_x/2
    global centro_y
    centro_y = casillero_y/2


    screen = pygame.display.set_mode(size)
    global BASE_DIR
    BASE_DIR = os.getcwd()
    global BASE_image
    BASE_image = os.path.join(BASE_DIR,"imagenes")

    #imagenes
    tablero =  pygame.image.load(os.path.join(BASE_image, "tablero.jpg")).convert()
    tablero = pygame.transform.scale(tablero, size)
    blancas = Jugador("blancas")
    negras = Jugador("negras")
    cargar_piezas(blancas)
    cargar_piezas(negras)

    return blancas, negras, tablero, screen
    

def cargar_piezas(jugador):
    dir_piezas = {}
    piezas ={}
    for i in os.scandir(os.path.join(BASE_image, jugador.color)):
        dir_piezas[i.name.split(".")[0]] = i.path
    offset = casillero_y
    if jugador.color == "blancas":
        offset = 6*casillero_y
    for i in range(8):
        pieza = Pieza(pygame.image.load(dir_piezas["peon"]).convert_alpha())
        pieza.rect.center = (centro_x+i*casillero_x,centro_y+offset)
        print(pieza.rect.center)
        jugador.add(pieza)
    offset = 0
    if jugador.color == "blancas":
        offset = 7*casillero_y
    piezas["torre_L"] = Pieza(pygame.image.load(dir_piezas["torre"]).convert_alpha())
    piezas["caballo_L"] = Pieza(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
    piezas["alfil_L"] = Pieza(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
    piezas["reina"] = Pieza(pygame.image.load(dir_piezas["reina"]).convert_alpha())
    piezas["rey"] = Pieza(pygame.image.load(dir_piezas["rey"]).convert_alpha())
    piezas["alfil_D"] = Pieza(pygame.image.load(dir_piezas["alfil"]).convert_alpha())
    piezas["caballo_D"] = Pieza(pygame.image.load(dir_piezas["caballo"]).convert_alpha())
    piezas["torre_D"] = Pieza(pygame.image.load(dir_piezas["torre"]).convert_alpha())
    for i, pieza in enumerate(piezas):
        piezas[pieza].rect.center = (centro_x+i*casillero_x,centro_y+offset)
        jugador.add(piezas[pieza])



