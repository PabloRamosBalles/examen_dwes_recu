from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import getenv
from flask_login import LoginManager, current_user

from models.entities.User import User
from models.ModelUser import ModelUser

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')
app.secret_key = getenv('SECRET_KEY')

mysql = MySQL(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(mysql, user_id)


@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       user = User(0, email, password)
       logged_user = ModelUser.login(mysql, user)
       print(logged_user)
       if logged_user:
           print(logged_user.email)
           return redirect(url_for('perfil'))
    
    return render_template('/login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        
        cur = mysql.connection.cursor()
        cur.execute('insert into user (email, password, username) values(%s,%s,%s)',(email,password,username))
        mysql.connection.commit()
        
    return render_template('/register.html')


@app.route('/perfil')
def perfil():
    return render_template('/perfil.html')

@app.route('/tienda', methods=['GET'])
def tienda():
    cur = mysql.connection.cursor()
    cur.execute('select * from productos')
    productos = cur.fetchall()
    print(productos)
    return render_template('/tienda.html', productos = productos)

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')