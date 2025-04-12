from ntcore import NetworkTableInstance


class gui:

    




    def __init__(self, table:NetworkTableInstance):
        self.table=table
        self.l1Publisher = table.getBooleanArrayTopic("CoralL1").publish()
        self.l2Publisher = table.getBooleanArrayTopic("CoralL2").publish()
        self.l3Publisher = table.getBooleanArrayTopic("CoralL3").publish()
        self.l4Publisher = table.getBooleanArrayTopic("CoralL4").publish()
        self.leftIntake = table.getBooleanArrayTopic("leftIntake").publish()
        self.rightIntake = table.getBooleanArrayTopic("rightIntake").publish()

