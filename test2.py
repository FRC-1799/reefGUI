import ntcore
import pygame
from gui import GUI


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
table:ntcore.NetworkTableInstance = ntcore.NetworkTableInstance.getDefault()
##table.setServerTeam(1799)
table.setServer("127.0.0.1")
gui = GUI(table, window_surface) 
isRunning=True
while isRunning:
    
    if pygame.event.peek(pygame.QUIT):
        print("quitDetected")
        #raise KeyError()
        isRunning = False
    #print("update")
    gui.periodic()