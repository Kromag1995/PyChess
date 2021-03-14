import os, sys, pygame, math
from clases import *
from carga_inicial import  carga_inicial, cargar_piezas

pygame.init()

blancas, negras, tablero_sprite, screen, tablero_virtual = carga_inicial()
dragging = False

def aproximar(pos):
    casillero_x = 1860/8
    casillero_y = int(1055/8)
    x = pos[0]/casillero_x
    y = pos[1]/casillero_y
    return (math.ceil(x),math.ceil(y))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sprite = blancas.click(event.pos)
            if sprite:
                dragging = True
                mouse_x,mouse_y =event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                sprite.move(aproximar(event.pos),tablero_virtual)
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                sprite.rect.center=event.pos
    screen.blit(tablero_sprite,tablero_sprite.get_rect())
    negras.draw(screen)
    blancas.draw(screen)
    pygame.display.flip()
