from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cluecrud:cluecrud@localhost:3306/cluecrud'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'whodunnit'
db = SQLAlchemy(app)
