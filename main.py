import psycopg2
from flask import Flask, request, jsonify, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from psycopg2 import sql
import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Lado administrador

@app.route('/', methods=['GET', 'POST'])
def index():
    datos = []  # Esto es para inicializar datos como una lista vacía
    try:
        if request.method == 'POST':
            id_usuario = request.form.get('id_usuario', '')
            e_fechaentrada = request.form.get('e_fechaentrada', '')
            e_fechasalida = request.form.get('e_fechasalida', '')

            conn = db.conectar()  # Esto es para usar la función de conexión personalizada
            cursor = conn.cursor()

            # Esto es para construir la consulta condicionalmente
            if id_usuario:
                query = sql.SQL("""
                    SELECT * FROM entradas_salidas
                    WHERE id_usuario = %s AND fecha BETWEEN %s AND %s
                """)
                params = (id_usuario, e_fechaentrada, e_fechasalida)
            else:
                query = sql.SQL("""
                    SELECT * FROM entradas_salidas
                    WHERE fecha BETWEEN %s AND %s
                """)
                params = (e_fechaentrada, e_fechasalida)

            cursor.execute(query, params)
            datos = cursor.fetchall()

            cursor.close()
            db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    except Exception as e:
        # Esto es para mostrar un mensaje de error en caso de excepción
        return f"Hubo un error en la solicitud: {e}", 500

    # Esto es para renderizar la plantilla con los resultados
    return render_template('base.html', datos=datos)

# Registro de usuarios

@app.route('/register')
def register():
    return render_template('register.html')

# Error de página

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/usuario')
def usuario():
        return render_template('usuarios.html')

@app.route('/delete_spagado/<string:id_usuario>', methods=['POST'])
def delete_spagado(id_usuario):
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Esto es para borrar el registro con el id_usuario seleccionado
    cursor.execute('DELETE FROM usuarios WHERE id_usuario=%s', (id_usuario,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return redirect(url_for('spagado'))

@app.route('/update1_spagado/<string:id_usuario>', methods=['GET', 'POST'])
def update1_spagado(id_usuario):
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Esto es para recuperar el registro del id_usuario seleccionado
    cursor.execute('''SELECT * FROM usuarios WHERE id_usuario=%s''', (id_usuario,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return render_template('editar_spagado.html', datos=datos)

@app.route('/update2_spagado/<string:id_usuario>', methods=['POST'])
def update2_spagado(id_usuario):
    usuario_usuario = request.form['nombre']  # Esto es para obtener el valor del campo 'nombre' del formulario
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Esto es para actualizar el registro del usuario
    cursor.execute('''UPDATE usuarios SET usuario_usuario=%s WHERE id_usuario=%s''', (usuario_usuario, id_usuario,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return redirect(url_for('spagado'))

@app.route('/configuracion')
def config():
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Aquí podría ejecutar una consulta en la base de datos si fuera necesario
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return render_template('configuracion.html')

@app.route('/sueldospagado', methods=['GET', 'POST'])
def spagado():
    datos = []  # Esto es para inicializar datos como una lista vacía

    try:
        if request.method == 'POST':
            id_pago = request.form['id_pago']  # Esto es para obtener el valor del campo 'id_pago'
            usuario_entradas = request.form['usuario_entradas']  # Esto es para obtener el valor del campo 'usuario_entradas'
            fecha_inicio = request.form['fecha_inicio']  # Esto es para obtener el valor del campo 'fecha_inicio'
            fecha_final = request.form['fecha_final']  # Esto es para obtener el valor del campo 'fecha_final'

            conn = db.conectar()  # Esto es para usar la función de conexión personalizada
            cursor = conn.cursor()

            # Esto es para construir la consulta condicionalmente
            if id_pago and usuario_entradas:
                query = sql.SQL("""
                    SELECT id_usuario, fecha, hora_entrada, hora_salida
                    FROM turnos
                    WHERE id_usuario = %s AND id_pago = %s AND fecha BETWEEN %s AND %s
                """)
                params = (usuario_entradas, id_pago, fecha_inicio, fecha_final)
            elif usuario_entradas:
                query = sql.SQL("""
                    SELECT id_usuario, fecha, hora_entrada, hora_salida
                    FROM turnos
                    WHERE id_usuario = %s AND fecha BETWEEN %s AND %s
                """)
                params = (usuario_entradas, fecha_inicio, fecha_final)
            else:
                query = sql.SQL("""
                    SELECT id_usuario, fecha, hora_entrada, hora_salida
                    FROM turnos
                    WHERE fecha BETWEEN %s AND %s
                """)
                params = (fecha_inicio, fecha_final)

            cursor.execute(query, params)
            datos = cursor.fetchall()

            cursor.close()
            db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    except Exception as e:
        # Esto es para mostrar un mensaje de error en caso de excepción
        return f"Hubo un error en la solicitud: {e}", 500

    # Esto es para renderizar la plantilla con los resultados
    return render_template('sueldospagados.html', datos=datos)

#Vinculos de trabajador
@app.route('/trabajadorinicio')
def trinicio():
    return render_template('tr-base.html')

@app.route('/guardar_hora', methods=['POST'])
def guardar_hora():
    data = request.get_json()
    hora = data.get('hora')
    minuto = data.get('minuto')
    id_usuario = data.get('id_usuario')

    fecha_actual = datetime.datetime.now().date()
    hora_entrada = f"{hora}:{minuto}"

    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO turnos (fecha, hora_entrada, id_usuario) VALUES (%s, %s, %s)",
                (fecha_actual, hora_entrada, id_usuario)
            )
            conn.commit()
            response = {'success': True}
    except Exception as e:
        conn.rollback()
        response = {'success': False, 'error': str(e)}
    finally:
        db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    return jsonify(response)

@app.route('/trabajadoreys', methods=['GET', 'POST'])
def treys():
    datos = None  # Esto es para inicializar datos como None para manejar el caso en que no hay resultados.

    try:
        if request.method == 'POST':
            usuario_entradas = request.form['usuario_entradas']  # Esto es para obtener el valor del campo 'usuario_entradas'
            fecha_inicio = request.form['fecha_inicio']  # Esto es para obtener el valor del campo 'fecha_inicio'
            fecha_final = request.form['fecha_final']  # Esto es para obtener el valor del campo 'fecha_final'

            conn = db.conectar()  # Esto es para usar la función de conexión personalizada
            cursor = conn.cursor()

            # Esto es para construir la consulta condicionalmente
            if usuario_entradas:
                query = sql.SQL("""
                    SELECT id_usuario, fecha, hora_entrada, hora_salida FROM turnos
                    WHERE id_usuario = %s AND fecha BETWEEN %s AND %s
                """)
                params = (usuario_entradas, fecha_inicio, fecha_final)
            else:
                query = sql.SQL("""
                    SELECT id_usuario, fecha, hora_entrada, hora_salida FROM turnos
                    WHERE fecha BETWEEN %s AND %s
                """)
                params = (fecha_inicio, fecha_final)

            cursor.execute(query, params)
            datos = cursor.fetchall()

            cursor.close()
            db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    except Exception as e:
        # Esto es para mostrar un mensaje de error en caso de excepción
        return f"Hubo un error en la solicitud: {e}", 500

    # Esto es para renderizar la plantilla con los resultados
    return render_template('tr-entradas-salidas.html', datos=datos)
