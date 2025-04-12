import ntcore

from gui import gui



class button:

    class buttonStates:
        pressedMaual=1
        unpressedManual=2
        pressedAuto = 3
        default=0


    def __init__(self, x:float, y:float, id:int, publisher:"gui", startingState = buttonStates.default):
        self.x=x
        self.y=y
        self.id=id
        self.parent = gui
        self.publisher = self.parentTable.getBooleanTopic(name)
        self.state=startingState

    def periodic(self):
        