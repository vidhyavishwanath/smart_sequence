
class Card:

    def __init__(self, imageLink, answer, topic, id, powerups):
        self.image = imageLink
        self.answer = answer
        self.topic = topic
        self.played = False
        self.playedBy = None
        self.id = id
        self.powerups = powerups
    
    def getImage(self):
        return self.image
    
    def getAnswer(self):
        return self.answer
    
    def getTopic(self):
        return self.topic
    
    def __eq__(self, other):
        if self.topic == other.getTopic():
            return True
    
    def isPlayed(self):
        return self.played
    
    def setPlayed(self):
        self.played = True
    
    def setPlayedBy(self, num):
        self.playedBy = num
