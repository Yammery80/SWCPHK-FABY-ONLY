import psycopg2
from flask import Flask, request, jsonify, redirect, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from psycopg2 import sql
import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.utils import secure_filename
import os
from werkzeug.security import  check_password_hash
from decimal import Decimal
from datetime import time
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
from flask import send_file
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
import io
from flask import request, jsonify
import requests
getcontext().prec = 10
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO as io
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'Yamilindel2704'  # Necesario para usar flash messages
app.config['UPLOAD_FOLDER-f'] = 'static/assets/Documents-SWCPHK/FotosPerfiles'  # Carpeta donde se guardarán las imágenes
app.config['UPLOAD_FOLDER-c'] = 'static/assets/Documents-SWCPHK/CartasRecomendacion'  # Carpeta donde se guardarán las imágenes
app.config['UPLOAD_FOLDER'] = 'static/assets/' #Acceder a la carpeta de recursos
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} #Permite este tipo de enxtensiones
# Directorio donde se guardarán los archivos subidos de configuración de interfaz
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

bootstrap = Bootstrap(app)

# Lado administrador
@app.route('/', methods=['GET', 'POST'])
def index():
    datos = []
    horas_trabajadas_total = Decimal(0)
    sueldo_calculado = Decimal(0)
    mensaje = None
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    config = get_config()
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario', '')
        e_fechaentrada = request.form.get('e_fechaentrada', '')
        e_fechasalida = request.form.get('e_fechasalida', '')

        session['id_usuario'] = id_usuario
        session['e_fechaentrada'] = e_fechaentrada
        session['e_fechasalida'] = e_fechasalida

        datos = get_data_from_db(id_usuario, e_fechaentrada, e_fechasalida)
        
        if 'calcular_sueldo' in request.form:
            if datos:
                horas_trabajadas_total, sueldo_calculado = calcular_sueldo(session.get('id_usuario'), session.get('e_fechaentrada'), session.get('e_fechasalida'))
                if sueldo_calculado == Decimal(0):
                    mensaje = "No se encontró información para calcular el sueldo."
            else:
                mensaje = "No se encontraron datos para calcular el sueldo."
# Obtener datos de configuración
    return render_template(
        'base.html',
        datos=datos,
        horas_trabajadas_total=horas_trabajadas_total,
        sueldo_calculado=sueldo_calculado,
        mensaje=mensaje,
        fecha_actual=fecha_actual,
        config=config  # Pasar los datos de configuración a la plantilla
    )

def get_data_from_db(id_usuario, e_fechaentrada, e_fechasalida):
    try:
        conn = db.conectar()
        cursor = conn.cursor()

        if not (id_usuario and e_fechaentrada and e_fechasalida):
            return []

        query = """
            SELECT id_usuariofk, nomcompleto_usuario, fecha, hora_entrada, hora_salida
            FROM entrada_salidas
            WHERE id_usuariofk = %s AND fecha BETWEEN %s AND %s
        """
        params = (id_usuario, e_fechaentrada, e_fechasalida)

        cursor.execute(query, params)
        datos = cursor.fetchall()

        return datos
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.desconectar(conn)

