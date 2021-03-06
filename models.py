from app import db
from hashutils import makePwHash
import random
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwHash = db.Column(db.String(120))
    #games = db.relationship('Games', backref='' #maybe connect with character, which has a game id column instead of games
    gamesPlayed = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=1000)

    def __init__(self, username, password):
        self.username = username
        self.pwHash = makePwHash(password)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarlet = db.Column(db.Integer, default=0)
    mustard = db.Column(db.Integer, default=0)
    white = db.Column(db.Integer, default=0)
    green = db.Column(db.Integer, default=0)
    peacock = db.Column(db.Integer, default=0)
    plum = db.Column(db.Integer, default=0)
    board = db.Column(db.Integer, default=0)
    solution = db.Column(db.Integer, default=0)
    currentPlayerTurn = db.Column(db.Integer, default=0)
    activePlayerList = db.Column(db.String(30), default="")
    currentTurnNumber = db.Column(db.Integer, default=0)
    log = db.Column(db.Integer, default=0)
    cards = db.Column(db.Integer, default=0)
    numPlayers = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    charList = db.Column(db.String(300), default="")
    gameCards = ['Misss. Scarlet', 'Mrs. White', 'Col. Mustard', 'Mr. Green', 'Mrs. Peacock', 'Professor Plum', 'Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Ballroom', 'Billiard Room', 'Conservatory', 'Diningroom', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study']

    def __init__(self, playerID, playerChar, numPlayers):
        if playerChar == "Scarlet":
            self.scarlet = playerID
        elif playerChar == "White":
            self.white = playerID
        elif playerChar == "Mustard":
            self.mustard = playerID
        elif playerChar == "Green":
            self.green = playerID
        elif playerChar == "Peacock":
            self.peacock = playerID
        elif playerChar == "Plum":
            self.plum = playerID
        self.numPlayers = numPlayers
        
        

    def addChar(self,playerID, playerChar, gameID): #NOte to self, just deleted the db parameter because I think its redundant, it is in the global scope as defined above
        characterName = ""
        if playerChar == "Scarlet" or playerChar == "scarlet" or playerChar == "Miss Scarlet":
            self.scarlet = playerID
            characterName = "Miss Scarlet"
        elif playerChar == "White" or playerChar == "white" or playerChar == "Mrs. White":
            self.white = playerID
            characterName = "Mrs. White"
        elif playerChar == "Mustard" or playerChar == "mustard" or playerChar == "Col. Mustard":
            self.mustard = playerID
            characterName = "Col. Mustard"
        elif playerChar == "Green" or playerChar == "green" or playerChar == "Mr. Green":
            self.green = playerID
            characterName = "Mr. Green"
        elif playerChar == "Peacock" or playerChar == "peacock" or playerChar == "Mrs. Peacock":
            self.peacock = playerID
            characterName = "Mrs. Peacock"
        elif playerChar == "Plum" or playerChar == "plum" or playerChar == "Professor Plum":
            self.plum = playerID
            characterName = "Professor Plum"
        print
        newCharacter = Character(gameID, playerID, characterName)
        currentPlayers = self.activePlayerList
        currentPlayers = currentPlayers + str(playerID) + ","
        self.activePlayerList = currentPlayers
        db.session.add(newCharacter)
        db.session.commit()

    def startGame(self):
        self.status = 1
        db.session.commit()
        suspects = list(range(0, 6))
        weapons = list(range(6, 12))
        rooms = list(range(12, 21))
        suspect = random.randrange(0, 6)
        weapon = random.randrange(6, 12)
        room = random.randrange(12, 21)
        solution = Solution(self.id, suspect, weapon, room)
        db.session.add(solution)
        db.session.commit()
        suspects.remove(suspect)
        weapons.remove(weapon)
        rooms.remove(room)
        remainingCards = []
        for suspect in suspects:
            remainingCards.append(suspect)
        for weapon in weapons:
            remainingCards.append(weapon)
        for room in rooms:
            remainingCards.append(room)
        handOne = []
        handTwo = []
        handThree = []
        listOfHands = [handOne, handTwo, handThree]
        if self.numPlayers > 3:
            handFour = []
            listOfHands.append(handFour)
        if self.numPlayers > 4:
            handFive = []
            listOfHands.append(handFive)
        if self.numPlayers > 5:
            handSix = []
            listOfHands.append(handSix)
        playerDealt = 0
        idList = [Character.id for character in Character.query.filter_by(gameID=self.id)]
        charListStr = ""
        for char in idList:
            charListStr = charListStr + str(char) + ','

        self.charList = charListStr
        #TODO Check above line for functionality
        #TODO Fix below for Loops to get hands dealt to character objects
        # for card in remainingCards:
        #     dealingCard = random.randrange(len(remainingCards))
        #     listOfHands[playerDealt].append(dealingCard)
        #     remainingCards.remove(dealingCard)
        #     playerDealt = playerDealt + 1 % self.numPlayers
        
        # handDealt = 0

        # for id in idList:
        #     currentChar = Character.query.filter_by(id=id).first()
        #     currentHand = listOfHands[handDealt]
        #     handString = ""
        #     for card in currentHand:
        #         handString = handString + str(card) + ","
        #     currentChar.hand = handString
            


        # for card in range(len(remainingCards)):

        #     pulledCard = random.randrange(len(remainingCards))
        #     remainingCards.


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer, default=0)
    userID = db.Column(db.Integer, default=0)
    character = db.Column(db.String(20), default="")
    hand = db.Column(db.String(50), default="")
    position = db.Column(db.String(12), default="")
    pter = db.Column(db.Integer, default=0)
    room = db.Column(db.Integer, default=0)
    notecard = db.Column(db.Integer, default=0)

    def __init__(self, gameID, userID, character):
        self.gameID = gameID
        self.userID = userID
        self.character = character

    
