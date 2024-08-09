$(document).ready(function() {
    // Mostrar ventana de Sueldos pagados
    const sueldoDataElement = $('#sueldo-data');
    const sueldoCalculado = parseFloat(sueldoDataElement.attr('data-sueldo-calculado'));

    if (sueldoCalculado !== 0) {
        $('#popup-sueldo').show();
    }

    // Manejar clic en el botón de cancelar en el popup de sueldo
    $('#cancelButton-s').click(function() {
        // Limpiar los campos del formulario de consulta
        $('#form-consulta input[type="text"]').val('');
        $('#form-consulta input[type="date"]').val('');

        // Limpiar la tabla de datos
        $('#tabla-datos tbody').empty();

        // Ocultar el popup
        $('#popup-sueldo').hide();
    });

    // Manejar clic en el botón de guardar en el popup de sueldo
    $('#acceptButton-s').click(function() {
        // Obtener los datos necesarios
        const sueldoCalculado = parseFloat($('#sueldo-data').attr('data-sueldo-calculado'));
        const idUsuario = $('#form-consulta input[name="id_usuario"]').val();
        const fechaActual = new Date().toISOString().slice(0, 10); // Fecha actual en formato YYYY-MM-DD

        // Enviar datos al servidor
        fetch('/guardar_pago', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fecha_pago: fechaActual,
                monto_total_pago: sueldoCalculado,
                id_usuariofok: idUsuario
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Pago guardado con éxito');
                // Ocultar el popup y limpiar datos
                $('#popup-sueldo').hide();
                $('#form-consulta input[type="text"]').val('');
                $('#form-consulta input[type="date"]').val('');
                $('#tabla-datos tbody').empty();
            } else {
                console.error('Error al guardar el pago:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Manejar clic en el botón de guardar y generar PDF en el popup de sueldo
    $('#pdfButton-s').click(function() {
        // Obtener los datos necesarios
        const sueldoCalculado = parseFloat($('#sueldo-data').attr('data-sueldo-calculado'));
        const idUsuario = $('#form-consulta input[name="id_usuario"]').val();
        const fechaActual = new Date().toISOString().slice(0, 10); // Fecha actual en formato YYYY-MM-DD
    
        // Recopilar datos de la tabla
        const tablaDatos = [];
        $('#tabla-datos tbody tr').each(function() {
            const row = $(this);
            const idUsuario = row.find('td').eq(0).text();
            const usuario = row.find('td').eq(1).text();
            const fecha = row.find('td').eq(2).text();
            const horaEntrada = row.find('td').eq(3).text();
            const horaSalida = row.find('td').eq(4).text();
            tablaDatos.push({ idUsuario, usuario, fecha, horaEntrada, horaSalida });
        });

        // Enviar datos al servidor
        fetch('/guardar_y_generar_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fecha_pago: fechaActual,
                monto_total_pago: sueldoCalculado,
                id_usuariofok: idUsuario,
                registros: tablaDatos
            })
        })
        .then(response => response.blob())
        .then(blob => {
            // Crear un enlace para descargar el PDF
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sueldo.pdf';
            a.click();
            window.URL.revokeObjectURL(url);

            // Limpiar datos ingresados y vaciar la tabla
            $('#form-consulta input[type="text"]').val('');
            $('#form-consulta input[type="date"]').val('');
            $('#tabla-datos tbody').empty();
    
            // Cerrar la ventana emergente
            $('#popup-sueldo').hide();
        })
        .catch(error => console.error('Error:', error));
    });

    // Mostrar ventana de Trabajador y horas de turno
    var popup = document.getElementById('popup');
    var acceptButton = document.getElementById('acceptButton');
    var cancelButton = document.getElementById('cancelButton');

    // Muestra la ventana emergente
    popup.style.display = 'flex';

    // Función para actualizar la hora y los minutos en la ventana emergente
    function updateClock() {
        var now = new Date();
        var hour = String(now.getHours()).padStart(2, '0');
        var minute = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('hour').textContent = hour;
        document.getElementById('minute').textContent = minute;
    }

    // Actualiza la hora y los minutos inmediatamente y luego cada segundo
    updateClock();
    setInterval(updateClock, 1000);

    // Verifica el ID del usuario desde el atributo `data-user-id`
    var userId = document.body.getAttribute('data-user-id');
    console.log('ID del usuario:', userId);

    // Cierra la ventana emergente y envía la hora al servidor al hacer clic en el botón de aceptar
    acceptButton.addEventListener('click', function() {
        console.log('Botón Aceptar clickeado'); // Línea de depuración

        // Obtiene la hora actual
        var now = new Date();
        var hour = String(now.getHours()).padStart(2, '0');
        var minute = String(now.getMinutes()).padStart(2, '0');
        var idUsuario = userId; // Obtener el ID del usuario desde el atributo `data-user-id`

        // Envía la hora al servidor
        fetch('/guardar_hora', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hora: hour, minuto: minute, id_usuario: idUsuario })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Hora guardada con éxito');
                popup.style.display = 'none'; // Cierra la ventana emergente
            } else {
                console.error('Error al guardar la hora:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Cierra la ventana emergente sin hacer nada al hacer clic en el botón de cancelar
    cancelButton.addEventListener('click', function() {
        console.log('Botón Cancelar clickeado'); // Línea de depuración
        popup.style.display = 'none';
    });

    // Crea ventana emergente para Usuario existente
    $(".alert").fadeIn();

    setTimeout(function() {
        $(".alert").fadeOut();
    }, 5000); // 5 seconds

    // Cambia automáticamente la foto de perfil
    function previewImage(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        if (file) {
            reader.onload = function(e) {
                // Obtén el elemento de imagen y actualiza su src
                document.getElementById('profileImage').src = e.target.result;
            }
            // Lee el archivo como una URL de datos
            reader.readAsDataURL(file);
        }
    }

    // Cambia automáticamente la foto de cartas recomendación
    $('#foto_usuario').change(function(event) {
        var reader = new FileReader();
        reader.onload = function(event) {
            $('#foto_usuario_preview').attr('src', event.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    });

    $('#cartas_reco').change(function(event) {
        var reader = new FileReader();
        reader.onload = function(event) {
            $('#cartas_reco_preview').attr('src', event.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    });

    // Login ventana
    function mostrarMensaje() {
        var flashMessage = document.getElementById('flash-message');
        flashMessage.style.display = 'block'; // Mostrar la ventana emergente

        setTimeout(function() {
            flashMessage.style.display = 'none'; // Ocultar la ventana emergente después de 1.5 segundos
        }, 1500); // 1500 milisegundos = 1.5 segundos
    }
});