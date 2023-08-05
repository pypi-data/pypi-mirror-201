import random

class date():
    def getName(self):
        name = str(random.choice(range(10, 999))) + '_' + str(random.choice(range(10, 999)))
        return name

    def getNameWhipptree(self):
        name = str(random.choice(range(10, 999)))  + str(random.choice(range(10, 999)))
        return name