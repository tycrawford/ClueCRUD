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
	userintID = int(userID)
	yourGames = Character.query.filter_by(userID=userID).all()
	idList = [character.gameID for character in Character.query.filter_by(userID=userID)]
	characterList = [character.character for character in Character.query.filter_by(userID=userID)]
	print("*********************Printing userID from currentUser.id********************************")
	print(userID)
	print(type(userID))
	statusList = []#[game.status for game in Game.query.filter(or_(Game.scarlet==userID, Game.mustard==userID, Game.white==userID, Game.green==userID, Game.peacock=userID, Game.plum=userID))]
	#TODO build a list of statuses based on game information. iterate through each game using each id
	for gameID in range(len(idList)):
		currentGameStatus = db.session.query(Game.status).filter_by(id=idList[gameID]).first()
		statusList.append(currentGameStatus)

	
	print("*******************Printing status, ID, character list*************************")
	print(statusList)
	print(idList)
	print(characterList)
	#TODO Build three separate tables, consisting of games awaiting players, games in progress, and games completed
	tableHeader = "<table>"
	tableFooter = "</table>"
	tableLabel = """
	<tr>
		<td>
			Game Number
		</td>
		<td>
			Character
		</td>
	</tr>
	"""
	tableRowsWaiting = ""
	tableRowsInProgress = ""
	tableRowsCompleted = ""
	for i in range(len(idList)):
		print(i)
		print(statusList[i])
		newRow = """
		<tr>
			<td>
				<a href="/game?gameid={0}"> {0} </a>
			</td>
			<td>
				{1}
			</td>
		"""
		strStatus = str(statusList[i])
		intStatus = strStatus.strip('(,) ')
		intStatus = int(intStatus)

		if intStatus == 0: #checks for games awaiting players
			tableRowsWaiting = tableRowsWaiting + newRow.format(idList[i], characterList[i])
		elif intStatus == 1: #checks for games in progress
			tableRowsInProgress = tableRowsInProgress + newRow.format(idList[i], characterList[i])
		elif intStatus == 2: #checks for games in 
			tableRowsCompleted = tableRowsCompleted + newRow.format(idList[i], characterList[i])
	print(statusList)
	#username = session['username']
	awaitingPlayers = tableHeader + tableLabel + tableRowsWaiting + tableFooter
	gamesInProgress = tableHeader + tableLabel + tableRowsInProgress + tableFooter
	completedGames = tableHeader + tableLabel + tableRowsCompleted + tableFooter
	
	
	
    #TODO enter code that looks for cookies to see if the user is logged in, turn into IF statement returning base.html with different loginHeaders
	return render_template('homepage.html', awaitingPlayers=awaitingPlayers , gamesInProgress=gamesInProgress , completedGames=completedGames )

