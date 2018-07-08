def start(self):
    for cell in self.cellList:
        if cell.type == 2:
            cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ATTR")
            cd.setLambda(20.0)
            cd.setSaturationCoef(200.0)

            # cd.initializeChemotactTowardsVectorTypes("Bacterium,Medium")
            cd.assignChemotactTowardsVectorTypes([0, 1])

            break
