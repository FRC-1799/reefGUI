from ntcore import Publisher
from pygame import Surface
import pygame
import pygame_gui
from pygame_gui.elements.ui_button import UIButton

from guiNTManager import guiNTManager


class GUI:

    
    buttonWidth=30
    buttonHeight=50

    intakeDisplayWidth=40
    intakeDisplayHeight=40

    buttonPadding=5
    canvasRightSide=130
    canvasTopSide=200
    downOffset = 20
    downOffsetIDS={2,3,8,9}
    centerOffset = 50

    intakeHeight = 550
    intakePoses = [50, 100, 150, 650, 700, 750]



    def __init__(self, teamNumber:int = 1799, drawSurface:Surface = pygame.display.set_mode((800, 600))):
        self.publisher:guiNTManager = guiNTManager(teamNumber)

        self.clock = pygame.time.Clock()

        self.drawSurface=drawSurface

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#666666'))

        self.intakeButtons:list[pygame_gui.elements.UIButton]=[]
        

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
                



        
        for width in GUI.intakePoses:
            self.intakeButtons.append(
                    pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                        ((width, self.intakeHeight)), 
                        (GUI.intakeDisplayWidth, GUI.intakeDisplayHeight)),
                    text='',
                    manager=self.manager))


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
                level=3
                for button in pole:
                    toPublish[level].append(button.is_selected)
                    level-=1
            self.publisher.publishReef(toPublish)

            leftIntake:list[bool] =[]
            rightIntake:list[bool]=[]

            for intake in range(0, 3):
                leftIntake.append(self.intakeButtons[intake].is_selected)
                rightIntake.append(self.intakeButtons[intake+3].is_selected)

            self.publisher.publishIntake(leftIntake, rightIntake)
        

        pygame.draw.rect(self.background, (0, 255,0) if self.publisher.isConnected() else (255, 0, 0), (400, 100, 20, 20), 0) 


        pygame.display.update()
        pygame.event.pump()
        

    