class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer)
    suspect = db.Column(db.Integer)
    weapon = db.Column(db.Integer)
    room = db.Column(db.Integer)

    def __init__(self, gameID, suspect, weapon, room):
        self.gameID = gameID
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        
class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer)
    turnNumber = db.Column(db.Integer)
    character = db.Column(db.Integer)
    dieRoll = db.Column(db.Integer)
    diceRolled = db.Column(db.Boolean)
    moveMade = db.Column(db.Boolean)
    pter = db.Column(db.Integer)
    room = db.Column(db.Integer)
    suggestionMade = db.Column(db.Boolean)
    turnOver = db.Column(db.Boolean)
    suggestion = db.Column(db.String(15))
    
    def __init__(self, gameID, turnNumber, pter, room, character):
        self.gameID = gameID
        self.turnNumber = turnNumber
        self.pter = pter
        self.character = character
        self.room = room
        self.dieRoll = 0
        self.suggestionMade = False
        self.turnOVer = False
        self.moveMade = False
        self.diceRolled = False

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer)
    name = db.Column(db.String(20))
    spaces = db.Column(db.String(200))
    characters = db.Column(db.String(30))
    spRoom = db.Column(db.Integer)
    doorSpaces = db.Column(db.String(30))

    def __init__(self, gameID, name, spaces, spRoom, doorSpaces):
        self.gameID = gameID
        self.name = name
        self.spaces = spaces
        self.spRoom = spRoom
        self.doorSpaces = doorSpaces
        
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer)
    publicString = db.Column(db.String(200))
    privateString = db.Column(db.String(200))
    privUser = db.Column(db.Integer)
    timeStamp = db.Column(db.String(30))
    
    def __init__(self, gameID, publicString, privateString, privUser, timeStamp):
        self.gameID = gameID
        self.publicString = publicString
        self.privateString = privateString
        self.privUser = privUser
        self.timeStamp = timeStamp
    
class NoteCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suspect = db.Column(db.String(200))
    weapon = db.Column(db.String(200))
    room = db.Column(db.String(200))
    
    def __init__(self, suspect, weapon, room):
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        