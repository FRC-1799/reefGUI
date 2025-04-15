import pygame
import pygame_gui
from GUI import GUI


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

gui = GUI(None, window_surface)

isRunning=True
while isRunning:
    
    if pygame.event.peek(pygame.QUIT):
        print("quitDetected")
        #raise KeyError()
        isRunning = False
    #print("update")
    gui.periodic()