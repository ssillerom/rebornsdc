
class wallet:

    def __init__(self, userType, name, amount):
        self.name = name
        self.token = "$BEC"
        self.TypeUser = userType
        self.amount = amount

    def addCash(self, amount):
        self.cash += amount

    def withdrawCash(self, amount):
        self.cash -= amount

class producer:

    def __init__(self, name, producerType, producedEnergy, address):
        self.name = name
        self.type = producerType
        self.energy = producedEnergy
        self.cash = 0
        self.address = address

    def addEnergy(self, amountEnergy):
        self.energy += amountEnergy

    def energySolded(self, amountEnergy):
        self.energy -= amountEnergy

    def addCash(self, amount):
        self.cash += amount

class buyer:

    def __init__(self, name, buyerType, address):
        self.name = name
        self.buyerType = buyerType
        self.address = address










