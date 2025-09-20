from pygame import Surface
import pygame
import pygame_gui
from pygame_gui.elements.ui_button import UIButton

from guiNTManager import guiNTManager


class GUI:

    
    buttonWidth=30
    buttonHeight=50
    buttonPadding=5
    canvasRightSide=130
    canvasTopSide=200
    downOffset = 20
    downOffsetIDS={2,3,8,9}
    centerOffset = 50



    def __init__(self, teamNumber:int = 1799, drawSurface:Surface = pygame.display.set_mode((800, 600))):
        self.publisher:guiNTManager = guiNTManager(teamNumber)

        self.clock = pygame.time.Clock()

        self.drawSurface=drawSurface

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#666666'))


        

        self.buttons:list[list[pygame_gui.elements.UIButton]]=[]
        self.manager = pygame_gui.UIManager((800, 600), "mainTheme.json")

        for pole in range(12):
            self.buttons.append([])
            for level in range(4):
                if pole in GUI.downOffsetIDS:
                    downBonus=GUI.downOffset
                else:
                    downBonus = 0

                if pole>5:
                    sideBonus=GUI.centerOffset
                else:
                    sideBonus=0


                self.buttons[pole].append(
                    pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                        (((pole+1)*(GUI.buttonWidth+GUI.buttonPadding)+GUI.canvasRightSide+sideBonus, (level+1)*(GUI.buttonHeight+GUI.buttonPadding)+GUI.canvasTopSide+downBonus)), 
                        (GUI.buttonWidth, GUI.buttonHeight)),
                    text='',
                    manager=self.manager))
                



        
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 275), (0, 0)),
                                            text='Say Hello',
                                            manager=self.manager)


    def periodic(self):
        time_delta = self.clock.tick(60)/1000.0
        
        for event in pygame.event.get(pump=False):


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                element:UIButton = event.ui_element
                if element.is_selected:
                    element.unselect()
                    
                else:
                    element.select()
                    #element.bind()

            self.manager.process_events(event)

        self.manager.update(time_delta)

        self.drawSurface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.drawSurface)

        

        if self.publisher.isConnected():
            toPublish:list[list[bool]] =[[],[],[],[]]

            for pole in self.buttons:
                level=0
                for button in pole:
                    toPublish[level].append(button.is_selected)
                    level+=1

            self.publisher.publishReef(toPublish)

        pygame.display.update()
        pygame.event.pump()
        

    
