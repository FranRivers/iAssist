from flask import redirect, Flask, render_template, session, flash, url_for
from flask_sqlalchemy import *
from sqlalchemy import Column, Integer, ForeignKey, String, update

"""Hacemos las respectivas configuraciones para el framework de flask """
app = Flask(__name__)
"""Configuramos la ruta de la base de datos y una llave"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iassist.db'
app.config['SECRET_KEY'] = 'uippc4'
db = SQLAlchemy(app)

class event(db.Model):

    id = Column(Integer, primary_key=True)
    name_event = Column(String(40), nullable=False)
    date_event = Column(String(10))
    user_id =(Integer, ForeignKey('User.id'))

    def __init__(self, name_event, date_event):

        self.name_event = name_event
        self.date_event = date_event
"""Creamos la clase evento convirtiendola en un modelo de base de datos, aquí se registrara el nombre del evento
la fecha y tienen un foreignkey para relacionar las ambas tablas."""

class User(db.Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(40), nullable=False)
    phone = Column(String(8))
    event = Column(Integer, ForeignKey('event.id'))
    estado = Column(String(1))


    def __init__(self, name, email, phone, event, estado):

        self.name = name
        self.email = email
        self.phone = phone
        self.event = event
        self.estado = estado
"""Creamos la clase User convirtiendola en un modelo de base de datos, aqui se registrara todos los datos necesarios
para registrar un invitado al evento deseado."""

@app.route('/')
def inicio():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('inicio.html')
    return render_template('inicio.html')
"""Definimos la ruta de inicio donde tiene una condicion que solo se podra entrar si esta logueado con los usuarios
definidos en el codigo."""

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'Fran720' and request.form['username'] == 'Fran' or \
                                request.form['password'] == '260115' and request.form['username'] == 'freddy':
            session['logged_in'] = True
            """Cambia session a logge_in para poder identificar si se ha iniciado sesion"""
            return render_template('inicio.html')
        else:
            return
            flash('wrong password!')
    return render_template('login.html', error = error)
"""Aquí tenemos la estructura del login con dos usuarios para poder crear y editar eventos."""

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return inicio()
"""Esta funcion es para cerrar sesion en caso de que el usuario lo desee cambiando la condicion de (session)"""

@app.route('/adde', methods=['GET', 'POST'])
def adde():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            """Tiene una condicion donde obliga a llenar ciertos campos de la informacion del evento"""
            if not request.form['name_event'] or not request.form['date_event']:
                flash('por favor introduce los campos obligatorios.', 'error')
            else:
                """al recibir toda la informacion necesaria la registra en la tabla event en sus respectivos campos"""
                events = event(request.form['name_event'],
                               request.form['date_event'])
                db.session.add(events)
                db.session.commit()
                flash('Evento creado con exito!')
                return redirect(url_for('inicio'))
    return render_template('adde.html')
"""Esta ruta o funcion es para crear los eventos"""


@app.route('/add', methods=['GET', 'POST'])
def add():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            """Tiene una condicion donde obliga a llenar ciertos campos de la informacion del invitado"""
            if not request.form['name'] or not request.form['email'] or not request.form['phone'] or not request.form\
                    ['event'] or not request.form['estado']:
                flash('Por favor introduzca todos los campos', 'error')
            else:
                """al recibir toda la informacion necesaria la registra en la tabla user en sus respectivos campos"""
                users = User(request.form['name'],
                             request.form['email'],
                             request.form['phone'],
                             request.form['event'],
                             request.form['estado'])
                db.session.add(users)
                db.session.commit()
                flash('asistidor guardado con exito!')
                return redirect(url_for('inicio'))
    return render_template('add.html')
"""ruta para crear los usuarios, en los campos a llenar hay uno llamado eventos que es para colocar el id del evento
el cual el usuario va a asistir (se puede ver cual es el id de los eventos en la siguiente ruta)"""

@app.route('/view')
def view():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('view.html', events=event.query.all(), users=User.query.all())
"""Esta ruta refleja los eventos su id y los invitados."""

@app.route('/how')
def how():

    if not session.get('logged_in'):
        return render_template('loguin.html')
    else:
        return render_template('how.html')
""" Ruta donde explica como usar la plataforma ."""

@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        u = None
        r = None
        if request.method == "POST":
            id = request.form.get("id")
            """Creamos una variable llamada id para vincularla con el id del usuario el cual se ingreso el dato para 
            solo modificarlo a él."""
            if 'S' in request.form.values():
                u = update(User).where(User.id == id).values(estado='S')
            elif 'N' in request.form.values():
                u = update(User).where(User.id == id).values(estado='N')
            elif 'P' in request.form.values():
                u = update(User).where(User.id == id).values(estado='P')
            elif 'D' in request.form.values():
                r = User.query.filter_by(id=id).one()
            else:
                flash("error")
        if u is not None:
            db.session.execute(u)
            db.session.commit()
        elif r is not None:
            db.session.delete(r)
            db.session.commit()

    return render_template('edit.html', events=event.query.all(), users=User.query.all())
"""Esta ruta tiene una estructura para editar el estado de los invitados o eliminarlos."""
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

