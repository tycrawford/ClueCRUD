from app import db
#from hashutils import make_pw_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pw_hash = db.Column(db.String(120))
    #games = db.relationship('Games', backref='' maybe connect with character, which has a game id column instead of games

    gamesPlayed = db.Column(db.Integer)
    score = db.Column(db.Integer)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarlet = db.Column(db.Integer,)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameID = db.Column()
    userID = db.Column()