@app.route("/game", methods=['GET', 'POST'])
def game():
	turnNumber = ""
	gameID = request.args.get('gameid')
	gameinfo = Game.query.filter_by(id=gameID).first()
	gameInfoStatus = gameinfo.status #PAY SPECIAL ATTENTION TO THIS SIMPLICITY
	username = session['username']
	user = User.query.filter_by(username=username).first()
	userID = user.id

	if gameInfoStatus == 0:
		status = "Awaiting Players"
	elif gameInfoStatus == 1:
		status = "Game In Progress"
		turnNumber = gameinfo.currentTurnNumber
	elif gameInfoStatus == 2:
		status = "Game completed"
	playerInGame = False
	activePlayerList = gameinfo.activePlayerList
	listofplayers = activePlayerList.split(',')
	for player in listofplayers:
		if player == str(userID):
			playerInGame = True
		

	#TODO Replace all this code with two for loops.
	#The first for loop goes through a list of attributes, gameinfo.attribute, and checks if == 0
	#Based on if, append list of jinja passthroughs accordingly

	if gameinfo.scarlet == 0 and playerInGame == False and gameInfoStatus == 0:
		scarlet = "<a href='/joingame?id={0}&char=scarlet'> Join This Game </a>".format(gameID)
	elif gameinfo.scarlet == 0 and playerInGame == True:
		scarlet = ""
	else:
		scarlet = (User.query.filter_by(id=gameinfo.scarlet).first()).username

	if gameinfo.white == 0 and playerInGame == False and gameInfoStatus == 0:
		white = "<a href='/joingame?id={0}&char=white'> Join This Game </a>".format(gameID)
	elif gameinfo.white == 0 and playerInGame == True:
		white = ""
	else:
		white = (User.query.filter_by(id=gameinfo.white).first()).username	

	if gameinfo.mustard == 0 and playerInGame == False and gameInfoStatus == 0:
		mustard = "<a href='/joingame?id={0}&char=mustard'> Join This Game </a>".format(gameID)
	elif gameinfo.mustard == 0 and playerInGame == True:
		mustard = ""
	else:
		mustard = (User.query.filter_by(id=gameinfo.mustard).first()).username
	
	if gameinfo.green == 0 and playerInGame == False and gameInfoStatus == 0:
		green = "<a href='/joingame?id={0}&char=green'> Join This Game </a>".format(gameID)
	elif gameinfo.green == 0 and playerInGame == True:
		green = ""
	else:
		green = (User.query.filter_by(id=gameinfo.green).first()).username

	if gameinfo.plum == 0 and playerInGame == False and gameInfoStatus == 0:
		plum = "<a href='/joingame?id={0}&char=plum'> Join This Game </a>".format(gameID)
	elif gameinfo.plum == 0 and playerInGame == True:
		plum = ""
	else:
		plum = (User.query.filter_by(id=gameinfo.plum).first()).username

	if gameinfo.peacock == 0 and playerInGame == False and gameInfoStatus == 0:
		peacock = "<a href='/joingame?id={0}&char=peacock'> Join This Game </a>".format(gameID)
	elif gameinfo.peacock == 0 and playerInGame == True:
		peacock = ""
	else:
		peacock = (User.query.filter_by(id=gameinfo.peacock).first()).username		
	return render_template('singleGame.html', gameID=gameID, status=status, turnNumber=turnNumber, scarlet=scarlet, white=white, mustard=mustard, green=green, peacock=peacock, plum=plum) #token comments
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
                session['username'] = user.username         #sets the sessions user to the username of the user object
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
		newGame.addChar(currentUserID, char,gameID)
		
		return redirect("/")
	else:
		return render_template("newgame.html")


@app.route("/joingame", methods=['GET', 'POST'])
def joingame():
	username = session['username']
	user = User.query.filter_by(username=username).first()
	userID = user.id
	if request.method == 'POST': #This should only happen when we have to choose a character, rather than following a character specific join link
		char = request.form['char']
		gameID = request.form['hiddengameID']
		thisGame = Game.query.filter_by(id=gameID).first()
		thisGame.addChar(userID, char, gameID)
		activePlayerList = thisGame.activePlayerList
		listofplayers = activePlayerList.split(',')
		if len(listofplayers) == (thisGame.numPlayers + 1):
			thisGame.startGame()
			print("game started")
			
		return redirect('/game?gameid={0}'.format(gameID))
	else:
		gameID = "<input type='hidden' name='hiddengameID' value='{0}'>".format(request.args.get('id'))
		char = request.args.get('char')
		gameinfo = Game.query.filter_by(id=request.args.get('id')).first()
		if char == "":
			optionsList = ""
			if gameinfo.scarlet == 0:
				optionsList = optionsList + "<option> Miss Scarlett </option>"
			if gameinfo.white == 0:
				optionsList = optionsList + "<option> Mrs. White </option>"
			if gameinfo.mustard == 0:
				optionsList = optionsList + "<option> Col. Mustard </option>"
			if gameinfo.green == 0:
				optionsList = optionsList + "<option> Mr. Green </option>"
			if gameinfo.peacock == 0:
				optionsList = optionsList + "<option> Mrs. Peacock </option>"
			if gameinfo.plum == 0:
				optionsList = optionsList + "<option> Professor Plum </option>"
								
			return render_template('joingame.html', gameID=gameID, optionsList=optionsList)
		elif char in ['scarlet', 'mustard', 'green', 'white', 'peacock', 'plum']:
			gameinfo.addChar(userID, char, gameinfo.id)
			activePlayerList = gameinfo.activePlayerList
			listofplayers = activePlayerList.split(',')
			if len(listofplayers) == (gameinfo.numPlayers + 1):
				gameinfo.startGame()
				print("game started")
				
			return redirect('/game?gameid={0}'.format(gameinfo.id))
		else:
			return redirect('/game?gameid={0}'.format(gameinfo.id))


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
