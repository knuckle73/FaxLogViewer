from flask import Flask
from flask_mysqldb import MySQL
from FaxLogViewer.config import credentials

app = Flask(__name__)

# Config MySQL
app.secret_key = "b48fb44860e75665aa4ec29c703bae6d"
app.config['MYSQL_HOST'] = 'schc-db02'
app.config['MYSQL_USER'] = credentials.username()
app.config['MYSQL_PASSWORD'] = credentials.passwd()
app.config['MYSQL_DB'] = 'faxlogs_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# init MYSQL
mysql = MySQL(app)


# routes.py requires mysql instance, therefore routes import must be done after instance is created or import will fail
from FaxLogViewer import routes
