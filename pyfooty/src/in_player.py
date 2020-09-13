from pyfooty.src.baseclass import FBref

class Player(FBref):
    def __repr__(self):
        desc = "<player: {}, id: {}>".format(self.name, id(self))
        return desc

if __name__ == "__main__":
    puli = Player("Jorginho")
    standard = puli.get_table("Standard Stats")