def calcular_sueldo(id_usuario, e_fechaentrada, e_fechasalida):
    try:
        if not e_fechaentrada or not e_fechasalida:
            print("Las fechas de entrada y salida no pueden estar vacías.")
            return Decimal(0), Decimal(0)  # Regresa horas_trabajadas_total y sueldo_calculado

        conn = db.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT pagohora_usuario FROM infopersonal WHERE id_usuario = %s", (id_usuario,))
        pagohora_usuario = cursor.fetchone()

        if not pagohora_usuario:
            print("No se encontró el pago por hora del usuario.")
            cursor.close()
            db.desconectar(conn)
            return Decimal(0), Decimal(0)

        pagohora_usuario = Decimal(pagohora_usuario[0])

        cursor.execute("""
            SELECT hora_entrada, hora_salida
            FROM entrada_salidas
            WHERE id_usuariofk = %s AND fecha BETWEEN %s AND %s
        """, (id_usuario, e_fechaentrada, e_fechasalida))
        registros = cursor.fetchall()

        horas_trabajadas_total = Decimal(0)
        for entrada, salida in registros:
            fecha_dummy = datetime(1900, 1, 1)
            entrada_datetime = datetime.combine(fecha_dummy, entrada)
            salida_datetime = datetime.combine(fecha_dummy, salida)
            horas_trabajadas = Decimal((salida_datetime - entrada_datetime).total_seconds()) / Decimal(3600)
            horas_trabajadas_total += horas_trabajadas

        cursor.close()
        db.desconectar(conn)

        sueldo_calculado = horas_trabajadas_total * pagohora_usuario

        return horas_trabajadas_total, sueldo_calculado

    except Exception as e:
        print(f"Error en calcular_sueldo: {e}")
        return Decimal(0), Decimal(0)
    

@app.route('/guardar_pago', methods=['POST'])
def guardar_pago():
    conn = None
    try:
        data = request.get_json()
        fecha_pago = data['fecha_pago']
        monto_total_pago = data['monto_total_pago']
        id_usuariofok = data['id_usuariofok']

        conn = db.conectar()
        with conn.cursor() as cur:
            query = sql.SQL("""
                INSERT INTO public.pagos (fecha_pago, montototal_pago, id_usuariofok)
                VALUES (%s, %s, %s)
            """)
            cur.execute(query, (fecha_pago, monto_total_pago, id_usuariofok))
            conn.commit()
        return {'success': True}  # Cambiar a dict

    except Exception as e:
        print(f'Error al guardar el pago: {e}')
        return {'success': False, 'error': str(e)}  # Cambiar a dict

    finally:
        if conn is not None:
            db.desconectar(conn)


