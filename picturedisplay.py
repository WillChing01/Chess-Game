import pygame
import sys
import os

sys.path.insert(0,os.getcwd())
#sys.path.insert(0,'C:\\Users\\willi\\OneDrive\\Desktop\\Python\\Chess Game')

from engine import *

class Button():
    def __init__(self,text,coords,width,height,colour):
        self.text=text
        self.coords=coords
        self.width=width
        self.height=height
        self.colour=colour

    def display(self):
        pygame

#pygame window.

size=800
title="Chess"
screen=pygame.display.set_mode((int(size),int(size)))

clock=pygame.time.Clock()

white=(255,253,208)
black=(163,72,27)
colours=[white,black]

screen.fill((255,255,255))

pygame.display.flip()

def drawsquares(flip=False):
    for x in range(8):
        for y in range(8):
            colour=colours[(x+y)%2]
            pygame.draw.rect(screen,colour,(round(x*size/8),round(y*size/8),round(size/8),round(size/8)))
            #draw pieces as well.
            coords=[x,7-y]

def drawmenu(size):
    screen.fill((white))

running=True
menu=False

while running:

    if menu==True:
        drawmenu(size)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                running=False

    else:
        
        drawsquares()
    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                running=False
            if event.type==pygame.MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                print(pos)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    b=Board() #reset
                    menu=True
                    print(menu)
                    continue

    pygame.display.flip()

    clock.tick(60)
