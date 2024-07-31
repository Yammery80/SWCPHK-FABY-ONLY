import psycopg2
from flask import Flask, request, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from psycopg2 import sql
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

#Vinculos de trabajador
@app.route('/trabajadorinicio')
def trinicio():
    return render_template('tr-base.html')

@app.route('/trabajadoreys', methods=['GET', 'POST'])
def treys():
    datos = None  # Inicializamos datos como None para manejar el caso en que no hay resultados.

    try:
        if request.method == 'POST':
            usuario_entradas = request.form['usuario_entradas']  # Accedemos directamente con []
            fecha_inicio = request.form['fecha_inicio']
            fecha_final = request.form['fecha_final']

            conn = db.conectar()  # Usamos la función de conexión personalizada
            cursor = conn.cursor()

            # Construir la consulta condicionalmente
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
            db.desconectar(conn)  # Usamos la función de desconexión personalizada

        # Renderiza la plantilla con los resultados
        return render_template('tr-entradas-salidas.html', datos=datos)

    except Exception as e:
        # En caso de error, muestra un mensaje de error
        return f"Hubo un error en la solicitud: {e}", 500