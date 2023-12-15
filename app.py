from flask import Flask, render_template, request, session, redirect, url_for #Importacion de módulo
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__) #Sirve para verificar si estamos trabajando el archivo incial del proyecto
app.secret_key = 'my_secret_key'

DATABASE = "users.db"

with sqlite3.connect(DATABASE) as connection:
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')




@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None  # Definir la variable con un valor predeterminado

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['username'] = username
                return redirect(url_for('principal'))
            else:
                error_message = 'Acceso denegado. Verifica tus credenciales.'

    return render_template('login.html', error_message=error_message)


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Utiliza el método de hash predeterminado de werkzeug
    hashed_password = generate_password_hash(password)

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()

    return redirect(url_for('login'))

@app.route('/login')
def home():
    if 'username' in session:
        return '¡Hola, {}! Has iniciado sesión.'.format(session['username'])
    return redirect(url_for('principal'))

@app.route('/pag')
def principal():
    return render_template('pag.html')

@app.route('/Jefe Maestro')
def Jefe_Maestro():
    return render_template('jefe.html')

@app.route('/Cortana')
def Cortana():
    return render_template('Cortana.html')

@app.route('/Johnson')
def Johnson():
    return render_template('johnson.html')

@app.route('/Inquisidor')
def Inquisidor():
    return render_template('Inquisidor.html')

if __name__=='__main__': 
    app.run(debug=True,port=1234)  #Levantamiento de app en la web  # debug=true = El servidor se reiniciará cuando uno de los archivos propios de la app tenga un cambio





