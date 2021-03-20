import os, sys, pygame, math
from clases import *
from carga_inicial import  carga_inicial, cargar_piezas, centrar

pygame.init()

blancas, negras, tablero_sprite, screen, tablero_virtual = carga_inicial()
dragging = False


while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sprite = blancas.click(event.pos)
            if sprite:
                dragging = True
                mouse_x,mouse_y =event.pos
                sprite.pos_moves(tablero_virtual)
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                sprite.try_move(centrar(event.pos),tablero_virtual)
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                sprite.rect.center=event.pos
    screen.blit(tablero_sprite,tablero_sprite.get_rect())
    negras.draw(screen)
    blancas.draw(screen)
    if dragging:            sprite.show_moves(screen,tablero_virtual)
    pygame.display.flip()
