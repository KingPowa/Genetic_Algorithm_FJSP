# An Operation is an tuple (machine, optime), which is an assignable task
class Operation:
    def __init__(self, id_machine, processing_time):
        self.id_machine = id_machine
        self.processing_time = processing_time
        self.time = 0

    def __str__(self):
        return "ID_Machine: " + str(self.id_machine) + "| Processing_Time: " + str(self.processing_time) + "\n"

    @property
    def finished(self):
        if self.processing_time <= self.time:
            return True
        return False

