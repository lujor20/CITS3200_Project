import shutil
class copyOutput:
    def __init__(self, output):
        self.output = output
        self.copy()

    def copy(self):
        # Copy output to staticInternalSave.csv
        shutil.copy(self.output, "staticInternalSave.csv")



        