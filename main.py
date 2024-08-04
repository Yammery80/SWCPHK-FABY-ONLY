import psycopg2
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from psycopg2 import sql
import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Yamilindel2704'  # Necesario para usar flash messages
app.config['UPLOAD_FOLDER'] = 'static/assets/Documents-SWCPHK/FotosPerfiles'  # Carpeta donde se guardarán las imágenes
app.config['UPLOAD_FOLDER'] = 'static/assets/Documents-SWCPHK/CartasRecomendacion'  # Carpeta donde se guardarán las imágenes
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

@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            foto_usuario = request.files.get('foto_usuario')
            id_usuario = request.form['id_usuario']
            nomcompleto_usuario = request.form['nomcompleto_usuario']
            tipo_usuario = request.form['tipo_usuario']
            descripcion_usuario = request.form['descripcion_usuario']
            nummedico_usuario = request.form['nummedico_usuario']
            tiposegmedico_usuario = request.form['tiposegmedico_usuario']
            pagohora_usuario = request.form['pagohora_usuario']
            pagobase_usuario = request.form['pagobase_usuario']
            horaentrada_usuario = request.form['horaentrada_usuario']
            horasalida_usuario = request.form['horasalida_usuario']
            cartasreco_usuario = request.files.get('cartasreco_usuario')
            contrasena_usuario = request.form['contrasena_usuario']
            confirmarcontrasena_usuario = request.form['confirmarcontrasena_usuario']
            numtel_usuario = request.form['numtel_usuario']
            telemer_usuario = request.form['telemer_usuario']
            edad_usuario = request.form['edad_usuario']
            domicilio_usuario = request.form['domicilio_usuario']

            # Validar que las contraseñas coincidan
            if contrasena_usuario != confirmarcontrasena_usuario:
                flash("Las contraseñas no coinciden", "error")
                return redirect(url_for('usuario'))

            # Encriptar la contraseña
            contrasena_hash = generate_password_hash(contrasena_usuario)

            # Guardar la imagen de perfil
            foto_filename = None
            if foto_usuario:
                foto_filename = foto_usuario.filename
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
                foto_usuario.save(foto_path)
            
            # Guardar las cartas de recomendación
            cartas_filename = None
            if cartasreco_usuario:
                cartas_filename = cartasreco_usuario.filename
                cartas_path = os.path.join(app.config['UPLOAD_FOLDER'], cartas_filename)
                cartasreco_usuario.save(cartas_path)

            # Conectar a la base de datos
            conn = db.conectar() 
            cursor = conn.cursor()
            
            # Verificar si el ID de usuario ya existe
            cursor.execute("SELECT COUNT(*) FROM public.infopersonal WHERE id_usuario = %s;", (id_usuario,))
            if cursor.fetchone()[0] > 0:
                flash("Usuario ya existente", "error")
                return redirect(url_for('usuario'))

            # Preparar la consulta SQL
            insert_query = """
            INSERT INTO public.infopersonal(
                foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario, horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Ejecutar la consulta SQL
            cursor.execute(insert_query, (
                foto_filename, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_hash, confirmarcontrasena_usuario, horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartas_filename))
            conn.commit()
            
            flash("Usuario creado con éxito", "success")
            return redirect(url_for('usuario'))

        except Exception as e:
            print("Error:", e)
            flash("Hubo un error al crear el usuario", "error")
            return redirect(url_for('usuario'))
        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)

    return render_template('usuarios.html')


#Consulta de Usuarios
@app.route('/consultausers', methods=['GET', 'POST'])
def consultausers():
    datos = []  # Esto es para inicializar datos como una lista vacía

    try:
        conn = db.conectar()  # Esto es para usar la función de conexión personalizada
        cursor = conn.cursor()

        if request.method == 'POST':
            id_usuario = request.form.get('id_usuario')  # Usamos .get() para evitar KeyError
            tipo_usuario = request.form.get('tipo_usuario')

            # Esto es para construir la consulta condicionalmente
            if id_usuario and tipo_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario,  nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, horaentrada_usuario, horasalida_usuario,  pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario
                    FROM infopersonal WHERE id_usuario = %s AND tipo_usuario = %s
                """)
                params = (id_usuario, tipo_usuario)
            elif id_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario,  nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, horaentrada_usuario, horasalida_usuario,  pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario
                    FROM infopersonal WHERE id_usuario = %s
                """)
                params = (id_usuario,)
            elif tipo_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario,  nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, horaentrada_usuario, horasalida_usuario,  pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario
                    FROM infopersonal WHERE tipo_usuario = %s
                """)
                params = (tipo_usuario,)
            else:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario,  nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, horaentrada_usuario, horasalida_usuario,  pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario
                    FROM infopersonal
                """)
                params = ()

            cursor.execute(query, params)
            datos = cursor.fetchall()
            cursor.close()
            db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    except Exception as e:
        # Esto es para mostrar un mensaje de error en caso de excepción
        return f"Hubo un error en la solicitud: {e}", 500

    # Esto es para renderizar la plantilla con los resultados
    return render_template('consultar_usuario.html', datos=datos)


@app.route('/delete_usuario/<string:id_usuario>', methods=['POST'])
def delete_usuario(id_usuario):
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Esto es para borrar el registro con el id_usuario seleccionado
    cursor.execute('DELETE FROM infopersonal WHERE id_usuario=%s', (id_usuario,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return redirect(url_for('consultausers'))

@app.route('/update1_usuario/<string:id_usuario>', methods=['GET', 'POST'])
def update1_usuario(id_usuario):
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    # Esto es para recuperar el registro del id_usuario seleccionado
    cursor.execute('''SELECT foto_usuario, id_usuario,  nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario, horaentrada_usuario, horasalida_usuario,  pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario FROM infopersonal WHERE id_usuario=%s''', (id_usuario,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada
    return render_template('editar-usuario.html', datos=datos)


@app.route('/update2_usuario/<string:id_usuario>', methods=['GET', 'POST'])
def update2_usuario(id_usuario):
    if request.method == 'POST':
        # Obtener todos los valores del formulario con valores predeterminados
        foto_usuario = request.files.get('foto_usuario')  # Para archivos
        nomcompleto_usuario = request.form.get('nomcompleto_usuario')
        tipo_usuario = request.form.get('tipo_usuario')
        descripcion_usuario = request.form.get('descripcion_usuario')
        edad_usuario = request.form.get('edad_usuario')
        domicilio_usuario = request.form.get('domicilio_usuario')
        numtel_usuario = request.form.get('numtel_usuario')
        telemer_usuario = request.form.get('telemer_usuario')
        contrasena_usuario = request.form.get('contrasena_usuario')
        confirmarcontrasena_usuario = request.form.get('confirmarcontrasena_usuario')
        horaentrada_usuario = request.form.get('horaentrada_usuario')
        horasalida_usuario = request.form.get('horasalida_usuario')
        pagobase_usuario = request.form.get('pagobase_usuario')
        pagohora_usuario = request.form.get('pagohora_usuario')
        nummedico_usuario = request.form.get('nummedico_usuario')
        tiposegmedico_usuario = request.form.get('tiposegmedico_usuario')
        cartasreco_usuario = request.files.get('cartasreco_usuario')  # Para archivos

        # Rutas para guardar los archivos
        cartasreco_folder = 'C:\\SWCPHK-OFFICIAL\\static\\assets\\Documents-SWCPHK\\CartasRecomendacion'
        foto_folder = 'C:\\SWCPHK-OFFICIAL\\static\\assets\\Documents-SWCPHK\\FotosPerfiles'
        os.makedirs(cartasreco_folder, exist_ok=True)
        os.makedirs(foto_folder, exist_ok=True)

        # Guardar los archivos y obtener las rutas
        cartasreco_path = None
        foto_path = None

        if cartasreco_usuario and cartasreco_usuario.filename:
            cartasreco_filename = secure_filename(cartasreco_usuario.filename)
            cartasreco_path = os.path.join(cartasreco_folder, cartasreco_filename)
            cartasreco_usuario.save(cartasreco_path)

        if foto_usuario and foto_usuario.filename:
            foto_filename = secure_filename(foto_usuario.filename)
            foto_path = os.path.join(foto_folder, foto_filename)
            foto_usuario.save(foto_path)

        # Encriptar la contraseña si se proporciona
        contrasena_hash = None
        if contrasena_usuario and confirmarcontrasena_usuario:
            if contrasena_usuario != confirmarcontrasena_usuario:
                flash("Las contraseñas no coinciden", "error")
                return redirect(url_for('update2_usuario', id_usuario=id_usuario))
            contrasena_hash = generate_password_hash(contrasena_usuario)

        conn = None
        cursor = None
        try:
            conn = db.conectar() 
            cursor = conn.cursor()

            # Construir la consulta de actualización
            update_query = '''
                UPDATE public.infopersonal
                SET nomcompleto_usuario = %s,
                    edad_usuario = %s,
                    numtel_usuario = %s,
                    telemer_usuario = %s,
                    tipo_usuario = %s,
                    descripcion_usuario = %s,
                    nummedico_usuario = %s,
                    tiposegmedico_usuario = %s,
                    pagohora_usuario = %s,
                    pagobase_usuario = %s,
                    horaentrada_usuario = %s,
                    horasalida_usuario = %s,
                    contrasena_usuario = %s,
                    cartasreco_usuario = %s,
                    foto_usuario = %s,
                    domicilio_usuario = %s
                WHERE id_usuario = %s;
            '''

            # Parámetros para la consulta (en el mismo orden que los placeholders)
            params = (
                nomcompleto_usuario,
                edad_usuario,
                numtel_usuario,
                telemer_usuario,
                tipo_usuario,
                descripcion_usuario,
                nummedico_usuario,
                tiposegmedico_usuario,
                pagohora_usuario,
                pagobase_usuario,
                horaentrada_usuario,
                horasalida_usuario,
                contrasena_hash,
                cartasreco_path,
                foto_path,
                domicilio_usuario,
                id_usuario
            )

            cursor.execute(update_query, params)
            conn.commit()
            flash("Datos actualizados correctamente", "success")
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f"Error al actualizar los datos: {e}", "error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)
    return redirect(url_for('consultausers', id_usuario=id_usuario))



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
