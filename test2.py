import ntcore
import pygame
from gui import GUI


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
table:ntcore.NetworkTableInstance = ntcore.NetworkTableInstance.getDefault()
##table.setServerTeam(1799)
table.setServer("127.0.0.1")
gui = GUI( drawSurface=window_surface) 
while True:
    
    if pygame.event.peek(pygame.QUIT):
        print("quitDetected")
        #raise KeyError()
        break
    #print("update")
    gui.periodic()