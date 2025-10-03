import threading
import time
from ntcore import BooleanArrayPublisher, BooleanArraySubscriber, NetworkTableInstance
import ntcore


class guiNTManager:
    def __init__(self, teamNumber:int = 1799):
        self.teamNumber=teamNumber
        self.table:NetworkTableInstance=None # type: ignore

        self.publisher:ntcore.NetworkTableInstance=None # type: ignore

        self.teamNumber=teamNumber


        self.loop = threading.Thread(target=self.connectionTester, daemon=True)
        self.loop.start()

    def setUpTables(self):
        

        

        self.l1Publisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/CoralL1").publish()
        self.l2Publisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/CoralL2").publish()
        self.l3Publisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/CoralL3").publish()
        self.l4Publisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/CoralL4").publish()

        self.l1Getter:BooleanArraySubscriber = self.publisher.getBooleanArrayTopic("CoralPositions/ReefL1").subscribe([])
        self.l2Getter:BooleanArraySubscriber = self.publisher.getBooleanArrayTopic("CoralPositions/ReefL1").subscribe([])
        self.l3Getter:BooleanArraySubscriber = self.publisher.getBooleanArrayTopic("CoralPositions/ReefL1").subscribe([])
        self.l4Getter:BooleanArraySubscriber = self.publisher.getBooleanArrayTopic("CoralPositions/ReefL1").subscribe([])



        self.leftIntakePublisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/leftIntake").publish()
        self.rightIntakePublisher:BooleanArrayPublisher = self.publisher.getBooleanArrayTopic("GUI/rightIntake").publish()

    def connect(self, port:str=None, teamNumber:int=None, name="lidar", startAsServer=False, saveConnectionIfSuccessful=True)->bool: # type: ignore
        connecter:ntcore.NetworkTableInstance = ntcore.NetworkTableInstance.getDefault()
        if port == teamNumber: # type: ignore
            raise ValueError("Must give a team number or a port when trying to connect to network tables. values given were port:", port,". TeamNumber:", teamNumber)

        if teamNumber:
            connecter.setServerTeam(teamNumber)

        else:
            connecter.setServer(port)
        
        
        if startAsServer:
            pass#connecter.startServer()
        else:
            connecter.startClient4(name)


        if connecter.isConnected() and saveConnectionIfSuccessful:
            self.publisher=connecter
            self.setUpTables()


        return connecter.isConnected()
    

    def connectionTester(self):
        while True:
            if not self.isConnected():
                if self.teamNumber!=0:        
                    if self.connect(teamNumber=self.teamNumber) or self.connect(port="127.0.0.1"):
                        print("Connected to", self.teamNumber)
                else:
                    if self.connect(port="127.0.0.1"):
                        print("Connected to sim")

            time.sleep(4)
                
    def isConnected(self)->bool:
        return self.publisher!=None and self.publisher.isConnected()

    def publishReef(self, reef:list[list[bool]]):
        self.l1Publisher.set(reef[0]) # type: ignore
        self.l2Publisher.set(reef[1]) # type: ignore
        self.l3Publisher.set(reef[2]) # type: ignore
        self.l4Publisher.set(reef[3]) # type: ignore

    def getReef(self)->list[list[bool]]:
        return [
            self.l1Getter.get(), 
            self.l2Getter.get(),
            self.l3Getter.get(),
            self.l4Getter.get(),
        ] # type: ignore
    
    def publishIntake(self, leftIntake:list[bool], rightIntake:list[bool]):
        self.leftIntakePublisher.set(leftIntake) # type: ignore
        self.rightIntakePublisher.set(rightIntake) # type: ignore