#   Botón de guardar y generar PDF
@app.route('/guardar_y_generar_pdf', methods=['POST'])
def guardar_y_generar_pdf():
    conn = None
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        fecha_pago = data['fecha_pago']
        monto_total_pago = data['monto_total_pago']
        id_usuariofok = data['id_usuariofok']
        registros = data['registros']

        # Imprimir datos para depuración
        print('Datos recibidos:', data)

        # Verificar la estructura de los registros
        if not registros or not all('horaEntrada' in reg and 'horaSalida' in reg for reg in registros):
            raise ValueError('Uno o más registros no contienen las claves "horaEntrada" o "horaSalida"')

        # Calcular total de horas trabajadas
        def calcular_total_horas(registros):
            total_horas = 0
            for reg in registros:
                # Suponiendo que tienes las horas de entrada y salida en formato HH:MM
                from datetime import datetime

                formato = "%H:%M"
                entrada = datetime.strptime(reg['horaEntrada'], formato)
                salida = datetime.strptime(reg['horaSalida'], formato)
                diferencia = (salida - entrada).total_seconds() / 3600.0  # Convertir segundos a horas
                total_horas += diferencia
            return total_horas

        total_horas_trabajadas = calcular_total_horas(registros)

        # Guardar el pago en la base de datos
        conn = db.conectar()
        with conn.cursor() as cur:
            query = """
                INSERT INTO public.pagos (fecha_pago, montototal_pago, id_usuariofok)
                VALUES (%s, %s, %s)
            """
            cur.execute(query, (fecha_pago, monto_total_pago, id_usuariofok))
            conn.commit()
        flash('Pago guardado y PDF generado exitosamente', 'exito')
        # Crear un buffer para el PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Agregar el logo del establecimiento
        logo_path = 'static/assets/Documents-SWCPHK/Imagenes-interfaz/logo-banner.jpg'  # Reemplaza con la ruta correcta
        c.drawImage(logo_path, 50, height - 100, width=100, height=100)

        # Agregar nombre del establecimiento y subtítulo
        c.setFont('Helvetica-Bold', 14)
        c.drawString(160, height - 45, "Hakkunna-Matata")
        c.setFont('Helvetica', 12)
        c.drawString(160, height - 60, "Un lugar para relajarte")

        # Título centrado
        c.setFont('Helvetica-Bold', 18)
        c.drawCentredString(width / 2, height - 130, "Pago de sueldo")

        # Crear estilos para la lista
        styles = getSampleStyleSheet()
        bold_style = ParagraphStyle(name='BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold')
        normal_style = ParagraphStyle(name='NormalStyle', parent=styles['Normal'], fontName='Helvetica')

        # Información de la lista
        data_list = [
            ('ID de trabajador:', id_usuariofok),
            ('Fecha del pago:', fecha_pago),
            ('Total de horas trabajadas:', f'{total_horas_trabajadas:.2f}'),
            ('Monto total:', f'{monto_total_pago:.2f}')
        ]

        y_position = height - 180
        for item in data_list:
            para = Paragraph(f"<b>{item[0]}</b> {item[1]}", normal_style)
            para.wrapOn(c, width, height)
            para.drawOn(c, 100, y_position)
            y_position -= 20

        # Tabla de datos
        table_data = [
            ['ID Usuario', 'Usuario', 'Fecha', 'Hora de Entrada', 'Hora de Salida']
        ]
        for reg in registros:
            table_data.append([reg['idUsuario'], reg['usuario'], reg['fecha'], reg['horaEntrada'], reg['horaSalida']])

        table = Table(table_data, colWidths=[100, 100, 100, 100, 100], hAlign='CENTER')
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.047, 0.341, 0.145)),  # RGB(12, 87, 37)
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Alternar color de fondo de los registros
        row_count = len(table_data)
        for i in range(1, row_count):
            if i % 2 == 1:  # Alternar cada fila (pares e impares)
                table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightgrey)]))

        # Agregar tabla al PDF
        table.wrapOn(c, width, height)
        table.drawOn(c, 100, y_position - 40)  # Ajustar la posición según sea necesario

        c.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='sueldo.pdf', mimetype='application/pdf')

    except Exception as e:
        print(f'Error al guardar el pago o generar el PDF: {e}')
        return {'success': False, 'error': str(e)}

    finally:
        if conn is not None:
            db.desconectar(conn)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    config = get_config()  # Obtener la configuración

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.conectar()
        cur = conn.cursor()

        cur.execute('SELECT id_usuario, contrasena_usuario, tipo_usuario, intentos_fallidos, cuenta_bloqueada, nomcompleto_usuario, foto_usuario FROM infopersonal WHERE id_usuario = %s', (username,))
        user = cur.fetchone()

        if user:
            user_id, stored_password, tipo_usuario, intentos_fallidos, cuenta_bloqueada, nomcompleto_usuario, foto_usuario = user

            if cuenta_bloqueada:
                flash('Tu cuenta ha sido bloqueada, contacta a tu administrador.', 'danger')
                cur.close()
                db.desconectar(conn)
                return redirect(url_for('login'))

            # Comparar contraseñas en texto plano
            if stored_password == password:
                # Login exitoso
                session['user_id'] = user_id
                session['user_name'] = nomcompleto_usuario
                session['foto_filename'] = foto_usuario if foto_usuario else 'default_image.jpg'
                cur.execute('UPDATE infopersonal SET intentos_fallidos = 0 WHERE id_usuario = %s', (username,))
                conn.commit()
                cur.close()
                db.desconectar(conn)
                if tipo_usuario == 'Administrador':
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('trinicio'))
            else:
                # Contraseña incorrecta
                intentos_fallidos += 1
                if intentos_fallidos >= 3:
                    cur.execute('UPDATE infopersonal SET cuenta_bloqueada = true WHERE id_usuario = %s', (username,))
                    flash('Tu cuenta ha sido bloqueada, contacta a tu administrador.', 'danger')
                else:
                    flash(f'Tienes {3 - intentos_fallidos} intentos antes de bloquear la cuenta.', 'warning')
                cur.execute('UPDATE infopersonal SET intentos_fallidos = %s WHERE id_usuario = %s', (intentos_fallidos, username))
                conn.commit()
                cur.close()
                db.desconectar(conn)
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

        return redirect(url_for('login'))

    return render_template('login.html', config=config)

