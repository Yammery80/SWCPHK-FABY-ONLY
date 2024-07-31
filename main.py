import psycopg2
from flask import Flask, request, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
import db

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    conn= db.conectar()
    # Crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    #Ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM entradas_salidas''')
    #Recuperar información
    datos = cursor.fetchall()
    #Cerrar cursor y conexión a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('base.html', datos=datos)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/usuario')
def usuario():
    conn= db.conectar()
    # Crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    #Ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM usuarios ORDER BY id_usuario''')
    #Recuperar información
    datos = cursor.fetchall()
    #Cerrar cursor y conexión a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('usuarios.html', datos=datos)

@app.route('/delete_spagado/<string:id_usuario>', methods=['POST'])
def delete_spagado(id_usuario):
    conn= db.conectar()
    # Crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    #Borrar el registro con el id_pasi seleccionado
    cursor.execute('DELETE FROM usuarios WHERE id_usuario=%s', (id_usuario,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for ('spagado'))

@app.route('/update1_spagado/<string:id_usuario>', methods=['GET', 'POST'])
def update1_spagado(id_usuario):
    conn= db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # recuperar el registro del id_pais seleccionado
    cursor.execute('''SELECT * FROM usuarios WHERE id_usuario=%s''',
                   (id_usuario,))
    datos= cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template ('editar_spagado.html', datos=datos)

@app.route('/update2_spagado/<string:id_usuario>', methods=['POST'])
def update2_spagado(id_usuario):
    usuario_usuario = request.form['nombre']  # Obtener el valor del campo 'nombre' del formulario
    conn= db.conectar()
    cursor = conn.cursor()
    cursor.execute('''UPDATE usuarios SET usuario_usuario=%s WHERE id_usuario=%s''', (usuario_usuario, id_usuario,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('spagado'))

@app.route('/sueldospagado')
def spagado():
    conn= db.conectar()
    # Crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    #Ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM usuarios''')
    #Recuperar información
    datos = cursor.fetchall()
    #Cerrar cursor y conexión a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('sueldospagados.html', datos=datos)

@app.route('/configuracion')
def config():
    conn= db.conectar()
    # Crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    #Ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM usuarios''')
    #Recuperar información
    datos = cursor.fetchall()
    #Cerrar cursor y conexión a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('configuracion.html', datos=datos)