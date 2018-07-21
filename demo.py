def __init__(self, _simulator, _frequency=1):
    SecretionBasePy.__init__(self, _simulator, _frequency)


def start(self):
    self.field = CompuCell.getConcentrationField \
        (self.simulator, "FGF")

    secrConst = 10
    for x, y, z in self.everyPixel(1, 1, 1):
        cell = self.cellField[x, y, z]
        if cell and cell.type == 1:
            self.field[x, y, z] = -secrConst
        else:
            self.field[x, y, z] = 0.0


def step(self, mcs):
    secrConst = mcs
    for x, y, z in self.everyPixel(1, 1, 1):
        cell = self.cellField[x, y, z]
        if cell and cell.type == 1:
            self.field[x, y, z] = -secrConst
        else:
            self.field[x, y, z] = 0.0