# Error de página

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')



#Usuario
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
                flash("Las contraseñas no coinciden", "peligroso")
                return redirect(url_for('usuario'))

            # Guardar la imagen de perfil
            foto_filename = None
            if foto_usuario:
                foto_filename = foto_usuario.filename
                foto_path = os.path.join(app.config['UPLOAD_FOLDER-f'], foto_filename)
                foto_usuario.save(foto_path)
            
            # Guardar las cartas de recomendación
            cartas_filename = None
            if cartasreco_usuario:
                cartas_filename = cartasreco_usuario.filename
                cartas_path = os.path.join(app.config['UPLOAD_FOLDER-c'], cartas_filename)
                cartasreco_usuario.save(cartas_path)

            # Conectar a la base de datos
            conn = db.conectar() 
            cursor = conn.cursor()
            
            # Verificar si el ID de usuario ya existe
            cursor.execute("SELECT COUNT(*) FROM public.infopersonal WHERE id_usuario = %s;", (id_usuario,))
            if cursor.fetchone()[0] > 0:
                flash("Usuario ya existente", "peligroso")
                return redirect(url_for('usuario'))

            # Preparar la consulta SQL
            insert_query = """
            INSERT INTO public.infopersonal(
                foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario, horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartasreco_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Ejecutar la consulta SQL
            cursor.execute(insert_query, (
                foto_filename, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario, domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario, horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario, tiposegmedico_usuario, cartas_filename))
            conn.commit()
            
            flash("Usuario creado con éxito", "exitoso")
            return redirect(url_for('usuario'))

        except Exception as e:
            print("Error:", e)
            flash("Hubo un error al crear el usuario", "peligroso")
            return redirect(url_for('usuario'))
        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)
    
    # Si es un GET, se recupera la información del usuario (si el ID se proporciona)
    id_usuario = request.args.get('id_usuario')
    foto_filename = None
    cartas_filename = None
    if id_usuario:
        try:
            # Conectar a la base de datos
            conn = db.conectar() 
            cursor = conn.cursor()
            
            # Consultar la base de datos
            cursor.execute("SELECT foto_usuario, cartasreco_usuario FROM public.infopersonal WHERE id_usuario = %s;", (id_usuario,))
            result = cursor.fetchone()
            
            if result:
                foto_filename, cartas_filename = result
            
        except Exception as e:
            print("Error:", e)
            flash("Hubo un error al recuperar los datos del usuario", "peligroso")
        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)

    # Obtener datos de configuración
    config = get_config()

    return render_template('usuarios.html', foto_filename=foto_filename, cartas_filename=cartas_filename, config=config)

#Consulta de Usuarios
@app.route('/consultausers', methods=['GET', 'POST'])
def consultausers():
    datos = []  # Inicializar datos como una lista vacía

    try:
        conn = db.conectar()  # Usar la función de conexión personalizada
        cursor = conn.cursor()

        # Obtener datos de configuración
        config = get_config()

        if request.method == 'POST':
            id_usuario = request.form.get('id_usuario')
            tipo_usuario = request.form.get('tipo_usuario')

            # Construir la consulta condicionalmente
            if id_usuario and tipo_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario,
                           domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario,
                           horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario,
                           tiposegmedico_usuario, cartasreco_usuario, intentos_fallidos, cuenta_bloqueada
                    FROM infopersonal WHERE id_usuario = %s AND tipo_usuario = %s
                """)
                params = (id_usuario, tipo_usuario)
            elif id_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario,
                           domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario,
                           horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario,
                           tiposegmedico_usuario, cartasreco_usuario, intentos_fallidos, cuenta_bloqueada
                    FROM infopersonal WHERE id_usuario = %s
                """)
                params = (id_usuario,)
            elif tipo_usuario:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario,
                           domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario,
                           horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario,
                           tiposegmedico_usuario, cartasreco_usuario, intentos_fallidos, cuenta_bloqueada
                    FROM infopersonal WHERE tipo_usuario = %s
                """)
                params = (tipo_usuario,)
            else:
                query = sql.SQL("""
                    SELECT foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario,
                           domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario,
                           horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario,
                           tiposegmedico_usuario, cartasreco_usuario, intentos_fallidos, cuenta_bloqueada
                    FROM infopersonal
                """)
                params = ()
            cursor.execute(query, params)
            datos = cursor.fetchall()
            cursor.close()
            db.desconectar(conn)  # Usar la función de desconexión personalizada
    except Exception as e:
        return f"Hubo un error en la solicitud: {e}", 500

    return render_template('consultar_usuario.html', datos=datos, config=config)


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
    conn = db.conectar()
    cursor = conn.cursor()
    try:
        # Obtener datos de configuración
        config = get_config()

        # Obtener datos del usuario
        cursor.execute('''
            SELECT foto_usuario, id_usuario, nomcompleto_usuario, tipo_usuario, descripcion_usuario, edad_usuario,
                   domicilio_usuario, numtel_usuario, telemer_usuario, contrasena_usuario, confirmarcontrasena_usuario,
                   horaentrada_usuario, horasalida_usuario, pagobase_usuario, pagohora_usuario, nummedico_usuario,
                   tiposegmedico_usuario, cartasreco_usuario, intentos_fallidos, cuenta_bloqueada
            FROM infopersonal
            WHERE id_usuario=%s
        ''', (id_usuario,))
        datos = cursor.fetchall()  # Obtiene todos los resultados
        
        if not datos:
            return "Usuario no encontrado", 404

        # Selecciona solo el primer resultado
        datos = datos[0]

        # Convertir horaentrada_usuario y horasalida_usuario a formato HH:MM
        def format_time_with_tz(time_with_tz):
            if time_with_tz:
                return time_with_tz.strftime('%H:%M')
            return ''

        horaentrada = format_time_with_tz(datos[11])
        horasalida = format_time_with_tz(datos[12])

    except Exception as e:
        return f"Error al consultar los datos: {e}", 500
    finally:
        cursor.close()
        db.desconectar(conn)
    
    return render_template('editar-usuario.html', datos=datos, horaentrada=horaentrada, horasalida=horasalida, config=config)


