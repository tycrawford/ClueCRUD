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
	username = session['username']
	currentUser = User.query.filter_by(username=username).first()
	userID = currentUser.id
	yourGames = Character.query.filter_by(userID=userID).all()
	idList = [character.gameID for character in Character.query.filter_by(userID=userID)]
	characterList = [character.character for character in Character.query.filter_by(userID=userID)]
	tableHeader = "<table>"
	tableFooter = "</table>"
	tableRows = """
	<tr>
		<td>
			Game Number
		</td>
		<td>
			Character
		</td>
	</tr>
	"""
	for i in range(len(idList)):
		newRow = """
		<tr>
			<td>
				<a href="/game?id={0}"> {0} </a>
			</td>
			<td>
				{1}
			</td>
		"""
		tableRows = tableRows + newRow.format(idList[i], characterList[i])
	#username = session['username']
	listofgames = tableHeader + tableRows + tableFooter
	print(yourGames)
	
	
    #TODO enter code that looks for cookies to see if the user is logged in, turn into IF statement returning base.html with different loginHeaders
	return render_template('homepage.html', listofgames=listofgames)

@app.route("/game", methods=['GET', 'POST'])
def game():
	pass
	#TODO this is where you will set up an individual game window

@app.route("/login", methods=['GET', 'POST'])
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
                return render_template("login.html", passwordError="Bad Password") #returns the appropriate bad password error
        else:
            return render_template("login.html", usernameError="Bad Username") #returns bad username error

@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
	if request.method == 'POST':
		username = session['username']
		currentUser = User.query.filter_by(username=username).first()
		currentUserID = currentUser.id
		char = request.form['char']
		#TODO add information to enable selection of which other players
		#TODO 
		numPlayers = request.form['numPlayers']
		newGame = Game(currentUserID, char, numPlayers)
		db.session.add(newGame)
		db.session.commit()
		#TODO create a board
		game = Game.query.order_by(Game.id.desc()).first()
		gameID = game.id
		newGame.addChar(currentUserID, char,gameID,db)
		
		return render_template("homepage.html")
	else:
		return render_template("newgame.html")


@app.route("/joingame", methods=['GET', 'POST'])
def joingame():
	pass
	#TODO allow a user to see a list of games to join
	#TODO allow a user to select which character they would like to play
	#TODO on this page, modify the gameID in question to assign the users ID to the character of their choosing
	#TODO instantiate a character based on information given
	#TODO build all other resources relating to the character


@app.route("/signup", methods=['GET', 'POST'])
def usersignup():
	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		confirm = request.form['confirm']
		usernameError = ""
		passwordError = ""
		users = User.query.filter_by(username=username)
		if users.count() == 1:
			usernameError = "Username already in use!"
		if len(username) < 3 or len(username) > 20:
			usernameError = "Username must be between 3 and 20 characters long"
		if len(password) < 3 or len(password) > 20:
			passwordError = "Password must be between 3 and 20 characters long"
		if password != confirm:
			passwordError = "Passwords do not match!"
		if passwordError == "" and usernameError == "":
			newUser = User(username, password)
			db.session.add(newUser)
			db.session.commit()
			session['username'] = username
			return render_template("login.html")
		else:
			return render_template("usersignup.html", usernameError=usernameError, passwordError=passwordError)
	else:
		return render_template("usersignup.html")


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
