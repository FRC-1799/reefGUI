
from pygame import Surface
import pygame
import pygame_gui
from pygame_gui.elements.ui_button import UIButton

from guiNTManager import guiNTManager


class GUI:

    
    buttonWidth=30
    buttonHeight=40

    intakeDisplayWidth=40
    intakeDisplayHeight=40

    buttonPadding=5
    canvasRightSide=130
    canvasTopSide=70

    reefBottomHalfOffset=220

    downOffset = 20
    downOffsetIDS=[0,1,6,7]
    centerOffset = 50

    canvasWidth=800
    canvasHeight=600

    intakeHeight = 550

    selectAllHight = 500
    selectAllSide=20

    isConnectedSideLen=20
    isConnectedX = (canvasWidth-isConnectedSideLen)/2
    isConnectedY=30


    intakePoses = [50, 100, 150, 650, 700, 750]

    poleOrder = [10, 11, 0, 1, 2, 3, 9, 8, 7, 6, 5, 4]



    def __init__(self, teamNumber:int = 1799, drawSurface:Surface = pygame.display.set_mode((800, 600))):
        self.publisher:guiNTManager = guiNTManager(teamNumber)

        self.clock = pygame.time.Clock()

        self.drawSurface=drawSurface

        self.background = pygame.Surface((GUI.canvasWidth, GUI.canvasHeight))
        self.background.fill(pygame.Color('#666666'))

        self.intakeButtons:list[pygame_gui.elements.UIButton]=[]
        

        self.selectPoleButtons:list[pygame_gui.elements.UIButton]=[]

        self.buttons:list[list[pygame_gui.elements.UIButton]]=[]
        self.manager = pygame_gui.UIManager((GUI.canvasWidth, GUI.canvasHeight), "mainTheme.json")

        for pole in range(12):

            positionalIndex = GUI.poleOrder.index(pole)

            buttonX = (((positionalIndex)%6)-3) * (GUI.buttonWidth+GUI.buttonPadding) + GUI.canvasWidth/2


            self.buttons.append([])

            buttonY = (
                    GUI.canvasTopSide + 
                    (GUI.reefBottomHalfOffset if positionalIndex<6 else 0) 
                    + (5 if positionalIndex<6 else 0.5)*(GUI.buttonHeight+GUI.buttonPadding) 
                    +((GUI.downOffset if (GUI.downOffsetIDS.__contains__( pole)) else 0) * (1 if positionalIndex<5 else -1))
                )
            
            self.selectPoleButtons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                        (buttonX+(GUI.buttonWidth-GUI.selectAllSide)/2, buttonY), 
                        (GUI.selectAllSide, GUI.selectAllSide)),
                    text='',
                    manager=self.manager))
            
            for level in range(4):


                buttonY= (
                    GUI.canvasTopSide + 
                    (GUI.reefBottomHalfOffset if positionalIndex<6 else 0) 
                    + (level+1)*(GUI.buttonHeight+GUI.buttonPadding) 
                    +((GUI.downOffset if (GUI.downOffsetIDS.__contains__( pole)) else 0) * (1 if positionalIndex<5 else -1))
                )



                self.buttons[pole].append(
                    pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                        ((buttonX, buttonY)), 
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


        poleID=0
        for selectButton in self.selectPoleButtons:
            shouldUnselectButton=True
            for button in self.buttons[poleID]:
                if not button.is_selected:
                    shouldUnselectButton=False
                    break

         

            if selectButton.is_selected:
                for button in self.buttons[poleID]:
                    if shouldUnselectButton:
                        button.unselect()
                    else:
                        button.select()

            selectButton.unselect()
            poleID+=1



        if self.publisher.isConnected():




            toPublish:list[list[bool]] =[[],[],[],[]]

            poleID=0
            for pole in self.buttons:
                level=3
                for button in pole:
                    toPublish[level].append(not button.is_selected)
                    level-=1

                    if self.publisher.getReef()[level][poleID]:
                        button.disable()
                    elif not button.is_enabled:
                        button.enable

            self.publisher.publishReef(toPublish)




            leftIntake:list[bool] =[]
            rightIntake:list[bool]=[]

            for intake in range(0, 3):
                leftIntake.append(not self.intakeButtons[intake].is_selected)
                rightIntake.append(not self.intakeButtons[intake+3].is_selected)

            self.publisher.publishIntake(leftIntake, rightIntake)
        

        pygame.draw.rect(self.background, (0, 255,0) if self.publisher.isConnected() else (255, 0, 0), (GUI.isConnectedX, GUI.isConnectedY, GUI.isConnectedSideLen, GUI.isConnectedSideLen), 0) 


        pygame.display.update()
        pygame.event.pump()
        

    