@app.route('/update2_usuario/<string:id_usuario>', methods=['GET', 'POST'])
def update2_usuario(id_usuario):
    if request.method == 'POST':
        # Obtener los archivos del formulario
        foto_usuario = request.files.get('foto_usuario')
        cartasreco_usuario = request.files.get('cartasreco_usuario')

        # Rutas para guardar los archivos
        cartasreco_folder = 'assets\\Documents-SWCPHK\\CartasRecomendacion'
        foto_folder = 'assets\\Documents-SWCPHK\\FotosPerfiles'
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

        # Obtener otros valores del formulario
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
        intentos_fallidos = request.form.get('intentos_fallidos')
        cuenta_bloqueada = request.form.get('cuenta_bloqueada')

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
                    confirmarcontrasena_usuario = %s,
                    cartasreco_usuario = %s,
                    foto_usuario = %s,
                    domicilio_usuario = %s,
                    intentos_fallidos = %s,
                    cuenta_bloqueada = %s
                WHERE id_usuario = %s;
            '''

            # Parámetros para la consulta
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
                contrasena_usuario,
                confirmarcontrasena_usuario,
                cartasreco_path,
                foto_path,
                domicilio_usuario,
                intentos_fallidos,
                cuenta_bloqueada,
                id_usuario  # Asegúrate de poner id_usuario al final
            )

            cursor.execute(update_query, params)
            conn.commit()
            flash("Datos actualizados correctamente", "exitouser")
            return redirect(url_for('consultausers'))
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f"Error al actualizar los datos: {e}", "erroruser")
        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)
    # Obtener datos de configuración
    config = get_config()
    return render_template('consultar_usuario.html', id_usuario=id_usuario, config=config)


@app.route('/sueldospagado', methods=['GET', 'POST'])
def spagado():
    datos = []  # Inicializar datos como una lista vacía

    try:
        if request.method == 'POST':
            id_pago = request.form.get('id_pago')
            id_usuariofok = request.form.get('id_usuariofok')
            fecha_iniciofok = request.form.get('e_fechaentradafok')
            fecha_finalfok = request.form.get('e_fechasalidafok')

            print("id_pago:", id_pago)
            print("id_usuariofok:", id_usuariofok)
            print("fecha_iniciofok:", fecha_iniciofok)
            print("fecha_finalfok:", fecha_finalfok)

            conn = db.conectar()  # Usa la función de conexión personalizada
            cursor = conn.cursor()

            # Construir la consulta condicionalmente
            if id_pago and id_usuariofok:
                query = """
                    SELECT id_pago, id_usuariofok, nomcompleto_usuario, fecha_pago, montototal_pago
                    FROM public.sueldos_pagados
                    WHERE id_usuariofok = %s AND id_pago = %s AND fecha_pago BETWEEN %s AND %s
                """
                params = (id_usuariofok, id_pago, fecha_iniciofok, fecha_finalfok)
            else:
                query = """
                     SELECT id_pago, id_usuariofok, nomcompleto_usuario, fecha_pago, montototal_pago
                     FROM public.sueldos_pagados
                     WHERE fecha_pago BETWEEN %s AND %s
                """
                params = (fecha_iniciofok, fecha_finalfok)

            cursor.execute(query, params)
            datos = cursor.fetchall()

            cursor.close()
            db.desconectar(conn)  # Usa la función de desconexión personalizada

    except Exception as e:
        # Mostrar un mensaje de error detallado en caso de excepción
        return f"Hubo un error en la solicitud: {e}", 500

    # Obtener datos de configuración
    config = get_config()

    # Renderizar la plantilla con los resultados y la configuración
    return render_template('sueldospagados.html', datos=datos, config=config)


@app.route('/update1_spagado/<int:id_pago>', methods=['GET', 'POST'])
def update1_spagado(id_pago):
    conn = db.conectar()  # Esto es para usar la función de conexión personalizada
    cursor = conn.cursor()
    
    try:
        # Recuperar el registro del id_pago seleccionado
        cursor.execute('''SELECT * FROM sueldos_pagados WHERE id_pago=%s''', (id_pago,))
        datos = cursor.fetchall()
    finally:
        cursor.close()
        db.desconectar(conn)  # Esto es para usar la función de desconexión personalizada

    # Obtener datos de configuración
    config = get_config()

    return render_template('editar_spagado.html', datos=datos, config=config)


@app.route('/update2_spagado/<int:id_pago>', methods=['POST'])
def update2_spagado(id_pago):
    fecha_pago = request.form['fecha-s']  # Obtiene la nueva fecha
    conn = db.conectar()
    cursor = conn.cursor()
    # Actualiza la fecha_pago en la vista
    cursor.execute('UPDATE sueldos_pagados SET fecha_pago=%s WHERE id_pago=%s', (fecha_pago, id_pago,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('spagado'))

@app.route('/delete_spagado/<int:id_pago>', methods=['POST'])
def delete_spagado(id_pago):
    conn = db.conectar()  # Usa la función de conexión personalizada
    cursor = conn.cursor()
    
    # Elimina el registro de la vista 'sueldos_pagados' basado en el id_pago
    cursor.execute('DELETE FROM sueldos_pagados WHERE id_pago=%s', (id_pago,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)  # Usa la función de desconexión personalizada
    
    return redirect(url_for('spagado'))


#Configuracion
@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if request.method == 'POST':
        # Obtener archivos y campos del formulario
        logo = request.files.get('logo')
        nombre_local = request.form.get('nom-local')
        tipo_servicio = request.form.get('tipo-servicio')
        domicilio = request.form.get('domiciolio-local')
        num_tel_local = request.form.get('num-tel-local')
        tipografia_sistema = request.form.get('tipografia-sistema')
        tamaño_local = request.form.get('tamaño-local')
        imagen_banner = request.files.get('imagen-banner')
        color_interfaz = request.form.get('color-interfaz')
        politicas = request.files.get('politicas')

        try:
            # Verificar y guardar el logo
            if logo and allowed_file(logo.filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                logo_filename = secure_filename(logo.filename)
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                logo.save(logo_path)
            else:
                logo_filename = None

            # Verificar y guardar el banner
            if imagen_banner and allowed_file(imagen_banner.filename):
                imagen_banner_filename = secure_filename(imagen_banner.filename)
                imagen_banner_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen_banner_filename)
                imagen_banner.save(imagen_banner_path)
            else:
                imagen_banner_filename = None

            # Verificar y guardar las políticas
            if politicas and allowed_file(politicas.filename):
                politicas_filename = secure_filename(politicas.filename)
                politicas_path = os.path.join(app.config['UPLOAD_FOLDER'], politicas_filename)
                politicas.save(politicas_path)
            else:
                politicas_filename = None

            # Conectar a la base de datos y actualizar la configuración
            conn = db.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO public.configuracion (id_config, logo_sistem, nombre_establecimiento, tipo_servicio,
                                                  domicilio, numero_telefonico, tipografia_letra, tamano_empresa,
                                                  imagen_banner, color_interfaz, politicas)
                VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_config)
                DO UPDATE SET logo_sistem = EXCLUDED.logo_sistem,
                              nombre_establecimiento = EXCLUDED.nombre_establecimiento,
                              tipo_servicio = EXCLUDED.tipo_servicio,
                              domicilio = EXCLUDED.domicilio,
                              numero_telefonico = EXCLUDED.numero_telefonico,
                              tipografia_letra = EXCLUDED.tipografia_letra,
                              tamano_empresa = EXCLUDED.tamano_empresa,
                              imagen_banner = EXCLUDED.imagen_banner,
                              color_interfaz = EXCLUDED.color_interfaz,
                              politicas = EXCLUDED.politicas;
            """, (logo_filename, nombre_local, tipo_servicio, domicilio, num_tel_local,
                  tipografia_sistema, tamaño_local, imagen_banner_filename,
                  color_interfaz, politicas_filename))

            conn.commit()
            cursor.close()
            db.desconectar(conn)

            flash('Éxito al actualizar.', 'exito')
            return redirect(url_for('configuracion'))
        except Exception as e:
            # Manejar cualquier excepción y mostrar el mensaje de error
            flash(f'Error al actualizar configuración: {str(e)}', 'error')
            return redirect(url_for('configuracion'))
    
    # Obtener configuración actual
    config = get_config()
    return render_template('configuracion.html', config=config)

def get_config():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.configuracion WHERE id_config = 1;")
    result = cursor.fetchone()
    cursor.close()
    db.desconectar(conn)

    if result:
        return {
            'logo_sistem': result[1],
            'nombre_establecimiento': result[2],
            'tipo_servicio': result[3],
            'domicilio': result[4],
            'numero_telefonico': result[5],
            'tipografia_letra': result[6],
            'tamano_empresa': result[7],
            'imagen_banner': result[8],
            'color_interfaz': result[9],
            'politicas': result[10]
        }
    return {}

#Vinculos de trabajador
@app.route('/trabajadorinicio')
def trinicio():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    # Consulta la información del usuario desde la base de datos
    with db.conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nomcompleto_usuario, foto_usuario FROM infopersonal WHERE id_usuario = %s", (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

    if user_info:
        nomcompleto_usuario, foto_usuario = user_info
        # Extraer solo el nombre del archivo
        foto_usuario = foto_usuario.split('/')[-1]
    else:
        nomcompleto_usuario = "Desconocido"
        foto_usuario = None

    # Obtener configuración actual
    config = get_config()

    return render_template('tr-base.html', nomcompleto_usuario=nomcompleto_usuario, foto_usuario=foto_usuario, config=config)

@app.route('/guardar_hora', methods=['POST'])
def guardar_hora():
    try:
        data = request.get_json()
        hora = data.get('hora')
        minuto = data.get('minuto')
        id_usuario = data.get('id_usuario')

        print(f"Datos recibidos: hora={hora}, minuto={minuto}, id_usuario={id_usuario}")

        if not hora or not minuto or not id_usuario:
            return jsonify({'success': False, 'error': 'Datos incompletos'}), 400

        fecha = datetime.now().date()
        hora_actual = f"{hora}:{minuto}"

        conn = db.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                'SELECT id_turno, hora_entrada, hora_salida FROM public.turnos WHERE fecha = %s AND id_usuariofk = %s',
                (fecha, id_usuario)
            )
            registro = cursor.fetchone()

            if registro:
                id_turno, hora_entrada, hora_salida = registro
                if hora_salida is None:
                    cursor.execute(
                        'UPDATE public.turnos SET hora_salida = %s WHERE id_turno = %s',
                        (hora_actual, id_turno)
                    )
                    conn.commit()
                    return jsonify({'success': True, 'message': 'Hora de salida actualizada'})
                else:
                    return jsonify({'success': False, 'message': 'Hora de salida ya registrada'}), 400
            else:
                cursor.execute(
                    'INSERT INTO public.turnos (fecha, hora_entrada, hora_salida, id_usuariofk) VALUES (%s, %s, %s, %s)',
                    (fecha, hora_actual, None, id_usuario)
                )
                conn.commit()
                return jsonify({'success': True, 'message': 'Hora de entrada registrada'})
        except Exception as e:
            conn.rollback()
            print(f"Error al ejecutar la consulta: {e}")
            return jsonify({'success': False, 'error': 'Error al guardar la hora'}), 500
        finally:
            cursor.close()
            db.desconectar(conn)
    except Exception as e:
        print(f"Error en la función guardar_hora: {e}")
        return jsonify({'success': False, 'error': 'Error en la función guardar_hora'}), 500

@app.route('/trabajadoreys', methods=['GET', 'POST'])
def treys():
    datos = []  # Inicializar datos
    nomcompleto_usuario = "Desconocido"
    foto_usuario = None
    
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('login'))
    
    # Consulta la información del usuario desde la base de datos
    try:
        with db.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nomcompleto_usuario, foto_usuario FROM infopersonal WHERE id_usuario = %s", (user_id,))
                user_info = cursor.fetchone()
    
        if user_info:
            nomcompleto_usuario, foto_usuario = user_info
            # Extraer solo el nombre del archivo
            if foto_usuario:
                foto_usuario = foto_usuario.split('\\')[-1]  # Usar '\\' para Windows
    except Exception as e:
        # Manejo de errores, puedes registrar el error si lo deseas
        print(f"Error al obtener información del usuario: {e}")

    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_final = request.form['fecha_final']
        
        try:
            with db.conectar() as conn:
                with conn.cursor() as cursor:
                    # Consulta para obtener datos de entradas y salidas
                    query = """
                        SELECT fecha, hora_entrada, hora_salida
                        FROM turnos
                        WHERE id_usuariofk = %s AND fecha BETWEEN %s AND %s
                    """
                    params = (user_id, fecha_inicio, fecha_final)
                    cursor.execute(query, params)
                    datos = cursor.fetchall()
        except Exception as e:
            # Manejo de errores, puedes registrar el error si lo deseas
            print(f"Error al consultar entradas y salidas: {e}")
    
    # Obtener configuración actual
    config = get_config()

    return render_template('tr-entradas-salidas.html', datos=datos, nomcompleto_usuario=nomcompleto_usuario, foto_usuario=foto_usuario, config=config)
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
