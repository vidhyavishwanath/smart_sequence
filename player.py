

class Player:

    def __init__(self,number, imagesList):
        self.name = None
        self.cards = []
        self.played = []
        self.number = number
        self.playerImages = imagesList
    
    def playCard(self, card):
        self.cards.remove(card)
        self.played.append(card)
    
    def getImages(self):
        return self.playerImages

