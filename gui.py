from ntcore import NetworkTableInstance
from pygame import Surface
import pygame
import pygame_gui
from pygame_gui.elements.ui_button import UIButton


class GUI:

    
    buttonWidth=30
    buttonHeight=50
    buttonPadding=5
    canvasRightSide=130
    canvasTopSide=200
    downOffset = 20
    downOffsetIDS={2,3,8,9}
    centerOffset = 50



    def __init__(self, table:NetworkTableInstance, drawSurface = pygame.display.set_mode((800, 600))):
        if table:
            self.table=table
            self.l1Publisher = table.getBooleanArrayTopic("CoralL1").publish()
            self.l2Publisher = table.getBooleanArrayTopic("CoralL2").publish()
            self.l3Publisher = table.getBooleanArrayTopic("CoralL3").publish()
            self.l4Publisher = table.getBooleanArrayTopic("CoralL4").publish()
            self.leftIntakePublisher = table.getBooleanArrayTopic("leftIntake").publish()
            self.rightIntakePublisher = table.getBooleanArrayTopic("rightIntake").publish()

        self.clock = pygame.time.Clock()

        self.drawSurface=drawSurface

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#666666'))

        self.buttons=[]
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
                    element.bind()

            self.manager.process_events(event)

        self.manager.update(time_delta)

        self.drawSurface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.drawSurface)

        pygame.display.update()
        pygame.event.pump()
        


