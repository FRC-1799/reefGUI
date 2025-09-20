import threading
import time
from ntcore import NetworkTableInstance
import ntcore


class guiNTManager:
    def __init__(self, teamNumber:int = 1799):
        self.isConnected=False
        self.teamNumber=teamNumber
        self.table:NetworkTableInstance=None # type: ignore

        self.publisher:ntcore.NetworkTableInstance=None # type: ignore

        self.teamNumber=teamNumber


        self.loop = threading.Thread(target=self.connectionTester, daemon=True)
        self.loop.start()

    def setUpTables(self):
        

        

        self.l1Publisher = table.getBooleanArrayTopic("GUI/CoralL1").publish()
        self.l2Publisher = table.getBooleanArrayTopic("GUI/CoralL2").publish()
        self.l3Publisher = table.getBooleanArrayTopic("GUI/CoralL3").publish()
        self.l4Publisher = table.getBooleanArrayTopic("GUI/CoralL4").publish()

        self.l1Getter = table.getBooleanArrayTopic("CoralL1").publish()
        self.l2Getter = table.getBooleanArrayTopic("CoralL2").publish()
        self.l3Getter = table.getBooleanArrayTopic("CoralL3").publish()
        self.l4Getter = table.getBooleanArrayTopic("CoralL4").publish()



        self.leftIntakePublisher = table.getBooleanArrayTopic("leftIntake").publish()
        self.rightIntakePublisher = table.getBooleanArrayTopic("rightIntake").publish()

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
            if self.teamNumber!=0:        
                if self.connect(teamNumber=self.teamNumber) or self.connect(port="127.0.0.1"):
                    break
            else:
                if self.connect(port="127.0.0.1"):
                    break

            time.sleep(4)
        print("Connected on port", self.publisher.getConnections()[0].remote_ip)
                


