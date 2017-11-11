from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Game, Solution, Turn, Room, NoteCard, Log, Character
from hashutils import checkPwHash

defaultLoginHeader = """

""" #TODO consider entering a basic form here that will redirect to hte login route with the appropriate post method to trigger a login function, rhather than force the user to go straight to a login page to login
 
userLoggedInHeader = """
Signed in as {0} LOGOUT
""" #TODO enter a proper href for the logout

@app.route("/")
def homepage():
    #TODO enter code that looks for cookies to see if the user is logged in, turn into IF statement returning base.html with different loginHeaders
    return render_template('base.html')

@app.route("/login")
def login():
    if request.method == 'GET':
        return render_template('login.html')            #Allows for just the basic login screen
    else:
        username = request.form['username']             #Gathers posted usernamne
        password = request.form['password']             #Gathers posted password
        users = User.query.filter_by(username=username) #compares username against usernames in database
        if users.count() == 1:                          #If there is a match (should only be one, usernames are unique)
            user = users.first()                        #Pull the first (and only) resulting object
            if checkPwHash(password, user.pwHash):      #If the password entered hashes properly and produces the hashed database password
                session['user'] = user.username         #sets the sessions user to the username of the user object
                return redirect("/")                    #brings us back to the homepage
            else:
                return render_template("/login", passwordError="Bad Password") #returns the appropriate bad password error
        else:
            return render_template("/login", usernameError="Bad Username") #returns bad username error

@app.route("/mygames")
def mygames():
    pass

    #TODO enter code that queries the databse for a list of all games belonging to the player attributed to teh signed in user. 
    #TODO find a way to format them into a jiinja template
    #TODO return in the form of a table, show basic information, player username unordered list, game status, current player turn, etc. 
    #TODO if game is awaiting players, and the only player is the user that started the game, and that user is signed in, allow a delete option
    #TODO limit the page to 25 games, add a paramter on the URL to accommodate for more results

@app.route("/gamenumber")
def gamenumber():

    pass
    #TODO enter code that pulls all relevant data on the game passed in the URL
    #TODO format it into blocks to send to a jinja template


@app.route("/gameslist")
def gameslist():
    pass
    #TODO mimic myGames
    #TODO remove user restraint

@app.route("/rules")
def rules():
    pass
    #TODO basic webpage that describes the rules of play and how the website works


if __name__ == "__main__":
    app.run()
