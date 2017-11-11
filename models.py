from app import db
from hashutils import makePwHash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwHash = db.Column(db.String(120))
    #games = db.relationship('Games', backref='' #maybe connect with character, which has a game id column instead of games
    gamesPlayed = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.pwHash = makePwHash(password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarlet = db.Column(db.Integer)

    def __init__(self, playerID, playerChar):
        if playerChar == "Scarlet":
            self.Scarlet = playerID
        elif playerChar == "White":
            self.White = playerID
        elif playerChar == "Mustard":
            self.Mustard = playerID
        elif playerChar == "Green":
            self.Green = playerID
        elif playerChar == "Peacock":
            self.Peacock = playerID
        elif playerChar == "Plum":
            self.Plum = playerID


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer, db.ForeignKey('Game.id'))
    userID = db.Column(db.Integer, db.ForeignKey('User.id'))
    character = db.Column(db.String(20))
    hand = db.Column(db.String(50))
    position = db.Column(db.String(12))
    pter = db.Column(db.String(20))
    room = db.Column(db.String(20))
    notecard = db.Column(db.Integer, db.ForeignKey('notecard.id'))

    def __init__(self, gameID, userID, character):
        self.gameID = gameID
        self.userID = userID
        self.character = character

    
class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer, db.ForeignKey('Game.id'))
    suspect = db.Column(db.Integer)
    weapon = db.Column(db.Integer)
    room = db.Column(db.Integer)

    def __init__(self, suspect, weapon, room):
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        
class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column(db.Integer, db.ForeignKey('Game.id'))
    turnNumber = db.Column(db.Integer)
    character = db.Column(db.String(20))
    dieRoll = db.Column(db.Integer)
    diceRolled = db.Column(db.Boolean)
    moveMade = db.Column(db.Boolean)
    pter = db.Column(db.String(20))
    room = db.Column(db.String(20))
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
    privUser = db.Column(db.String(20))
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
        