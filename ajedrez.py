import os, sys, pygame
from clases import *
from carga_inicial import  carga_inicial, cargar_piezas

pygame.init()
blancas, negras, tablero, screen = carga_inicial()

dragging = False
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sprite = blancas.click(event.pos)
            if sprite:
                dragging = True
                mouse_x,mouse_y =event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            print(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                sprite.rect.center=event.pos
    screen.blit(tablero,tablero.get_rect())
    negras.draw(screen)
    blancas.draw(screen)
    pygame.display.flip()