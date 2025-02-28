##Por temas de tiempo he decidio tomarme bastantes licencias con el modelo de datos
##No he podido validar formularios con wtf ni hacer el jwt

from functools import wraps
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import getenv
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
import werkzeug
# from flask_JWT 

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

def admin_required(f):
    print('llega')
    @login_required
    @wraps(f)
    def isAdmin(*args, **kwargs):
        print('admin?: '+current_user.email)
        if current_user.email != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return isAdmin

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request! 😭', 404

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
            # if logged_user.password:
                if logged_user.email == 'admin':
                    return redirect(url_for('admin'))
                else: 
                    login_user(logged_user)
                    return redirect(url_for('perfil'))
            # else: return 'contraseña incorrecta'
       else: return 'Datos incorrectos'
    
    return render_template('/login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        
        cur = mysql.connection.cursor()
        cur.execute('insert into user (id, email, password, username) values(null, %s,%s,%s)',(email,password,username))
        mysql.connection.commit()

        user = User(0, email, password)
        logged_user = ModelUser.login(mysql, user)
        print(logged_user)
        if logged_user:
                if logged_user.email == 'admin':
                    return redirect(url_for('admin'))
                else: 
                    login_user(logged_user)
                    return redirect(url_for('perfil'))
            # else: return 'contraseña incorrecta'
        else: return 'Datos incorrectos'

        
    return render_template('/register.html')


@app.route('/perfil')
@login_required
def perfil():
    return render_template('/perfil.html')

@app.route('/tienda', methods=['GET'])
@login_required
def tienda():
    cur = mysql.connection.cursor()
    cur.execute('select * from productos')
    productos = cur.fetchall()
    print(productos)
    return render_template('/tienda.html', productos = productos)

@app.route('/comprar/<string:id>')
def comprar(id):
    cur = mysql.connection.cursor()
    cur.execute('update productos set comprado=true where id=%s',(id,))
    mysql.connection.commit()
    return 'producto comprado'
    #faltaria añadir a la tabla de productos un user_id para saber que usuario lo ha comprado
    #y desde perfil hacer una consulta where user_id = current_user.get_id() para sacarlos

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#El decorador de admin da error de prohibido acceso
@app.route('/admin')
# @admin_required
def admin():
    return render_template('/admin.html')

@app.route('/add_product', methods=['GET','POST'])
# @admin_required
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (id, comprado, nombre) values(null, false, %s)',(nombre,))
        mysql.connection.commit()
        return 'producto añadido'
    else:
       return render_template('/add_product.html')

if __name__ == '__main__': 
    app.register_error_handler(404, handle_bad_request)
    app.run(debug=True, host='0.0.0.0')